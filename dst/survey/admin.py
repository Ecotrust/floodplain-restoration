from django.contrib.gis import admin
from survey.models import GravelSite, Pit, InputNode, Question, MapLayer

admin.site.register(GravelSite, admin.GeoModelAdmin)
admin.site.register(Pit, admin.GeoModelAdmin)
admin.site.register(InputNode, admin.ModelAdmin)
admin.site.register(MapLayer, admin.ModelAdmin)
admin.site.register(Question, admin.ModelAdmin)
