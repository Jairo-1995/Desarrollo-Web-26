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
        validators=[
            DataRequired(message="El correo electrónico es obligatorio: no puede quedar vacío."),
            Email(message="Correo electrónico incorrecto. Debe tener un formato válido, "
                          "por ejemplo: nombre@dominio.com"),
            Length(max=120, message="Máximo 120 caracteres."),
        ],
        render_kw={"placeholder": "Ej: cliente@correo.com", "type": "email"},
    )
    telefono = TelField(
        "Teléfono",
        validators=[Optional(),
                    Regexp(r"^\d{10}$",
                           message="Ingresa solo 10 dígitos numéricos.")],
        # maxlength evita escribir más de 10 y inputmode muestra teclado
        # numérico en dispositivos móviles.
        render_kw={"maxlength": "10", "inputmode": "numeric",
                   "placeholder": "Ej: 0991234567"},
    )
