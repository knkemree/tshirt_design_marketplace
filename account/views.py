from nameparser import HumanName
import stripe
import json
from decimal import Decimal
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.views.generic import DetailView
from django.views.generic.edit import UpdateView, FormView, CreateView
from django.shortcuts import render
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth import authenticate, login
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.http.response import HttpResponse, JsonResponse
from .tokens import account_activation_token
from .forms import UserAdminCreationForm, CustomAuthenticationForm, AuthenticationForm
from .models import Customer, Seller
from core.tasks import send_activation_email
from account.forms import UpdateCreditForm
from account.models import Credit




# Create your views here.
def signup(request):
    if request.user.is_authenticated:
        return redirect('/')
    data = {}
    if request.method == 'POST':
        login_form = CustomAuthenticationForm(request=request, data=request.POST)
        signup_form = UserAdminCreationForm(request.POST)
        # Extract values
        parsed_name = HumanName(request.POST.get('fullname'))
        if signup_form.is_valid():
            user = signup_form.save(commit=False)
            user.first_name = parsed_name.first
            user.last_name = parsed_name.last
            user.active = False
            user.buyer = True
            user.save()
            customer = Customer.objects.get(email=user.email)
            created_customer = stripe.Customer.create(
                description=user.email,
                email=user.email
            )
            customer.stripe_id = created_customer.id
            customer.save()
            current_site = get_current_site(request)
            subject = 'Activate Your Context Custom Account'
            message = render_to_string('account_activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            #send_activation_email.delay(user, subject, message)
            data['success'] = 'signedup'
            user.email_customer(subject, message)
            return JsonResponse(data)
            # return redirect('account_activation_sent')
        elif login_form.is_valid():
            username = login_form.cleaned_data.get('username')
            password = login_form.cleaned_data.get('password')
            remember_me = login_form.cleaned_data.get('remember_me')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                data['success'] = 'loggedin'
                if remember_me == False:
                    request.session.set_expiry(0)
                return JsonResponse(data)
                # return redirect('/')
            # elif user.is_active == False:
            #     messages.error(request, "Your account is not active.")
            else:
                data['error'] = login_form.errors
                messages.error(request, "User not found!")

        else:
            data['login_error'] = login_form.errors
            data['signup_error'] = signup_form.errors
            #messages.error(request, "None of the forms are valid!")
            return JsonResponse(data)
    else:
        signup_form = UserAdminCreationForm()
        login_form = CustomAuthenticationForm()
    return render(request, 'signup.html', {'signup_form': signup_form,'login_form':login_form})
    #return JsonResponse(data)

def account_activation_sent(request):
    return render(request, 'account_activation_sent.html')

def activated(request):
    #return render(request, 'home_page.html')
    return redirect('home')


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = Customer.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, Customer.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        #normlade Seller class'inda Onetoonefield kullanabilseydim burda for loop'a gerek kalmayacakti ve daha clean bir cozum olacakti.
        #eger seller kaydolduysa bunu uygula
        try:
            for i in user.creator.all():
                i.active = True
                i.email_confirmed = True
                i.save()
        except:
            pass
        
        # eger buyer kaydolduysa bunu uygula
        try:
            for i in user.shopper.all():
                i.active = True
                i.email_confirmed = True
                i.save()
        except:
            pass
        
        login(request, user)
        return redirect('activated')
    else:
        return render(request, 'account_activation_invalid.html')


def login_request(request):
    if request.user.is_authenticated:
        return redirect('/')
    data = {}
    if request.method == 'POST':
        login_form = CustomAuthenticationForm(request=request, data=request.POST)
        if login_form.is_valid():
            username = login_form.cleaned_data.get('username')
            password = login_form.cleaned_data.get('password')
            remember_me = login_form.cleaned_data.get('remember_me')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                data['success'] = 'loggedin'
                if remember_me == False:
                    request.session.set_expiry(0)
                return JsonResponse(data)
                # return redirect('/')
            elif user.is_active == False:
                messages.error(request, "Your account is not active.")
            else:
                data['error'] = login_form.errors
                messages.error(request, "Invalid username or password.")
        else:
            
            data['error'] = login_form.errors
            messages.error(request, "Invalid username or password.")
    else:
        login_form = CustomAuthenticationForm()
    return JsonResponse(data)
    
    # return render(request = request,
    #                 template_name = "registration/login.html",
    #                 context={'login_form':login_form,})

@login_required(login_url='/signup/')
def create_credit(request):
    form =  UpdateCreditForm()
    seller_email = get_object_or_404(Seller, seller_id=request.user.id)
    orders = seller_email.orders.all()

    recommeded_upload_amount = 0
    total_of_unpaid_orders = 0
    for order in orders:
        #exclude canceled orders
        if order.paid == False and order.status != '4' :
            total_of_unpaid_orders += order.total

    if seller_email.credit:
        if seller_email.credit > total_of_unpaid_orders:
            recommeded_upload_amount = 0
        else:
            recommeded_upload_amount = total_of_unpaid_orders - seller_email.credit 
    else:
        print(total_of_unpaid_orders, 'odenmemis')
        recommeded_upload_amount = total_of_unpaid_orders

    if request.method == 'POST':
        form = UpdateCreditForm(request.POST)
        if form.is_valid():
            amount = form.cleaned_data['amount']
            request.session['amount'] = str(amount) # I had to convert it to str to make it JSOn serializable
            return redirect(reverse('payment:pay_for_credit'))
    else:
        context = {'form':form, 'orders':orders, 'total_of_unpaid_orders':total_of_unpaid_orders, 'recommeded_upload_amount':recommeded_upload_amount}
        return render(request, 'credit_form.html', context)
            


class SellerDetailView(DetailView):

    queryset = Seller.objects.all()

    def get_object(self):
        obj = super().get_object()
        # Record the last accessed date
        # obj.last_accessed = timezone.now()
        # obj.save()
        return obj
  
class CreditUpdateFormView(FormView): 
    # specify the Form you want to use 
    form_class = UpdateCreditForm 
      
    # sepcify name of template 
    template_name = "account / seller_credit_update_form.html"
  
    # can specify success url 
    # url to redirect after successfully 
    # updating details 
    success_url ="/thanks/"