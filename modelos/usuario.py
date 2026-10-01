"""Modelo de usuario con Flask-Login para el módulo de sesión."""

from flask_login import UserMixin


class Usuario(UserMixin):
    """Usuario de la tabla ``usuarios`` para inicio de sesión.

    Flask-Login solo necesita id, el resto se usa para mostrar el nombre
    en el dashboard y el navbar.
    """

    def __init__(self, id, nombre, email, rol="usuario"):
        self.id = id
        self.nombre = nombre
        self.email = email
        self.rol = rol

    @property
    def es_admin(self):
        """True si la cuenta es administrador (puede editar y eliminar)."""
        return self.rol == "admin"

    @classmethod
    def desde_fila(cls, fila):
        """Crea un Usuario a partir de una fila de la base de datos."""
        return cls(
            fila["id"],
            fila["nombre"],
            fila["email"],
            fila["rol"] if "rol" in fila.keys() else "usuario",
        )
