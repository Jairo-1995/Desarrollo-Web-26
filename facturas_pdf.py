"""Generación de facturas en PDF con formato de factura real.

Usa fpdf2 para dibujar una factura al estilo de las facturas fiscales
ecuatorianas: encabezado de la empresa con datos legales, numeración,
datos del cliente, tabla de productos, IVA (15 %) y totales.
"""

from datetime import date

from fpdf import FPDF

# Datos de la empresa emisora (puedes cambiarlos por los tuyos).
EMPRESA = {
    "nombre": "Productos Amazónicos S.A.S.",
    "razon": "PRODUCTOS AMAZONICOS S.A.S.",
    "ruc": "1792845639001",
    "direccion": "Av. Amazonas N45-12 y Av. Baez, Quito - Ecuador",
    "telefono": "+593 99 876 5432",
    "correo": "ventas@productosamazonicos.com",
    "matriz": "Matriz: Amazonas N12-80 y Av. Pinto, Quito",
}

TASA_IVA = 0.15  # IVA 15 % vigente en Ecuador


def _dinero(valor):
    """Formatea un número como monto monetario: 1.005,50 (usando miles y coma)."""
    texto = f"{valor:,.2f}"          # 1,005.50
    return texto.replace(",", "X").replace(".", ",").replace("X", ".")


class FacturaPDF(FPDF):
    """PDF con cabecera y pie repetidos en cada página."""

    def __init__(self, factura):
        self.factura = factura
        super().__init__(orientation="P", unit="mm", format="A4")
        self.alias_nb_pages()

    # ------------------------------------------------------------------
    def cabecera_empresa(self, x, y, ancho):
        """Dibuja el bloque de datos de la empresa emisora."""
        self.set_xy(x, y)
        self.set_font("Arial", "B", 11)
        self.set_text_color(30, 30, 30)
        self.cell(ancho, 5, EMPRESA["nombre"], 0, 1)
        self.set_font("Arial", "", 7.5)
        self.set_text_color(80, 80, 80)
        for linea in (
            f"RUC: {EMPRESA['ruc']}",
            f"Dirección Matriz: {EMPRESA['direccion']}",
            f"Teléf: {EMPRESA['telefono']}   Correo: {EMPRESA['correo']}",
        ):
            self.set_x(x)
            self.cell(ancho, 3.4, linea, 0, 1)

    # ------------------------------------------------------------------
    def bloque_numeracion(self, x, y, ancho):
        """Cuadro gris con la palabra FACTURA, número, fecha y demás datos."""
        alto = 27
        self.set_fill_color(241, 241, 241)
        self.set_draw_color(150, 150, 150)
        self.set_line_width(0.3)
        self.rect(x, y, ancho, alto, "DF")

        self.set_xy(x, y + 1)
        self.set_font("Arial", "B", 9)
        self.set_text_color(0, 0, 0)
        self.cell(20, 5, "FACTURA", 0, 0, "L")
        self.set_font("Arial", "", 8)
        self.cell(6, 5, "No.", 0, 0, "L")
        self.cell(ancho - 26, 5, "001-001-" + self.factura["numero_formateado"], 0, 1, "L")

        filas = [
            ("FECHA EMISIÓN:", self.factura["fecha"]),
            ("FORMA DE PAGO:", "SIN UTILIZACIÓN DEL SISTEMA FINANCIERO"),
            ("ESTADO:", str(self.factura["estado"]).upper()),
        ]
        for etiqueta, valor in filas:
            self.set_x(x + 2)
            self.set_font("Arial", "", 6.8)
            self.cell(24, 4.6, etiqueta, 0, 0, "L")
            self.set_font("Arial", "B", 7.4)
            self.cell(ancho - 26, 4.6, valor, 0, 1, "L")

    # ------------------------------------------------------------------
    def bloque_cliente(self, x, y, ancho):
        """Cuadro con los datos del cliente (razón social, RUC/CI, teléfono...)."""
        self.set_line_width(0.3)
        self.set_draw_color(150, 150, 150)

        filas = [
            ("RAZÓN SOCIAL / NOMBRES:", str(self.factura["cliente"])),
            ("DIRECCIÓN:", self.factura.get("direccion") or "S/N"),
            ("TELÉFONO:", str(self.factura.get("telefono") or "S/N")),
            ("CORREO:", str(self.factura.get("correo") or "S/N")),
        ]
        alto = 4.8 * len(filas) + 4
        self.rect(x, y, ancho, alto, "D")
        self.set_xy(x + 2, y + 2)
        self.set_font("Arial", "B", 7.5)
        self.set_text_color(0, 0, 0)
        for etiqueta, valor in filas:
            self.set_x(x + 2)
            self.cell(38, 4.8, etiqueta, 0, 0, "L")
            self.set_font("Arial", "", 7.5)
            self.cell(ancho - 40, 4.8, valor, 0, 1, "L")
            self.set_font("Arial", "B", 7.5)
        return y + alto

    # ------------------------------------------------------------------
    def tabla_productos(self, y):
        """Tabla de productos con cantidades, precios e IVA."""
        margen = 10
        ancho = 190
        # Columnas: código, descripción, cant, valor unit, descuento, precio total
        anchos = [22, 66, 14, 24, 24, 20, 20]
        encabezados = ["Cód. Principal", "Descripción", "Cant.", "Valor Unit.", "Descuento", "IVA", "Precio Total"]

        self.set_xy(margen, y)
        self.set_font("Arial", "B", 6.8)
        self.set_fill_color(214, 229, 214)
        self.set_draw_color(120, 120, 120)
        self.set_text_color(0, 0, 0)
        for titulo, w in zip(encabezados, anchos):
            self.cell(w, 6, titulo, 1, 0, "C", True)
        self.ln()

        self.set_font("Arial", "", 7)
        detalle = self.factura["lineas"]
        for linea in detalle:
            alto = 6.2
            if self.get_y() + alto > 270:  # salto de página
                self.add_page()
            self.set_x(margen)
            self.cell(anchos[0], alto, linea["codigo"], 1, 0, "C")
            # Solo el nombre del producto, sin el prefijo "3 x"
            texto = linea["descripcion"]
            self.set_font("Arial", "B", 7)
            self.cell(anchos[1], alto, texto, 1, 0, "L")
            self.set_font("Arial", "", 7)
            self.cell(anchos[2], alto, f"{linea['cantidad']:g}", 1, 0, "R")
            self.cell(anchos[3], alto, _dinero(linea["unitario"]), 1, 0, "R")
            self.cell(anchos[4], alto, "0.00", 1, 0, "R")
            self.cell(anchos[5], alto, _dinero(linea["iva"]), 1, 0, "R")
            self.cell(anchos[6], alto, _dinero(linea["importe"]), 1, 0, "R")
            self.ln()

        # Fila final con el total a la derecha
        self.set_x(margen + anchos[0] + anchos[1] + anchos[2] + anchos[3] + anchos[4] + anchos[5])
        self.set_font("Arial", "B", 7.6)
        self.cell(anchos[6], 6.6, _dinero(self.factura["subtotal_sin_iva"] + self.factura["iva"]), 1, 1, "R")
        return self.get_y()

    # ------------------------------------------------------------------
    def bloque_totales(self, x, y):
        """Cuadro derecho con subtotal, IVA y total a pagar."""
        ancho = 62
        self.set_line_width(0.3)
        self.set_draw_color(150, 150, 150)
        filas = [
            ("SUBTOTAL", self.factura["subtotal_sin_iva"]),
            ("SUBTOTAL IVA 15%", self.factura["subtotal_sin_iva"]),
            ("IVA 15%", self.factura["iva"]),
            ("TOTAL", self.factura["subtotal_sin_iva"] + self.factura["iva"]),
        ]
        self.rect(x, y, ancho, 4.8 * len(filas), "D")
        yy = y
        for etiqueta, valor in filas:
            self.set_xy(x, yy)
            self.set_font("Arial", "B" if etiqueta == "TOTAL" else "", 7.4)
            self.cell(30, 4.8, etiqueta, 0, 0, "L")
            self.cell(ancho - 30, 4.8, _dinero(valor), 0, 1, "R")
            yy += 4.8

    # ------------------------------------------------------------------
    def bloque_informacion_adicional(self, x, y, ancho, alto):
        """Cuadro izquierdo de información adicional + número de guías."""
        self.set_line_width(0.3)
        self.set_draw_color(150, 150, 150)
        self.rect(x, y, ancho, alto, "D")
        self.set_xy(x + 2, y + 2)
        self.set_font("Arial", "B", 7.2)
        self.cell(30, 5, "INFORMACIÓN ADICIONAL", 0, 1, "L")
        self.set_font("Arial", "", 7)
        self.set_x(x + 2)
        self.cell(30, 5, "Cliente:", 0, 0, "L")
        self.cell(ancho - 34, 5, str(self.factura["cliente"]), 0, 1, "L")

    # ------------------------------------------------------------------
    def header(self):
        if self.page_no() == 1:
            return
        self.set_y(10)
        self.set_font("Arial", "B", 9)
        self.cell(60, 5, EMPRESA["nombre"], 0, 0, "L")
        self.cell(130, 5, "FACTURA " + self.factura["numero"], 0, 1, "R")
        self.ln(2)

    def footer(self):
        self.set_y(-13)
        self.set_font("Arial", "I", 6.5)
        self.set_text_color(120, 120, 120)
        self.cell(0, 4, "Factura generada por el sistema Productos Amazónicos.", 0, 1, "C")
        self.cell(0, 4, f"Página {self.page_no()} de {{nb}}", 0, 1, "C")


def generar_factura_pdf(factura):
    """Genera el PDF de una factura y devuelve los bytes.

    ``factura`` es un diccionario con las llaves:
      numero, numero_formateado, fecha, estado, cliente,
      direccion/telefono/correo (opcionales), lineas (lista de dicts con
      codigo, descripcion, cantidad, unitario, iva, importe),
      subtotal_sin_iva, iva.
    """
    doc = FacturaPDF(factura)
    doc.set_auto_page_break(auto=True, margin=18)
    doc.add_page()

    # Encabezado: empresa a la izquierda, numeración a la derecha
    doc.cabecera_empresa(12, 14, 90)
    doc.bloque_numeracion(112, 12, 76)

    y = doc.get_y() + 6
    y = doc.bloque_cliente(12, y, 186) + 5
    y = doc.tabla_productos(y) + 8

    # Información adicional (izquierda) y totales (derecha)
    doc.bloque_informacion_adicional(12, y, 118, 30)
    doc.bloque_totales(138, y)

    y_firmas = max(doc.get_y(), y + 34) + 14
    doc.set_y(y_firmas)
    doc.set_draw_color(60, 60, 60)
    doc.set_line_width(0.3)
    # Línea y leyenda de la firma
    doc.line(28, y_firmas + 8, 92, y_firmas + 8)
    doc.line(118, y_firmas + 8, 182, y_firmas + 8)
    doc.set_font("Arial", "", 7.2)
    doc.set_text_color(60, 60, 60)
    doc.set_xy(28, y_firmas + 9)
    doc.cell(64, 4.5, "Firma autorizada", 0, 0, "C")
    doc.set_xy(118, y_firmas + 9)
    doc.cell(64, 4.5, "Firma del cliente", 0, 1, "C")

    return bytes(doc.output())


def factura_completa(datos_bd, lineas):
    """Arma el diccionario completo de la factura a partir de la fila de la BD.

    ``lineas``: lista de tuplas/dicts (descripcion, cantidad, unitario) que
    componen la factura. Los productos repetidos se agrupan en una sola
    línea sumando sus cantidades. Calcula subtotal, IVA y totales.
    """
    subtotal = 0.0
    detalle = []
    # Agrupamos por producto (código + descripción): si el mismo producto
    # aparece varias veces en la compra, se une en una sola fila con la
    # cantidad total comprada.
    agrupados = {}
    orden = []
    for item in lineas:
        codigo = str(item.get("codigo", "PRD"))
        descripcion = str(item.get("descripcion", "Producto"))
        cantidad = float(item.get("cantidad", 1)) or 1.0
        unitario = float(item.get("unitario", 0))
        clave = (codigo, descripcion, unitario)
        if clave in agrupados:
            agrupados[clave]["cantidad"] += cantidad
        else:
            registro = {
                "codigo": codigo,
                "descripcion": descripcion,
                "cantidad": cantidad,
                "unitario": unitario,
            }
            agrupados[clave] = registro
            orden.append(registro)

    for linea in orden:
        cantidad = linea["cantidad"]
        unitario = linea["unitario"]
        importe = round(cantidad * unitario, 2)
        subtotal += importe
        linea["iva"] = round(importe * TASA_IVA, 2)
        linea["importe"] = importe
        detalle.append(linea)
    subtotal = round(subtotal, 2)
    iva = round(subtotal * TASA_IVA, 2)

    # Número formateado estilo SRI: 001-001-000XXXXXX
    numero = str(datos_bd.get("numero", "")).replace("FAC-", "").lstrip("0")
    try:
        secuencia = int(numero) if numero else 1
    except ValueError:
        secuencia = 1

    return {
        "numero": str(datos_bd.get("numero", "FAC-001")),
        "numero_formateado": f"{secuencia:09d}",
        "fecha": str(datos_bd.get("fecha", date.today().isoformat())),
        "estado": str(datos_bd.get("estado", "Pendiente")),
        "cliente": str(datos_bd.get("cliente", "Consumidor Final")),
        "direccion": datos_bd.get("direccion", "S/N"),
        "telefono": datos_bd.get("telefono", "S/N"),
        "correo": datos_bd.get("correo", "S/N"),
        "lineas": detalle,
        "subtotal_sin_iva": subtotal,
        "iva": iva,
    }
