from django.apps import AppConfig


class UsuariosConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.users'
    
    
    def ready(self):
        from .signals import send_password_reset_email  #  Importa el signal al iniciar el app, para enviar correo de recuperacion

    
