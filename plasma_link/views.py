from django.http.response import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.views.generic.edit import CreateView, FormView
from .models import Donor
from django.views.generic.base import TemplateView
from .forms import RegisterDonorForm, FindDonorForm, Verify
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from g_recaptcha.validate_recaptcha import validate_captcha
from django.conf import settings
from django.db.models import IntegerField, Value

class AboutView(TemplateView):
    template_name = 'plasma_link/about.html'

class RegisterDonor(LoginRequiredMixin, CreateView):
    template_name = 'plasma_link/register_donor.html'
    form_class = RegisterDonorForm
    success_url = reverse_lazy('find_donor')

    def form_valid(self, form):
        self.donor = form.save()
        self.donor.user = self.request.user
        self.donor.process_lat_lon()
        self.donor.save()
        return HttpResponseRedirect(self.get_success_url())
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if Donor.objects.filter(user=self.request.user).exists():
            context['already_registered_donor'] = Donor.objects.filter(user=self.request.user)[0]
        context['labels'] = {'button_text': 'Register as a Donor'}
        return context
    
    def get_success_url(self):
        return self.success_url
    
def FindDonor(request):
    context = {}

    dataset = Donor.objects.all().order_by('-views')

    if request.method == 'POST':
        form = FindDonorForm(request.POST)
        if form.is_valid():
            location = form.cleaned_data['search_location'].split(',')

            dataset = dataset.filter(latitude__gt=float(
                location[0])-1, latitude__lt=float(location[0])+1,
                longitude__gt=float(location[1])-1, longitude__lt=float(location[1])+1,
                blood_group=form.cleaned_data['blood_group']) 

            for obj in dataset:
                obj.distance = round(obj.calc_distance(float(location[0]), float(location[1]))) + 1

            dataset = sorted(dataset, key= lambda obj: (obj.distance*.6 + obj.views*0.4))
                        
    else:
        form = FindDonorForm()
    context['form'] = form

    context['dataset'] = dataset

    # Paginator
    paginator = Paginator(dataset, 10) 
    page_obj = paginator.get_page(request.GET.get('page'))
    context['page_obj'] = page_obj

    context['labels']= {'button_text': 'Refresh'}
    return render(request, 'plasma_link/find_donor.html', context)

@validate_captcha
def donor_detail(request, pk):
    context = {}
    donor = get_object_or_404(Donor, pk=pk)

    if request.method == 'POST':
        form = Verify(request.POST)
        if form.is_valid():
            donor.views += 1
            donor.save()
            context['secret'] = donor.phone
    else:
        form = Verify()
    context['form'] = form

    context['donor'] = donor
    context['GOOGLE_RECAPTCHA_SITE_KEY'] = settings.GOOGLE_RECAPTCHA_SITE_KEY
    return render(request, 'plasma_link/donor_detail.html', context)
