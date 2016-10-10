# djangoForum

This Django 1.9 project is a first attempt at building a Django site.

The site has a login/logout/registration, uses all-auth for social media authentication.

Forum for signed in users to create topics and add posts.

Blog for users to submit articles for admin approval.

A file sharing app for users to upload files for admin approval.

This project has been integrated with the Bootstrap-Admin-Template theme.

Local path /home/pi/djangoForum/djangoForum

# General Setup

$ mkdir djangoForum
$ cd djangoForum
$ virtualenv .
$ source bin/activate
$ git clone ''...this repo...''
$ cd djangoForum
$ git init    (optional)

# Setup emails:
$ cd crudProject/settings.py

Add gmail password to
DEFAULT_FROM_EMAIL = 'shanegibney@gmail.com'
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'shanegibney@gmail.com'
EMAIL_HOST_PASSWORD = '\*\*\*\*\*\*\*\*\*\*'
EMAIL_USE_TLS = True

 <img width="1266" alt="screen shot 2016-06-20 at 23 38 37" src="https://cloud.githubusercontent.com/assets/17167992/16212578/a920aa5e-3740-11e6-99be-e3dc7f0134d5.png">
