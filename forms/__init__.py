"""Paquete de formularios de la aplicación Productos Amazónicos.

Cada módulo de la aplicación tiene su propio archivo de formularios:
- producto_form.py     -> FormularioProducto
- cliente_form.py      -> FormularioCliente
- proveedor_form.py    -> FormularioProveedor
- facturacion_form.py  -> FormularioFactura

Todas las clases se reexportan aquí para poder importarlas de forma
sencilla, por ejemplo:  from forms import FormularioProducto
"""

from forms.cliente_form import FormularioCliente
from forms.facturacion_form import FormularioFactura
from forms.eliminar_producto_form import FormularioEliminarProducto
from forms.producto_form import FormularioProducto
from forms.proveedor_form import FormularioProveedor

__all__ = [
    "FormularioCliente",
    "FormularioFactura",
    "FormularioEliminarProducto",
    "FormularioProducto",
    "FormularioProveedor",
]
