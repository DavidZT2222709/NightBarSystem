"""
Django settings for backend project.
"""

import os
from pathlib import Path
from datetime import timedelta
from decouple import config as env
import dj_database_url

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# --- SEGURIDAD ---
SECRET_KEY = env('SECRET_KEY')
DEBUG = env('DEBUG', default=False, cast=bool)

# SECURITY WARNING: don't run with debug turned on in production!

ALLOWED_HOSTS = ['*']
CORS_ALLOW_ALL_ORIGINS = True

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Apps de Terceros
    'rest_framework',
    'rest_framework_simplejwt',
    'rest_framework_simplejwt.token_blacklist', # Necesario para la regla de BLACKLIST_AFTER_ROTATION
    'corsheaders',
    'social_django',
    'drf_yasg',
    'django_rest_passwordreset',

    # Tus Apps Locales
    'apps.users',
    'apps.products',
    'apps.orders',
    'apps.tables',
    'apps.stats',
]

# --- MIDDLEWARE ---
MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'social_django.middleware.SocialAuthExceptionMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'social_django.context_processors.backends',
                'social_django.context_processors.login_redirect',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'

# --- BASE DE DATOS (PostgreSQL) ---
_DATABASE_URL = env('DATABASE_URL', default=None)
if _DATABASE_URL:
    DATABASES = {'default': dj_database_url.parse(_DATABASE_URL, conn_max_age=600)}
else:
    DATABASES = {
        'default': {
            'ENGINE':   'django.db.backends.postgresql',
            'NAME':     env('DB_NAME'),
            'USER':     env('DB_USER'),
            'PASSWORD': env('DB_PASSWORD'),
            'HOST':     env('DB_HOST', default='localhost'),
            'PORT':     env('DB_PORT', default='5432'),
        }
    }

# --- VALIDACIÓN DE CONTRASEÑAS ---
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# --- MODELO DE USUARIO PERSONALIZADO ---
# CORRECCIÓN: Estaba en plural y con nombre incorrecto.

# --- DJANGO REST FRAMEWORK ---
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
}

# --- JWT (JSON Web Tokens) ---
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME':  timedelta(hours=8),   # Dura un turno de trabajo
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'ROTATE_REFRESH_TOKENS':  True,                 # Cada refresh genera un token nuevo
    'BLACKLIST_AFTER_ROTATION': True,               # El token viejo queda invalidado
    'AUTH_HEADER_TYPES': ('Bearer',),
}

# --- SOCIAL AUTH (Google) ---
AUTHENTICATION_BACKENDS = (
    'social_core.backends.google.GoogleOAuth2',
    'django.contrib.auth.backends.ModelBackend',
)

AUTH_USER_MODEL = 'users.Usuario'

SOCIAL_AUTH_PIPELINE = (
    'social_core.pipeline.social_auth.social_details',
    'social_core.pipeline.social_auth.social_uid',
    'social_core.pipeline.social_auth.auth_allowed',
    'apps.usuarios.pipelines.associate_by_email', 
    'social_core.pipeline.social_auth.social_user',
    'social_core.pipeline.user.create_user',
    'social_core.pipeline.social_auth.associate_user',
    'social_core.pipeline.social_auth.load_extra_data',
   'apps.users.pipelines.associate_by_email',
'apps.users.pipelines.save_profile',
'apps.users.pipelines.asignar_rol_por_defecto',
'apps.users.pipelines.create_jwt_token_with_role', 
)

# --- CORS ---
CORS_ALLOWED_ORIGINS = [
    'http://localhost:5173', # React frontend
    # Nota: Si pruebas React Native en un celular físico, añade la IP de tu PC aquí (ej. 'http://192.168.1.5:8081')
]

# --- LOCALIZACIÓN ---
LANGUAGE_CODE = 'es-co'  # Español de Colombia
TIME_ZONE = 'America/Bogota'
USE_I18N = True
USE_TZ = True

# --- ARCHIVOS ESTÁTICOS Y MULTIMEDIA ---
STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# CORRECCIÓN: Necesario para guardar las fotos de los productos
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# --- CONFIGURACIÓN DE CORREO (Para reset de contraseña) ---
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = env('EMAIL_USER', default='powerstock2025@gmail.com')
EMAIL_HOST_PASSWORD = env('EMAIL_PASSWORD', default='')
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

# --- URL DEL FRONTEND ---
FRONTEND_URL = env('FRONTEND_URL', default='http://localhost:5173/')