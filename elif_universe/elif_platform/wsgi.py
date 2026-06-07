"""
WSGI config for elif_platform project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/6.0/howto/deployment/wsgi/
"""

import os
import sys
from pathlib import Path

# Add the elif_universe directory to the python path
path_to_elif_universe = Path(__file__).resolve().parent.parent
if str(path_to_elif_universe) not in sys.path:
    sys.path.append(str(path_to_elif_universe))

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'elif_platform.settings')

application = get_wsgi_application()
app = application
