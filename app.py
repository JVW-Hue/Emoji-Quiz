import os
import django
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'emoji_quiz.settings')
django.setup()

app = get_wsgi_application()