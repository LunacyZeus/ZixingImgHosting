"""
ASGI config for zeroEngine project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application

import dotenv
dotenv.load_dotenv(dotenv_path = "app.env",override = True)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "application.settings")
os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"

application = get_asgi_application()
