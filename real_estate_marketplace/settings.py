
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-dv0j=(eu%udn-nrxr6g&0pl1+e*7f)dzr%$(=#s+4-vsdgh#a@'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["*"]


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',

    # custom apps
    'accounts',
    'listings',
    'corsheaders',
    # Authentication
    'rest_framework',
    'rest_framework.authtoken',
    'rest_framework_simplejwt',
    'dj_rest_auth',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.facebook',
    'allauth.socialaccount.providers.google',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    # "allauth.account.middleware.AccountMiddleware",
]

ROOT_URLCONF = 'real_estate_marketplace.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'real_estate_marketplace.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


AUTHENTICATION_BACKENDS = (
    'allauth.account.auth_backends.AuthenticationBackend',
    'django.contrib.auth.backends.ModelBackend',
)

ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_EMAIL_VERIFICATION = 'optional'
LOGIN_REDIRECT_URL = '/'


# AUTHENTICATION_BACKENDS = (
#     'allauth.account.auth_backends.AuthenticationBackend',
#     'django.contrib.auth.backends.ModelBackend',
# )

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
}


import datetime

JWT_AUTH = {
    # how long the original token is valid for
    'JWT_EXPIRATION_DELTA': datetime.timedelta(days=2),

    # allow refreshing of tokens
    'JWT_ALLOW_REFRESH': True,

    # this is the maximum time AFTER the token was issued that
    # it can be refreshed.  exprired tokens can't be refreshed.
    'JWT_REFRESH_EXPIRATION_DELTA': datetime.timedelta(days=7),
}

SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'SCOPE': [
            'profile',
            'email',
        ],
        'AUTH_PARAMS': {
            'access_type': 'online',
        },
        'OAUTH_PKCE_ENABLED': True,
    }
}

SITE_ID = 1
LOGIN_REDIRECT_URL = '/'
ACCOUNT_LOGOUT_REDIRECT_URL = 'account_login'
ACCOUNT_EMAIL_REQUIRED = True
SOCIALACCOUNT_QUERY_EMAIL = True
ACCOUNT_SESSION_REMEMBER = True


# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/
import os

STATIC_URL = 'static/'

STATICFILES_DIRS = [
os.path.join(BASE_DIR, 'static')
]
MEDIA_ROOT= os.path.join(BASE_DIR, "media")
MEDIA_URL="/media/"
# STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")


# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# from corsheaders.defaults import default_headers

# CORS_ALLOW_HEADERS = list(default_headers) + [
#     'X-Amz-Date',
#     'Access-Control-Request-Headers',
#     'Access-Control-Allow-Headers',
#     'Access-Control-Allow-Origin',
#     'XMLHttpRequest',
# ]
# CORS_EXPOSE_HEADERS = ['Content-Type', 'X-CSRFToken']
# CORS_ALLOW_ALL_ORIGINS = True
# CORS_ALLOW_CREDENTIALS = True

# CSRF_USE_SESSIONS = False
# CSRF_COOKIE_HTTPONLY = True
# CSRF_COOKIE_SAMESITE = None

# SESSION_COOKIE_HTTPONLY = True 
# SESSION_COOKIE_SAMESITE = None

# SECURE_BROWSER_XSS_FILTER = True
# SECURE_CONTENT_TYPE_NOSNIFF = True

# SESSION_COOKIE_SECURE = True # changed
# CSRF_COOKIE_SECURE = True

# CSRF_TRUSTED_ORIGINS = [
#     'http://localhost:3000',
#     'http://127.0.0.1:3000',
#     'http://127.0.0.1:8000',
#     'https://main.d1eqcgh0d7v0dg.amplifyapp.com',
# #    "https://main.d1eqcgh0d7v0dg.amplifyapp.com/"
# ]
# CORS_ORIGIN_WHITELIST = (
#     'http://localhost:3000',
#     'http://127.0.0.1:3000',
#     'http://127.0.0.1:8000',
#     'https://main.d1eqcgh0d7v0dg.amplifyapp.com'
# )


# CORS_EXPOSE_HEADERS = [
#     "set-cookie"
# ]
# CORS_ALLOW_METHODS = [
# 'DELETE',
# 'GET',
# 'OPTIONS',
# 'PATCH',
# 'POST',
# 'PUT',
# ]

# # CORS_ALLOW_HEADERS = [
# #     'accept',
# #     'accept-encoding',
# #     'authorization',
# #     'content-type',
# #     'dnt',
# #     'origin',
# #     'user-agent',
# #     'x-csrftoken',
# #     'x-requested-with',
# #     'set-cookie'
# # ]

# # Consolidated CORS configuration
# CORS_ALLOW_HEADERS = list(default_headers) + [
#     'X-Amz-Date',
#     'Access-Control-Request-Headers',
#     'Access-Control-Allow-Headers',
#     'Access-Control-Allow-Origin',
#     'XMLHttpRequest',
#     'set-cookie',  # Add set-cookie to CORS_ALLOW_HEADERS
# ]


from corsheaders.defaults import default_headers

# Consolidated CORS configuration
CORS_ALLOW_HEADERS = list(default_headers) + [
    'X-Amz-Date',
    'Access-Control-Request-Headers',
    'Access-Control-Allow-Headers',
    'Access-Control-Allow-Origin',
    'XMLHttpRequest',
    'set-cookie', 
]

CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOW_CREDENTIALS = True

CORS_ORIGIN_WHITELIST = (
    'http://localhost:3000',
    'http://127.0.0.1:3000',
    'http://127.0.0.1:8000',
    'https://main.d1eqcgh0d7v0dg.amplifyapp.com',
)

# Consolidated CSRF configuration
CSRF_COOKIE_HTTPONLY = True
CSRF_COOKIE_SECURE = True
CSRF_COOKIE_SAMESITE = None #'Lax'  # or 'Strict'

# Session cookie settings
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SECURE = True
SESSION_COOKIE_SAMESITE = None #'Lax'  # or 'Strict'

# Secure headers
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True

# Consolidated CORS_ALLOW_METHODS
CORS_ALLOW_METHODS = [
    'DELETE',
    'GET',
    'OPTIONS',
    'PATCH',
    'POST',
    'PUT',
]
