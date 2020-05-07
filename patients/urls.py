from django.urls import path, re_path
from patients import views

urlpatterns = [
    path(
        "profile/<slug:case_no>/",
        views.PatientProfile.as_view(),
        name="profile"
    ),
    re_path(r'^records/$', views.records),
    re_path(r'^search/$', views.search),
]