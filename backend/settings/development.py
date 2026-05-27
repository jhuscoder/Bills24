from . import *

HEALTH_CHECK = {
    'DISK_USAGE_MAX': 90,  # percent
    'MEMORY_MIN': 100,    # in MB
}

# REST_FRAMEWORK['DEFAULT_RENDERER_CLASSES'] = (
#     'backend.middleware.EncryptedJSONRenderer',
# )