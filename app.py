"""Punto de entrada de la aplicación Productos Amazónicos."""

from flask import Flask, render_template

# Los recursos del sitio se sirven desde la carpeta estática convencional de Flask.
app = Flask(__name__, static_folder="static", template_folder="templates")


@app.route("/")
def inicio():
    """Muestra la página principal del sitio."""
    return render_template("index.html")


@app.route("/productos")
def productos():
    """Muestra el módulo de productos."""
    return render_template("productos.html")


@app.route("/clientes")
def clientes():
    """Muestra el módulo de clientes."""
    return render_template("clientes.html")


@app.route("/proveedores")
def proveedores():
    """Muestra el módulo de proveedores."""
    return render_template("proveedores.html")


@app.route("/facturacion")
def facturacion():
    """Muestra el módulo de facturación."""
    return render_template("facturacion.html")


if __name__ == "__main__":
    app.run(debug=True)
