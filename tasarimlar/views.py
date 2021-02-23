import os

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.views.generic.edit import FormMixin
from django.urls import reverse

from cart.cart import Cart
from cart.forms import CartAddProductForm

from tasarimlar.models import Design


# Create your views here.
class DesignListView(ListView):
    template_name = 'mockup_list.html' #default ta da zatem boyle aslinda silinse olur ama sildim calismadi
    queryset = Design.activated.all()
    context_object_name = 'designs'
    #paginate_by = 45
    ordering = ['-created_at']

    #In case you want to filter the queryset differently for different web requests
    #queryset'i silve asagidakini yaz
    # def get_queryset(self):
    #     return Mockup.objects.filter(brand='gildan')

    # def get_context_data(self, *args, **kwargs):
	# 	context = super(MockupListView, self).get_context_data(*args, **kwargs)
	# 	context['mockups'] = Mockup.objects.filter(active=1)
	# 	return context

class DesignDetailView(LoginRequiredMixin, FormMixin, DetailView):
    login_url = '/signup/'
    template_name= 'tasarimlar/design_detail.html'
    model = Design
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
    context_object_name="design" # bunu yazmasan {{ object }} yazinca oluyor
    queryset = Design.activated.all()
    form_class = CartAddProductForm

    def get_success_url(self):
        return reverse('cart:cart_detail')

    def get_context_data(self, **kwargs):
        context = super(DesignDetailView, self).get_context_data(**kwargs)
        context['form'] = CartAddProductForm(initial={'quantity': 1})
        return context

    def post(self, request, *args, **kwargs):
        cart = Cart(request)
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            cd = form.cleaned_data
            cart.add_design(
                instance_pk = self.object.pk,
                quantity=cd['quantity'],
                
            )
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self,  form):
        return super(DesignDetailView, self).form_valid(form)
    #daha komplike birsey yazilacaksa asagidaki gibi birsey olabilir
    # def get_queryset(self):
	# 	if self.request.user.is_authenticated:
	# 		return Book.objects.filter(is_published=True, user=self.request.user)
	# 	else:
	# 		return Book.objects.none()

    # override context data 
    # def get_context_data(self, *args, **kwargs): 
    #     context = super(DesignDetailView, self).get_context_data(*args, **kwargs) 
    #     # add extra field  
    #     context["thumbnails"] = 
    #     return context 

