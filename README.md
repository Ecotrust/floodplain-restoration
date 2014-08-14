floodplain-restoration
======================

Decision support tool for floodplain gravel mine restoration

This has been tested with `Python 3.4` and `Django 1.7`; YMMV when trying other versions. 

# Quickstart

### Setup
	virtualenv --python /usr/bin/python3.4 ~/env/tnc
	source ~/env/tnc/bin/activate
	sudo apt-get install libtiff5-dev libjpeg8-dev zlib1g-dev libfreetype6-dev python3-dev 
	sudo apt-get install redis-server
	pip install -r requirements.txt

	cd dst  # just a container

### create a spatialite db
	spatialite dst/db.sqlite3 "SELECT InitSpatialMetaData();"


### create dirs
	mkdir dst/static
	mkdir dst/media

### Initialize the application
	python manage.py migrate
	python manage.py createsuperuser
	python manage.py loaddata survey/fixtures/questions.json

### To reset migrations during early development (Use with caution)
	rm survey/migrations/000*.py 
	python manage.py makemigrations
	rm dst/db.sqlite3
	spatialite dst/db.sqlite3 "SELECT InitSpatialMetaData();"
	python manage.py migrate


# Process for Creating/Updating the Bayesian Belief Network

The Bayesian Belief Network (BBN) is defined in the [.BIF interchange format](http://www.cs.cmu.edu/~fgcozman/Research/InterchangeFormat/Old/xmlbif02.html). By default, the canonical bbn for the project resides at `dst/data/bbn.bif`. Creating or updating this file goes as follows:

0. cd dst
1. Create or edit `dst/data/definition.json`; this is a json representation of the hierarchical conceptual model. 
2. run `python ../scripts/generate_bif.py`; this will create and *overwrite*
	- `dst/data/bbn.bif`
	- `survey/fixtures/questions.json`
3. Either a) optimize using `../scripts/optimize.py` and/or edit `dst/data/bbn.bif` directly with a text editor. 
4. reload question fixtures with `python manage.py loaddata survey/fixtures/questions.json` (*warning: this will destroy all questions in the database and requires though about data migration*)


# TODO
* tying inputnodes back to questions so the client side knows when to post/put
* /api/site/1/status > 
   (if there is a next questions) /api/question/:next: > 
   (if question has an answer node) /api/node/:answer:  (then populate UI)
* system_check function/mgmt command 
    - make sure the terminal nodes of the belief network matches questions
    - make sure we can construct and query the network from the bif 
* pit vs property-specific questions/inputnodes
* translate cpt_edited to our new bif format
* setup routine to create test data
* seperate db for silk?
* unit tests against web api
* auth
* caching
* django pipeline
* angular integration
* flatblocks
* report generation (word, pdf, html)
* public sharing
* testing: ensure unique input nodes
* Add image credits
	Image credits:
	Tracey Saxby, IAN Image Library (ian.umces.edu/imagelibrary/)

