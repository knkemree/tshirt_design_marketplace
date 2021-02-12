from django.urls import path
from . import views
from account.views import SellerDetailView, create_credit

app_name = 'account'
urlpatterns = [
    path('seller/<int:pk>/', SellerDetailView.as_view(), name='seller-detail'),
    path('create_credit/', create_credit, name='create_credit'),
]