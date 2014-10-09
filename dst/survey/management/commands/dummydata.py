from django.core.management.base import BaseCommand, CommandError
from survey.validate import systemcheck, SystemCheckError
from django.contrib.auth.models import User
from survey.models import GravelSite, Pit, InputNode, Question, MapLayer


MULTIPOLY = """MULTIPOLYGON (((-13737541 5483225, -13737541 5615730, -13559249 5615730, -13559249 5483225, -13737541 5483225)))"""
POLY = """POLYGON ((-13682677 5540964, -13682677 5575747, -13635875 5575747, -13635875 5540964, -13682677 5540964))"""


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
