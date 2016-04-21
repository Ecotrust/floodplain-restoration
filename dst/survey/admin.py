from django.contrib.gis import admin
from survey.models import GravelSite, Pit, InputNode, Question, Context, QuestionCategory, BifSettings

admin.site.register(GravelSite, admin.GeoModelAdmin)
admin.site.register(Pit, admin.GeoModelAdmin)
admin.site.register(InputNode, admin.ModelAdmin)
# admin.site.register(MapLayer, admin.ModelAdmin)
# admin.site.register(BifSettings, admin.ModelAdmin)

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

class BifAdmin(admin.ModelAdmin):

    # def changelist_view(self, request):
    #     return survey_views.edit_bbn(self, request)

    def change_view(self, request, bifid):
        from survey import views as survey_views
        return survey_views.admin_change_form(self, request, bifid)

    def add_view(self, request):
        from survey import views as survey_views
        return survey_views.admin_add_form(self, request)

    def get_urls(self):
        from django.conf.urls import patterns
        # Set up the URLS dynamically
        urls = super(BifAdmin, self).get_urls()
        my_urls = patterns('',
                            # ('^$', self.changelist_view),
                            ('^(?P<bifid>d+)/$', self.change_view),
                            ('^add/$', self.add_view),
                        )

        return my_urls + urls

    def save_model(self, request, obj, form, change):
        from survey.views import update_bbn_bif
        ## TODO: validate first!
        update_bbn_bif(request.POST)
        obj.save()

admin.site.register(BifSettings, BifAdmin)
