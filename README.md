floodplain-restoration
======================

Decision support tool for floodplain gravel mine restoration

```
virtualenv --python /usr/bin/python3.4 ~/env/tnc
source ~/env/tnc/bin/activate
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

# Project
```
django-admin.py startproject dst
cd dst  # just a container

#create db
spatialite db.sqlite3 "SELECT InitSpatialMetaData();"
```

# edit settings
```
vim dst/settings.py

INSTALLED_APPS = (
    ...
    'django.contrib.gis',
)
DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.spatialite',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}
```


STATIC_ROOT = "dst/static"
MEDIA_ROOT = "dst/media"

mkdir  dst/static
mkdir dst/media

# App
```
python manage.py migrate
python manage.py startapp bbn 

 # create models.pyt THEN

python manage.py makemigrations bbn


python manage.py migrate

 python manage.py createsuperuser

 https://docs.djangoproject.com/en/dev/ref/contrib/gis/tutorial/#geographic-admin

rm bbn/migrations/000*.py 
python manage.py makemigrations
rm db.sqlite3
spatialite db.sqlite3 "SELECT InitSpatialMetaData();"
python manage.py migrate

