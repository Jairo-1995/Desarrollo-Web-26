"""Modelo de factura de la tabla ``facturas``."""


class Factura:
    """Representa una factura emitida a un cliente."""

    def __init__(self, numero, cliente, cliente_id, fecha, total, estado):
        self.numero = numero
        self.cliente = cliente          # nombre del cliente (texto o JOIN)
        self.cliente_id = cliente_id    # clave foránea a clientes.id
        self.fecha = fecha
        self.total = total
        self.estado = estado

    @classmethod
    def desde_fila(cls, fila):
        """Crea una Factura a partir de una fila de la base de datos."""
        return cls(
            fila["numero"], fila["cliente"], fila["cliente_id"],
            fila["fecha"], fila["total"], fila["estado"],
        )
