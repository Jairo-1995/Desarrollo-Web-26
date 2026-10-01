"""Modelo de proveedor de la tabla ``proveedores``."""


class Proveedor:
    """Representa un proveedor de productos amazónicos."""

    def __init__(self, id, nombre, producto_principal, ciudad):
        self.id = id
        self.nombre = nombre
        self.producto_principal = producto_principal
        self.ciudad = ciudad

    @classmethod
    def desde_fila(cls, fila):
        """Crea un Proveedor a partir de una fila de la base de datos."""
        return cls(fila["id"], fila["nombre"], fila["producto_principal"], fila["ciudad"])
