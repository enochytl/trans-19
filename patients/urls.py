from django.urls import path
from patients import views

urlpatterns = [
    path(
        "",
        views.PatientRecords.as_view(),
        name="records"
    ),
    path(
        "profile/<slug:case_no>/",
        views.PatientProfile.as_view(),
        name="profile"
    ),
]