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
# Default from email used by automated features
DEFAULT_FROM_EMAIL = 'The Bills24 <eigwesi@the3prime.com>'
SERVER_EMAIL = 'eigwesi@the3prime.com'