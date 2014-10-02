DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': '{{ dbname }}',
        'USER': '{{ dbname }}',
        'PASSWORD': '{{ dbname }}',
        'HOST':'localhost',
    }
}

DEBUG = {{ debug }}
TEMPLATE_DEBUG = {{ debug }} 

ADMINS = (('Matt Perry', 'mperry@ecotrust.org'),)
ALLOWED_HOSTS = ['localhost']

SECRET_KEY = '{{ secretkey }}'
