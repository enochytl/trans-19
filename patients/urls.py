from django.urls import path, re_path
from patients import views

urlpatterns = [
    path(
        "profile/<slug:case_no>/",
        views.PatientProfile.as_view(),
        name="profile"
    ),
    path(
        "search/",
        views.SearchPage.as_view(),
        name="search"
    ),
    re_path(r'^records/$', views.records),
    re_path(r'^locations/$', views.locations, name='locations'),
    path("dpatient/", views.dpatient, name = "dpatient"),
    path("dlocation/", views.dlocation, name = 'dlocation'),
    path("modify/", views.modify, name = 'modify'),
#    path("modify/<slug:case_no>", views.Modify.as_view(), name = 'modify'),
    
]