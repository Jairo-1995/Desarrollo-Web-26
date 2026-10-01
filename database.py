"""Gestión de la conexión a la base de datos (PostgreSQL).

Se conecta usando DATABASE_URL (formato postgres://usuario:password@host:puerto/basededatos,
como el Internal Database URL de Render) o con las variables PG_HOST, PG_USER,
PG_PASSWORD, PG_NAME y PG_PORT.
"""

import os

from flask import g

# Excepción de integridad de PostgreSQL (clave duplicada o foránea).
def _errores_integridad():
    try:
        from psycopg2.errors import IntegrityError as ErrorPostgres
        return (ErrorPostgres,)
    except ImportError:
        return ()  # psycopg2 no está instalado


ERROR_INTEGRIDAD = _errores_integridad()


class Fila(dict):
    """Fila de MySQL accesible como diccionario y también por índice (fila[0])."""

    def __getitem__(self, clave):
        if isinstance(clave, int):
            return list(self.values())[clave]
        return dict.__getitem__(self, clave)


class ConexionPostgres:
    """Adaptador de la conexión PostgreSQL que acepta marcadores '?' (estilo SQLite)."""

    def __init__(self, conexion):
        self._conexion = conexion
        self._cursor = conexion.cursor()

    def _traducir(self, sql):
        """PostgreSQL usa marcadores %s: reemplaza los '?' de las consultas."""
        return sql.replace("?", "%s")

    def execute(self, sql, parametros=()):
        self._cursor.execute(self._traducir(sql), tuple(parametros))
        return self  # permite encadenar .fetchone()/.fetchall() del adaptador

    @property
    def description(self):
        """Descripción de las columnas de la última consulta (como el cursor)."""
        return self._cursor.description

    @property
    def rowcount(self):
        return self._cursor.rowcount

    def fetchone(self):
        """Devuelve la fila actual como Fila (dict + acceso por índice)."""
        columnas = [col[0] for col in self._cursor.description or ()]
        fila = self._cursor.fetchone()
        if fila is None:
            return None
        return Fila(zip(columnas, fila))

    def fetchall(self):
        """Devuelve todas las filas como Fila (dict + acceso por índice)."""
        columnas = [col[0] for col in self._cursor.description or ()]
        return [Fila(zip(columnas, fila)) for fila in self._cursor.fetchall()]

    def commit(self):
        self._conexion.commit()

    def close(self):
        self._cursor.close()
        self._conexion.close()


def get_db():
    """Establece y devuelve la conexión PostgreSQL.

    La conexión se guarda en el objeto ``g`` de Flask para reutilizarla
    durante la misma petición y cerrarla automáticamente al terminar.
    """
    if "db" not in g:
        from conexion.conexion import obtener_conexion_postgres
        # psycopg2 usa los mismos marcadores %s que MySQL, y sus
        # métodos (cursor, fetchone, commit...) son idénticos, por lo
        # que el adaptador ConexionPostgres sirve para PostgreSQL.
        g.db = ConexionPostgres(obtener_conexion_postgres())
    return g.db


def close_db(_exc=None):
    """Cierra la conexión al finalizar la petición."""
    db = g.pop("db", None)
    if db is not None:
        db.close()


def init_db(app):
    """Crea las tablas (si no existen) y registra el cierre de conexión."""
    app.teardown_appcontext(close_db)
    _init_db_postgres()


# ---------------------------------------------------------------------------
# PostgreSQL
# ---------------------------------------------------------------------------

def _init_db_postgres():
    """Crea las tablas en PostgreSQL (si no existen) y las pobla.

    Se conecta usando DATABASE_URL (formato del Internal Database URL de
    Render) o las variables PG_HOST/PG_USER/PG_PASSWORD/PG_NAME/PG_PORT.
    """
    from conexion.conexion import obtener_conexion_postgres

    esquema = """
    CREATE TABLE IF NOT EXISTS usuarios (
        id       SERIAL PRIMARY KEY,
        nombre   VARCHAR(100) NOT NULL,
        email    VARCHAR(120) NOT NULL UNIQUE,
        password VARCHAR(255) NOT NULL,
        rol      VARCHAR(20)  NOT NULL DEFAULT 'usuario'
    );

    CREATE TABLE IF NOT EXISTS clientes (
        id       SERIAL PRIMARY KEY,
        nombre   VARCHAR(100) NOT NULL,
        correo   VARCHAR(120) NOT NULL UNIQUE,
        telefono VARCHAR(30)  NOT NULL,
        direccion VARCHAR(200)
    );

    CREATE TABLE IF NOT EXISTS proveedores (
        id                 SERIAL PRIMARY KEY,
        nombre             VARCHAR(100) NOT NULL,
        producto_principal VARCHAR(100) NOT NULL,
        ciudad             VARCHAR(60)  NOT NULL
    );

    CREATE TABLE IF NOT EXISTS productos (
        id          SERIAL PRIMARY KEY,
        nombre      VARCHAR(100) NOT NULL CHECK (length(nombre) <= 100),
        categoria   VARCHAR(50)  NOT NULL,
        descripcion TEXT,
        precio      NUMERIC(10, 2) NOT NULL CHECK (precio >= 0),
        unidad      VARCHAR(30)  NOT NULL CHECK (length(unidad) <= 30),
        stock       INTEGER      NOT NULL DEFAULT 0 CHECK (stock >= 0),
        imagen      VARCHAR(100) CHECK (length(imagen) <= 100),
        proveedor_id INTEGER,
        CONSTRAINT fk_productos_proveedor
            FOREIGN KEY (proveedor_id) REFERENCES proveedores (id)
            ON UPDATE CASCADE ON DELETE SET NULL
    );

    CREATE TABLE IF NOT EXISTS facturas (
        numero     VARCHAR(30) PRIMARY KEY,
        cliente    VARCHAR(100) NOT NULL,
        cliente_id INTEGER,
        fecha      VARCHAR(10)  NOT NULL,
        total      NUMERIC(10, 2) NOT NULL,
        estado     VARCHAR(30)  NOT NULL,
        producto   VARCHAR(200),
        detalle    TEXT,
        CONSTRAINT fk_facturas_cliente
            FOREIGN KEY (cliente_id) REFERENCES clientes (id)
            ON UPDATE CASCADE ON DELETE SET NULL
    );
    """

    conexion = obtener_conexion_postgres()
    try:
        cursor = conexion.cursor()
        cursor.execute(esquema)
        # Migración para bases creadas antes: añade la columna producto
        # (nombre del producto real, p. ej. "Yuca") a la tabla facturas.
        cursor.execute(
            "ALTER TABLE facturas ADD COLUMN IF NOT EXISTS producto VARCHAR(200)"
        )
        # Dirección de envío del cliente (la pide la ventana de compra).
        cursor.execute(
            "ALTER TABLE clientes ADD COLUMN IF NOT EXISTS direccion VARCHAR(200)"
        )
        # Detalle de la compra en JSON: [{producto, cantidad, unitario, importe}, ...]
        cursor.execute(
            "ALTER TABLE facturas ADD COLUMN IF NOT EXISTS detalle TEXT"
        )
        # Migración para bases creadas antes: añade la clave foránea del
        # proveedor a la tabla productos (la usa el formulario de productos).
        cursor.execute(
            "ALTER TABLE productos ADD COLUMN IF NOT EXISTS proveedor_id INTEGER"
        )
        # Rol de la cuenta: 'admin' puede editar y eliminar; 'usuario' solo
        # comprar. Migración para bases creadas antes del rol.
        cursor.execute(
            """DO $$ BEGIN
                   IF NOT EXISTS (
                       SELECT 1 FROM information_schema.columns
                       WHERE table_name = 'usuarios' AND column_name = 'rol'
                   ) THEN
                       ALTER TABLE usuarios ADD COLUMN rol VARCHAR(20) NOT NULL DEFAULT 'usuario';
                   END IF;
               END $$;"""
        )
        cursor.execute(
            """DO $$ BEGIN
                   IF NOT EXISTS (
                       SELECT 1 FROM pg_constraint WHERE conname = 'fk_productos_proveedor'
                   ) THEN
                       ALTER TABLE productos ADD CONSTRAINT fk_productos_proveedor
                           FOREIGN KEY (proveedor_id) REFERENCES proveedores (id)
                           ON UPDATE CASCADE ON DELETE SET NULL;
                   END IF;
               END $$"""
        )
        _poblar_postgres(cursor)
        conexion.commit()
        cursor.close()
    finally:
        conexion.close()


def _poblar_postgres(cursor):
    """Inserta datos de ejemplo solo si las tablas están vacías."""
    cursor.execute("SELECT COUNT(*) FROM proveedores")
    if cursor.fetchone()[0] == 0:
        cursor.executemany(
            "INSERT INTO proveedores (nombre, producto_principal, ciudad) VALUES (%s, %s, %s)",
            [
                ("Asociación Kichwa Sumak", "Miel y guayusa", "Tena"),
                ("Cacao del Oriente", "Cacao fino", "Puyo"),
                ("Frutas del Amazonas", "Frutas tropicales", "Shushufindi"),
            ],
        )

    cursor.execute("SELECT COUNT(*) FROM productos")
    if cursor.fetchone()[0] == 0:
        cursor.executemany(
            "INSERT INTO productos (nombre, categoria, descripcion, precio, unidad, stock, imagen, proveedor_id) "
            "VALUES (%s, %s, %s, %s, %s, %s, %s, (SELECT id FROM proveedores WHERE nombre = %s))",
            [
                ("Caña", "Frutas", "Caña de la región amazónica, ideal para bebidas tradicionales y dulces.", 1.00, "unidad", 30, "caña.jpg", "Frutas del Amazonas"),
                ("Morete", "Frutas", "Fruto amazónico tradicional para usos culinarios y medicinales.", 3.00, "kilogramo", 18, "morete.jpg", "Frutas del Amazonas"),
                ("Ungurahua", "Productos naturales", "Fruto usado tradicionalmente en preparaciones de cuidado personal.", 3.50, "kilogramo", 14, "ungurahua.jpg", "Asociación Kichwa Sumak"),
                ("Miel Amazónica", "Productos naturales", "Miel pura y orgánica recolectada de colmenas silvestres.", 5.00, "frasco", 24, "miel.jpg", "Asociación Kichwa Sumak"),
                ("Yuca Fresca", "Alimentos", "Tubérculo amazónico nutritivo y versátil para tus comidas.", 5.00, "kg", 20, "yuca.jpg", "Frutas del Amazonas"),
                ("Plátanos Amazónicos", "Frutas", "Plátanos frescos y naturales de nuestros campos.", 6.00, "racimo", 16, "platanos.jpg", "Frutas del Amazonas"),
                ("Maní Tostado", "Alimentos", "Maní 100 % natural tostado al fuego tradicional.", 10.00, "kg", 10, "mani.jpg", "Cacao del Oriente"),
                ("Aceite de Coco", "Productos naturales", "Aceite de coco virgen prensado en frío, puro y natural.", 4.00, "litro", 15, "coco.jpg", "Asociación Kichwa Sumak"),
                ("Chocolate Artesanal", "Alimentos", "Chocolate elaborado con cacao amazónico de alta calidad.", 2.00, "barra", 36, "chocolate.jpg", "Cacao del Oriente"),
                ("Papaya", "Frutas", "Fruta tropical de sabor delicioso y alta en vitaminas.", 1.00, "unidad", 22, "papaya.jpg", "Frutas del Amazonas"),
                ("Choclo", "Alimentos", "Maíz fresco de la región amazónica para platos tradicionales.", 3.00, "kg", 19, "maiz.webp", "Frutas del Amazonas"),
                ("Hoja de Guayusa", "Productos naturales", "Infusión tradicional amazónica con propiedades energizantes.", 4.00, "kilogramo", 0, "guayusa.jpg", "Asociación Kichwa Sumak"),
                ("Naranjilla", "Frutas", "Fruta exótica agridulce, perfecta para jugos y postres.", 8.00, "caja", 13, "naranjilla.jpg", "Frutas del Amazonas"),
                ("Uvas Amazónicas", "Frutas", "Uvas de la región amazónica para consumo directo o jugos.", 6.50, "bandeja", 11, "uva.jpg", "Frutas del Amazonas"),
                ("Chonta Amazónica", "Productos naturales", "Fruto tradicional amazónico de múltiples usos culinarios.", 4.00, "500 g", 0, "chonta.jpg", "Asociación Kichwa Sumak"),
            ],
        )
    else:
        # Bases ya pobladas antes de existir proveedor_id: se vinculan los
        # productos de ejemplo con sus proveedores (operación idempotente).
        for producto, proveedor in (
            ("Miel Amazónica", "Asociación Kichwa Sumak"),
            ("Hoja de Guayusa", "Asociación Kichwa Sumak"),
            ("Ungurahua", "Asociación Kichwa Sumak"),
            ("Aceite de Coco", "Asociación Kichwa Sumak"),
            ("Chonta Amazónica", "Asociación Kichwa Sumak"),
            ("Chocolate Artesanal", "Cacao del Oriente"),
            ("Maní Tostado", "Cacao del Oriente"),
            ("Caña", "Frutas del Amazonas"),
            ("Morete", "Frutas del Amazonas"),
            ("Yuca Fresca", "Frutas del Amazonas"),
            ("Plátanos Amazónicos", "Frutas del Amazonas"),
            ("Papaya", "Frutas del Amazonas"),
            ("Choclo", "Frutas del Amazonas"),
            ("Naranjilla", "Frutas del Amazonas"),
            ("Uvas Amazónicas", "Frutas del Amazonas"),
        ):
            cursor.execute(
                "UPDATE productos SET proveedor_id = (SELECT id FROM proveedores WHERE nombre = %s) "
                "WHERE nombre = %s AND proveedor_id IS NULL",
                (proveedor, producto),
            )

    cursor.execute("SELECT COUNT(*) FROM clientes")
    if cursor.fetchone()[0] == 0:
        cursor.executemany(
            "INSERT INTO clientes (nombre, correo, telefono) VALUES (%s, %s, %s)",
            [
                ("Ana Paredes", "ana.paredes@ejemplo.com", "099 123 4567"),
                ("Carlos Mena", "carlos.mena@ejemplo.com", "098 765 4321"),
            ],
        )

    cursor.execute("SELECT COUNT(*) FROM facturas")
    if cursor.fetchone()[0] == 0:
        cursor.executemany(
            "INSERT INTO facturas (numero, cliente, fecha, total, estado) VALUES (%s, %s, %s, %s, %s)",
            [
                ("FAC-001", "Ana Paredes", "2026-08-15", 21.25, "Pagada"),
                ("FAC-002", "Carlos Mena", "2026-08-18", 18.00, "Pendiente"),
            ],
        )
