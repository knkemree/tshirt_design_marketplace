from django.urls import path, include
from . import views
from designs.views import DesignDetailView, DesignListView


app_name = "designs"

urlpatterns = [
    path('', DesignListView.as_view(), name='design-list'),
    path('<slug>/', DesignDetailView.as_view(), name='design-detail'),
    #path('download/<int:id>/', mockup_download, name='mockup-download')
    
]