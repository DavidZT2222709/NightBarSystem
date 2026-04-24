from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager, PermissionsMixin

class Rol(models.Model):
    # Constantes para evitar errores de escritura en el resto del código
    MESERO = 'Mesero'
    BARTENDER = 'Bartender'
    ADMINISTRADOR = 'Administrador'
    
    NOMBRES_ROLES = [
        (MESERO, 'Mesero'),
        (BARTENDER, 'Bartender'),
        (ADMINISTRADOR, 'Administrador'),
    ]

    # Aplicamos las opciones (choices) y un valor por defecto
    nombre = models.CharField(
        max_length=100, 
        unique=True, 
        choices=NOMBRES_ROLES, 
        default=MESERO
    )

    def __str__(self):
        return self.nombre
    

class UserManager(BaseUserManager):
    def create_user(self, email, nombre=None, password=None, **extra_fields):

        if not email:
            raise ValueError('El usuario debe contar con correo electronico')
        
        email = self.normalize_email(email)
        user = self.model(email=email, nombre=nombre, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user
    
    def create_superuser(self,email, nombre=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, nombre, password, **extra_fields)
    
class Usuario(AbstractUser, PermissionsMixin):

    email = models.EmailField(unique=True)
    username = models.CharField(max_length=150, unique=True)
    nombre = models.CharField(max_length=150, null=True, blank=True)
    numero_telefono = models.CharField(max_length=20, null=True, blank=True)

    rol = models.ForeignKey(Rol, on_delete=models.SET_NULL, null=True, blank=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nombre']

    def __str__(self):
        return self.email