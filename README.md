floodplain-restoration
======================

Decision support tool for floodplain gravel mine restoration

### Setup
	virtualenv --python /usr/bin/python3.4 ~/env/tnc
	source ~/env/tnc/bin/activate
	sudo apt-get install libtiff5-dev libjpeg8-dev zlib1g-dev libfreetype6-dev python3-dev 
	sudo apt-get install redis-server
	pip install -r requirements.txt

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
	python manage.py startapp survey 

	# create models.py 

	python manage.py makemigrations survey

	python manage.py migrate

	python manage.py createsuperuser

	# https://docs.djangoproject.com/en/dev/ref/contrib/gis/tutorial/#geographic-admin

### To reset migrations during early dev
	rm survey/migrations/000*.py 
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
* tying inputnodes back to questions so the client side knows when to post/put
* /api/site/1/status > 
   (if there is a next questions) /api/question/:next: > 
   (if question has an answer node) /api/node/:answer:  (then populate UI)


* system_check function/mgmt command to make sure CPT matches questions

* pit vs property-specific questions/inputnodes

* translate cpt_edited to our new ~format
* setup routine to create test data
* seperate db for silk
* unit tests against web api
* auth
* caching
* django pipeline
* angular integration
* flatblocks
* report generation
* public sharing


## Test
* system check
* ensure unique input nodes
* status after nodes and pits

Image credits:
Tracey Saxby, IAN Image Library (ian.umces.edu/imagelibrary/)


# Process
0. cd dst
1. Create or edit `dst/data/definition.json`
2. run `python ../scripts/generate_bif.py`; this will create and *overwrite*
	- `dst/data/bbn.bif`
	- `survey/fixtures/questions.json`
3. Optimize and/or edit `data/bbn.bif`
4. load fixtures with `python manage.py loaddata survey/fixtures/questions.json`

# OLD STUFF vvvvvvvv

## process for *Initial* creation
1. Edit definition.json
2. python generate.py; creates
	cpt.py
	cpt.xls
	questions.json
3. optimize/edit cpt.xls
4. copy cpt* to dst/bbn/cpt/ and copy questions.json to dst/bbn/fixtures
    cd dst
	cp ../data/cpt.xls bbn/cpt/cpt.xls
	cp ../data/cpt.py bbn/cpt/cpt.py
	cp ../data/questions.json bbn/fixtures/questions.json
5. load fixtures
    python manage.py loaddata bbn/fixtures/questions.json



## process for updating
1. Edit definition.json
2. generate
3. ???


http://textik.com/#6cbb27a529229ac2