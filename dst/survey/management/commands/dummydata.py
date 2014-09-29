from django.core.management.base import BaseCommand, CommandError
from survey.validate import systemcheck, SystemCheckError
from django.contrib.auth.models import User
from survey.models import GravelSite, Pit, InputNode, Question, MapLayer


MULTIPOLY = """MULTIPOLYGON (((-401141.5244410000159405 273728.5500730000203475, -587036.3772299999836832 68183.1278420000016922, -489196.9810249999864027 -39441.7579719999994268, -117407.2754459999996470 87752.4768060000060359, -401141.5244410000159405 273728.5500730000203475)))"""
POLY = """POLYGON ((-401141.5244410000159405 273728.5500730000203475, -587036.3772299999836832 68183.1278420000016922, -489196.9810249999864027 -39441.7579719999994268, -117407.2754459999996470 87752.4768060000060359, -401141.5244410000159405 273728.5500730000203475))"""
SITE1 = {
    'name': 'GravelSite1',
    'notes': 'Notes on Site 1',
    'geometry': MULTIPOLY,
}
PIT1 = {
    'name': 'testpit',
    'geometry': POLY,
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

        print("Create site...")
        site = GravelSite.objects.create(user=user, **SITE1)

        print("Create pits...")
        pit = Pit.objects.create(user=user, site=site, **PIT1)

        print("Create some input nodes (answers)...")
        q = Question.objects.get(id=1)
        inode = InputNode.objects.create(user=user, site=site, question=q, value=0.3)
