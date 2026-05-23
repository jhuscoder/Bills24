from . import *

# Database Settings (e.g., PostgreSQL)
DB_NAME=env('DB_NAME')
DB_USER=env('DB_USER')
DB_PASSWORD=env('DB_PASSWORD', )
DB_HOST=env('DB_HOST')
DB_PORT=env('DB_PORT')

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

# ENCRYPT ALL OUTGOING PAYLOAD BY DEFAULT
# REST_FRAMEWORK['DEFAULT_RENDERER_CLASSES'] = (
#     'backend.middleware.EncryptedJSONRenderer',
# )