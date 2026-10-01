"""Conexión a la base de datos PostgreSQL del proyecto.

Los parámetros de conexión se configuran con DATABASE_URL (formato
postgres://usuario:password@host:puerto/basededatos, como el Internal
Database URL de Render) o con PG_HOST, PG_USER, PG_PASSWORD, PG_NAME y
PG_PORT.
"""

import os


# ---------------------------------------------------------------------------
# PostgreSQL
# ---------------------------------------------------------------------------

def _url_postgres():
    """Devuelve la URL de conexión a PostgreSQL (DATABASE_URL o PG_*)."""
    url = os.environ.get("DATABASE_URL") or os.environ.get("POSTGRES_URL")
    if url:
        # Render entrega "postgres://..." y psycopg2 exige "postgresql://..."
        if url.startswith("postgres://"):
            url = url.replace("postgres://", "postgresql://", 1)
        elif url.startswith("postgresql+psycopg2://"):
            url = url.replace("postgresql+psycopg2://", "postgresql://", 1)
        return url
    # Fallback: variables PG_* individuales
    host = os.environ.get("PG_HOST", "localhost")
    puerto = os.environ.get("PG_PORT", "5432")
    usuario = os.environ.get("PG_USER", "postgres")
    password = os.environ.get("PG_PASSWORD", "1995")
    nombre = os.environ.get("PG_NAME", "bdamazonicas")
    return f"postgresql://{usuario}:{password}@{host}:{puerto}/{nombre}"


def obtener_conexion_postgres():
    """Conexión a PostgreSQL usando DATABASE_URL o las variables PG_*.

    Devuelve una conexión psycopg2 (usa marcadores %s; el adaptador
    ConexionPostgres de database.py traduce los '?' de las consultas).
    """
    import psycopg2

    return psycopg2.connect(_url_postgres())