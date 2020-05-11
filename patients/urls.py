from django.urls import path, re_path
from patients import views

urlpatterns = [
    path(
        "patients/<slug:case_no>/",
        views.PatientProfile.as_view(),
        name="patients_profile"
    ),
    path(
        "patientmodify/<slug:case_no>/",
        views.patientModify.as_view(),
        name="patients_modify"
    ),
    path(
        "locationmodify/<slug:location_id>/",
        views.locationModify.as_view(),
        name="locations_modify"
    ),
    path(
        "recordmodify/<slug:case_no>/<slug:record_id>/",
        views.recordModify.as_view(),
        name="records_modify"
    ),
    path(
        "search/",
        views.SearchPage.as_view(),
        name="search"
    ),
    re_path(r'^patients/$', views.patients, name='patients'),
    re_path(r'^locations/$', views.locations, name='locations'),
    
]
