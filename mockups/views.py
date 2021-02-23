import os
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView
from .models import Mockup
from django.http import HttpResponse

# Create your views here.
class MockupListView(LoginRequiredMixin, ListView):
    login_url = '/signup/'
    template_name = 'mockup_list.html' #default ta da zatem boyle aslinda silinse olur ama sildim calismadi
    queryset = Mockup.activated.all()
    context_object_name = 'mockups'
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

class MockupDetailView(LoginRequiredMixin, DetailView):
    login_url = '/signup/'
    model = Mockup
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
    context_object_name="mockup" # bunu yazmasan {{ object }} yazinca oluyor
    queryset = Mockup.activated.all()


    #daha komplike birsey yazilacaksa asagidaki gibi birsey olabilir
    # def get_queryset(self):
	# 	if self.request.user.is_authenticated:
	# 		return Book.objects.filter(is_published=True, user=self.request.user)
	# 	else:
	# 		return Book.objects.none()

    # override context data 
    # def get_context_data(self, *args, **kwargs): 
    #     context = super(GeeksDetailView, 
    #          self).get_context_data(*args, **kwargs) 
    #     # add extra field  
    #     context["category"] = "MISC"        
    #     return context 

def mockup_download(request, id):
    mockup = Mockup.objects.get(id=id)
    fsock = open(mockup.image.path,'rb').read()
    response = HttpResponse(fsock, content_type='image/*')
    file_name, file_extension = os.path.splitext(mockup.image.path)
    response['Content-Disposition'] = 'attachment;'+ 'filename={}{}'.format(mockup.slug, file_extension)
    return response