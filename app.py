"""Punto de entrada de la aplicación Productos Amazónicos."""

import os
import re
import json

from datetime import date

from flask import Flask, abort, flash, redirect, render_template, request, url_for
from flask_login import (
    LoginManager,
    current_user,
    login_required,
    login_user,
    logout_user,
)
from flask_wtf import CSRFProtect
from werkzeug.security import check_password_hash, generate_password_hash
import database
from modelos.usuario import Usuario
from facturas_pdf import generar_factura_pdf, factura_completa
from forms import (
    FormularioCliente,
    FormularioEliminarProducto,
    FormularioEstadoFactura,
    FormularioFactura,
    FormularioLogin,
    FormularioProducto,
    FormularioProveedor,
    FormularioUsuario,
)
# Los recursos del sitio se sirven desde la carpeta estática convencional de Flask.
app = Flask(__name__, static_folder="static", template_folder="templates")

# Clave secreta indispensable para el manejo de sesiones (Flask/Flask-Login:
# cookie de sesión, current_user, login/logout) y para la protección CSRF
# de los formularios (Flask-WTF: csrf_token()). Debe declararse ANTES de
# inicializar CSRFProtect y LoginManager. En producción debe definirse una
# clave aleatoria mediante la variable de entorno SECRET_KEY; el valor
# predeterminado se utiliza exclusivamente en desarrollo.
app.config["SECRET_KEY"] = os.environ.get(
    "SECRET_KEY", "desarrollo-productos-amazonicos-clave-secreta"
)

# Protección CSRF global: habilita el helper csrf_token() en las plantillas
# (lo usa el formulario de cierre de sesión del navbar) y valida todos los POST.
csrf = CSRFProtect(app)

# Inicializa la base de datos PostgreSQL y las tablas.
database.init_db(app)

# Gestor de sesión de Flask-Login.
login_manager = LoginManager(app)
login_manager.login_view = "login"
login_manager.login_message = "Inicia sesión para acceder a esta página."
login_manager.login_message_category = "warning"


@login_manager.user_loader
def cargar_usuario(id_usuario):
    """Recarga el usuario autenticado a partir del id guardado en la sesión."""
    fila = database.get_db().execute(
        "SELECT id, email, nombre, rol FROM usuarios WHERE id = ?",
        (id_usuario,),
    ).fetchone()
    return Usuario.desde_fila(fila) if fila else None


def _usuario_actual():
    """Devuelve el Usuario autenticado (o None).

    Flask-Login expone current_user, el usuario de la sesión activa
    recargado por user_loader; no es necesario volver a la base de datos.
    """
    return current_user if current_user.is_authenticated else None


from functools import wraps


def _es_admin():
    """True si el usuario autenticado es administrador."""
    return bool(current_user.is_authenticated and getattr(current_user, "rol", "") == "admin")


def admin_requerido(vista):
    """Decorador: solo permite editar/eliminar a los administradores."""
    @wraps(vista)
    def envuelta(*args, **kwargs):
        if not _es_admin():
            flash(
                "Solo el administrador puede realizar esta acción.",
                "warning",
            )
            return redirect(url_for("dashboard"))
        return vista(*args, **kwargs)
    return envuelta


@app.route("/login", methods=["GET", "POST"])
def login():
    """Autentica a un usuario contra la tabla usuarios."""
    if current_user.is_authenticated:
        return redirect(url_for("dashboard"))
    formulario = FormularioLogin()
    if formulario.validate_on_submit():
        fila = database.get_db().execute(
            "SELECT * FROM usuarios WHERE email = ?", (formulario.email.data.strip().lower(),)
        ).fetchone()
        if fila and check_password_hash(fila["password"], formulario.password.data):
            login_user(Usuario.desde_fila(fila))
            flash(f"Bienvenido, {fila['nombre']}.", "success")
            destino = request.args.get("next")
            if destino and destino.startswith("/"):
                return redirect(destino)
            return redirect(url_for("dashboard"))
        flash("Usuario o contraseña incorrectos.", "danger")
    return render_template("login.html", form=formulario)


@app.route("/registro", methods=["GET", "POST"])
def registro():
    """Registra un nuevo usuario con contraseña cifrada (hash)."""
    if current_user.is_authenticated:
        return redirect(url_for("dashboard"))
    formulario = FormularioUsuario()
    if formulario.validate_on_submit():
        con = database.get_db()
        if con.execute(
            "SELECT id FROM usuarios WHERE email = ?", (formulario.email.data.strip().lower(),)
        ).fetchone():
            flash("Ese correo electrónico ya está registrado.", "danger")
            return render_template("registro.html", form=formulario)
        con.execute(
            "INSERT INTO usuarios (nombre, email, password, rol) VALUES (?, ?, ?, ?)",
            (
                formulario.nombre.data.strip(),
                formulario.email.data.strip().lower(),
                generate_password_hash(formulario.password.data),
                # Solo se aceptan los dos roles válidos del formulario.
                "admin" if formulario.rol.data == "admin" else "usuario",
            ),
        )
        con.commit()
        flash("Cuenta creada correctamente. Ahora puedes iniciar sesión.", "success")
        return redirect(url_for("login"))
    return render_template("registro.html", form=formulario)


@app.route("/dashboard")
@login_required
def dashboard():
    """Panel principal del usuario autenticado con resumen de los módulos."""
    con = database.get_db()
    resumen = {
        modulo: con.execute(f"SELECT COUNT(*) FROM {modulo}").fetchone()[0]
        for modulo in ("productos", "clientes", "proveedores", "facturas")
    }
    return render_template("dashboard.html", usuario=current_user, resumen=resumen)


@app.post("/logout")
def logout():
    """Cierra la sesión y redirige al usuario.

    Tras logout_user() el destino es la página de login (url_for("login")),
    donde verá el mensaje flash de confirmación; para enviarlo a la página
    principal bastaría con usar url_for("inicio") en el redirect.
    """
    logout_user()
    flash("Sesión cerrada correctamente.", "success")
    return redirect(url_for("login"))



def _filas(sql, parametros=()):
    """Ejecuta una consulta SELECT y devuelve las filas como diccionarios.

    Usa la conexión activa (database.get_db) a PostgreSQL.
    Usa fetchall() para recuperar varios registros de una sola vez.
    """
    con = database.get_db()
    cursor = con.execute(sql, tuple(parametros))
    # fetchall() devuelve objetos Fila (dict); solo se reemplazan los valores
    # None (NULL en PostgreSQL) por una cadena vacía para que no aparezca
    # "None" en las tablas de las vistas.
    return [{clave: ("" if valor is None else valor) for clave, valor in fila.items()}
            for fila in cursor.fetchall()]

# Los datos de los módulos se obtienen mediante consultas SELECT con
# fetchall() sobre la conexión activa en cada ruta de listado.


@app.route("/")
def inicio():
    """Muestra la página principal del sitio."""
    mensaje_bienvenida = "Descubre productos auténticos de la Amazonía ecuatoriana."
    # Proveedores registrados para el select del formulario de registro de productos.
    proveedores = _filas("SELECT nombre, producto_principal, ciudad FROM proveedores ORDER BY nombre")
    # Stock disponible de cada producto (por nombre) para las tarjetas de
    # "Productos Amazónicos Disponibles" de la página de inicio.
    stocks = {f["nombre"]: int(f["stock"] or 0)
              for f in _filas("SELECT nombre, stock FROM productos")}
    return render_template(
        "index.html",
        mensaje_bienvenida=mensaje_bienvenida,
        proveedores=proveedores,
        stocks=stocks,
    )


@app.post("/productos/registro-rapido")
def registro_rapido_producto():
    """Guarda el producto desde el formulario público de la página principal.

    Recibe JSON: {nombre, descripcion, categoria, proveedor (nombre, opcional)}.
    Si el nombre del proveedor existe en ``proveedores``, se guarda su id en
    ``productos.proveedor_id`` (relación clave foránea).
    """
    datos = request.get_json(silent=True) or {}
    nombre = str(datos.get("nombre", "")).strip()
    descripcion = str(datos.get("descripcion", "")).strip()
    categoria = str(datos.get("categoria", "")).strip()
    proveedor_nombre = str(datos.get("proveedor", "")).strip()

    if not (nombre and descripcion and categoria):
        return {"ok": False, "error": "Faltan campos obligatorios."}, 400

    con = database.get_db()
    if con.execute("SELECT id FROM productos WHERE nombre = ?", (nombre,)).fetchone():
        return {"ok": False, "error": "Ya existe un producto con ese nombre."}, 409

    proveedor_id = None
    if proveedor_nombre:
        fila = con.execute(
            "SELECT id FROM proveedores WHERE nombre = ?", (proveedor_nombre,)
        ).fetchone()
        if fila:
            proveedor_id = fila[0]
        else:
            # Si el proveedor no existe aún, se registra con el producto como principal.
            proveedor_id = con.execute(
                "INSERT INTO proveedores (nombre, producto_principal, ciudad) VALUES (?, ?, ?) RETURNING id",
                (proveedor_nombre, nombre, "No registrado"),
            ).fetchone()[0]

    con.execute(
        """INSERT INTO productos (nombre, categoria, descripcion, precio, unidad, stock, imagen, proveedor_id)
           VALUES (?, ?, ?, 0, "unidad", 0, NULL, ?)""",
        (nombre, categoria, descripcion, proveedor_id),
    )
    con.commit()
    return {"ok": True}

@app.route("/productos")
@login_required
def productos():
    """Muestra el módulo de productos.

    Acepta un parámetro opcional ?q= para filtrar los productos con una
    consulta SELECT ... WHERE nombre LIKE ?, parametrizada y segura.
    """
    busqueda = request.args.get("q", "").strip()
    if busqueda:
        # Consulta con WHERE: filtra por nombre o descripción (parámetros separados)
        filas = _filas(
            "SELECT p.id, p.nombre, p.categoria, p.descripcion, p.precio, p.unidad, "
            "p.stock, p.imagen, COALESCE(prov.nombre, '') AS proveedor "
            "FROM productos p LEFT JOIN proveedores prov ON prov.id = p.proveedor_id "
            "WHERE p.nombre LIKE ? OR p.descripcion LIKE ? ORDER BY p.id",
            (f"%{busqueda}%", f"%{busqueda}%"),
        )
    else:
        filas = _filas(
            "SELECT p.id, p.nombre, p.categoria, p.descripcion, p.precio, p.unidad, "
            "p.stock, p.imagen, COALESCE(prov.nombre, '') AS proveedor "
            "FROM productos p LEFT JOIN proveedores prov ON prov.id = p.proveedor_id "
            "ORDER BY p.id"
        )
    return render_template(
        "productos.html",
        productos=filas,
        busqueda=busqueda,
        formulario_eliminar=FormularioEliminarProducto(),
    )


@app.route("/productos/crear", methods=["GET", "POST"])
@login_required
@admin_requerido
def crear_producto():
    formulario = FormularioProducto()
    if formulario.validate_on_submit():
        con = database.get_db()
        nombre = formulario.nombre.data.strip()
        if con.execute(
            "SELECT id FROM productos WHERE nombre = ?", (nombre,)
        ).fetchone():
            flash("Este producto ya existe: no se puede repetir el nombre.", "danger")
            return render_template("formulario_producto.html", form=formulario)
        con.execute(
            """INSERT INTO productos (nombre, categoria, descripcion, precio, unidad, stock, imagen, proveedor_id)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
            (
                formulario.nombre.data,
                formulario.categoria.data,
                formulario.descripcion.data,
                float(formulario.precio.data),
                formulario.unidad.data,
                formulario.stock.data,
                formulario.imagen.data,
                int(formulario.proveedor.data) if formulario.proveedor.data else None,
            ),
        )
        con.commit()
        flash("Producto registrado correctamente.", "success")
        return redirect(url_for("productos"))
    return render_template("formulario_producto.html", form=formulario)


@app.route("/productos/<int:producto_id>/editar", methods=["GET", "POST"])
@login_required
@admin_requerido
def editar_producto(producto_id):
    """Edita un producto existente desde el catálogo."""
    con = database.get_db()
    producto = con.execute(
        "SELECT * FROM productos WHERE id = ?", (producto_id,)
    ).fetchone()
    if producto is None:
        abort(404)

    formulario = FormularioProducto(data=dict(producto))
    # Precarga el proveedor actual del producto en el select SOLO al abrir
    # la página (GET). En el POST no se toca: el valor que envió el usuario
    # ya está procesado por WTForms y sobrescribirlo aquí lo perdería.
    if not formulario.is_submitted:
        formulario.proveedor.data = str(producto["proveedor_id"]) if producto["proveedor_id"] else ""
    if formulario.validate_on_submit():
        nombre = formulario.nombre.data.strip()
        if con.execute(
            "SELECT id FROM productos WHERE nombre = ? AND id != ?",
            (nombre, producto_id),
        ).fetchone():
            flash("Este producto ya existe: no se puede repetir el nombre.", "danger")
            return render_template("formulario_producto.html", form=formulario, editando=True)
        con.execute(
            """UPDATE productos
               SET nombre = ?, categoria = ?, descripcion = ?, precio = ?,
                   unidad = ?, stock = ?, imagen = ?, proveedor_id = ?
               WHERE id = ?""",
            (
                formulario.nombre.data,
                formulario.categoria.data,
                formulario.descripcion.data,
                float(formulario.precio.data),
                formulario.unidad.data,
                formulario.stock.data,
                formulario.imagen.data,
                int(formulario.proveedor.data) if formulario.proveedor.data else None,
                producto_id,
            ),
        )
        con.commit()
        flash("Producto actualizado correctamente.", "success")
        return redirect(url_for("productos"))

    return render_template(
        "formulario_producto.html", form=formulario, editando=True
    )


@app.post("/productos/<int:producto_id>/eliminar")
@login_required
@admin_requerido
def eliminar_producto(producto_id):
    """Elimina un producto existente tras validar el token CSRF."""
    formulario = FormularioEliminarProducto()
    if not formulario.validate_on_submit():
        abort(400)

    con = database.get_db()
    resultado = con.execute("DELETE FROM productos WHERE id = ?", (producto_id,))
    if resultado.rowcount == 0:
        abort(404)
    con.commit()
    flash("Producto eliminado correctamente.", "success")
    return redirect(url_for("productos"))


@app.route("/clientes")
@login_required
def clientes():
    """Muestra el módulo de clientes."""
    return render_template(
        "clientes.html",
        # JOIN relacionado: cuenta las facturas de cada cliente usando
        # la clave foránea facturas.cliente_id -> clientes.id
        clientes=_filas(
            """SELECT c.id, c.nombre, c.correo, c.telefono,
                      COUNT(f.numero) AS total_facturas
               FROM clientes c
               LEFT JOIN facturas f ON f.cliente_id = c.id
               GROUP BY c.id, c.nombre, c.correo, c.telefono
               ORDER BY c.id"""
        ),
        formulario_eliminar=FormularioEliminarProducto(),
    )


@app.route("/clientes/crear", methods=["GET", "POST"])
@login_required
@admin_requerido
def crear_cliente():
    formulario = FormularioCliente()
    if formulario.validate_on_submit():
        try:
            con = database.get_db()
            telefono = formulario.telefono.data or ""
            if telefono and con.execute(
                "SELECT id FROM clientes WHERE telefono = ?", (telefono,)
            ).fetchone():
                flash("Ya existe un cliente con ese número de teléfono.", "danger")
                return render_template("formulario_cliente.html", form=formulario)
            con.execute(
                "INSERT INTO clientes (nombre, correo, telefono) VALUES (?, ?, ?)",
                (formulario.nombre.data, formulario.correo.data, formulario.telefono.data or ""),
            )
            con.commit()
        except database.ERROR_INTEGRIDAD:
            flash("Ya existe un cliente con ese correo electrónico.", "danger")
            return render_template("formulario_cliente.html", form=formulario)
        flash("Cliente registrado correctamente.", "success")
        return redirect(url_for("clientes"))
    return render_template("formulario_cliente.html", form=formulario)


@app.route("/clientes/<int:cliente_id>/editar", methods=["GET", "POST"])
@login_required
@admin_requerido
def editar_cliente(cliente_id):
    """Actualiza los datos de un cliente existente."""
    con = database.get_db()
    cliente = con.execute("SELECT * FROM clientes WHERE id = ?", (cliente_id,)).fetchone()
    if cliente is None:
        abort(404)

    formulario = FormularioCliente(data=dict(cliente))
    if formulario.validate_on_submit():
        try:
            telefono = formulario.telefono.data or ""
            if telefono and con.execute(
                "SELECT id FROM clientes WHERE telefono = ? AND id != ?",
                (telefono, cliente_id),
            ).fetchone():
                flash("Ya existe un cliente con ese número de teléfono.", "danger")
                return render_template("formulario_cliente.html", form=formulario, editando=True)
            con.execute(
                "UPDATE clientes SET nombre = ?, correo = ?, telefono = ? WHERE id = ?",
                (formulario.nombre.data, formulario.correo.data, formulario.telefono.data or "", cliente_id),
            )
            con.commit()
        except database.ERROR_INTEGRIDAD:
            flash("Ya existe un cliente con ese correo electrónico.", "danger")
            return render_template("formulario_cliente.html", form=formulario, editando=True)
        flash("Cliente actualizado correctamente.", "success")
        return redirect(url_for("clientes"))

    return render_template("formulario_cliente.html", form=formulario, editando=True)


@app.post("/clientes/<int:cliente_id>/eliminar")
@login_required
@admin_requerido
def eliminar_cliente(cliente_id):
    """Elimina un cliente tras validar el token CSRF.

    Si el cliente tiene facturas asociadas (clave foránea
    facturas.cliente_id -> clientes.id), no se elimina: se informa al
    usuario con un mensaje claro en lugar de provocar un error 500.
    """
    formulario = FormularioEliminarProducto()
    if not formulario.validate_on_submit():
        abort(400)

    con = database.get_db()
    try:
        resultado = con.execute("DELETE FROM clientes WHERE id = ?", (cliente_id,))
        if resultado.rowcount == 0:
            abort(404)
        con.commit()
    except database.ERROR_INTEGRIDAD:
        con.commit()  # descarta la transacción fallida del DELETE
        flash(
            "No se puede eliminar este cliente porque tiene facturas asociadas. "
            "Elimina primero sus facturas.",
            "warning",
        )
        return redirect(url_for("clientes"))
    flash("Cliente eliminado correctamente.", "success")
    return redirect(url_for("clientes"))


@app.route("/proveedores")
@login_required
def proveedores():
    """Muestra el módulo de proveedores."""
    return render_template(
        "proveedores.html",
        proveedores=_filas("SELECT * FROM proveedores ORDER BY id"),
        formulario_eliminar=FormularioEliminarProducto(),
    )


@app.route("/proveedores/crear", methods=["GET", "POST"])
@login_required
@admin_requerido
def crear_proveedor():
    formulario = FormularioProveedor()
    if formulario.validate_on_submit():
        con = database.get_db()
        con.execute(
            "INSERT INTO proveedores (nombre, producto_principal, ciudad) VALUES (?, ?, ?)",
            (formulario.nombre.data, formulario.producto_principal.data, formulario.ciudad.data),
        )
        con.commit()
        flash("Proveedor registrado correctamente.", "success")
        return redirect(url_for("proveedores"))
    return render_template("formulario_proveedor.html", form=formulario)


@app.route("/proveedores/<int:proveedor_id>/editar", methods=["GET", "POST"])
@login_required
@admin_requerido
def editar_proveedor(proveedor_id):
    con = database.get_db()
    proveedor = con.execute("SELECT * FROM proveedores WHERE id = ?", (proveedor_id,)).fetchone()
    if proveedor is None:
        abort(404)
    formulario = FormularioProveedor(data=dict(proveedor))
    if formulario.validate_on_submit():
        con.execute(
            "UPDATE proveedores SET nombre = ?, producto_principal = ?, ciudad = ? WHERE id = ?",
            (formulario.nombre.data, formulario.producto_principal.data, formulario.ciudad.data, proveedor_id),
        )
        con.commit()
        flash("Proveedor actualizado correctamente.", "success")
        return redirect(url_for("proveedores"))
    return render_template("formulario_proveedor.html", form=formulario, editando=True)


@app.post("/proveedores/<int:proveedor_id>/eliminar")
@login_required
@admin_requerido
def eliminar_proveedor(proveedor_id):
    formulario = FormularioEliminarProducto()
    if not formulario.validate_on_submit():
        abort(400)
    resultado = database.get_db().execute("DELETE FROM proveedores WHERE id = ?", (proveedor_id,))
    if resultado.rowcount == 0:
        abort(404)
    database.get_db().commit()
    flash("Proveedor eliminado correctamente.", "success")
    return redirect(url_for("proveedores"))


@app.route("/facturacion")
@login_required
def facturacion():
    """Muestra el módulo de facturación.

    Consulta relacionada entre dos tablas mediante clave foránea:
    facturas.cliente_id (FK) -> clientes.id, resuelta con un JOIN para
    mostrar el nombre real del cliente registrado.
    """
    facturas = _filas(
        """SELECT f.numero, f.fecha, f.total, f.estado,
                  COALESCE(c.nombre, f.cliente) AS cliente
           FROM facturas f
           LEFT JOIN clientes c ON f.cliente_id = c.id
           ORDER BY f.numero"""
    )
    return render_template(
        "facturacion.html",
        facturas=facturas,
        formulario_eliminar=FormularioEliminarProducto(),
    )


def _id_cliente_por_nombre(con, nombre):
    """Busca el id de un cliente por su nombre para asignar la clave foránea."""
    fila = con.execute("SELECT id FROM clientes WHERE nombre = ?", (nombre,)).fetchone()
    return fila[0] if fila else None


def _siguiente_numero_factura(con):
    """Genera el siguiente número de factura consecutivo (FAC-001, ...)."""
    base = con.execute("SELECT COUNT(*) FROM facturas").fetchone()[0]
    for incremento in range(1000):
        candidato = f"FAC-{base + 1 + incremento:03d}"
        if not con.execute(
            "SELECT numero FROM facturas WHERE numero = ?", (candidato,)
        ).fetchone():
            return candidato
    return None


@app.route("/facturacion/crear", methods=["GET", "POST"])
@login_required
@admin_requerido
def crear_factura():
    formulario = FormularioFactura()
    # El número de factura se genera automáticamente: se muestra en el
    # formulario (solo lectura) y se guarda ese valor al enviar.
    numero_automatico = _siguiente_numero_factura(database.get_db())
    formulario.numero.data = numero_automatico
    # Productos disponibles para la lista desplegable, junto con su precio
    # y stock: el navegador usa el precio para calcular el total al vuelo.
    productos = _filas("SELECT nombre, precio, stock FROM productos ORDER BY nombre")
    formulario.producto.choices = [("", "— Seleccione un producto —")] + [
        (p["nombre"], p["nombre"]) for p in productos
    ]
    precios = {p["nombre"]: float(p["precio"] or 0) for p in productos}
    stocks = {p["nombre"]: int(p["stock"] or 0) for p in productos}
    if formulario.validate_on_submit():
        try:
            con = database.get_db()
            producto = (formulario.producto.data or "").strip()
            cantidad = formulario.cantidad.data or 1
            # El total se calcula con el precio real del producto en la BD.
            precio = precios.get(producto, 0) if producto else 0
            total = round(precio * cantidad, 2)
            # No se permite facturar más de lo que hay en stock.
            disponible = stocks.get(producto, 0) if producto else 0
            if producto and cantidad > disponible:
                flash(
                    f"Solo hay {disponible} unidades de '{producto}' en stock.",
                    "warning",
                )
                return render_template(
                    "formulario_facturacion.html",
                    form=formulario, precios=precios, stocks=stocks,
                )
            # Detalle JSON: permite que el PDF muestre el nombre del
            # producto y la cantidad comprada por línea.
            unitario = precio
            detalle = json.dumps(
                [{
                    "producto": producto or "Productos amazónicos",
                    "cantidad": cantidad,
                    "unitario": unitario,
                    "importe": round(total, 2),
                }],
                ensure_ascii=False,
            ) if producto else None
            con.execute(
                """INSERT INTO facturas (numero, cliente, cliente_id, fecha, total, estado, producto, detalle)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
                (formulario.numero.data, formulario.cliente.data,
                 _id_cliente_por_nombre(con, formulario.cliente.data),
                 formulario.fecha.data.isoformat(), total, formulario.estado.data,
                 producto[:200] or None, detalle),
            )
            # Al facturar se descuenta la cantidad del stock del producto.
            if producto:
                con.execute(
                    "UPDATE productos SET stock = GREATEST(stock - ?, 0) WHERE nombre = ?",
                    (cantidad, producto),
                )
            con.commit()
        except database.ERROR_INTEGRIDAD:
            flash("Ya existe una factura con ese número.", "danger")
            formulario.numero.data = _siguiente_numero_factura(database.get_db())
            return render_template(
                "formulario_facturacion.html",
                form=formulario, precios=precios, stocks=stocks,
            )
        flash("Factura registrada correctamente.", "success")
        return redirect(url_for("facturacion"))
    return render_template(
        "formulario_facturacion.html",
        form=formulario, precios=precios, stocks=stocks,
    )


@app.route("/facturacion/<numero>/editar", methods=["GET", "POST"])
@login_required
@admin_requerido
def editar_factura(numero):
    """Cambia únicamente el estado de pago de la factura.

    Los demás datos (cliente, producto, cantidad, precio) se muestran
    como resumen de solo lectura; no se piden ni se modifican.
    """
    con = database.get_db()
    factura = con.execute("SELECT * FROM facturas WHERE numero = ?", (numero,)).fetchone()
    if factura is None:
        abort(404)
    # Cantidad comprada guardada en el detalle JSON (para el resumen).
    cantidad = 1
    try:
        detalle = json.loads(factura["detalle"] or "[]")
        if detalle:
            cantidad = int(float(detalle[0].get("cantidad", 1)))
    except (ValueError, TypeError):
        pass
    formulario = FormularioEstadoFactura(data={"estado": factura["estado"]})
    if formulario.validate_on_submit():
        con.execute(
            "UPDATE facturas SET estado = ? WHERE numero = ?",
            (formulario.estado.data, numero),
        )
        con.commit()
        flash("Estado de la factura actualizado correctamente.", "success")
        return redirect(url_for("facturacion"))
    return render_template(
        "formulario_estado_factura.html",
        form=formulario,
        factura=factura,
        cantidad=cantidad,
    )


@app.post("/facturacion/<numero>/eliminar")
@login_required
@admin_requerido
def eliminar_factura(numero):
    formulario = FormularioEliminarProducto()
    if not formulario.validate_on_submit():
        abort(400)
    con = database.get_db()
    factura = con.execute("SELECT estado FROM facturas WHERE numero = ?", (numero,)).fetchone()
    if factura is None:
        abort(404)
    # Una factura pendiente no se puede eliminar hasta que esté pagada.
    if str(factura["estado"]).lower() == "pendiente":
        flash(
            "No se puede eliminar una factura en estado PENDIENTE. "
            "Debes marcarla como Pagada primero.",
            "warning",
        )
        return redirect(url_for("facturacion"))
    resultado = con.execute("DELETE FROM facturas WHERE numero = ?", (numero,))
    if resultado.rowcount == 0:
        abort(404)
    con.commit()
    flash("Factura eliminada correctamente.", "success")
    return redirect(url_for("facturacion"))


@app.route("/facturacion/<numero>/pdf")
@login_required
def factura_pdf(numero):
    """Genera y descarga la factura seleccionada en formato PDF."""
    con = database.get_db()
    factura = con.execute(
        """SELECT f.numero, f.fecha, f.total, f.estado, f.producto, f.detalle,
                  COALESCE(c.nombre, f.cliente) AS cliente,
                  c.correo AS correo, c.telefono AS telefono, c.direccion AS direccion
           FROM facturas f
           LEFT JOIN clientes c ON f.cliente_id = c.id
           WHERE f.numero = ?""",
        (numero,),
    ).fetchone()
    if factura is None:
        abort(404)

    datos = dict(factura)
    # Se usa el detalle real de la compra guardado en la factura: una fila
    # por producto con su cantidad y precio unitario (p. ej. "2 x Yuca").
    try:
        detalle_guardado = json.loads(datos.get("detalle") or "[]")
    except (ValueError, TypeError):
        detalle_guardado = []
    lineas = [
        {
            "codigo": "PRD",
            "descripcion": str(item.get("producto", "Producto")),
            "cantidad": float(item.get("cantidad", 1)) or 1.0,
            "unitario": float(item.get("unitario", 0)),
        }
        for item in detalle_guardado
    ]
    if not lineas:
        # Respaldo para facturas antiguas sin detalle: una sola línea con
        # el nombre del producto (o el texto genérico) y su total.
        descripcion = str(datos.get("producto") or "").strip() or "Productos amazónicos"
        lineas = [{
            "codigo": "PRD",
            "descripcion": descripcion,
            "cantidad": 1,
            "unitario": float(datos["total"]),
        }]
    datos_pdf = factura_completa(datos, lineas)
    contenido = generar_factura_pdf(datos_pdf)

    from flask import Response
    return Response(
        contenido,
        mimetype="application/pdf",
        headers={
            "Content-Disposition": f"attachment; filename=Factura_{numero}.pdf",
            "Content-Length": str(len(contenido)),
        },
    )


@app.post("/comprar")
@login_required
def comprar():
    """Registra la compra desde la ventana flotante del catálogo.

    Crea (o reutiliza) el cliente en la tabla ``clientes`` usando los datos
    del usuario autenticado y guarda la factura en ``facturas`` con el
    nombre del cliente, la fecha actual y el valor de la compra.
    """
    producto = request.form.get("producto", "Producto").strip()
    correo_cliente = request.form.get("correo", "").strip() or current_user.email
    telefono_cliente = request.form.get("telefono", "").strip()
    direccion_cliente = request.form.get("direccion", "").strip()
    # Origen de la compra: para devolver al usuario a la misma página donde
    # estaba (inicio o productos). Se usa el campo oculto "origen" del
    # formulario y, como respaldo, la página desde la que se envió (referer).
    origen = request.form.get("origen", "").strip()
    if not origen:
        referer = request.headers.get("Referer", "")
        if "productos" in referer:
            origen = "productos"
    if origen not in ("inicio", "productos"):
        origen = "inicio"
    punto_destino = url_for(origen)
    # Validación igual a forms/cliente_form.py: solo 10 dígitos numéricos.
    if telefono_cliente and not re.fullmatch(r"\d{10}", telefono_cliente):
        flash("El teléfono debe tener exactamente 10 dígitos numéricos.", "danger")
        return redirect(punto_destino)
    try:
        total = float(request.form.get("total", "0"))
    except ValueError:
        total = 0.0

    if total <= 0:
        flash("No se pudo registrar la compra: valor no válido.", "danger")
        return redirect(punto_destino)

    con = database.get_db()
    # Descuento de stock: se busca el producto por nombre y se resta la
    # cantidad comprada. Si no alcanza el stock, la compra se rechaza;
    # al llegar a 0 queda agotado (el botón Comprar se deshabilita).
    try:
        cantidad = max(1, int(request.form.get("cantidad", "1")))
    except ValueError:
        cantidad = 1
    fila_producto = con.execute(
        "SELECT id, stock, precio FROM productos WHERE nombre = ?", (producto,)
    ).fetchone()
    stock_restante = None
    if fila_producto:
        stock_actual = fila_producto[1]
        precio_unitario = float(fila_producto[2] or 0) or total / cantidad
        if stock_actual < cantidad:
            flash(
                f"No hay stock suficiente de {producto}: quedan {stock_actual} "
                f"unidad(es) y pediste {cantidad}.",
                "danger",
            )
            return redirect(punto_destino)
        con.execute(
            "UPDATE productos SET stock = stock - ? WHERE id = ?",
            (cantidad, fila_producto[0]),
        )
        stock_restante = stock_actual - cantidad
    else:
        precio_unitario = total / cantidad
    # Elemento de detalle para la factura: producto, cantidad y precio unitario.
    item_detalle = {
        "producto": producto,
        "cantidad": cantidad,
        "unitario": round(precio_unitario, 2),
        "importe": round(precio_unitario * cantidad, 2),
    }
    # Cliente: se busca por el correo del usuario autenticado y, si no
    # existe, se registra automáticamente con su nombre y correo.
    fila = con.execute(
        "SELECT id FROM clientes WHERE correo = ?", (current_user.email,)
    ).fetchone()
    if fila:
        cliente_id = fila[0]
        nombre_cliente = current_user.nombre
        # Si el usuario indicó un teléfono o dirección en el formulario, se guardan.
        if telefono_cliente:
            con.execute(
                "UPDATE clientes SET telefono = ? WHERE id = ?",
                (telefono_cliente, cliente_id),
            )
        if direccion_cliente:
            con.execute(
                "UPDATE clientes SET direccion = ? WHERE id = ?",
                (direccion_cliente[:200], cliente_id),
            )
    else:
        cliente_id = con.execute(
            "INSERT INTO clientes (nombre, correo, telefono, direccion) VALUES (?, ?, ?, ?) RETURNING id",
            (current_user.nombre, correo_cliente,
             telefono_cliente or "No registrado",
             direccion_cliente[:200] or "S/N"),
        ).fetchone()[0]

    # Si el cliente ya tiene una factura pendiente, en lugar de crear una
    # factura nueva se suma el valor de esta compra a esa misma factura.
    pendiente = con.execute(
        """SELECT numero, total, producto, detalle FROM facturas
           WHERE cliente_id = ? AND estado = 'Pendiente'
           ORDER BY numero LIMIT 1""",
        (cliente_id,),
    ).fetchone()
    if pendiente:
        numero = pendiente[0]
        nuevo_total = float(pendiente[1]) + total
        # Se añade el producto comprado a la descripción de la factura.
        productos_previos = (pendiente[2] or "").strip()
        if productos_previos and producto not in productos_previos.split(", "):
            productos_actualizados = f"{productos_previos}, {producto}"
        elif not productos_previos:
            productos_actualizados = producto
        else:
            productos_actualizados = productos_previos
        # Detalle: si el producto ya está en la factura se suma la cantidad.
        try:
            detalle = json.loads(pendiente[3] or "[]")
        except (ValueError, TypeError):
            detalle = []
        for previo in detalle:
            if previo.get("producto") == producto:
                previo["cantidad"] = previo.get("cantidad", 1) + cantidad
                previo["importe"] = round(previo["cantidad"] * previo.get("unitario", precio_unitario), 2)
                break
        else:
            detalle.append(item_detalle)
        con.execute(
            "UPDATE facturas SET total = ?, producto = ?, detalle = ? WHERE numero = ?",
            (nuevo_total, productos_actualizados[:200], json.dumps(detalle, ensure_ascii=False), numero),
        )
        con.commit()
        extra = (
            f" Stock restante: {stock_restante}."
            if stock_restante is not None
            else ""
        )
        flash(
            f"¡Compra registrada! Producto: {producto}. Se sumó ${total:.2f} "
            f"a la factura {numero}, que ahora suma ${nuevo_total:.2f}."
            + extra,
            "success",
        )
        return redirect(punto_destino)

    # No hay factura pendiente: se crea una con número consecutivo
    # (FAC-001, FAC-002, ...) generado automáticamente.
    numero = _siguiente_numero_factura(con)
    if numero is None:
        flash("No se pudo generar el número de factura.", "danger")
        return redirect(punto_destino)

    con.execute(
        """INSERT INTO facturas (numero, cliente, cliente_id, fecha, total, estado, producto, detalle)
           VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
        (numero, current_user.nombre, cliente_id,
         date.today().isoformat(), total, "Pendiente", producto[:200],
         json.dumps([item_detalle], ensure_ascii=False)),
    )
    con.commit()
    extra = (
        f" Stock restante: {stock_restante}."
        if stock_restante is not None
        else ""
    )
    flash(
        f"¡Compra registrada! Producto: {producto}. Factura {numero} "
        f"por un valor de ${total:.2f}." + extra,
        "success",
    )
    return redirect(punto_destino)


if __name__ == "__main__":
    app.run(debug=True)
