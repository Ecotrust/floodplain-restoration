floodplain-restoration
======================

[![Build Status](https://api.travis-ci.org/Ecotrust/floodplain-restoration.svg)](https://travis-ci.org/Ecotrust/floodplain-restoration)
[![Coverage Status](https://img.shields.io/coveralls/Ecotrust/floodplain-restoration.svg)](https://coveralls.io/r/Ecotrust/floodplain-restoration)

Decision support tool for floodplain gravel mine restoration

This has been tested with `Python 3.4` and `Django 1.7`; YMMV when trying other versions.

# Quickstart

### Vagrant Init (if using local VM)
	vagrant up
	vagrant ssh
	sudo apt-get update
	sudo apt-get upgrade
	cd /usr/local/apps/floodplain-restoration/

### Local Init
	sudo apt-get install python-virtualenv
	sudo apt-get install python3-pip
	virtualenv --python /usr/bin/python3.4 ~/env/tnc
	source ~/env/tnc/bin/activate

### Setup
	sudo apt-get install libtiff5-dev libjpeg8-dev zlib1g-dev libfreetype6-dev python3-dev ansible
	sudo apt-get install redis-server
	sudo service redis-server start
	pip install -r requirements.txt

	cd dst  # just a container
	./test

### Initialize Database

	spatialite dst/db.sqlite3 "SELECT InitSpatialMetaData();"
	python manage.py migrate
	python manage.py createsuperuser
	python manage.py loaddata survey/fixtures/questions.json
	python manage.py loaddata dst/fixtures/flatblocks.json
	python manage.py systemcheck

### To reset migrations during early development (use with caution)
	rm survey/migrations/000*.py
	python manage.py makemigrations
	rm dst/db.sqlite3
	# follow steps in `Initialize` above

# Process for Creating/Updating the Bayesian Belief Network

The Bayesian Belief Network (BBN) is defined in the [.BIF interchange format](http://www.cs.cmu.edu/~fgcozman/Research/InterchangeFormat/Old/xmlbif02.html). By default, the canonical bbn for the project resides at `dst/data/bbn.bif`. Creating or updating this file goes as follows:

This file was **initially created** by the following process. You do not want to do this often, it will blow away all
previous changes but is probably the easiest way to start again from scratch or to deal
with significant structural changes to the network.

0. cd dst
1. Create or edit `dst/data/definition.json`; this is a json representation of the hierarchical conceptual model.
2. run `python ../scripts/generate_bif.py`; this will create and *overwrite*
	- `dst/data/bbn.bif`
	- `survey/fixtures/questions.json`
3. Optimize using `../scripts/optimize.py` which will generate a new bif file; copy to `dst/data/bbn.bif` if you want to use it.
4. Edit `dst/data/bbn.bif` by hand if necessary.
5. Reload question fixtures with `python manage.py loaddata survey/fixtures/questions.json` (*warning: this will destroy all questions in the database and requires careful thought about data migration*)
6. Check system integrity with `python manage.py systemcheck`

To **re-calibrate the BBN**, first become intimately familiar with the file format ([required reading](https://github.com/Ecotrust/floodplain-restoration/wiki/Defining-Bayseian-Belief-Networks-using-.bif-files)) then simply:

1. Edit `dst/data/bbn.bif` by hand.
2. Check system integrity with `python manage.py systemcheck`

To **update the BBN**, don't. If you **HAVE** to:

1. Update your source ('canonical') diagram first to be sure you understand how your changes affect the entire model.
2. Update your definitions JSON: `dst/data/definition.json`
3. Backup your current, hand-calibrated .BIF to somewhere safe: `dst/data/bbn.bif`
4. Backup your current survey question data: `manage.py dumpdata --indent=2 survey.question > survey/fixtures/questions_backup.json`
5. Generate the new bif and questions based on the definitions: `python ../scripts/generate_bif.py`
6. Manually review the changes between the old and newly generated .bif files. If you have hand-made calibrations in the old version to nodes that haven't changed, copy your old values back in line-by-line.
7. Run `python manage.py systemcheck` and note which questions were changed (added/removed)
8. Run `python manage.py runserver` and use the admin to add, remove, or update the changed questions.
9. Use the systemcheck technique to test that you've made all changes correctly.
10. When satisfied, dump your new questions fixture: `manage.py dumpddata --indent=2 survey.question > survey/fixtures/questions.json`

# Deployment

The deployment to stage and production is automated through the use of ansible
playbooks.

"Build" the javascript and html app using grunt. Check closely for errors:

```
cd ui && grunt build
```

Add the newly created js/css/html files, commit them and push to master:

```
git add dist/scripts/scripts.cd312094.js
git commit -a -m "new grunt build"
git push
```

Deploy to "stage", our local virtualbox machine from its host.

```
vagrant up
cd ../deploy
./deploy localhost
```

Test it and fix it if needed. Then deploy to production

```
./deploy <produciton hostname>
```
