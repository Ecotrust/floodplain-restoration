floodplain-restoration
======================

[![Build Status](https://api.travis-ci.org/Ecotrust/floodplain-restoration.svg)](https://travis-ci.org/Ecotrust/floodplain-restoration) 
[![Coverage Status](https://img.shields.io/coveralls/Ecotrust/floodplain-restoration.svg)](https://coveralls.io/r/Ecotrust/floodplain-restoration)

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
	./test

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

# Deployment 

The deployment to stage and production is automated through the use of ansible
playbooks. 

1. "Build" the javascript and html app using grunt. Check closely for errors:

	cd ui && grunt build

2. Add the newly created js/css/html files, commit them and push to master:

    git add dist/scripts/scripts.cd312094.js
    git commit -a -m "new grunt build"
    git push

3. Deploying to "stage", our local virtualbox machine.

	vagrant up
	cd ../deploy
	./deploy localhost

4. Test it. Fix it if needed.

5. Deploy to production

	./deploy <produciton hostname>

