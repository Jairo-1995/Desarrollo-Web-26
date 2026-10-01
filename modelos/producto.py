"""Modelo de producto del catálogo (tabla ``productos``)."""


class Producto:
    """Representa un producto amazónico del inventario."""

    def __init__(self, id, nombre, categoria, descripcion, precio,
                 unidad, stock, imagen=None, proveedor_id=None):
        self.id = id
        self.nombre = nombre
        self.categoria = categoria
        self.descripcion = descripcion
        self.precio = precio
        self.unidad = unidad
        self.stock = stock
        self.imagen = imagen
        self.proveedor_id = proveedor_id

    @classmethod
    def desde_fila(cls, fila):
        """Crea un Producto a partir de una fila de la base de datos."""
        proveedor = fila["proveedor_id"] if "proveedor_id" in fila.keys() else None
        return cls(
            fila["id"], fila["nombre"], fila["categoria"],
            fila["descripcion"], fila["precio"], fila["unidad"],
            fila["stock"], fila["imagen"], proveedor,
        )
