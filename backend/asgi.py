"""
ASGI config for backend project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/asgi/
"""

import os
import environ
from pathlib import Path

from django.core.asgi import get_asgi_application

# Ensure environment variables are loaded the same way as wsgi
BASE_DIR = Path(__file__).resolve().parent.parent
env = environ.Env(
	DEBUG=(bool, False)
)
environ.Env.read_env(BASE_DIR / '.env')

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings.' + env('PROJECT_ENVIRONMENT', default='development'))

application = get_asgi_application()
