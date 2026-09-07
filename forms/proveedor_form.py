"""Formulario del módulo de proveedores."""

from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired, Length


class FormularioProveedor(FlaskForm):
    """Formulario para registrar o editar un proveedor."""

    nombre = StringField(
        "Nombre",
        validators=[DataRequired(message="El nombre es obligatorio."),
                    Length(max=120, message="Máximo 120 caracteres.")],
    )
    producto_principal = StringField(
        "Producto principal",
        validators=[DataRequired(message="El producto principal es obligatorio."),
                    Length(max=120, message="Máximo 120 caracteres.")],
    )
    ciudad = StringField(
        "Ciudad",
        validators=[DataRequired(message="La ciudad es obligatoria."),
                    Length(max=60, message="Máximo 60 caracteres.")],
    )
