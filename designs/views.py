import os
from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Design
from django.http import HttpResponse

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

class DesignDetailView(DetailView):
    model = Design
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
    context_object_name="design" # bunu yazmasan {{ object }} yazinca oluyor
    queryset = Design.activated.all()


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