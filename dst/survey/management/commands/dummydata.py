from django.core.management.base import BaseCommand, CommandError
from survey.validate import systemcheck, SystemCheckError
from django.contrib.auth.models import User
from survey.models import GravelSite, Pit, InputNode, Question, MapLayer
import json
import os
from django.contrib.gis.geos import GEOSGeometry, MultiPolygon


SITETEMP = {
    'name': None,
    'notes': 'Notes on Site',
    'geometry': None,
}

PITTEMP = {
    'name': 'testpit',
    'geometry': None,
    # pit-specific attrs
    'contamination': 0.5,
    'substrate': 0.5,
    'adjacent_river_depth': 0.5,
    'slope_dist': 0.5,
    'pit_levies': 0.5,
    'bedrock': 0.5,
    'bank_slope': 0.5,
    'pit_depth': 0.5,
    'surface_area': 0.5,
    'complexity': 0.5,
    # site (with site id) is also required, filled in when needed
}

USER1 = dict(username="dummyuser", password="dummyuser")
DUMMYDATADIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..', 'dst', 'data', 'dummydata'))

DATA = [
  ('Willamette Confluence', os.path.join(DUMMYDATADIR, 'site1.geojson'), os.path.join(DUMMYDATADIR, 'site1_pits.geojson')),
  ('Site Two', os.path.join(DUMMYDATADIR, 'site2.geojson'), os.path.join(DUMMYDATADIR, 'site2_pits.geojson')),
  ('Site 3', os.path.join(DUMMYDATADIR, 'site3.geojson'), os.path.join(DUMMYDATADIR, 'site3_pits.geojson')),
]

class Command(BaseCommand):
    help = 'Checks the current system for data integrity'

    def handle(self, *args, **options):
        try:
            user = User.objects.get(username="dummyuser")
        except:
            user = User.objects.create_user(**USER1)

        print("Deleting existing dummyuser data...")
        GravelSite.objects.filter(user=user).delete()
        Pit.objects.filter(user=user).delete()
        InputNode.objects.filter(user=user).delete()

        for sitetuple in DATA:
            sitename = sitetuple[0]
            sitegeojson = sitetuple[1]
            pitsgeojson = sitetuple[2]

            print("Create site {} ...".format(sitename))

            thesite = SITETEMP.copy()
            thesite['name'] = sitename
            with open(sitegeojson, 'r') as fh:
                fc = json.loads(fh.read())

            thesite['geometry'] = MultiPolygon(GEOSGeometry(str(fc['features'][0]['geometry']))).wkt
            site = GravelSite.objects.create(user=user, **thesite)

            with open(pitsgeojson, 'r') as fh:
                fc = json.loads(fh.read())

                for feat in fc['features']:
                    thepit = PITTEMP.copy()
                    thepit['geometry'] = GEOSGeometry(str(feat['geometry'])).wkt
                    
                    print("\tCreate pits...")
                    pit = Pit.objects.create(user=user, site=site, **thepit)

            print("Create some input nodes (answers)...")
            q = Question.objects.get(id=1)
            inode = InputNode.objects.create(user=user, site=site, question=q, value=0.3)
