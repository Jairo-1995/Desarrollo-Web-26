"""Punto de entrada de la aplicación Productos Amazónicos."""

import os

import sqlite3
from datetime import date

from flask import Flask, abort, flash, redirect, render_template, url_for

import database
from forms import (
    FormularioCliente,
    FormularioEliminarProducto,
    FormularioFactura,
    FormularioProducto,
    FormularioProveedor,
)

# Los recursos del sitio se sirven desde la carpeta estática convencional de Flask.
app = Flask(__name__, static_folder="static", template_folder="templates")

# Clave secreta necesaria para la protección CSRF de los formularios (Flask-WTF).
# En producción debe definirse una clave aleatoria mediante la variable de entorno
# SECRET_KEY; el valor predeterminado se utiliza exclusivamente en desarrollo.
app.config["SECRET_KEY"] = os.environ.get(
    "SECRET_KEY", "desarrollo-productos-amazonicos-clave-secreta"
)

# Inicializa la base de datos SQLite (data/amazonia.db) y las tablas.
database.init_db(app)


def _filas(sql):
    """Ejecuta una consulta SELECT y devuelve las filas como diccionarios."""
    filas = database.get_db().execute(sql).fetchall()
    return [dict(fila) for fila in filas]

# Los datos de los módulos se obtienen desde la base de datos SQLite
# (data/amazonia.db) mediante consultas SELECT en cada ruta.


@app.route("/")
def inicio():
    """Muestra la página principal del sitio."""
    mensaje_bienvenida = "Descubre productos auténticos de la Amazonía ecuatoriana."
    return render_template("index.html", mensaje_bienvenida=mensaje_bienvenida)

@app.route("/productos")
def productos():
    """Muestra el módulo de productos."""
    return render_template(
        "productos.html",
        productos=_filas("SELECT * FROM productos ORDER BY id"),
        formulario_eliminar=FormularioEliminarProducto(),
    )


@app.route("/productos/crear", methods=["GET", "POST"])
def crear_producto():
    formulario = FormularioProducto()
    if formulario.validate_on_submit():
        con = database.get_db()
        con.execute(
            """INSERT INTO productos (nombre, categoria, descripcion, precio, unidad, stock, imagen)
               VALUES (?, ?, ?, ?, ?, ?, ?)""",
            (
                formulario.nombre.data,
                formulario.categoria.data,
                formulario.descripcion.data,
                float(formulario.precio.data),
                formulario.unidad.data,
                formulario.stock.data,
                formulario.imagen.data,
            ),
        )
        con.commit()
        flash("Producto registrado correctamente.", "success")
        return redirect(url_for("productos"))
    return render_template("formulario_producto.html", form=formulario)


@app.route("/productos/<int:producto_id>/editar", methods=["GET", "POST"])
def editar_producto(producto_id):
    """Edita un producto existente desde el catálogo."""
    con = database.get_db()
    producto = con.execute(
        "SELECT * FROM productos WHERE id = ?", (producto_id,)
    ).fetchone()
    if producto is None:
        abort(404)

    formulario = FormularioProducto(data=dict(producto))
    if formulario.validate_on_submit():
        con.execute(
            """UPDATE productos
               SET nombre = ?, categoria = ?, descripcion = ?, precio = ?,
                   unidad = ?, stock = ?, imagen = ?
               WHERE id = ?""",
            (
                formulario.nombre.data,
                formulario.categoria.data,
                formulario.descripcion.data,
                float(formulario.precio.data),
                formulario.unidad.data,
                formulario.stock.data,
                formulario.imagen.data,
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
def clientes():
    """Muestra el módulo de clientes."""
    return render_template(
        "clientes.html",
        clientes=_filas("SELECT * FROM clientes ORDER BY id"),
        formulario_eliminar=FormularioEliminarProducto(),
    )


@app.route("/clientes/crear", methods=["GET", "POST"])
def crear_cliente():
    formulario = FormularioCliente()
    if formulario.validate_on_submit():
        try:
            con = database.get_db()
            con.execute(
                "INSERT INTO clientes (nombre, correo, telefono) VALUES (?, ?, ?)",
                (formulario.nombre.data, formulario.correo.data, formulario.telefono.data or ""),
            )
            con.commit()
        except sqlite3.IntegrityError:
            flash("Ya existe un cliente con ese correo electrónico.", "danger")
            return render_template("formulario_cliente.html", form=formulario)
        flash("Cliente registrado correctamente.", "success")
        return redirect(url_for("clientes"))
    return render_template("formulario_cliente.html", form=formulario)


@app.route("/clientes/<int:cliente_id>/editar", methods=["GET", "POST"])
def editar_cliente(cliente_id):
    """Actualiza los datos de un cliente existente."""
    con = database.get_db()
    cliente = con.execute("SELECT * FROM clientes WHERE id = ?", (cliente_id,)).fetchone()
    if cliente is None:
        abort(404)

    formulario = FormularioCliente(data=dict(cliente))
    if formulario.validate_on_submit():
        try:
            con.execute(
                "UPDATE clientes SET nombre = ?, correo = ?, telefono = ? WHERE id = ?",
                (formulario.nombre.data, formulario.correo.data, formulario.telefono.data or "", cliente_id),
            )
            con.commit()
        except sqlite3.IntegrityError:
            flash("Ya existe un cliente con ese correo electrónico.", "danger")
            return render_template("formulario_cliente.html", form=formulario, editando=True)
        flash("Cliente actualizado correctamente.", "success")
        return redirect(url_for("clientes"))

    return render_template("formulario_cliente.html", form=formulario, editando=True)


@app.post("/clientes/<int:cliente_id>/eliminar")
def eliminar_cliente(cliente_id):
    """Elimina un cliente tras validar el token CSRF."""
    formulario = FormularioEliminarProducto()
    if not formulario.validate_on_submit():
        abort(400)

    con = database.get_db()
    resultado = con.execute("DELETE FROM clientes WHERE id = ?", (cliente_id,))
    if resultado.rowcount == 0:
        abort(404)
    con.commit()
    flash("Cliente eliminado correctamente.", "success")
    return redirect(url_for("clientes"))


@app.route("/proveedores")
def proveedores():
    """Muestra el módulo de proveedores."""
    return render_template(
        "proveedores.html",
        proveedores=_filas("SELECT * FROM proveedores ORDER BY id"),
        formulario_eliminar=FormularioEliminarProducto(),
    )


@app.route("/proveedores/crear", methods=["GET", "POST"])
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
def facturacion():
    """Muestra el módulo de facturación."""
    return render_template(
        "facturacion.html",
        facturas=_filas("SELECT * FROM facturas ORDER BY numero"),
        formulario_eliminar=FormularioEliminarProducto(),
    )


@app.route("/facturacion/crear", methods=["GET", "POST"])
def crear_factura():
    formulario = FormularioFactura()
    if formulario.validate_on_submit():
        try:
            con = database.get_db()
            con.execute(
                "INSERT INTO facturas (numero, cliente, fecha, total, estado) VALUES (?, ?, ?, ?, ?)",
                (formulario.numero.data, formulario.cliente.data, formulario.fecha.data.isoformat(), float(formulario.total.data), formulario.estado.data),
            )
            con.commit()
        except sqlite3.IntegrityError:
            flash("Ya existe una factura con ese número.", "danger")
            return render_template("formulario_facturacion.html", form=formulario)
        flash("Factura registrada correctamente.", "success")
        return redirect(url_for("facturacion"))
    return render_template("formulario_facturacion.html", form=formulario)


@app.route("/facturacion/<numero>/editar", methods=["GET", "POST"])
def editar_factura(numero):
    con = database.get_db()
    factura = con.execute("SELECT * FROM facturas WHERE numero = ?", (numero,)).fetchone()
    if factura is None:
        abort(404)
    datos_factura = dict(factura)
    datos_factura["fecha"] = date.fromisoformat(datos_factura["fecha"])
    formulario = FormularioFactura(data=datos_factura)
    if formulario.validate_on_submit():
        try:
            con.execute(
                """UPDATE facturas SET numero = ?, cliente = ?, fecha = ?, total = ?, estado = ?
                   WHERE numero = ?""",
                (formulario.numero.data, formulario.cliente.data, formulario.fecha.data.isoformat(), float(formulario.total.data), formulario.estado.data, numero),
            )
            con.commit()
        except sqlite3.IntegrityError:
            flash("Ya existe una factura con ese número.", "danger")
            return render_template("formulario_facturacion.html", form=formulario, editando=True)
        flash("Factura actualizada correctamente.", "success")
        return redirect(url_for("facturacion"))
    return render_template("formulario_facturacion.html", form=formulario, editando=True)


@app.post("/facturacion/<numero>/eliminar")
def eliminar_factura(numero):
    formulario = FormularioEliminarProducto()
    if not formulario.validate_on_submit():
        abort(400)
    resultado = database.get_db().execute("DELETE FROM facturas WHERE numero = ?", (numero,))
    if resultado.rowcount == 0:
        abort(404)
    database.get_db().commit()
    flash("Factura eliminada correctamente.", "success")
    return redirect(url_for("facturacion"))


if __name__ == "__main__":
    app.run(debug=True)
