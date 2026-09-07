"""Formulario del módulo de productos."""

from flask_wtf import FlaskForm
from wtforms import DecimalField, IntegerField, SelectField, StringField, TextAreaField
from wtforms.validators import DataRequired, Length, NumberRange, Optional

CATEGORIAS = [
    "Frutas",
    "Alimentos",
    "Productos naturales",
]


class FormularioProducto(FlaskForm):
    """Formulario para registrar o editar un producto."""

    nombre = StringField(
        "Nombre",
        validators=[DataRequired(message="El nombre es obligatorio."),
                    Length(max=100, message="Máximo 100 caracteres.")],
    )
    categoria = SelectField(
        "Categoría",
        choices=[(c, c) for c in CATEGORIAS],
        validators=[DataRequired(message="Seleccione una categoría.")],
    )
    descripcion = TextAreaField(
        "Descripción",
        validators=[Optional(), Length(max=300, message="Máximo 300 caracteres.")],
    )
    precio = DecimalField(
        "Precio",
        places=2,
        validators=[DataRequired(message="El precio es obligatorio."),
                    NumberRange(min=0, message="El precio debe ser positivo.")],
    )
    unidad = StringField(
        "Unidad",
        validators=[DataRequired(message="La unidad es obligatoria."),
                    Length(max=30, message="Máximo 30 caracteres.")],
    )
    stock = IntegerField(
        "Stock",
        validators=[DataRequired(message="El stock es obligatorio."),
                    NumberRange(min=0, message="El stock no puede ser negativo.")],
    )
    imagen = StringField(
        "Imagen",
        validators=[Optional(), Length(max=100, message="Máximo 100 caracteres.")],
    )
