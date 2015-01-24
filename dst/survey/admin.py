from django.contrib.gis import admin
from survey.models import GravelSite, Pit, InputNode, Question, MapLayer, Context, QuestionCategory

admin.site.register(GravelSite, admin.GeoModelAdmin)
admin.site.register(Pit, admin.GeoModelAdmin)
admin.site.register(InputNode, admin.ModelAdmin)
admin.site.register(MapLayer, admin.ModelAdmin)

class ContextAdmin(admin.ModelAdmin):
	list_display = ('name', 'order')
	list_filter = ['name', 'order']
	ordering = ['order', 'name']

class CategoryAdmin(admin.ModelAdmin):
	list_display = ('name', 'context', 'order')
	list_filter = ['name', 'context', 'order']
	ordering = ['context__order', 'order', 'name']

class QuestionAdmin(admin.ModelAdmin):
    list_display = ('title', 'question', 'order', 'questionCategory')
    list_filter = ['title', 'question', 'order', 'questionCategory']
    ordering = ['order', 'title', 'questionCategory']

admin.site.register(Context, ContextAdmin)
admin.site.register(QuestionCategory, CategoryAdmin)
admin.site.register(Question, QuestionAdmin)
