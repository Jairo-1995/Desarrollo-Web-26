"""Formulario del módulo de facturación."""

from flask_wtf import FlaskForm
from wtforms import DateField, DecimalField, IntegerField, SelectField, StringField, SubmitField
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
    producto = SelectField(
        "Producto",
        choices=[],  # se llena con los productos de la base de datos
        validators=[Optional()],
    )
    cantidad = IntegerField(
        "Cantidad",
        default=1,
        validators=[Optional(),
                    NumberRange(min=1, message="La cantidad debe ser al menos 1.")],
    )
    total = DecimalField(
        "Total",
        places=2,
        validators=[DataRequired(message="El total es obligatorio."),
                    NumberRange(min=0, message="El total debe ser positivo.")],
    )


class FormularioEstadoFactura(FlaskForm):
    """Formulario para cambiar solo el estado de pago de una factura."""

    estado = SelectField(
        "Estado de pago",
        choices=[(e, e) for e in ESTADOS],
        validators=[DataRequired(message="Seleccione un estado.")],
    )
    enviar = SubmitField("Actualizar estado")
