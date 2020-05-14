from django.shortcuts import render
from django.shortcuts import redirect
from django.views.generic import TemplateView
from patients.models import Patient, Location, VisitingRecord
from django.db.models import Q
from datetime import datetime, timedelta 

from django.template.defaulttags import register

from django.contrib.auth.decorators import login_required, user_passes_test

from django.contrib.auth.mixins import LoginRequiredMixin

from django.contrib.auth.mixins import UserPassesTestMixin

from django.contrib.auth import get_user_model
User = get_user_model()


@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)

# Create your views here.


class PatientProfile(LoginRequiredMixin, TemplateView):
    # @login_required
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


@login_required
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

@login_required
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

class patientModify(LoginRequiredMixin, TemplateView):
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


class recordModify(LoginRequiredMixin, TemplateView):
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

class locationModify(LoginRequiredMixin, TemplateView):
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

def epidemiologists(user):
    if user.user_type == 2 or user.is_superuser or user.is_staff:
        return True
    return False

class SearchPage(UserPassesTestMixin, LoginRequiredMixin, TemplateView):
    template_name = "search.html"

    def test_func(self):
        # print("UserDir: ", dir(self.request.user))
        if self.request.user.is_authenticated:
            if self.request.user.user_type == 2 or self.request.user.is_superuser or self.request.user.is_staff:
                return True
        return False
    def handle_no_permission(self):
        return redirect('denied')
    
    # @user_passes_test(epidemiologists, login_url='denied/')
    def get_context_data(self, **kwargs):
        # case_no = self.kwargs["case_no"]

        key_patient = self.request.GET.get('key_patient')
        window = self.request.GET.get('window')
        patients = set()
        connec = {}
        if key_patient and window:
            vrecords = VisitingRecord.objects.filter(case_no = key_patient)
           #print(vrecords)
            for v in vrecords:
                all_visit = VisitingRecord.objects.filter(loc = v.loc)
                s_date = v.start_date - timedelta(days = int(window))
               #print("s: ",s_date)
               #print("s: ",type(s_date))
                e_date = v.start_date + timedelta(days = int(window))
               #print("e: ", e_date)
               #print("e: ", type(e_date))
                for av in all_visit:
                    if (av.case_no == v.case_no):
                        continue
                    as_date = av.start_date
                    ae_date = av.end_date
                    if (not ((s_date < e_date < as_date < ae_date) or (as_date < ae_date < s_date < e_date))):
                        patients.add(Patient.objects.get(case_no = av.case_no))
                        if av.case_no not in  connec:
                            connec[av.case_no] = []
                       #print("av.case_no:",av.case_no)
                       #print("tmp.case_no:",tmp.case_no==patients.Patient.None)
                        connec[av.case_no].append([
                            av.case_no,
                            Patient.objects.get(case_no = av.case_no).name,
                            Patient.objects.get(case_no = av.case_no).date_of_confirmation,
                            Location.objects.get(name = av.loc).name,
                            str(as_date) + '---' + str(ae_date),
                           #Location.objects.get(name = v.loc).name,
                            str(v.start_date) + '---' + str(v.end_date),
                            ""
                            ])
        context = super().get_context_data(**kwargs)
        context["patients"] = patients
        context["allpatients"] = Patient.objects.all()
        if (key_patient):
            context["key_patient"] = Patient.objects.get(case_no = key_patient)
        print("connec:",connec)
        context["connec"] = connec
        context["window"] = window
        # context["locations_visited"] = Location.objects.filter(case_no=case_no)
        return context

from django.contrib import messages
from django.contrib.auth import login, authenticate, REDIRECT_FIELD_NAME
from django.contrib.auth.tokens import default_token_generator
# from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import (
    LogoutView as BaseLogoutView, PasswordChangeView as BasePasswordChangeView,
    PasswordResetDoneView as BasePasswordResetDoneView, PasswordResetConfirmView as BasePasswordResetConfirmView,
)
from django.shortcuts import get_object_or_404, redirect
from django.utils.crypto import get_random_string
from django.utils.decorators import method_decorator
from django.utils.http import is_safe_url
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.utils.translation import gettext_lazy as _
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters
from django.views.generic import View, FormView
from django.conf import settings


from .forms import (
    SignInViaUsernameForm
)
# from .models import Activation


class GuestOnlyView(View):
    def dispatch(self, request, *args, **kwargs):
        # Redirect to the index page if the user already authenticated
        if request.user.is_authenticated:
            return redirect(settings.LOGIN_REDIRECT_URL)

        return super().dispatch(request, *args, **kwargs)


class LogInView(GuestOnlyView, FormView):
    template_name = 'login.html'

    @staticmethod
    def get_form_class(**kwargs):
        # if settings.DISABLE_USERNAME or settings.LOGIN_VIA_EMAIL:
        #     return SignInViaEmailForm

        # if settings.LOGIN_VIA_EMAIL_OR_USERNAME:
        #     return SignInViaEmailOrUsernameForm

        return SignInViaUsernameForm

    @method_decorator(sensitive_post_parameters('password'))
    @method_decorator(csrf_protect)
    @method_decorator(never_cache)
    def dispatch(self, request, *args, **kwargs):
        # Sets a test cookie to make sure the user has cookies enabled
        request.session.set_test_cookie()

        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        request = self.request

        # If the test cookie worked, go ahead and delete it since its no longer needed
        if request.session.test_cookie_worked():
            request.session.delete_test_cookie()

        # The default Django's "remember me" lifetime is 2 weeks and can be changed by modifying
        # the SESSION_COOKIE_AGE settings' option.
        if settings.USE_REMEMBER_ME:
            if not form.cleaned_data['remember_me']:
                request.session.set_expiry(0)

        login(request, form.user_cache)

        redirect_to = request.POST.get(REDIRECT_FIELD_NAME, request.GET.get(REDIRECT_FIELD_NAME))
        url_is_safe = is_safe_url(redirect_to, allowed_hosts=request.get_host(), require_https=request.is_secure())

        if url_is_safe:
            return redirect(redirect_to)

        return redirect(settings.LOGIN_REDIRECT_URL)

class LogOutView(LoginRequiredMixin, BaseLogoutView):
    template_name = 'logout.html'    


class DeniedView(TemplateView):
    template_name = "denied.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context