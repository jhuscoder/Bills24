from .configuration import *

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env('DEBUG')

ALLOWED_HOSTS = ["*"]

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    "health_check",  # required
    'corsheaders',
    'rest_framework',
    'rest_framework.authtoken',
    'drf_spectacular',
    'djoser',
    'api',
    'apps.accounts',
    'apps.Bill',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'backend.middleware.ResponseHeadersMiddleware',
]

ROOT_URLCONF = env("ROOT_URLCONF")

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'public/templates'],
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

WSGI_APPLICATION = env("WSGI_APPLICATION")

# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Africa/Lagos'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'public/static']
STATIC_ROOT = BASE_DIR / 'public/assets'

# Enable WhiteNoise static file serving
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# CORS SETTINGS
CORS_ALLOW_METHODS = (
    "GET",
    "POST",
    "PUT",
    "OPTION",
    "DELETE"
)

CORS_ALLOW_HEADERS = (
    "accept",
    "Authorization",
    "content-Type",
    "user-agent",
    "X-csrftoken",
    "X-requested-with",
    "X-Auth-Token",
    "X-User-Location",
    "X-Device-Id",
    "X-User-Theme"
    'X-App-Version'
)

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_PARSER_CLASSES': [
        'rest_framework.parsers.JSONParser',
    ],
    'DEFAULT_RENDERER_CLASSES':[
        'rest_framework.renderers.JSONRenderer',
    ],
    'EXCEPTION_HANDLER': 'api.response.custom_exception_handler',
    'TEST_REQUEST_DEFAULT_FORMAT': 'json',
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
}

SPECTACULAR_SETTINGS = {
    'TITLE': 'Bills API V1',
    'DESCRIPTION': 'API for Bills Payment.',
    'VERSION': '3.0.3',
    # Configuration for serving a schema subset with SpectacularAPIView
    'SERVE_URLCONF': None,
    # complete public schema or a subset based on the requesting user
    'SERVE_PUBLIC': True,
    # include schema endpoint into schema
    'SERVE_INCLUDE_SCHEMA': True,
    # list of authentication/permission classes for spectacular's views.
    'SERVE_PERMISSIONS': ['rest_framework.permissions.AllowAny'],
    # None will default to DRF's AUTHENTICATION_CLASSES
    'SERVE_AUTHENTICATION': None,

    # Runs exemplary schema generation and emits warnings as part of "./manage.py check --deploy"
    'ENABLE_DJANGO_DEPLOY_CHECK': True,
    'CONTACT': {},
}

# SIMPLE_JWT SETTINGS
SIMPLE_JWT = {
    "JTI_CLAIM"                 : "jti",  
    "UPDATE_LAST_LOGIN"         : True,
    "BLACKLIST_AFTER_ROTATION"  : False,
    "ROTATE_REFRESH_TOKENS"     : False,
    "ALGORITHM"                 : "HS256",
    'USER_ID_FIELD'             : 'user_id',
    "SIGNING_KEY"               : AUTHENTICATION_KEY,
    "AUTH_HEADER_TYPES"         : ("Bearer",),
    "AUTH_HEADER_NAME"          : "HTTP_AUTHORIZATION",

    "REFRESH_TOKEN_LIFETIME"    : timedelta(days=10),
    "ACCESS_TOKEN_LIFETIME"     : timedelta(days=1, minutes=5),

    "TOKEN_TYPE_CLAIM"          : "token_type",
    "TOKEN_USER_CLASS"          : "rest_framework_simplejwt.models.TokenUser",
    "AUTH_TOKEN_CLASSES"        : ("rest_framework_simplejwt.tokens.AccessToken",),
    "USER_AUTHENTICATION_RULE"  : "rest_framework_simplejwt.authentication.default_user_authentication_rule",
}

# DJOSER SETTINGS
DJOSER = {    
    "SET_USERNAME_RETYPE"                   : True,
    "SET_PASSWORD_RETYPE"                   : True,
    "SEND_ACTIVATION_EMAIL"                 : True,
    "SEND_CONFIRMATION_EMAIL"               : True,
    "USER_CREATE_PASSWORD_RETYPE"           : True,
    "USERNAME_CHANGED_EMAIL_CONFIRMATION"   : True,
    "PASSWORD_CHANGED_EMAIL_CONFIRMATION"   : True,    
    "LOGIN_FIELD"                           : "email",
    "USER_ID_FIELD"                         : "user_id,",
    "ACTIVATION_URL"                        : "activate/{uid}/{token}",
    "PASSWORD_RESET_CONFIRM_URL"            : "password/reset/confirm/{uid}/{token}",
    "USERNAME_RESET_CONFIRM_URL"            : "email/reset/confirm/{uid}/{token}",
    
    "SERIALIZERS": {
        'user_create'   : 'apps.accounts.api.serializers.UserRegistrationSerializer',
        'user'          : 'apps.accounts.api.serializers.UserProfileSerializer',
        'user_delete'   : 'djoser.serializers.UserDeleteSerializer',
    },
}

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
}