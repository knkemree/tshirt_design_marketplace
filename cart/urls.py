from django.urls import path
from . import views
app_name = 'cart'

urlpatterns = [
    path('', views.cart_detail, name='cart_detail'),
    #path('add/', views.cart_add, name='cart_add'),
    path('add/<int:variant_id>/', views.cart_add, name='cart_add'),
    path('remove/<int:variant_id>/', views.cart_remove, name='cart_remove'),
]
