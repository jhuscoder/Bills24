from . import *
import dj_database_url

# Database Settings (e.g., PostgreSQL)
# DATABASES['default'] = dj_database_url.config(
#     'DATABASE_URL',
#     conn_max_age=600,
#     conn_health_checks=True,
# )

# DATABASES['default']['ENGINE'] = 'django.db.backends.postgresql'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': env('DB_NAME'),
        'USER': env('DB_USER'),
        'PASSWORD': env('DB_PASSWORD'),
        'HOST': env('DB_HOST'),
        'PORT': env('DB_PORT'),
    }
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