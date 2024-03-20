import smtplib
from .models import Proveedor
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from django.core.mail import send_mail

def enviar_correo_pedido(proveedor_id, pedido_texto):
    proveedor = Proveedor.objects.get(id_proveedor=proveedor_id)
    asunto = 'Pedido de productos'

    mensaje = f"""
    Estimado {proveedor.nombre_proveedor},

    Le escribimos desde la Ferreteria G&M,, el motivo de nuestro correo es para solicitar amablemente un pedido de los siguientes productos:
    {pedido_texto}:

    Cordialmente Ferreteria G&M
    """

    try:
        send_mail(asunto, mensaje, 'ferreteriagmsipm@gmail.com', [proveedor.correo_electronico], fail_silently=False)
        return True
    except:
        return False
