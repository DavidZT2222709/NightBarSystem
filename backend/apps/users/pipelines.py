# apps/usuarios/pipelines.py
from django.contrib.auth import get_user_model
from django.db.models import Q
from django.conf import settings

from social_django.models import UserSocialAuth
from social_core.pipeline.social_auth import associate_user as original
from social_core.exceptions import AuthForbidden  
from rest_framework_simplejwt.tokens import RefreshToken

from .models import Rol

# Importante: Obtener el modelo de usuario activo
Usuario = get_user_model()


def associate_by_email(strategy, details, backend, uid=None, user=None, *args, **kwargs):
    print("🚀 Entró al pipeline associate_by_email")
    email = (details.get('email') or '').strip().lower()

    if user:
        user = None # Ignorar usuario logueado para buscar coincidencia real

    if not email:
        return None

    try:
        usuario_existente = Usuario.objects.filter(Q(email__iexact=email)).first()
        
        if usuario_existente:
            if not usuario_existente.is_active:
                print(f"🚫 Usuario {email} está desactivado, no puede ingresar con Google.")
                raise AuthForbidden(backend)

            print(f"✅ Usuario existente encontrado: {usuario_existente.email}")
            return {'user': usuario_existente}
        else:
            # ⚠️ CAMBIO CLAVE: En lugar de bloquear (raise AuthForbidden), 
            # devolvemos None para que el pipeline continúe y CREA el usuario nuevo.
            print(f"⚪ No existe usuario con el correo {email}. Se continuará para crearlo.")
            return None 
            
    except Exception as e:
        print(f"💥 Error en associate_by_email: {e}")
        raise AuthForbidden(backend)


def asignar_rol_por_defecto(strategy, details, backend, user=None, *args, **kwargs):
    """
    Asigna rol 'Mesero' solo si el usuario es nuevo (creado por Google).
    Si ya existía, mantiene su rol actual.
    """
    if backend.name != 'google-oauth2' or user is None:
        return

    is_new = kwargs.get('is_new', False)

    try:
        if is_new:
            # Usar la constante exacta del modelo (Rol.MESERO = 'Mesero')
            rol_mesero, _ = Rol.objects.get_or_create(nombre=Rol.MESERO)
            user.rol = rol_mesero
            user.is_staff = False
            user.is_superuser = False
            user.save()
            print(f"✅ Nuevo usuario Google → {user.email} asignado a rol 'Mesero'")
        else:
            print(f"🔹 Usuario existente detectado: {user.email}, mantiene su rol ({user.rol})")
    except Exception as e:
        print(f"⚠️ Error asignando rol por defecto: {e}")


def save_profile(backend, user, response, *args, **kwargs):
    if backend.name != 'google-oauth2' or user is None:
        return
    user.nombre = response.get('name') or response.get('given_name') or user.nombre or 'Usuario'
    if not user.username:
        user.username = (response.get('email') or '').split('@')[0]
    user.save()


def create_jwt_token_with_role(strategy, backend, user, *args, **kwargs):
    if user is None:
        return
        
    refresh = RefreshToken.for_user(user)
    # Inyectar datos clave para el frontend
    refresh['rol'] = user.rol.nombre if getattr(user, 'rol', None) else 'sin_rol'
    refresh['nombre'] = user.nombre or user.first_name or ""
    refresh['email'] = user.email or ""
    
    access_token = str(refresh.access_token)
    refresh_token = str(refresh)
    
    # 🔧 Mejor práctica: Tomar URL del frontend de las variables de entorno (settings)
    frontend_url = getattr(settings, 'FRONTEND_URL', 'http://localhost:5173/')
    
    return strategy.redirect(f"{frontend_url}?token={access_token}&refresh={refresh_token}")


# --- SAFE WRAPPERS ---
def associate_user_safe(backend, uid, user=None, *args, **kwargs):
    try:
        return original(backend, uid, user=user, *args, **kwargs)
    except Exception:
        return {}


def social_user_safe(backend, uid, user=None, *args, **kwargs):
    try:
        social = UserSocialAuth.objects.get(provider=backend.name, uid=uid)
        return {'user': social.user}
    except UserSocialAuth.DoesNotExist:
        return {'user': None}