"""Modelo de cliente de la tabla ``clientes``."""


class Cliente:
    """Representa un cliente registrado con sus datos de contacto."""

    def __init__(self, id, nombre, correo, telefono, total_facturas=0):
        self.id = id
        self.nombre = nombre
        self.correo = correo
        self.telefono = telefono
        self.total_facturas = total_facturas

    @classmethod
    def desde_fila(cls, fila):
        """Crea un Cliente a partir de una fila de la base de datos.

        Acepta filas con la columna calculada ``total_facturas`` (JOIN con
        facturas) o sin ella.
        """
        return cls(
            fila["id"],
            fila["nombre"],
            fila["correo"],
            fila["telefono"],
            fila["total_facturas"] if "total_facturas" in fila.keys() else 0,
        )
