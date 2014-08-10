floodplain-restoration
======================

Decision support tool for floodplain gravel mine restoration

### Setup
	virtualenv --python /usr/bin/python3.4 ~/env/tnc
	source ~/env/tnc/bin/activate
	sudo apt-get install libtiff5-dev libjpeg8-dev zlib1g-dev libfreetype6-dev python3-dev 
	sudo apt-get install redis-server
	pip install -r requirements.txt
	pip install -r requirements-dev.txt

	django-admin.py startproject dst
	cd dst  # just a container

### create db
	spatialite dst/db.sqlite3 "SELECT InitSpatialMetaData();"

### settings
	vim dst/settings.py

	INSTALLED_APPS = (
	    ...
	    'django.contrib.gis',
	)
	DATABASES = {
	    'default': {
	        'ENGINE': 'django.contrib.gis.db.backends.spatialite',
	        'NAME': os.path.join(BASE_DIR, 'dst', db.sqlite3'),
	    }
	}

	STATIC_ROOT = "dst/static"
	MEDIA_ROOT = "dst/media"

### create dirs
	mkdir dst/static
	mkdir dst/media

### setup
	python manage.py migrate
	python manage.py startapp bbn 

	# create models.py 

	python manage.py makemigrations bbn

	python manage.py migrate

	python manage.py createsuperuser

	# https://docs.djangoproject.com/en/dev/ref/contrib/gis/tutorial/#geographic-admin

### To reset migrations during early dev
	rm bbn/migrations/000*.py 
	python manage.py makemigrations
	rm dst/db.sqlite3
	spatialite dst/db.sqlite3 "SELECT InitSpatialMetaData();"
	python manage.py migrate


### Profiling
	from silk.profiling.profiler import silk_profile
	@silk_profile(name='Some function I want to profile')
	def some_func():
		...


## TODO
* generate.py script to create from definition.json
	cpt.py (with query_cpt, mimics runit_try2) 
	cpt_orig.xls and cpt.xls (identical at first)
	questions.json (fixture)
* bayes_xls cptdict2xls function
* optimize.py script to use query_cpt() and cptdict2xls()
* file location refactoring
	from bbn.cpt.xls import xls2cptdict, ...
	from bbn.cpt import query_cpt  # defined in cpt.py but imported in __init__
	# scripts dir with generate and optimize
* load CPT in settings
* suitability @property using cpt.query_cpt(settings.CPT, inputnodes, )
* system_check function/mgmt command to make sure CPT matches questions
* setup routine to create test data
* unit tests against web api
* auth
* caching
* django pipeline
* angular integration
* flatblocks


Maybe not
*   django-secure
*   celery
*    django admin2 or xadmin or ???

## Test
* Ensure unique inputnodes for each site/question
* status after nodes and pits

Image credits:
Tracey Saxby, IAN Image Library (ian.umces.edu/imagelibrary/)