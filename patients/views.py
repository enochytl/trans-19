from django.shortcuts import render
from django.views.generic import TemplateView
from patients.models import Patients, Locations_visited

# Create your views here.
class PatientRecords(TemplateView):
    template_name = "records.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["patients"] = Patients.objects.all()
        return context

class PatientProfile(TemplateView):
    template_name = "patientprofile.html"

    def get_context_data(self, **kwargs):
        case_no = self.kwargs["case_no"]

        context = super().get_context_data(**kwargs)
        context["patient"] = Patients.objects.get(pk = case_no)
        context["locations_visited"] = Locations_visited.objects.filter(case_no=case_no)
        return context