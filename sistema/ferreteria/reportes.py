from django.urls import reverse
from django.utils.html import format_html
from django.http import HttpResponse
from reportlab.pdfgen import canvas
import xlwt
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, landscape
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from .models import Producto, Venta, DetalleVenta, DetalleOrdenCompra


def generate_excel_report(headers, data, filename):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = f'attachment; filename="{filename}.xls"'

    workbook = xlwt.Workbook()
    sheet = workbook.add_sheet(filename)

    # Estilos para el encabezado y el contenido
    
    header_style = xlwt.easyxf('font: bold on; align: vertical center, horizontal center; pattern: pattern solid, fore_color gray25')
    content_style = xlwt.easyxf('align: vertical center, horizontal center')

    # Aplicar estilo al encabezado
    for col, header in enumerate(headers):
        sheet.write(0, col, header, header_style)

    # Escribir los datos en las celdas y aplicar estilo
    for row, row_data in enumerate(data, start=1):
        for col, cell_data in enumerate(row_data):
            sheet.write(row, col, cell_data, content_style)

    workbook.save(response)
    return response


# Función para generar PDF del reporte de productos
def generate_pdf_report_productos(modeladmin, request, queryset):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="reporte_productos.pdf"'

    doc = SimpleDocTemplate(response, pagesize=landscape(letter))
    elements = []

    # Encabezado
    elements.append(Paragraph("Reporte de Productos", getSampleStyleSheet()['Heading1']))
    


    # Detalles
    data = [["ID", "Nombre", "Descripción", "Precio", "Cantidad", "Categoría"]]
    for producto in queryset:
        data.append([producto.id_producto,
                     producto.nombre_producto,
                     producto.descripcion_producto,
                     producto.precio_producto,
                     producto.cantidad_producto,
                     str(producto.id_categoria.nombre_categoria if producto.id_categoria else "N/A")])

    # Crear tabla
    table = Table(data)
    style = TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                        ('GRID', (0, 0), (-1, -1), 1, colors.black)])
    table.setStyle(style)
    elements.append(table)

    # Construir PDF
    doc.build(elements)

    return response

generate_pdf_report_productos.short_description = "Generar PDF del reporte de productos"


# Función para generar Excel del reporte de productos
def generate_excel_report_productos(modeladmin, request, queryset):
    headers = ['ID', 'Nombre', 'Descripción', 'Precio', 'Cantidad', 'Categoría']
    data = [[producto.id_producto,
             producto.nombre_producto,
             producto.descripcion_producto,
             producto.precio_producto,
             producto.cantidad_producto,
             str(producto.id_categoria.nombre_categoria if producto.id_categoria else "N/A")]
            for producto in queryset]
    filename = 'reporte_productos'
    return generate_excel_report(headers, data, filename)

generate_excel_report_productos.short_description = "Generar Excel del reporte de productos"


# Función para generar PDF del reporte de ventas
def generate_pdf_report_ventas(modeladmin, request, queryset):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="reporte_ventas.pdf"'

    doc = SimpleDocTemplate(response, pagesize=landscape(letter))
    elements = []

    elements.append(Paragraph("Reporte de Ventas", getSampleStyleSheet()['Heading1']))

    data = [["ID Venta", "Nombre Usuario", "Tipo Venta", "Fecha Venta", "Valor Total Venta"]]
    for venta in queryset:
        data.append([venta.id_venta,
                     venta.id_usuario.primer_nombre if venta.id_usuario else "Inexistente",
                     venta.tipo_venta,
                     venta.fecha_venta,
                     venta.valor_total_venta])

    table = Table(data)
    style = TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                        ('GRID', (0, 0), (-1, -1), 1, colors.black)])
    table.setStyle(style)
    elements.append(table)

    doc.build(elements)

    return response

generate_pdf_report_ventas.short_description = "Generar PDF del reporte de ventas"


# Función para generar Excel del reporte de ventas
def generate_excel_report_ventas(modeladmin, request, queryset):
    headers = ['ID Venta', 'Nombre Usuario', 'Tipo Venta', 'Fecha Venta', 'Valor Total Venta']
    data = [[venta.id_venta,
             venta.id_usuario.primer_nombre if venta.id_usuario else "Inexistente",
             venta.tipo_venta,
             venta.fecha_venta,
             venta.valor_total_venta]
            for venta in queryset]
    filename = 'reporte_ventas'
    return generate_excel_report(headers, data, filename)

generate_excel_report_ventas.short_description = "Generar Excel del reporte de ventas"


# Función para generar PDF del reporte de detalles de ventas
def generate_pdf_report_detalle_ventas(modeladmin, request, queryset):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="reporte_detalle_ventas.pdf"'

    doc = SimpleDocTemplate(response, pagesize=landscape(letter))
    elements = []

    elements.append(Paragraph("Reporte de Detalles de Ventas", getSampleStyleSheet()['Heading1']))

    data = [["Id detalle venta", "Id venta", "Id producto", "Cantidad vendida", "Valor unitario", "Valor total"]]
    for detalle in queryset:
        data.append([detalle.id_detalle_venta,
                     detalle.id_venta,
                     detalle.id_producto,
                     detalle.cantidad_vendida,
                     detalle.valor_unitario,
                     detalle.valor_total])

    table = Table(data)
    style = TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                        ('GRID', (0, 0), (-1, -1), 1, colors.black)])
    table.setStyle(style)
    elements.append(table)

    doc.build(elements)

    return response

generate_pdf_report_detalle_ventas.short_description = "Generar PDF del reporte de detalles de ventas"


# Función para generar Excel del reporte de detalles de ventas
def generate_excel_report_detalle_ventas(modeladmin, request, queryset):
    headers = ['Id detalle venta', 'Id venta', 'Id producto', 'Cantidad vendida', 'Valor unitario', 'Valor total']
    data = [[detalle.id_detalle_venta,
             detalle.id_venta,
             detalle.id_producto,
             detalle.cantidad_vendida,
             detalle.valor_unitario,
             detalle.valor_total]
            for detalle in queryset]
    filename = 'reporte_detalle_ventas'
    return generate_excel_report(headers, data, filename)

generate_excel_report_detalle_ventas.short_description = "Generar Excel del reporte de detalles de ventas"


# Función para generar PDF del reporte de detalles de compras
def generate_pdf_report_detalle_compra(modeladmin, request, queryset):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="reporte_detalle_compras.pdf"'

    doc = SimpleDocTemplate(response, pagesize=landscape(letter))
    elements = []

    elements.append(Paragraph("Reporte de Detalles de Compras", getSampleStyleSheet()['Heading1']))

    data = [["Id detalle compra", "Id orden compra", "Id producto", "Cantidad comprada", "Valor unitario", "Valor total"]]
    for detalle in queryset:
        data.append([detalle.id_detalle_orden_compra,
                     detalle.id_orden_compra,
                     detalle.id_producto,
                     detalle.cantidad_comprada,
                     detalle.valor_unitario,
                     detalle.valor_total])

    table = Table(data)
    style = TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                        ('GRID', (0, 0), (-1, -1), 1, colors.black)])
    table.setStyle(style)
    elements.append(table)

    doc.build(elements)

    return response

generate_pdf_report_detalle_compra.short_description = "Generar PDF del reporte de detalles de compras"


# Función para generar Excel del reporte de detalles de compras
def generate_excel_report_detalle_compra(modeladmin, request, queryset):
    headers = ['Id detalle compra', 'Id orden compra', 'Id producto', 'Cantidad comprada', 'Valor unitario', 'Valor total']
    data = [[detalle.id_detalle_orden_compra,
             detalle.id_orden_compra,
             detalle.id_producto,
             detalle.cantidad_comprada,
             detalle.valor_unitario,
             detalle.valor_total]
            for detalle in queryset]
    filename = 'reporte_detalle_compras'
    return generate_excel_report(headers, data, filename)

generate_excel_report_detalle_compra.short_description = "Generar Excel del reporte de detalles de compras"
