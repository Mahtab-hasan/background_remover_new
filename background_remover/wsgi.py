"""
WSGI config for background_remover project.

It exposes the WSGI callable as a module-level variable named ``application``.
"""

import os
import sys

# -----------------------
# Add project folder to sys.path
# -----------------------
project_home = '/home/mahtabhasan/background_remover'
if project_home not in sys.path:
    sys.path.insert(0, project_home)

# -----------------------
# Set Django settings module
# -----------------------
os.environ['DJANGO_SETTINGS_MODULE'] = 'background_remover.settings'

# -----------------------
# Activate virtualenv
# -----------------------
activate_this = '/home/mahtabhasan/background_remover/venv/bin/activate_this.py'
with open(activate_this) as file_:
    exec(file_.read(), dict(__file__=activate_this))

# -----------------------
# Get WSGI application
# -----------------------
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
