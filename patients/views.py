from django.shortcuts import render
from django.views.generic import TemplateView
from patients.models import Patients, Locations_visited
from django.db.models import Q
from datetime import datetime, timedelta 

from django.template.defaulttags import register

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)

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

class SearchPage(TemplateView):
    template_name = "search.html"

    def get_context_data(self, **kwargs):
        # case_no = self.kwargs["case_no"]

        district_val = self.request.GET.get('district')
        window = self.request.GET.get('window')
        location = self.request.GET.get('location')
        patients = []

        connec = {}
        if district_val and window and location:

            patients_no  = list(Locations_visited.objects.filter(Q(name__icontains=location)).filter(district = district_val).values_list("case_no", flat=True).distinct())
            print("patient no: ", patients_no)
            patients = Patients.objects.filter(pk__in=patients_no)
            for pa in patients:
                pa_visted = Locations_visited.objects.filter(Q(name__icontains=location)).filter(district = district_val).filter(case_no=pa)
                for pav in pa_visted:
                    start_date = pav.start_date - timedelta(days = int(window))
                    print("start: ",start_date)
                    print("start: ",type(start_date))
                    end_date = pav.start_date + timedelta(days = int(window))
                    print("end: ", end_date)
                    print("end: ", type(end_date))
                    covisited_start = Locations_visited.objects.filter(Q(name__icontains=location)).filter(district = district_val).filter(start_date__range=( start_date, end_date ) )
                    covisited_end = Locations_visited.objects.filter(Q(name__icontains=location)).filter(district = district_val).filter(end_date__range=( start_date, end_date ) )
                    # covisited_end = Locations_visited.objects.filter(Q(name__icontains=location)).filter(district = district_val).filter(start_date_range=[pav.end_date-timedelta( end_date_range=[pav.start_date-timedelta(days = int(window)), pav.start_date + timedelta(days = int(window))])
                    covisited = covisited_start | covisited_end
                    print("covisited: ",covisited)
                    # covisited = covisited_start.union(covisited_end)

                    for tmp in covisited:
                        print("tmp:", tmp.case_no.all())
                        if pa.case_no not in  connec:
                            connec[pa.case_no] = []
                        print("tmp.case_no:",tmp.case_no)
                        # print("tmp.case_no:",tmp.case_no==patients.Patients.None)
                        for case in tmp.case_no.all():
                            # tmp_pa = Patients.objects.get(pk = tmp.case_no)
                            if case.case_no != pa.case_no:
                                connec[pa.case_no].append([case.case_no, case.name, case.date_of_confirmation, tmp.name, tmp.start_date, tmp.description, pav.start_date, pav.description])


        context = super().get_context_data(**kwargs)
        context["patients"] = patients
        print("connec:",connec)
        context["connec"] = connec
        context["district"] = district_val
        context["window"] = window
        context["location"] = location
        # context["locations_visited"] = Locations_visited.objects.filter(case_no=case_no)
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

