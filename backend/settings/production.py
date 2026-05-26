from . import *

# Database Settings (e.g., PostgreSQL)
DATABASES = {
    'default': env.db('DATABASE_URL')
}
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': env('DB_NAME', default=''),
#         'USER': env('DB_USER', default=''),
#         'PASSWORD': env('DB_PASSWORD', default=''),
#         'HOST': env('DB_HOST', default=''),
#         'PORT': env('DB_PORT', default=''),
#     }
# }


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

# Security recommendations for production
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_SSL_REDIRECT = env.bool('SECURE_SSL_REDIRECT', default=True)

# ENCRYPT ALL OUTGOING PAYLOAD BY DEFAULT
# REST_FRAMEWORK['DEFAULT_RENDERER_CLASSES'] = (
#     'backend.middleware.EncryptedJSONRenderer',
# )