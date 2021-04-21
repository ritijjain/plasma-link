from django.shortcuts import render
from django.views.generic.edit import CreateView, FormView
from .models import Donor
from django.views.generic.base import TemplateView
from .forms import CreateDonorForm

class DonorCreateView(FormView):
    template_name = 'plasma_link/register_donor.html'
    form_class = CreateDonorForm
    success_url = '/'

    def form_valid(self, form):
        return super().form_valid(form)

class DonorListView(TemplateView):
    template_name = 'plasma_link/donor_list.html'

    def get(self, request, *args, **kwargs):
        pass
        return render(request, self.template_name, self.get_context_data())
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

