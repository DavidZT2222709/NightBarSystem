# apps/usuarios/signals.py
from django_rest_passwordreset.signals import reset_password_token_created
from django.core.mail import send_mail
from django.conf import settings

@reset_password_token_created.connect
def send_password_reset_email(sender, instance, reset_password_token, *args, **kwargs):
    # Actualizado al nombre de tu proyecto actual
    subject = "Recuperación de contraseña - IroMarket"
    
    message = f"""
    Hola {reset_password_token.user.nombre},

    Has solicitado restablecer tu contraseña para acceder a IroMarket.
    
    Tu token de recuperación es: {reset_password_token.key}

    Si no solicitaste esto, ignora este mensaje por seguridad.
    """
    
    # Es mejor usar la variable de settings para el remitente
    remitente = getattr(settings, 'DEFAULT_FROM_EMAIL', 'tu_correo_iromarket@gmail.com')
    
    send_mail(
        subject=subject, 
        message=message, 
        from_email=remitente, 
        recipient_list=[reset_password_token.user.email]
    )