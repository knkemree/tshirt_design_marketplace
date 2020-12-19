from .base import *

DEBUG = True

ALLOWED_HOSTS = ['64.225.8.100', 'contextcustom.com', 'www.contextcustom.com']

INTERNAL_IPS = ['64.225.8.100', 'contextcustom.com']



def custom_show_toolbar(request):
    return False  # Always show toolbar, for example purposes only.

DEBUG_TOOLBAR_CONFIG = {
    'INTERCEPT_REDIRECTS': True,
    'SHOW_TOOLBAR_CALLBACK': custom_show_toolbar,

}

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'ccdb',
        'USER': 'emre',
        'PASSWORD': 'Ziy@emre1992',
        'HOST': 'localhost',
        'PORT': '',
    }
}

# AWS_ACCESS_KEY_ID = '7E2P4RU72GNS5Z4USMPC'
# AWS_SECRET_ACCESS_KEY = 'G22GYFbv1Yjkp/5malq7BeUWGUSVV4MU4NYdwlRJlCk'
# AWS_STORAGE_BUCKET_NAME = 'samnm'
# AWS_S3_ENDPOINT_URL = 'https://nyc3.digitaloceanspaces.com'
# AWS_S3_OBJECT_PARAMETERS = {
#     'CacheControl': 'max-age=86400',
# }
# AWS_LOCATION = 'samnm-static'
# AWS_DEFAULT_ACL = 'public-read'


# STATIC_URL = 'https://%s/%s/' % (AWS_S3_ENDPOINT_URL, AWS_LOCATION)
# STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
# DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
CELERY_BROKER_URL='amqp://localhost'
CELERY_RESULT_BACKEND='amqp://localhost'



STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static_cdn', 'static_root')

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'static_cdn', 'media_root')