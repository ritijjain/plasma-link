from django.http.response import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic.edit import CreateView, FormView
from .models import Donor
from django.views.generic.base import TemplateView
from .forms import RegisterDonorForm, FindDonorForm
from django.core.paginator import Paginator

class RegisterDonor(FormView):
    template_name = 'plasma_link/register_donor.html'
    form_class = RegisterDonorForm
    success_url = '/'

    def form_valid(self, form):
        return super().form_valid(form)

def FindDonor(request):
    context = {}

    dataset = Donor.objects.filter().order_by('-hits')

    if request.method == 'POST':
        form = FindDonorForm(request.POST)
        if form.is_valid():
            pass
            # return HttpResponseRedirect('/thanks/')
    else:
        form = FindDonorForm()

    context['dataset'] = dataset

    # Paginator
    paginator = Paginator(dataset, 25) 
    page_obj = paginator.get_page(request.GET.get('page'))
    context['page_obj'] = page_obj

    
    return render(request, 'plasma_link/find_donor.html', context)


