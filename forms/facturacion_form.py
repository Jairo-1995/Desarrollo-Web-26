"""Formulario del módulo de facturación."""

from flask_wtf import FlaskForm
from wtforms import DateField, DecimalField, SelectField, StringField
from wtforms.validators import DataRequired, Length, NumberRange, Optional

ESTADOS = ["Pagada", "Pendiente", "Anulada"]


class FormularioFactura(FlaskForm):
    """Formulario para registrar o editar una factura."""

    numero = StringField(
        "Número de factura",
        validators=[DataRequired(message="El número es obligatorio."),
                    Length(max=20, message="Máximo 20 caracteres.")],
    )
    cliente = StringField(
        "Cliente",
        validators=[DataRequired(message="El cliente es obligatorio."),
                    Length(max=100, message="Máximo 100 caracteres.")],
    )
    fecha = DateField(
        "Fecha",
        format="%Y-%m-%d",
        validators=[DataRequired(message="La fecha es obligatoria.")],
    )
    estado = SelectField(
        "Estado",
        choices=[(e, e) for e in ESTADOS],
        validators=[DataRequired(message="Seleccione un estado.")],
    )
    total = DecimalField(
        "Total",
        places=2,
        validators=[DataRequired(message="El total es obligatorio."),
                    NumberRange(min=0, message="El total debe ser positivo.")],
    )
