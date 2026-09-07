"""Formulario del módulo de clientes."""

from flask_wtf import FlaskForm
from wtforms import EmailField, StringField, TelField
from wtforms.validators import DataRequired, Email, Length, Optional, Regexp


try:
    import email_validator  # noqa: F401
except ImportError:
    # Permite ejecutar el proyecto si se usa un intérprete sin la dependencia.
    def Email(message=None):
        return Regexp(
            r"^[^\s@]+@[^\s@]+\.[^\s@]+$",
            message=message or "Ingrese un correo valido.",
        )


class FormularioCliente(FlaskForm):
    """Formulario para registrar o editar un cliente."""

    nombre = StringField(
        "Nombre",
        validators=[DataRequired(message="El nombre es obligatorio."),
                    Length(max=100, message="Máximo 100 caracteres.")],
    )
    correo = EmailField(
        "Correo electrónico",
        validators=[DataRequired(message="El correo es obligatorio."),
                    Email(message="Ingrese un correo válido."),
                    Length(max=120, message="Máximo 120 caracteres.")],
    )
    telefono = TelField(
        "Teléfono",
        validators=[Optional(),
                    Regexp(r"^[\d\s\-\+]{7,15}$",
                           message="Ingrese un teléfono válido (7 a 15 dígitos).")],
    )
