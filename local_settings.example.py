# -*- coding: utf-8 -*-

DEBUG = True
DISPLAY_DEBUG_TOOLBAR = True

ADMINS = (
    ('Your Email Here', 'abc@gmail.com'),
)

DATABASE_ENGINE = 'django.db.backends.postgresql_psycopg2' # 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
DATABASE_NAME = 'freesound'             # Or path to database file if using sqlite3.
DATABASE_USER = 'freesound'             # Not used with sqlite3.
DATABASE_HOST = ''             # Set to empty string for localhost. Not used with sqlite3.
DATABASE_PORT = ''             # Set to empty string for default. Not used with sqlite3.
DATABASE_PASSWORD = ''

# Make this unique, and don't share it with anybody.
SECRET_KEY = ''

EMAIL_HOST = 'localhost'
EMAIL_PORT = 2525

PROXIES = {} #'http': 'http://proxy.upf.edu:8080'}

RECAPTCHA_PRIVATE_KEY = ''
RECAPTCHA_PUBLIC_KEY = ''
AKISMET_KEY = ''

GOOGLE_API_KEY = ''
GOOGLE_ANALYTICS_KEY = ''

SOLR_URL = "http://localhost:8983/solr/"

GEARMAN_JOB_SERVERS = ["localhost:4730"]