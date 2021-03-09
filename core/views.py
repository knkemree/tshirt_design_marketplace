from django.shortcuts import redirect, render
from django.views.generic import TemplateView
from django.contrib import messages
from account.forms import UserAdminCreationForm
from account.models import Customer
from django.contrib.auth.forms import AuthenticationForm
from essentials.models import Product

class HomeView(TemplateView):
    template_name = 'home_page.html'

def home_page(request):
    latest_products = Product.objects.filter(active=True).order_by('-created_at')[:4]
    context = {
        'latest_products':latest_products
    }
    return render(request, "home_page.html", context)


def how_it_works(request):
    context = {}
    return render(request, 'how_it_works.html', context)

def test(request):
    context = {}
    return render(request,'test.html', context)

def free_mockup(request):
    context = {}
    return render(request, 'free_mockup.html', context)
    
