from django.shortcuts import render
from django.shortcuts import redirect
from django.views.generic import TemplateView
from patients.models import Patient, Location, VisitingRecord
from django.db.models import Q
from datetime import datetime, timedelta 

from django.template.defaulttags import register

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)

# Create your views here.

class PatientProfile(TemplateView):
    def dispatch(self, request, *args, **kwargs):
        page_case_no = self.kwargs["case_no"]
    
        if request.method == "POST":
            if 'add_submit' in request.POST:
                VisitingRecord.objects.create(
                    start_date = request.POST['start_date'],
                    end_date = request.POST['end_date'],
                    loc = Location.objects.get(name=request.POST['location']),
                    case_no = page_case_no
                    )
            elif 'delete_submit' in request.POST:
                delete_list = request.POST.getlist('check_box_list')
                for item in delete_list:
                    VisitingRecord.objects.filter(id=item).delete()

        return render(request, 'patientprofile.html', {"patient": Patient.objects.get(pk=page_case_no),
                       "visiting_records": VisitingRecord.objects.filter(case_no=page_case_no),
                       "locations": Location.objects.all()})



def patients(request):
    if request.method == "POST":
        if 'add_submit' in request.POST:
            Patient.objects.create(
                name = request.POST['name'],
                id_document_no = request.POST['id_document_no'],
                date_of_birth = request.POST['date_of_birth'],
                date_of_confirmation = request.POST['date_of_confirmation'],
                case_no = request.POST['case_no']
                )
        elif 'delete_submit' in request.POST:
            delete_list = request.POST.getlist('check_box_list')
            for item in delete_list:
                Patient.objects.filter(case_no = item).delete()

                # delete all visiting records associated with patients to be deleted
                recordList = VisitingRecord.objects.filter(case_no=item)
                for record in recordList:
                    record.delete()

    user_list_obj = Patient.objects.all()
    return render(request, 'patients.html', {'patients': user_list_obj})


def locations(request):
    if request.method == "POST":
        if 'add_submit' in request.POST:
            Location.objects.create(
                name = request.POST['name'],
                x = request.POST['x'],
                y = request.POST['y'],
                address_line_1 = request.POST['address_line_1'],
                address_line_2 = request.POST['address_line_2'],
                address_line_3 = request.POST['address_line_3'],
                category = request.POST['category'],
                description = request.POST['description'],
                district = request.POST['district']
        )
        elif 'delete_submit' in request.POST:
            delete_list = request.POST.getlist('check_box_list')
            print(delete_list)
            for item in delete_list:
                Location.objects.filter(name = item).delete()

    user_list_obj = Location.objects.all()
    return render(request, 'locations.html', {'locations':user_list_obj})

class patientModify(TemplateView):
    template_name = "patientmodify.html"

    def post(self, request, **kwargs):
        old_case_no = self.kwargs["case_no"]
        new_case_no = old_case_no
        if request.method == 'POST':
            new_case_no = request.POST['new_case_no']
            patient = Patient.objects.get(pk=old_case_no) 
            patient.name = request.POST['name'] 
            patient.id_document_no = request.POST['id_document_no']
            patient.date_of_birth = request.POST['date_of_birth']
            patient.date_of_confirmation = request.POST['date_of_confirmation']
            patient.case_no = new_case_no
            patient.save()
            Patient.objects.get(pk=old_case_no).delete()

            # modify all visiting records associated with patient to be changed
            changeList = VisitingRecord.objects.filter(case_no=old_case_no)
            for item in changeList:
                item.case_no = new_case_no
                item.save()
        return redirect('/patients/') 

    def get_context_data(self, **kwargs):
        case_no = self.kwargs['case_no']
        context = super().get_context_data(**kwargs)
        context['patient'] = Patient.objects.get(pk=case_no)
        return context


class recordModify(TemplateView):
    template_name = "recordmodify.html"

    def post(self, request, **kwargs):
        case_no = self.kwargs["case_no"]
        record_id = self.kwargs['record_id'] 
        if request.method == 'POST':
            record = VisitingRecord.objects.get(id=record_id)
            record.start_date = request.POST['start_date']
            record.end_date = request.POST['end_date']
            record.loc = Location.objects.get(name=request.POST['location'])
            record.save()

        return redirect('/patients/'+case_no) 

    def get_context_data(self, **kwargs):
        case_no = self.kwargs['case_no']
        record_id = self.kwargs['record_id']        
        context = super().get_context_data(**kwargs)
        context['patient'] = Patient.objects.get(case_no=case_no)
        context['locations'] = Location.objects.all()
        context['record'] = VisitingRecord.objects.get(id=record_id)
        return context

class locationModify(TemplateView):
    template_name = "locationmodify.html"

    def post(self, request, **kwargs):
        if request.method == 'POST':
            location_id = self.kwargs["location_id"]
            location = Location.objects.get(id=location_id)
            location.name = request.POST['name']
            location.x = request.POST['x']
            location.y = request.POST['y']
            location.address_line_1 = request.POST['address_line_1']
            location.address_line_2 = request.POST['address_line_2']
            location.address_line_3 = request.POST['address_line_3']
            location.category = request.POST['category']
            location.description = request.POST['description']
            location.district = request.POST['district']
            location.save()

        return redirect('/locations/') 

    def get_context_data(self, **kwargs):
        location_id = self.kwargs["location_id"]
        context = super().get_context_data(**kwargs)
        context['location'] = Location.objects.get(id=location_id)
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

            patients_no  = list(Location.objects.filter(Q(name__icontains=location)).filter(district = district_val).values_list("case_no", flat=True).distinct())
            print("patient no: ", patients_no)
            patients = Patient.objects.filter(pk__in=patients_no)
            for pa in patients:
                pa_visted = Location.objects.filter(Q(name__icontains=location)).filter(district = district_val).filter(case_no=pa)
                for pav in pa_visted:
                    start_date = pav.start_date - timedelta(days = int(window))
                    print("start: ",start_date)
                    print("start: ",type(start_date))
                    end_date = pav.start_date + timedelta(days = int(window))
                    print("end: ", end_date)
                    print("end: ", type(end_date))
                    covisited_start = Location.objects.filter(Q(name__icontains=location)).filter(district = district_val).filter(start_date__range=( start_date, end_date ) )
                    covisited_end = Location.objects.filter(Q(name__icontains=location)).filter(district = district_val).filter(end_date__range=( start_date, end_date ) )
                    # covisited_end = Location.objects.filter(Q(name__icontains=location)).filter(district = district_val).filter(start_date_range=[pav.end_date-timedelta( end_date_range=[pav.start_date-timedelta(days = int(window)), pav.start_date + timedelta(days = int(window))])
                    covisited = covisited_start | covisited_end
                    print("covisited: ",covisited)
                    # covisited = covisited_start.union(covisited_end)

                    for tmp in covisited:
                        print("tmp:", tmp.case_no.all())
                        if pa.case_no not in  connec:
                            connec[pa.case_no] = []
                        print("tmp.case_no:",tmp.case_no)
                        # print("tmp.case_no:",tmp.case_no==patients.Patient.None)
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
        # context["locations_visited"] = Location.objects.filter(case_no=case_no)
        return context
