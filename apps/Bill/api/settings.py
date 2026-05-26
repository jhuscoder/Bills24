from django.conf import settings

ALLOWED_HOST    = getattr(settings, 'ALLOWED_HOST', [])
EBILL_USERNAME  = getattr(settings, 'EBILL_USERNAME', None)
EBILL_PASSWORD  = getattr(settings, 'EBILL_PASSWORD', None)
EBILL_URL       = getattr(settings, 'EBILL_URL', None)
EBILL_TIMEOUT   = getattr(settings, 'EBILL_TIMEOUT', 30)
EBILL_AUTH_URL  = getattr(settings, 'EBILL_AUTH_URL', None)
EBILL_TOKEN     = getattr(settings, 'EBILL_TOKEN')
EBILL_TOKEN_REFRESH_SECONDS = getattr(settings, 'EBILL_TOKEN_REFRESH_SECONDS', 60 * 60 * 24 * 3)
