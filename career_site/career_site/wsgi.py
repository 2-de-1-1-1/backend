"""
WSGI config for career_site project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

settings_module = 'career_site.production' if 'WEBSITE_HOSTNAME' in os.environ else 'quickstartproject.settings'
os.environ.setdefault('DJANGO_SETTINGS_MODULE', settings_module)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'career_site.settings')

application = get_wsgi_application()
