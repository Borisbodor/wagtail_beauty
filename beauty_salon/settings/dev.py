from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-95y(+ng_jcm(6+$&qziyg)h_00o9i$$o#8v9%-jm93^$(02!!y"

# SECURITY WARNING: define the correct hosts in production!
ALLOWED_HOSTS = ["*"]

# Trusted origins for ngrok and local development
CSRF_TRUSTED_ORIGINS = [
    "https://test.statcats.net",
    "https://beautyapp.ngrok.app",
    "https://*.ngrok.app",
    "https://*.ngrok.io",
    "http://localhost:8000",
    "http://127.0.0.1:8000",
]

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"


try:
    from .local import *
except ImportError:
    pass
