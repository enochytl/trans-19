from django.contrib import admin

from .models import *
# Register your models here.

admin.site.site_header = 'Trans-19: Staff Administration Site'

class PatientAdmin(admin.ModelAdmin):
    #change_form_template(admin/
    list_display = ('name', 'id_document_no', 'date_of_birth', 'date_of_confirmation',
                    'case_no')
    list_display_links = ('name', 'id_document_no', 'case_no')
    list_filter = ('date_of_confirmation', 'date_of_birth')
    search_fields = ('name', 'id_document_no', 'case_no')

class LocationsAdmin(admin.ModelAdmin):
    list_display = ('name', 'start_date', 'end_date', 'Coordinates', 'Address',
                    'description', 'category')
    
    def Coordinates(self, obj):
        return "({}, {})".format(obj.x, obj.y)
    
    def Address(self, obj):
        return "{} {} {}".format(obj.address_line_1, obj.address_line_2, obj.address_line_3)

admin.site.register(Patients, PatientAdmin)

admin.site.register(Locations_visited, LocationsAdmin)
