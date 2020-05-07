from django.shortcuts import render
from django.views.generic import TemplateView
from patients.models import Patients, Locations_visited

# Create your views here.

class PatientProfile(TemplateView):
    template_name = "patientprofile.html"

    def get_context_data(self, **kwargs):
        case_no = self.kwargs["case_no"]

        context = super().get_context_data(**kwargs)
        context["patient"] = Patients.objects.get(pk = case_no)
        context["locations_visited"] = Locations_visited.objects.filter(case_no=case_no)
        return context

def search(request):
    key = request.GET.get('key')
    error_msg = ''

    if not key:
        error_msg = 'Please Enter Patient Name'
        return render(request, 'errors.html', {'error_msg': error_msg})
    patient_list = Patients.objects.filter(name__icontains = key)
    if (patient_list):
        return render(request, 'results.html', {'patient_list': patient_list})
    else:
        info = 'No Such Patient'

def records(request):
    if request.method == "POST":
        Patients.objects.create(
            name=request.POST['name'],
            id_document_no=request.POST['id_document_no'],
            date_of_birth=request.POST['date_of_birth'],
            date_of_confirmation=request.POST['date_of_confirmation'],
            case_no=request.POST['case_no']
            )
    user_list_obj = Patients.objects.all()
    return render(request, 'records.html', {'patients': user_list_obj})

