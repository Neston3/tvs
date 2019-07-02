from django.contrib import admin
from django.contrib.auth.models import Group
from django.urls import path

from tvs import models as models

admin.site.site_header = 'Volunteer Management System'
admin.site.unregister(Group)


# Register your models here.

class UserField(admin.ModelAdmin):
    list_display = ('user', 'home_address', 'phone_number', 'role')


admin.site.register(models.Users, UserField)


class VolunteerField(admin.ModelAdmin):
    list_display = ('full_name', 'contact', 'location', 'certificate', 'experience'
                    , 'why_volunteer', 'status_update', 'length')


admin.site.register(models.Volunteer, VolunteerField)

class UploadCvs(admin.ModelAdmin):
    list_display = ('filename','year','uploadcvs')

admin.site.register(models.UploadFileCvs, UploadCvs)


class TestingField(admin.ModelAdmin):
    list_display = ('region', 'council', 'ward', 'school', 'enrolment', 'teacher', 'ptr')


class ToChart(admin.ModelAdmin):
    list_display = ('region', 'enrolment', 'teacher', 'ptr')


admin.site.register(models.ToChart, ToChart)


# custom clean button
class MyModelAdmin(admin.ModelAdmin):
    def get_urls(self):
        urls = super(MyModelAdmin, self).get_urls()
        my_urls = [
            path('admin/list', self.my_view, name="custom_view")
        ]
        return my_urls + urls

    def my_view(self, request):
        # custom view which should return an HttpResponse
        pass

    # In case your template resides in a non-standard location
    change_list_template = "volunteer/tvs/templates/admin/change_list.html"
