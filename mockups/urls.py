from django.urls import path, include
from . import views
from mockups.views import MockupDetailView, MockupListView, mockup_download


app_name = "mockups"

urlpatterns = [
    #path('', views.index, name='index'),
    path('', MockupListView.as_view(), name='mockup-list'),
    path('<slug>/', MockupDetailView.as_view(), name='mockup-detail'),
    path('download/<int:id>/', mockup_download, name='mockup-download')
    
]