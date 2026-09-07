"""Formulario de confirmación para eliminar productos."""

from flask_wtf import FlaskForm
from wtforms import SubmitField


class FormularioEliminarProducto(FlaskForm):
    """Protege la acción de eliminación mediante un token CSRF."""

    enviar = SubmitField("Eliminar")
