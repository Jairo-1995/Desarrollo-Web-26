"""Formulario de registro de usuarios."""

from flask_wtf import FlaskForm
from wtforms import PasswordField, RadioField, StringField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, Length, Regexp


class FormularioUsuario(FlaskForm):
    """Formulario para registrar un nuevo usuario (tabla usuarios)."""

    nombre = StringField(
        "Nombre",
        validators=[
            DataRequired(message="El nombre es obligatorio."),
            Length(max=100, message="Máximo 100 caracteres."),
        ],
        render_kw={"placeholder": "Ej: María Pérez"},
    )
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
        validators=[
            DataRequired(message="La contraseña es obligatoria."),
            Length(min=6, message="La contraseña debe tener al menos 6 caracteres."),
            # Debe contener al menos una letra y un número.
            Regexp(
                r"^(?=.*[A-Za-z])(?=.*\d).+$",
                message="La contraseña debe incluir al menos una letra y un número.",
            ),
        ],
        render_kw={"placeholder": "Mínimo 6 caracteres, con letras y números"},
    )
    confirmar_password = PasswordField(
        "Confirmar contraseña",
        validators=[
            DataRequired(message="Debes confirmar la contraseña."),
            EqualTo("password", message="Las contraseñas no coinciden."),
        ],
        render_kw={"placeholder": "Repite la contraseña"},
    )
    # Tipo de cuenta: el administrador administra (editar/eliminar), el
    # usuario solo compra.
    rol = RadioField(
        "Tipo de cuenta",
        choices=[
            ("admin", "Crear como Administrador (administra el sistema)"),
            ("usuario", "Crear como Usuario (para comprar)"),
        ],
        default="usuario",
        validators=[DataRequired(message="Selecciona el tipo de cuenta.")],
    )
    enviar = SubmitField("Registrarme")
