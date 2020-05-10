from django.urls import path, re_path
from patients import views

urlpatterns = [
    path(
        "patients/<slug:case_no>/",
        views.PatientProfile.as_view(),
        name="patients_profile"
    ),
    path(
        "search/",
        views.SearchPage.as_view(),
        name="search"
    ),
    re_path(r'^patients/$', views.patients, name='patients'),
    re_path(r'^locations/$', views.locations, name='locations'),
   #path("dpatient/", views.dpatient, name = "dpatient"),
   #path("dlocation/", views.dlocation, name = 'dlocation'),
    path("modify/", views.modify, name = 'modify'),
    path("modify/<slug:case_no>", views.Modify.as_view(), name = 'modify'),
    
]
