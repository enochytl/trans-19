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

def records(request):
    if request.method == "POST":
        Patients.objects.create(
            name = request.POST['name'],
            id_document_no = request.POST['id_document_no'],
            date_of_birth = request.POST['date_of_birth'],
            date_of_confirmation = request.POST['date_of_confirmation'],
            case_no = request.POST['case_no']
            )
    user_list_obj = Patients.objects.all()
    return render(request, 'records.html', {'patients': user_list_obj})

def dpatient(request):
    if request.method == "POST":
        delete_list = request.POST.getlist('check_box_list')
        for item in delete_list:
            Patients.objects.filter(case_no = item).delete()
    user_list_obj = Patients.objects.all()
    return render(request, 'dpatient.html', {'patients': user_list_obj})

def dlocation(request):
    if request.method == "POST":
        delete_list = request.POST.getlist('check_box_list')
        print(delete_list)
        for item in delete_list:
            Locations_visited.objects.filter(name = item).delete()
    user_list_obj = Locations_visited.objects.all()
    return render(request, 'dlocation.html', {'locations_visited': user_list_obj})

def locations(request):
    if request.method == "POST":
        Locations_visited.objects.create(
            name = request.POST['name'],
            start_date = request.POST['start_date'],
            end_date = request.POST['end_date'],
            x = request.POST['x'],
            y = request.POST['y'],
            address_line_1 = request.POST['address_line_1'],
            address_line_2 = request.POST['address_line_2'],
            address_line_3 = request.POST['address_line_3'],
            category = request.POST['category'],
            description = request.POST['description']
        )
    return render(request, 'locations.html')

class Modify(TemplateView):

    template_name = "modify.html"
    def post(self, request, **kwargs):
        case_no = self.kwargs["case_no"]
        check_list = request.POST.getlist('check_box_list')
        user_list_obj = Locations_visited.objects.all()
        return render(request, "{% url 'modify' case_no %}", {'locations_visited': user_list_obj})
    def get_context_data(self, **kwargs):
        case_no = self.kwargs["case_no"]
        context = super().get_context_data(**kwargs)
        context["patient"] = Patients.objects.get(pk = case_no)
        context["locations_visited"] = Locations_visited.objects.filter(case_no=case_no)
        return context


def modify(request, *wargs, **kwargs):
    if request.method == "POST":
        p_id = request.POST["patient"]
        loc_list = request.POST.getlist('check_box_list')
        for item in loc_list:
            Locations_visited.objects.get(name = item).case_no.add(p_id)
    p_list_obj = Patients.objects.all()
    loc_list_obj = Locations_visited.objects.all()
    return render(request, "modify.html", {'patients' : p_list_obj, 'locations_visited': loc_list_obj})

