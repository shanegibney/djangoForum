"""
Django settings for crudProject project.
Generated by 'django-admin startproject' using Django 1.9.5.
For more information on this file, see
https://docs.djangoproject.com/en/1.9/topics/settings/
For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.9/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.9/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'm$_e*c2#82c_hz@$y&+e5s=bkrlb2&q4$j&u6gj6m0+#ko*u6z'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

# AUTH_USER_MODEL = 'accounts.User'

# AUTHENTICATION_BACKENDS = ('accounts.backends.EmailAuth')

# Instead of sending out real emails the console backend just writes the emails that
# would be sent to the standard output.
# EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

DEFAULT_FROM_EMAIL = 'shanegibney@gmail.com'
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'shanegibney@gmail.com'
EMAIL_HOST_PASSWORD = ''
EMAIL_USE_TLS = True

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'bootstrapform',
    'django.contrib.sites',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.facebook',
    'tinymce',
    'crudapp',
    'fileuploader',
]

SITE_ID = 1

MIDDLEWARE_CLASSES = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'crudProject.urls'

MEDIA_ROOT = os.path.join(BASE_DIR, 'fileuploader/uploaded_files')

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, "templates")],
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

AUTHENTICATION_BACKENDS = (
    # Needed to login by username in Django admin, regardless of `allauth`
    'django.contrib.auth.backends.ModelBackend',
    # `allauth` specific authentication methods, such as login by e-mail
    'allauth.account.auth_backends.AuthenticationBackend',
)

WSGI_APPLICATION = 'crudProject.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/1.9/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/1.9/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# django-allauth email settings
# ACCOUNT_USER_MODEL_USERNAME_FIELD = None
ACCOUNT_USERNAME_REQUIRED = True
# ACCOUNT_AUTHENTICATION_METHOD = 'email'

# The user is required to hand over an e-mail address when signing up
ACCOUNT_EMAIL_REQUIRED = True

# The URL to redirect to after a successful e-mail confirmation, in case of an authenticated user.
# Set to None to use settings.LOGIN_REDIRECT_URL.
ACCOUNT_EMAIL_CONFIRMATION_AUTHENTICATED_REDIRECT_URL = None

# In order to verify an email address a key is mailed identifying the email address to be verified.
# In previous versions, a record was stored in the database for each ongoing email confirmation,
# keeping track of these keys. Current versions use HMAC based keys that do not require server side state.
ACCOUNT_EMAIL_CONFIRMATION_HMAC = True

# After signing up, keep the user account inactive until the e-mail address is verified
ACCOUNT_EMAIL_VERIFICATION = 'mandatory'

# Login by e-mail address, not username
# ACCOUNT_EMAIL_AUTHENTICATION is deprecated see site-packages/allauth/account/app_settings.py line 103
ACCOUNT_AUTHENTICATION_METHOD = 'email'

# Enforce uniqueness of e-mail addresses
ACCOUNT_UNIQUE_EMAIL = True

# Determines the expiration date of email confirmation mails sent by django-email-confirmation.
EMAIL_CONFIRMATION_DAYS = 3 #####

# Request e-mail address from 3rd party account provider? E.g. using OpenID AX, or the Facebook "email" permission
# SOCIALACCOUNT_QUERY_EMAIL (=ACCOUNT_EMAIL_REQUIRED)

# Attempt to bypass the signup form by using fields (e.g. username, email) retrieved from the social account provider. If a conflict arises due to a duplicate e-mail address the signup form will still kick in.
# SOCIALACCOUNT_AUTO_SIGNUP (=True)

# Enable support for django-avatar. When enabled, the profile image of the user is copied locally into django-avatar at signup.
# SOCIALACCOUNT_AVATAR_SUPPORT (= 'avatar' in settings.INSTALLED_APPS)



# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/

STATIC_URL = '/static/'

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "static"),
)

LOGIN_REDIRECT_URL = '/'
