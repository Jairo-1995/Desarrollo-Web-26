"""Formulario de inicio de sesión."""

from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField
from wtforms.validators import DataRequired, Email, Length


class FormularioLogin(FlaskForm):
    """Formulario para iniciar sesión con correo electrónico."""

    email = StringField(
        "Correo electrónico",
        validators=[
            DataRequired(message="El correo es obligatorio."),
            Email(message="Ingresa un correo electrónico válido."),
            Length(max=150, message="Máximo 150 caracteres."),
        ],
        render_kw={"placeholder": "Ej: maria@ejemplo.com"},
    )
    password = PasswordField(
        "Contraseña",
        validators=[DataRequired(message="La contraseña es obligatoria.")],
        render_kw={"placeholder": "********"},
    )
    enviar = SubmitField("Iniciar sesión")
