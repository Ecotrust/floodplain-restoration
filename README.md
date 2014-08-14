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
    sudo service redis-server start
	pip install -r requirements.txt

	cd dst  # just a container

### Initialize

	spatialite dst/db.sqlite3 "SELECT InitSpatialMetaData();"
	python manage.py migrate
	python manage.py createsuperuser
	python manage.py loaddata survey/fixtures/questions.json
	python manage.py systemcheck

### To reset migrations during early development (use with caution)
	rm survey/migrations/000*.py 
	python manage.py makemigrations
	rm dst/db.sqlite3
	# follow steps in `Initialize` above

# Process for Creating/Updating the Bayesian Belief Network

The Bayesian Belief Network (BBN) is defined in the [.BIF interchange format](http://www.cs.cmu.edu/~fgcozman/Research/InterchangeFormat/Old/xmlbif02.html). By default, the canonical bbn for the project resides at `dst/data/bbn.bif`. Creating or updating this file goes as follows:

0. cd dst
1. Create or edit `dst/data/definition.json`; this is a json representation of the hierarchical conceptual model. 
2. run `python ../scripts/generate_bif.py`; this will create and *overwrite*
	- `dst/data/bbn.bif`
	- `survey/fixtures/questions.json`
3. Optimize using `../scripts/optimize.py` which will generate a new bif file; copy to `dst/data/bbn.bif` if you want to use it.
4. Edit `dst/data/bbn.bif` by hand if necessary.
5. Reload question fixtures with `python manage.py loaddata survey/fixtures/questions.json` (*warning: this will destroy all questions in the database and requires careful thought about data migration*)
6. Check system integrity with `python manage.py systemcheck`


# TODO
* tying inputnodes back to questions so the client side knows when to post/put
* /api/site/1/status > 
   (if there is a next questions) /api/question/:next: > 
   (if question has an answer node) /api/node/:answer:  (then populate UI)
* pit vs property-specific questions/inputnodes
* setup routine to create test data
* seperate db for silk?
* auth
* caching
* django pipeline
* angular integration
* flatblocks
* report generation (word, pdf, html)
* public sharing
* testing
    - ensure unique input nodes
    - ensure public sharing works
    - reports
    - bad values and expected HTTP errors

* Add image credits
	Image credits:
	Tracey Saxby, IAN Image Library (ian.umces.edu/imagelibrary/)

