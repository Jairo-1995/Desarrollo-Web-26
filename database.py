"""Gestión de la conexión a la base de datos SQLite con el módulo sqlite3."""

import os
import sqlite3

from flask import g

# Ruta absoluta al archivo de la base de datos local (dentro de la carpeta data).
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "data", "amazonia.db")


def get_db():
    """Establece y devuelve la conexión SQLite con data/amazonia.db.

    La conexión se guarda en el objeto ``g`` de Flask para reutilizarla
    durante la misma petición y cerrarla automáticamente al terminar.
    """
    if "db" not in g:
        g.db = sqlite3.connect(DB_PATH)  # Conexión mediante sqlite3.connect()
        g.db.row_factory = sqlite3.Row  # filas accesibles como diccionarios
        g.db.execute("PRAGMA foreign_keys = ON")
    return g.db


def close_db(_exc=None):
    """Cierra la conexión al finalizar la petición."""
    db = g.pop("db", None)
    if db is not None:
        db.close()


def init_db(app):
    """Crea las tablas (si no existen) y registra el cierre de conexión."""
    app.teardown_appcontext(close_db)

    esquema = """
    CREATE TABLE IF NOT EXISTS productos (
        id          INTEGER PRIMARY KEY AUTOINCREMENT,            -- clave primaria
        nombre      TEXT    NOT NULL CHECK (length(nombre) <= 100),   -- StringField obligatorio
        categoria   TEXT    NOT NULL,                                 -- SelectField con CATEGORIAS
        descripcion TEXT,                                            -- TextAreaField opcional
        precio      REAL    NOT NULL CHECK (precio >= 0),             -- DecimalField >= 0
        unidad      TEXT    NOT NULL CHECK (length(unidad) <= 30),    -- StringField obligatorio
        stock       INTEGER NOT NULL DEFAULT 0 CHECK (stock >= 0),    -- IntegerField >= 0
        imagen      TEXT CHECK (length(imagen) <= 100)                -- StringField opcional
    );

    CREATE TABLE IF NOT EXISTS clientes (
        id       INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre   TEXT NOT NULL,
        correo   TEXT NOT NULL UNIQUE,
        telefono TEXT NOT NULL
    );

    CREATE TABLE IF NOT EXISTS proveedores (
        id                 INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre             TEXT NOT NULL,
        producto_principal TEXT NOT NULL,
        ciudad             TEXT NOT NULL
    );

    CREATE TABLE IF NOT EXISTS facturas (
        numero  TEXT PRIMARY KEY,
        cliente TEXT NOT NULL,
        fecha   TEXT NOT NULL,
        total   REAL NOT NULL,
        estado  TEXT NOT NULL
    );
    """

    with sqlite3.connect(DB_PATH) as con:
        con.executescript(esquema)
        _poblar(con)
        con.commit()  # Se confirman los cambios
    con.close()  # Se cierra correctamente la conexión


def _poblar(con):
    """Inserta datos de ejemplo solo si las tablas están vacías."""
    if con.execute("SELECT COUNT(*) FROM productos").fetchone()[0] == 0:
        con.executemany(
            "INSERT INTO productos (nombre, categoria, descripcion, precio, unidad, stock, imagen) VALUES (?, ?, ?, ?, ?, ?, ?)",
            [
                ("Caña", "Frutas", "Caña de la región amazónica, ideal para bebidas tradicionales y dulces.", 1.00, "unidad", 30, "caña.jpg"),
                ("Morete", "Frutas", "Fruto amazónico tradicional para usos culinarios y medicinales.", 3.00, "kilogramo", 18, "morete.jpg"),
                ("Ungurahua", "Productos naturales", "Fruto usado tradicionalmente en preparaciones de cuidado personal.", 3.50, "kilogramo", 14, "ungurahua.jpg"),
                ("Miel Amazónica", "Productos naturales", "Miel pura y orgánica recolectada de colmenas silvestres.", 5.00, "frasco", 24, "miel.jpg"),
                ("Yuca Fresca", "Alimentos", "Tubérculo amazónico nutritivo y versátil para tus comidas.", 5.00, "kg", 20, "yuca.jpg"),
                ("Plátanos Amazónicos", "Frutas", "Plátanos frescos y naturales de nuestros campos.", 6.00, "racimo", 16, "platanos.jpg"),
                ("Maní Tostado", "Alimentos", "Maní 100 % natural tostado al fuego tradicional.", 10.00, "kg", 10, "mani.jpg"),
                ("Aceite de Coco", "Productos naturales", "Aceite de coco virgen prensado en frío, puro y natural.", 4.00, "litro", 15, "coco.jpg"),
                ("Chocolate Artesanal", "Alimentos", "Chocolate elaborado con cacao amazónico de alta calidad.", 2.00, "barra", 36, "chocolate.jpg"),
                ("Papaya", "Frutas", "Fruta tropical de sabor delicioso y alta en vitaminas.", 1.00, "unidad", 22, "papaya.jpg"),
                ("Choclo", "Alimentos", "Maíz fresco de la región amazónica para platos tradicionales.", 3.00, "kg", 19, "maiz.webp"),
                ("Hoja de Guayusa", "Productos naturales", "Infusión tradicional amazónica con propiedades energizantes.", 4.00, "kilogramo", 0, "guayusa.jpg"),
                ("Naranjilla", "Frutas", "Fruta exótica agridulce, perfecta para jugos y postres.", 8.00, "caja", 13, "naranjilla.jpg"),
                ("Uvas Amazónicas", "Frutas", "Uvas de la región amazónica para consumo directo o jugos.", 6.50, "bandeja", 11, "uva.jpg"),
                ("Chonta Amazónica", "Productos naturales", "Fruto tradicional amazónico de múltiples usos culinarios.", 4.00, "500 g", 0, "chonta.jpg"),
            ],
        )
    if con.execute("SELECT COUNT(*) FROM clientes").fetchone()[0] == 0:
        con.executemany(
            "INSERT INTO clientes (nombre, correo, telefono) VALUES (?, ?, ?)",
            [
                ("Ana Paredes", "ana.paredes@ejemplo.com", "099 123 4567"),
                ("Carlos Mena", "carlos.mena@ejemplo.com", "098 765 4321"),
            ],
        )
    if con.execute("SELECT COUNT(*) FROM proveedores").fetchone()[0] == 0:
        con.executemany(
            "INSERT INTO proveedores (nombre, producto_principal, ciudad) VALUES (?, ?, ?)",
            [
                ("Asociación Kichwa Sumak", "Miel y guayusa", "Tena"),
                ("Cacao del Oriente", "Cacao fino", "Puyo"),
            ],
        )
    if con.execute("SELECT COUNT(*) FROM facturas").fetchone()[0] == 0:
        con.executemany(
            "INSERT INTO facturas (numero, cliente, fecha, total, estado) VALUES (?, ?, ?, ?, ?)",
            [
                ("FAC-001", "Ana Paredes", "2026-08-15", 21.25, "Pagada"),
                ("FAC-002", "Carlos Mena", "2026-08-18", 18.00, "Pendiente"),
            ],
        )
