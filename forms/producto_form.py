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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Proveedores cargados desde la base de datos para el select.
        import database
        filas = database.get_db().execute(
            "SELECT id, nombre FROM proveedores ORDER BY nombre"
        ).fetchall()
        self.proveedor.choices = [("", "Sin proveedor (opcional)")] + [
            (str(f["id"]), f["nombre"]) for f in filas
        ]

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
    proveedor = SelectField(
        "Proveedor",
        choices=[],
        validators=[Optional()],
    )
