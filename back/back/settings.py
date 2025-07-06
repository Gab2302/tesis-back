from pathlib import Path
from datetime import timedelta
import os
from dotenv import load_dotenv
load_dotenv()


# ------------------- BASE -------------------
BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-j)s%x7hi+l!ehh5$1tzbi!_$4_14^qdg5oss(p9ap7l=x=h&-s'

DEBUG = True  # ⚠️ Cambiar a False en producción
ALLOWED_HOSTS = ["*"]

# ------------------- APPS -------------------
INSTALLED_APPS = [ 
    # Django
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Terceros
    'rest_framework',
    'rest_framework_simplejwt',
    'corsheaders',

    # Tu app
    'core',
]

# ------------------- MIDDLEWARE -------------------
MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',  # Siempre primero
     'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# ------------------- URLs & WSGI -------------------
ROOT_URLCONF = 'back.urls'
WSGI_APPLICATION = 'back.wsgi.application'

# ------------------- TEMPLATES -------------------
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
            ],
        },
    },
]

# ------------------- DATABASE -------------------


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.environ.get('DB_NAME', 'NutriLabel'),
        'USER': os.environ.get('DB_USER', 'root'),
        'PASSWORD': os.environ.get('DB_PASSWORD', ''),
        'HOST': os.environ.get('DB_HOST', ''),
        'PORT': os.environ.get('DB_PORT', '3306'),
    }
}


# ------------------- VALIDACIÓN DE CONTRASEÑAS -------------------
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# ------------------- INTERNACIONALIZACIÓN -------------------
LANGUAGE_CODE = 'es'
TIME_ZONE = 'America/Lima'
USE_I18N = True
USE_TZ = True

# ------------------- ARCHIVOS ESTÁTICOS -------------------
STATIC_URL = 'static/'

STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")
STATICFILES_DIRS = [os.path.join(BASE_DIR, "static")]

# ------------------- CLAVE PRIMARIA POR DEFECTO -------------------
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# ------------------- MODELO DE USUARIO PERSONALIZADO -------------------
AUTH_USER_MODEL = 'core.User'

# ------------------- CONFIGURACIÓN DE DJANGO REST FRAMEWORK -------------------
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    )
}

# ------------------- CONFIGURACIÓN DE JWT -------------------
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=30),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'ROTATE_REFRESH_TOKENS': False,
    'BLACKLIST_AFTER_ROTATION': True,
    'ALGORITHM': 'HS256',
    'AUTH_HEADER_TYPES': ('Bearer',),
}

# ------------------- CORS -------------------
CORS_ALLOW_ALL_ORIGINS = True  # ⚠️ En producción, mejor usar CORS_ALLOWED_ORIGINS
