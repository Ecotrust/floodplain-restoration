from django.contrib.gis import admin
from survey.models import GravelSite, Pit, InputNode, Question, MapLayer

admin.site.register(GravelSite, admin.GeoModelAdmin)
admin.site.register(Pit, admin.GeoModelAdmin)
admin.site.register(InputNode, admin.ModelAdmin)
admin.site.register(MapLayer, admin.ModelAdmin)

class QuestionAdmin(admin.ModelAdmin):
    list_display = ('title', 'question', 'order', 'category')
    list_filter = ['title', 'question', 'order', 'category']
    ordering = ['order', 'category', 'title', 'question']

admin.site.register(Question, QuestionAdmin)
