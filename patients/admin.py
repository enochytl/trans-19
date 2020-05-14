from django.contrib import admin
from django.contrib.auth.models import Group
from .models import *

from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserChangeForm
# from django.contrib.auth.models import User

# Register your models here.

admin.site.site_header = 'Trans-19: Staff Administration Site'

class PatientAdmin(admin.ModelAdmin):
    list_display = ('name', 'id_document_no', 'date_of_birth', 'date_of_confirmation',
                    'case_no')
    list_display_links = ('name', 'id_document_no', 'case_no')
    list_filter = ('date_of_confirmation', 'date_of_birth')
    search_fields = ('name', 'id_document_no', 'case_no')

class LocationAdmin(admin.ModelAdmin):
    list_display = ('name', 'Coordinates', 'Address',
                    'district', 'description', 'category')
    list_editable = ('description', 'category')
    def Coordinates(self, obj):
        return "({}, {})".format(obj.x, obj.y)
    
    def Address(self, obj):
        line1 = '' if (obj.address_line_1 is None) else obj.address_line_1
        line2 = '' if (obj.address_line_2 is None) else obj.address_line_2
        line3 = '' if (obj.address_line_3 is None) else obj.address_line_3
        return "{} {} {}".format(line1, line2, line3) 


class StaffUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = StaffUser
        # fields = UserAdmin.fields + ['user_type']
        # fields = ['username', 'password', 'first_name', 'last_name', 'email', 'is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions', 'last_login', 'date_joined', 
        #                         'user_type',]
    #     fieldsets = UserAdmin.fieldsets + (
    #     (None, {'fields': ('user_type', )}),
    # )
    # USER_TYPE_CHOICES = (
    #     (1, 'CHP'),
    #     (2, 'Epidemiologists'),
        
    # )
    # def __init__(self, *args, **kwargs):
    #     super(StaffUserChangeForm, self).__init__(*args, **kwargs)
    #     current_state = self.instance.user_type
    #     ...construct available_choices based on current state...
    #     self.fields['state'].choices = available_choices

    # user_type = models.PositiveSmallIntegerField(choices=USER_TYPE_CHOICES)

class StaffUserAdmin(UserAdmin):
    form = StaffUserChangeForm
    # editable = ("user_type")
    # add_fields = ("user_type",)
    # fields = ("user_type",)
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('user_type',)}),
    )
    # fieldsets = StaffUser.USER_TYPE_CHOICES + (
    #         (None, {'fields': ('USER_TYPE_CHOICES',)}),
    # )

# admin.site.unregister(User)
# admin.site.register(User, UserAdmin)
admin.site.register(StaffUser, StaffUserAdmin)


admin.site.register(Patient, PatientAdmin)

admin.site.register(Location, LocationAdmin)

admin.site.register(VisitingRecord)
# admin.site.unregister(Group)
