from django.core.mail import send_mail
from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from django.contrib import messages
from django import forms
from django_select2.forms import Select2Widget
from .reportes import generate_pdf_report_ventas
from .reportes import generate_pdf_report_ventas
from .reportes import (
    generate_pdf_report_productos, generate_excel_report_productos,
    generate_pdf_report_ventas, generate_excel_report_ventas,
    generate_pdf_report_detalle_ventas, generate_excel_report_detalle_ventas,
    generate_pdf_report_detalle_compra, generate_excel_report_detalle_compra
)
from .models import (
    Producto, CategoriaProducto, MovimientoInventario, DetalleMovimientoInventario,
    Venta, DetalleVenta, OrdenCompra, DetalleOrdenCompra, Usuario, Rol, Proveedor
)

class EstadoProductoFilter(admin.SimpleListFilter):
    title = _('Estado del producto')
    parameter_name = 'estado_producto'

    def lookups(self, request, model_admin):
        return (
            ('disponible', _('Disponible')),
            ('no_disponible', _('No disponible')),
            ('agotado', _('Agotado')),
            ('todos', _('Ver todos los productos')),
        )

    def queryset(self, request, queryset):
        if self.value() == 'disponible':
            return queryset.filter(estado_producto='Disponible')
        elif self.value() == 'no_disponible':
            return queryset.filter(estado_producto='No disponible')
        elif self.value() == 'agotado':
            return queryset.filter(cantidad_producto=0)
        else:
            return queryset


class ProductosAdminForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = '__all__'
        widgets = {
            'productos_relacionados': Select2Widget,
        }

class ProductosAdmin(admin.ModelAdmin):
    list_display = ('id_producto', 'nombre_producto', 'descripcion_producto', 'precio_producto', 'format_cantidad_producto', 'imagen_producto', 'estado_producto', 'nombre_categoria')
    list_display_links = ('id_producto', 'nombre_producto', 'descripcion_producto', 'precio_producto', 'format_cantidad_producto', 'imagen_producto', 'estado_producto', 'nombre_categoria')
    ordering = ('id_producto',)
    search_fields = ('nombre_producto', 'descripcion_producto', 'precio_producto', 'cantidad_producto', 'estado_producto')  
    list_filter = ('cantidad_producto', 'id_categoria__nombre_categoria', EstadoProductoFilter)  
    list_per_page = 10 
    actions = ['marcar_como_no_disponible', 'marcar_como_disponible', generate_pdf_report_productos, generate_excel_report_productos]
    exclude = ['estado_producto']  

    def nombre_categoria(self, obj):
        return obj.id_categoria.nombre_categoria if obj.id_categoria else "Sin categoría"
    nombre_categoria.short_description = 'Categoría' 

    def marcar_como_no_disponible(self, request, queryset):
        queryset.update(estado_producto='No disponible')
        self.message_user(request, _("Se cambió el estado a No disponible"), level='warning')
    marcar_como_no_disponible.short_description = "Marcar como no disponible"

    def marcar_como_disponible(self, request, queryset):
        queryset.update(estado_producto='Disponible')
        self.message_user(request, _("Se cambió el estado a Disponible"), level=messages.SUCCESS)
    marcar_como_disponible.short_description = "Marcar como disponible"

    def format_cantidad_producto(self, obj):
        return str(obj.cantidad_producto) if obj.cantidad_producto is not None else ''
    format_cantidad_producto.short_description = 'Cantidad'

    def changelist_view(self, request, extra_context=None):
        response = super().changelist_view(request, extra_context=extra_context)
        try:
            qs = response.context_data['cl'].queryset
        except (AttributeError, KeyError):
            return response

        for obj in qs:
            if obj.cantidad_producto is not None and obj.cantidad_producto < 5:
                messages.warning(request, f"Se necesita reabastecer el producto {obj.nombre_producto}")
        return response

admin.site.register(Producto, ProductosAdmin)

@admin.register(Rol)
class RolAdmin(admin.ModelAdmin):
    list_display = ('id_rol', 'nombre_rol', 'descripcion_rol')
    search_fields = ('id_rol', 'nombre_rol')
    list_display_links = ('id_rol', 'nombre_rol', 'descripcion_rol')
    ordering = ('id_rol',)
    list_per_page = 10 

@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    list_display = ('id_usuario', 'primer_nombre', 'primer_apellido', 'telefono', 'correo_electronico', 'contrasena_usuario', 'id_rol')
    search_fields = ('id_usuario', 'primer_nombre', 'primer_apellido', 'correo_electronico')
    list_display_links = ('id_usuario', 'primer_nombre', 'primer_apellido', 'telefono', 'correo_electronico', 'contrasena_usuario', 'id_rol')
    ordering = ('id_usuario',)
    list_per_page = 10 

@admin.register(CategoriaProducto)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('id_categoria', 'nombre_categoria', 'descripcion_categoria')
    list_display_links = ('id_categoria','nombre_categoria', 'descripcion_categoria')
    ordering = ('id_categoria',)
    list_per_page = 10 

@admin.register(MovimientoInventario)
class MovimientoinventarioAdmin(admin.ModelAdmin):
    list_display = ('id_movimiento', 'tipo_movimiento', 'fecha_movimiento')
    list_display_links = ('id_movimiento', 'tipo_movimiento', 'fecha_movimiento')
    ordering = ('id_movimiento',)
    list_per_page = 10

@admin.register(DetalleMovimientoInventario)
class DetallesmovimientoinventarioAdmin(admin.ModelAdmin):
    list_display = ('id_detalle_movimiento', 'id_movimiento', 'id_producto')
    list_display_links = ('id_detalle_movimiento', 'id_movimiento', 'id_producto')
    ordering = ('id_detalle_movimiento',)
    list_per_page = 10

@admin.register(Venta)
class VentasAdmin(admin.ModelAdmin):
    list_display = ('id_venta', 'nombre_usuario', 'tipo_venta', 'fecha_venta', 'valor_total_venta')
    search_fields = ('id_venta', 'tipo_venta', 'fecha_venta', 'valor_total_venta')
    list_display_links = ('id_venta', 'nombre_usuario', 'tipo_venta', 'fecha_venta', 'valor_total_venta')
    ordering = ('id_venta',)
    list_per_page = 10 
    actions = [generate_pdf_report_ventas, generate_excel_report_ventas]

    def nombre_usuario(self, obj):
        return obj.id_usuario.primer_nombre if obj.id_usuario else "Inexistente"
    nombre_usuario.short_description = 'Primer nombre' 

@admin.register(DetalleVenta)
class DetallesVentaAdmin(admin.ModelAdmin):
    list_display = ('id_detalle_venta', 'id_Venta', 'nombre_producto', 'cantidad_vendida', 'valor_unitario', 'valor_total')
    search_fields = ('id_detalle_venta', 'cantidad_vendida', 'valor_unitario', 'valor_total')
    list_display_links = ('id_detalle_venta', 'id_Venta', 'nombre_producto', 'cantidad_vendida', 'valor_unitario', 'valor_total')
    ordering = ('id_detalle_venta',)
    list_per_page = 10 
    actions = [generate_pdf_report_detalle_ventas, generate_excel_report_detalle_ventas]

    def id_Venta(self, obj):
        return obj.id_venta.id_venta if obj.id_venta else "Inexistente"
    id_Venta.short_description = 'id venta' 

    def nombre_producto(self, obj):
        return obj.id_producto.nombre_producto if obj.id_producto else "Inexistente"
    nombre_producto.short_description = 'Producto' 

@admin.register(Proveedor)
class ProveedorAdmin(admin.ModelAdmin):
    form = ProductosAdminForm
    list_display = ('id_proveedor', 'nombre_categoria', 'nombre_proveedor', 'correo_electronico', 'telefono', 'estado_proveedor')
    search_fields = ('id_proveedor', 'correo_electronico', 'telefono', 'estado_proveedor')
    list_display_links = ('id_proveedor', 'nombre_categoria', 'nombre_proveedor', 'correo_electronico', 'telefono')
    ordering = ('id_proveedor',)
    list_per_page = 10 
    actions = ['habilitar_proveedor', 'deshabilitar_proveedor', 'generar_pedido_productos', generate_pdf_report_detalle_compra, generate_excel_report_detalle_compra]
    list_filter = ('estado_proveedor',)

    def nombre_categoria(self, obj):
        return obj.id_categoria.nombre_categoria if obj.id_categoria else "Inexistente"
    nombre_categoria.short_description = 'Categoría' 

    def habilitar_proveedor(self, request, queryset):
        queryset.update(estado_proveedor='Habilitado')
        self.message_user(request, _("Proveedor(es) habilitado(s) correctamente."), level='success')
    habilitar_proveedor.short_description = "Habilitar proveedor"

    def deshabilitar_proveedor(self, request, queryset):
        queryset.update(estado_proveedor='Deshabilitado')
        self.message_user(request, _("Proveedor(es) deshabilitado(s) correctamente."), level='warning')
    deshabilitar_proveedor.short_description = "Deshabilitar proveedor"

    def generar_pedido_productos(self, request, queryset):
        if queryset.count() != 1:
            self.message_user(request, "Por favor selecciona un único proveedor para generar el pedido de productos.", level='error')
            return

        proveedor = queryset.first()
        cantidad_productos = request.POST.get('cantidad_productos', 0) 
        categoria = proveedor.id_categoria
        productos_relacionados = Producto.objects.filter(id_categoria=categoria)
        mensaje_correo = f"""
        <html>
        <body>
        <p>Estimado {proveedor.nombre_proveedor},</p>
        <p>El motivo de comunicarnos con usted es para solicitar amablemente un pedido de los siguientes productos:</p>
        <ul>
        """

        for producto in productos_relacionados:
            mensaje_correo += f"<li>{producto.nombre_producto} - {cantidad_productos}</li>"

        mensaje_correo += """
        </ul>
        <p>Cordialmente,<br>
        Ferreteria G&M</p>
        </body>
        </html>
        """

        subject = 'Pedido de productos'
        from_email = 'ferreteriagmsipm@gmail.com' 
        to_email = [proveedor.correo_electronico]  

        send_mail(subject, '', from_email, to_email, html_message=mensaje_correo, fail_silently=False)
        self.message_user(request, "Pedido de productos generado correctamente y enviado al proveedor.", level='success')

    generar_pedido_productos.short_description = "Generar pedido de productos"
