from django.shortcuts import redirect, render
from django.views.generic import TemplateView
from django.contrib import messages
from account.forms import UserAdminCreationForm
from account.models import Customer
from django.contrib.auth.forms import AuthenticationForm

class HomeView(TemplateView):
    template_name = 'home_page.html'

def home_page(request):
    context = {
        
    }
    return render(request, "home_page.html", context)


def how_it_works(request):
    context = {}
    return render(request, 'how_it_works.html', context)

def test(request):
    context = {}
    return render(request,'test.html', context)
    
