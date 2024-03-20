from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import DetalleOrdenCompra, OrdenCompra, Producto, DetalleVenta
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver


@receiver(post_save, sender=DetalleOrdenCompra)
def actualizar_valor_total_orden_compra(sender, instance, created, **kwargs):
    if created:
        # Obtener el precio del producto
        precio_producto = instance.id_producto.precio_producto

        # Calcular el valor total del detalle de la orden de compra
        valor_total_detalle = instance.cantidad_comprada * precio_producto
        # Actualizar el campo valor_total en el detalle de la orden de compra
        instance.valor_total = valor_total_detalle
        instance.save()

        # Sumar los valores totales de todos los detalles relacionados a la orden de compra
        valor_total_orden_compra = DetalleOrdenCompra.objects.filter(id_orden_compra=instance.id_orden_compra).aggregate(total=models.Sum('valor_total'))['total']

        # Actualizar el campo valor_total_orden_compra en el modelo OrdenCompra
        orden_compra = instance.id_orden_compra
        orden_compra.valor_total_orden_compra = valor_total_orden_compra
        orden_compra.save()

        # Actualizar la cantidad de producto disponible
        producto = instance.id_producto
        producto.cantidad_producto += instance.cantidad_comprada
        producto.save()




@receiver(pre_save, sender=DetalleOrdenCompra)
def calcular_valor_total(sender, instance, **kwargs):
    if instance.id_producto and instance.cantidad_comprada and instance.valor_unitario:
        instance.valor_total = instance.cantidad_comprada * instance.valor_unitario

@receiver(post_save, sender=DetalleOrdenCompra)
def actualizar_orden_compra(sender, instance, created, **kwargs):
    if created or instance.id_orden_compra:
        orden_compra = instance.id_orden_compra
        if orden_compra:
            detalles_orden_compra = DetalleOrdenCompra.objects.filter(id_orden_compra=orden_compra)
            valor_total_orden_compra = detalles_orden_compra.aggregate(total=models.Sum('valor_total'))['total']
            orden_compra.valor_total_orden_compra = valor_total_orden_compra
            orden_compra.save()




from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver

@receiver(pre_save, sender=DetalleVenta)
def calcular_valor_total(sender, instance, **kwargs):
    if instance.id_producto and instance.cantidad_vendida and instance.valor_unitario:
        instance.valor_total = instance.cantidad_vendida * instance.valor_unitario

@receiver(post_save, sender=DetalleVenta)
def actualizar_venta(sender, instance, created, **kwargs):
    if created or instance.id_venta:
        venta = instance.id_venta
        if venta:
            detalles_venta = DetalleVenta.objects.filter(id_venta=venta)
            valor_total_venta = detalles_venta.aggregate(total=models.Sum('valor_total'))['total']
            venta.valor_total_venta = valor_total_venta
            venta.save()

@receiver(pre_save, sender=DetalleVenta)
def calcular_valor_total(sender, instance, **kwargs):
    if instance.id_producto and instance.cantidad_vendida and instance.valor_unitario:
        instance.valor_total = instance.cantidad_vendida * instance.valor_unitario

@receiver(post_save, sender=DetalleVenta)
def actualizar_venta(sender, instance, created, **kwargs):
    if created or instance.id_venta:
        venta = instance.id_venta
        if venta:
            detalles_venta = DetalleVenta.objects.filter(id_venta=venta)
            valor_total_venta = detalles_venta.aggregate(total=models.Sum('valor_total'))['total']
            venta.valor_total_venta = valor_total_venta
            venta.save()
