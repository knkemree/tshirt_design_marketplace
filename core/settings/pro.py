from .base import *

DEBUG = False

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



# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/

...
# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

AWS_ACCESS_KEY_ID = 'SQOWXRXUG533D4DSUHJD'
AWS_SECRET_ACCESS_KEY = '/UCd/CzPtnf5IdNDoOd6L/ZH1QN7VXSRZDV2L8iDAaM'
AWS_STORAGE_BUCKET_NAME = 'contextcustom-space'
AWS_S3_ENDPOINT_URL = 'https://nyc3.digitaloceanspaces.com'
AWS_S3_OBJECT_PARAMETERS = {
    'CacheControl': 'max-age=86400',
}
AWS_LOCATION = 'static'
AWS_DEFAULT_ACL = None


STATIC_URL = 'https://%s/%s/' % (AWS_S3_ENDPOINT_URL, AWS_LOCATION)
STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

CELERY_BROKER_URL='amqp://localhost'
CELERY_RESULT_BACKEND='amqp://localhost'



# STATIC_URL = '/static/'
# STATIC_ROOT = os.path.join(BASE_DIR, 'static_cdn', 'static_root')

# MEDIA_URL = '/media/'
# MEDIA_ROOT = os.path.join(BASE_DIR, 'static_cdn', 'media_root')