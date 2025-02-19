import os

from tutorial.settings import BASE_DIR
from decouple import config

SECRET_KEY = "your-secret-key"
DEBUG = True
ALLOWED_HOSTS = ["165.232.73.98", "localhost", "127.0.0.1"]
CSRF_TRUSTED_ORIGINS = [
    "https://165.232.73.98",
]

INSTALLED_APPS = [
    "django.contrib.sessions",
    "django.contrib.contenttypes",
    "django.contrib.auth",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "MedsRecognition",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "MedsRecognition.urls"
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "templates")],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": config("DATABASE_NAME", default="postgres"),
        "USER": config("DATABASE_USER", default="test"),
        "PASSWORD": config("DATABASE_PASSWORD", default="test"),
        "HOST": config("DATABASE_HOST", default="localhost"),
        "PORT": config("DATABASE_PORT", default="5432"),
        "OPTIONS": {"options": "-c search_path=auth,public"},
    }
}

REST_FRAMEWORK = {
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 10,  # Customize the number of results per page
}


WSGI_APPLICATION = "MedsRecognition.wsgi.application"

STATIC_URL = "/templates/"
LOGIN_URL = "/login/"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

TEST_RUNNER = "django.test.runner.DiscoverRunner"
