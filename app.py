"""Punto de entrada de la aplicación Productos Amazónicos."""

from flask import Flask, render_template

# Los recursos del sitio se sirven desde la carpeta estática convencional de Flask.
app = Flask(__name__, static_folder="static", template_folder="templates")

# Datos de ejemplo para los módulos de la aplicación. En una versión con base
# de datos, estos registros se obtendrían desde el almacenamiento persistente.
PRODUCTOS = [
    {"id": 1, "nombre": "Caña", "categoria": "Frutas", "descripcion": "Caña de la región amazónica, ideal para bebidas tradicionales y dulces.", "precio": 1.00, "unidad": "unidad", "stock": 30, "imagen": "caña.jpg"},
    {"id": 2, "nombre": "Morete", "categoria": "Frutas", "descripcion": "Fruto amazónico tradicional para usos culinarios y medicinales.", "precio": 3.00, "unidad": "kilogramo", "stock": 18, "imagen": "morete.jpg"},
    {"id": 3, "nombre": "Ungurahua", "categoria": "Productos naturales", "descripcion": "Fruto usado tradicionalmente en preparaciones de cuidado personal.", "precio": 3.50, "unidad": "kilogramo", "stock": 14, "imagen": "ungurahua.jpg"},
    {"id": 4, "nombre": "Miel Amazónica", "categoria": "Productos naturales", "descripcion": "Miel pura y orgánica recolectada de colmenas silvestres.", "precio": 5.00, "unidad": "frasco", "stock": 24, "imagen": "miel.jpg"},
    {"id": 5, "nombre": "Yuca Fresca", "categoria": "Alimentos", "descripcion": "Tubérculo amazónico nutritivo y versátil para tus comidas.", "precio": 5.00, "unidad": "kg", "stock": 20, "imagen": "yuca.jpg"},
    {"id": 6, "nombre": "Plátanos Amazónicos", "categoria": "Frutas", "descripcion": "Plátanos frescos y naturales de nuestros campos.", "precio": 6.00, "unidad": "racimo", "stock": 16, "imagen": "platanos.jpg"},
    {"id": 7, "nombre": "Maní Tostado", "categoria": "Alimentos", "descripcion": "Maní 100 % natural tostado al fuego tradicional.", "precio": 10.00, "unidad": "kg", "stock": 10, "imagen": "mani.jpg"},
    {"id": 8, "nombre": "Aceite de Coco", "categoria": "Productos naturales", "descripcion": "Aceite de coco virgen prensado en frío, puro y natural.", "precio": 4.00, "unidad": "litro", "stock": 15, "imagen": "coco.jpg"},
    {"id": 9, "nombre": "Chocolate Artesanal", "categoria": "Alimentos", "descripcion": "Chocolate elaborado con cacao amazónico de alta calidad.", "precio": 2.00, "unidad": "barra", "stock": 36, "imagen": "chocolate.jpg"},
    {"id": 10, "nombre": "Papaya", "categoria": "Frutas", "descripcion": "Fruta tropical de sabor delicioso y alta en vitaminas.", "precio": 1.00, "unidad": "unidad", "stock": 22, "imagen": "papaya.jpg"},
    {"id": 11, "nombre": "Choclo", "categoria": "Alimentos", "descripcion": "Maíz fresco de la región amazónica para platos tradicionales.", "precio": 3.00, "unidad": "kg", "stock": 19, "imagen": "choclo.jpg"},
    {"id": 12, "nombre": "Hoja de Guayusa", "categoria": "Productos naturales", "descripcion": "Infusión tradicional amazónica con propiedades energizantes.", "precio": 4.00, "unidad": "kilogramo", "stock": 0, "imagen": "guayusa.jpg"},
    {"id": 13, "nombre": "Naranjilla", "categoria": "Frutas", "descripcion": "Fruta exótica agridulce, perfecta para jugos y postres.", "precio": 8.00, "unidad": "caja", "stock": 13, "imagen": "naranjilla.jpg"},
    {"id": 14, "nombre": "Uvas Amazónicas", "categoria": "Frutas", "descripcion": "Uvas de la región amazónica para consumo directo o jugos.", "precio": 6.50, "unidad": "bandeja", "stock": 11, "imagen": "uva.jpg"},
    {"id": 15, "nombre": "Chonta Amazónica", "categoria": "Productos naturales", "descripcion": "Fruto tradicional amazónico de múltiples usos culinarios.", "precio": 4.00, "unidad": "500 g", "stock": 0, "imagen": "chonta.jpg"},
]

CLIENTES = [
    {"id": 1, "nombre": "Ana Paredes", "correo": "ana.paredes@ejemplo.com", "telefono": "099 123 4567"},
    {"id": 2, "nombre": "Carlos Mena", "correo": "carlos.mena@ejemplo.com", "telefono": "098 765 4321"},
]

PROVEEDORES = [
    {"id": 1, "nombre": "Asociación Kichwa Sumak", "producto_principal": "Miel y guayusa", "ciudad": "Tena"},
    {"id": 2, "nombre": "Cacao del Oriente", "producto_principal": "Cacao fino", "ciudad": "Puyo"},
]

FACTURAS = [
    {"numero": "FAC-001", "cliente": "Ana Paredes", "fecha": "2026-08-15", "total": 21.25, "estado": "Pagada"},
    {"numero": "FAC-002", "cliente": "Carlos Mena", "fecha": "2026-08-18", "total": 18.00, "estado": "Pendiente"},
]


@app.route("/")
def inicio():
    """Muestra la página principal del sitio."""
    mensaje_bienvenida = "Descubre productos auténticos de la Amazonía ecuatoriana."
    return render_template("index.html", mensaje_bienvenida=mensaje_bienvenida)


@app.route("/productos")
def productos():
    """Muestra el módulo de productos."""
    return render_template("productos.html", productos=PRODUCTOS)


@app.route("/clientes")
def clientes():
    """Muestra el módulo de clientes."""
    return render_template("clientes.html", clientes=CLIENTES)


@app.route("/proveedores")
def proveedores():
    """Muestra el módulo de proveedores."""
    return render_template("proveedores.html", proveedores=PROVEEDORES)


@app.route("/facturacion")
def facturacion():
    """Muestra el módulo de facturación."""
    return render_template("facturacion.html", facturas=FACTURAS)


if __name__ == "__main__":
    app.run(debug=True)
