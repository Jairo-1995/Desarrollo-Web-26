-- ============================================================
-- Proyecto Integrador: Productos Amazónicos
-- Esquema de la base de datos MySQL (bdamazonicas)
-- Ejecutar con:  mysql -u root -p < sql/esquema.sql
-- (la aplicación también lo ejecuta automáticamente al iniciar)
-- ============================================================

CREATE DATABASE IF NOT EXISTS bdamazonicas
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;

USE bdamazonicas;

-- Usuarios autorizados para ingresar al sistema (Semana 13).
-- La contraseña se guarda hasheada (generate_password_hash de Werkzeug),
-- nunca en texto plano.
CREATE TABLE IF NOT EXISTS usuarios (
    id       BIGINT AUTO_INCREMENT PRIMARY KEY,
    nombre   VARCHAR(100) NOT NULL,
    email    VARCHAR(150) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL
);

-- Clientes registrados
CREATE TABLE IF NOT EXISTS clientes (
    id       INT AUTO_INCREMENT PRIMARY KEY,
    nombre   VARCHAR(100) NOT NULL,
    correo   VARCHAR(120) NOT NULL UNIQUE,           -- correo único por cliente
    telefono VARCHAR(30)  NOT NULL
);

-- Proveedores de productos
CREATE TABLE IF NOT EXISTS proveedores (
    id                 INT AUTO_INCREMENT PRIMARY KEY,
    nombre             VARCHAR(100) NOT NULL,
    producto_principal VARCHAR(100) NOT NULL,
    ciudad             VARCHAR(60)  NOT NULL
);

-- Catálogo de productos amazónicos
CREATE TABLE IF NOT EXISTS productos (
    id           INT AUTO_INCREMENT PRIMARY KEY,     -- clave primaria
    nombre       VARCHAR(100) NOT NULL,              -- StringField obligatorio
    categoria    VARCHAR(50)  NOT NULL,              -- SelectField con CATEGORIAS
    descripcion  TEXT,                               -- TextAreaField opcional
    precio       DECIMAL(10, 2) NOT NULL,            -- DecimalField >= 0
    unidad       VARCHAR(30)  NOT NULL,              -- StringField obligatorio
    stock        INT NOT NULL DEFAULT 0,             -- IntegerField >= 0
    imagen       VARCHAR(100),                       -- StringField opcional
    proveedor_id INT NULL,                           -- proveedor que lo suministra
    CONSTRAINT fk_productos_proveedor
        FOREIGN KEY (proveedor_id) REFERENCES proveedores (id)
        ON UPDATE CASCADE ON DELETE SET NULL
);

-- Facturas emitidas
CREATE TABLE IF NOT EXISTS facturas (
    numero     VARCHAR(20) PRIMARY KEY,
    cliente    VARCHAR(100) NOT NULL,
    cliente_id INT NULL,                             -- relación con clientes
    fecha      DATE NOT NULL,
    total      DECIMAL(10, 2) NOT NULL,
    estado     VARCHAR(20) NOT NULL,
    CONSTRAINT fk_facturas_cliente
        FOREIGN KEY (cliente_id) REFERENCES clientes (id)
        ON UPDATE CASCADE ON DELETE SET NULL
);
