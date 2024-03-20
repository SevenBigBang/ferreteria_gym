from django.db import models
from django import forms
from django.core.exceptions import ValidationError

class CategoriaProducto(models.Model):
    id_categoria = models.AutoField(primary_key=True, db_column='idCategoria')
    nombre_categoria = models.CharField(max_length=100, db_column='nombreCategoria')
    descripcion_categoria = models.TextField(db_column='descripcionCategoria')

    def clean(self):
        if not self.nombre_categoria:
            raise ValidationError("El nombre de la categoría no puede estar vacío.")
        if not self.descripcion_categoria:
            raise ValidationError("La descripción de la categoría no puede estar vacía.")

    def __str__(self):
        return self.nombre_categoria

    class Meta:
        managed = False
        db_table = 'categoriaproducto'

class Rol(models.Model):
    id_rol = models.AutoField(primary_key=True, db_column='idRol')
    nombre_rol = models.CharField(max_length=50, blank=True, null=True, db_column='rolNombre')
    descripcion_rol = models.TextField(blank=True, null=True, db_column='descripcionRol')

    def __str__(self):
        return self.nombre_rol
#nombre_rol
    class Meta:
        managed = False
        db_table = 'roles'

class Usuario(models.Model):
    id_usuario = models.AutoField(primary_key=True, db_column='idUsuario')
    primer_nombre = models.CharField(max_length=100, blank=True, null=True, db_column='primerNombre')
    primer_apellido = models.CharField(max_length=100, blank=True, null=True, db_column='primerApellido')
    telefono = models.CharField(max_length=10, blank=True, null=True)
    correo_electronico = models.CharField(max_length=100, blank=True, null=True, db_column='correoElectronico')
    contrasena_usuario = models.CharField(max_length=50, blank=True, null=True, db_column='contrasenaUsuario')
    id_rol = models.ForeignKey(Rol, on_delete=models.DO_NOTHING, blank=True, null=True, db_column='idRol')

    def __str__(self):
        return self.id_rol.nombre_rol

    class Meta:
        managed = False
        db_table = 'usuarios'

class MovimientoInventario(models.Model):
    id_movimiento = models.AutoField(primary_key=True, db_column='idMovimiento')
    tipo_movimiento = models.CharField(max_length=50, db_column='tipoMovimiento')
    fecha_movimiento = models.DateTimeField(db_column='fechaMovimiento')

    def clean(self):
        if not self.tipo_movimiento:
            raise ValidationError("El tipo de movimiento no puede estar vacío.")
        if not self.fecha_movimiento:
            raise ValidationError("La fecha de movimiento no puede estar vacía.")
        if not self.id_movimiento:
            raise ValidationError("El ID del movimiento no puede estar vacío.")

    def __str__(self):
        return f"Movimiento de inventario #{self.id_movimiento}"

    class Meta:
        managed = False
        db_table = 'movimientoinventario'

class Producto(models.Model):
    id_producto = models.AutoField(primary_key=True, db_column='idProducto')
    nombre_producto = models.CharField(max_length=100, db_column='nombreProducto')
    descripcion_producto = models.TextField(db_column='descripcionProducto')
    precio_producto = models.DecimalField(max_digits=10, decimal_places=2, db_column='precioProducto')
    cantidad_producto = models.IntegerField(db_column='cantidadProducto')
    imagen_producto = models.ImageField(upload_to='productos/', blank=True, null=True, db_column='imagenProducto') 
    estado_producto = models.CharField(max_length=250, blank=True, null=True, db_column='estadoProducto')
    id_categoria = models.ForeignKey(CategoriaProducto, on_delete=models.DO_NOTHING, db_column='idCategoria')

    def clean(self):
        if not self.nombre_producto:
            raise ValidationError("El nombre del producto no puede estar vacío.")
        if not self.descripcion_producto:
            raise ValidationError("La descripción del producto no puede estar vacía.")
        if self.precio_producto is None or self.precio_producto <= 0:
            raise ValidationError("El precio del producto debe ser mayor que cero.")
        if self.cantidad_producto is None or self.cantidad_producto < 0:
            raise ValidationError("La cantidad del producto no puede ser negativa.")
        if not self.id_categoria:
            raise ValidationError("Debe seleccionar una categoría para el producto.")

    def __str__(self):
        return self.nombre_producto

    def delete(self, using=None, keep_parents=False):
        self.estado_producto = 'No disponible'
        self.save()

    def save(self, *args, **kwargs):
        if self.cantidad_producto == 0:
            self.estado_producto = 'Agotado'
        else:
            self.estado_producto = 'Disponible'
        super().save(*args, **kwargs)

    class Meta:
        managed = False
        db_table = 'productos'


from django.db import models

class Proveedor(models.Model):
    id_proveedor = models.AutoField(primary_key=True, db_column='idProveedor')
    id_categoria = models.ForeignKey(CategoriaProducto, on_delete=models.DO_NOTHING, blank=True, null=True, db_column='idCategoria')
    nombre_proveedor = models.CharField(max_length=50, db_column='nombreProveedor')
    correo_electronico = models.CharField(max_length=50, db_column='correoElectronico')
    telefono = models.CharField(max_length=10)
    estado_proveedor = models.CharField(max_length=20, choices=[('Habilitado', 'Habilitado'), ('Deshabilitado', 'Deshabilitado')], default='Habilitado', db_column='estadoProveedor')

    def clean(self):
        if not self.nombre_proveedor:
            raise ValidationError("El nombre del proveedor no puede estar vacío.")
        if not self.correo_electronico:
            raise ValidationError("El correo electrónico del proveedor no puede estar vacío.")
        if not self.id_categoria:
            raise ValidationError("Debe seleccionar una categoría para el proveedor.")
        if self.telefono:
            if len(self.telefono) != 10:
                raise ValidationError("El número de teléfono debe tener 10 dígitos.")
            try:
                int(self.telefono)  # Verifica que el teléfono sea un número
            except ValueError:
                raise ValidationError("El número de teléfono debe ser un valor numérico.")
        # Verificar si ya existe un proveedor con el mismo nombre
        if Proveedor.objects.filter(nombre_proveedor=self.nombre_proveedor).exists():
            raise ValidationError("Ya existe un proveedor con este nombre.")

    def __str__(self):
        return self.nombre_proveedor
    
    class Meta:
        managed = False
        db_table = 'proveedor'

class OrdenCompra(models.Model):
    id_orden_compra = models.AutoField(primary_key=True,db_column='idOrdenCompra')
    id_proveedor = models.ForeignKey(Proveedor, on_delete=models.DO_NOTHING, blank=True, null=True, db_column='idProveedor')
    id_usuario = models.ForeignKey(Usuario, on_delete=models.DO_NOTHING, blank=True, null=True, db_column='idUsuario')
    fecha_orden_compra = models.DateField(blank=True, null=True, db_column='fechaOrdenCompra')
    valor_total_orden_compra = models.DecimalField(max_digits=10, decimal_places=2, default=0.0, db_column='valorTotalOrdenCompra')

    def __str__(self):
        return f"Orden de compra #{self.id_orden_compra}"

    class Meta:
        managed = False
        db_table = 'ordencompra'

class DetalleOrdenCompra(models.Model):
    id_detalle_orden_compra = models.AutoField(primary_key=True, db_column='idDetalleOrdenCompra')
    id_orden_compra = models.ForeignKey(OrdenCompra, on_delete=models.DO_NOTHING, blank=True, null=True, db_column='idOrdenCompra')
    id_producto = models.ForeignKey(Producto, on_delete=models.DO_NOTHING, blank=True, null=True, db_column='idProducto')
    cantidad_comprada = models.IntegerField(blank=True, null=True, db_column='cantidadComprada')
    valor_unitario = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, db_column='valorUnitario')
    valor_total = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, db_column='valorTotal')

    def __str__(self):
        return f"Detalle de orden de compra #{self.id_detalle_orden_compra}"

    class Meta:
        managed = False
        db_table = 'detalleordencompra'

class Venta(models.Model):
    TIPO_VENTA_CHOICES = [
        ('Vendedor', 'Vendedor'),
        ('Cliente', 'Cliente'),
    ]
    id_venta = models.AutoField(primary_key=True, db_column='idVenta')
    id_usuario = models.ForeignKey(Usuario, on_delete=models.DO_NOTHING, db_column='idUsuario', blank=True, null=True)
    tipo_venta = models.CharField(max_length=50, db_column='tipoVenta', choices=TIPO_VENTA_CHOICES, blank=True, null=True)
    fecha_venta = models.DateField(db_column='fechaVenta', blank=True, null=True)
    valor_total_venta = models.DecimalField(max_digits=10, decimal_places=2, db_column='valorTotalVenta', blank=True, null=True)

    def clean(self):
        if not self.tipo_venta:
            raise ValidationError("El tipo de venta no puede estar vacío.")
        if not self.fecha_venta:
            raise ValidationError("La fecha de venta no puede estar vacía.")
        if self.valor_total_venta is None or self.valor_total_venta <= 0:
            raise ValidationError("El valor total de la venta debe ser mayor que cero.")

    def __str__(self):
        return f"Venta #{self.id_venta}"

    class Meta:
        managed = False
        db_table = 'ventas'

class DetalleVenta(models.Model):
    id_detalle_venta = models.AutoField(primary_key=True, db_column='idDetalleVenta')
    id_venta = models.ForeignKey(Venta, on_delete=models.DO_NOTHING, blank=True, null=True, db_column='idVenta')
    id_producto = models.ForeignKey(Producto, on_delete=models.DO_NOTHING, blank=True, null=True, db_column='idProducto')
    cantidad_vendida = models.IntegerField(blank=True, null=True, db_column='cantidadVendida')
    valor_unitario = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, db_column='valorUnitario')
    valor_total = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, db_column='valorTotal')

    def __str__(self):
        return f"Detalle Venta #{self.id_detalle_venta}"

    class Meta:
        managed = False
        db_table = 'detalleventa'

class DetalleMovimientoInventario(models.Model):
    id_detalle_movimiento = models.AutoField(primary_key=True, db_column='idDetalleMovimiento')
    id_movimiento = models.ForeignKey(MovimientoInventario, on_delete=models.DO_NOTHING, blank=True, null=True, db_column='idMovimiento')
    id_producto = models.ForeignKey(Producto, on_delete=models.DO_NOTHING, blank=True, null=True, db_column='idProducto')
    cantidad = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return f"Detalle de movimiento #{self.id_detalle_movimiento}"

    class Meta:
        managed = False
        db_table = 'detallemovimientoinventario'