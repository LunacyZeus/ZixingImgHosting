"""
WSGI config for backend project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

import dotenv
dotenv.load_dotenv(dotenv_path = "app.env",override = True)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "application.settings")
os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"

application = get_wsgi_application()
