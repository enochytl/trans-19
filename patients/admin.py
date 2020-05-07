from django.contrib import admin
from django.contrib.auth.models import Group
from .models import *
# Register your models here.

admin.site.site_header = 'Trans-19: Staff Administration Site'

class PatientAdmin(admin.ModelAdmin):
    list_display = ('name', 'id_document_no', 'date_of_birth', 'date_of_confirmation',
                    'case_no')
    list_display_links = ('name', 'id_document_no', 'case_no')
    list_filter = ('date_of_confirmation', 'date_of_birth')
    search_fields = ('name', 'id_document_no', 'case_no')

class LocationsAdmin(admin.ModelAdmin):
    list_display = ('name', 'start_date', 'end_date', 'Coordinates', 'Address',
                    'description', 'category')
    list_editable = ('description', 'category')
    def Coordinates(self, obj):
        return "({}, {})".format(obj.x, obj.y)
    
    def Address(self, obj):
        line1 = '' if (obj.address_line_1 is None) else obj.address_line_1
        line2 = '' if (obj.address_line_2 is None) else obj.address_line_2
        line3 = '' if (obj.address_line_3 is None) else obj.address_line_3
        return "{} {} {}".format(line1, line2, line3) 

admin.site.register(Patients, PatientAdmin)

admin.site.register(Locations_visited, LocationsAdmin)

admin.site.unregister(Group)
