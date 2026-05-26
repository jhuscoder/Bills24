import os
import environ
from pathlib import Path
from datetime import timedelta

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Initialize environment object
env = environ.Env(
    # set casting and default value
    DEBUG=(bool, False)
)

# Take environment variables from .env file
environ.Env.read_env(BASE_DIR / '.env')

AUTHENTICATION_KEY = env("AUTHENTICATION_KEY")

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
    'TITLE': 'Bills API',
    'DESCRIPTION': 'API for Bills Payment.',
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': False,
    # OTHER SETTINGS
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


CORS_EXPOSE_HEADERS = [ 'X-Device-Id', 'X-App-Version']
CORS_ALLOWED_ORIGINS = [env("NEXT_ROUTE")]
CSRF_TRUSTED_ORIGINS = CORS_ALLOWED_ORIGINS
CORS_ALLOW_ALL_ORIGINS = True

EBILL_URL       = env('EBILL_URL')
EBILL_USERNAME  = env('EBILL_USERNAME')
EBILL_PASSWORD  = env('EBILL_PASSWORD')
EBILL_AUTH_URL  = env('EBILL_AUTH_URL')
EBILL_TOKEN     = env('EBILL_TOKEN')

WSGI_APPLICATION = env("WSGI_APPLICATION")
AUTH_USER_MODEL = env("AUTH_USER_MODEL")
# LOGIN_URL   = env("LOGIN_URL")


# GMAIL CONFIGURATIONS
EMAIL_BACKEND       = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST          = 'smtp.gmail.com'
EMAIL_PORT          = 587  # For TLS
EMAIL_USE_TLS       = True
EMAIL_USE_SSL       = False  # Set to False for TLS
EMAIL_HOST_USER     = env('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = env('EMAIL_HOST_PASSWORD')
