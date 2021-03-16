from django.urls import path
from . import views
app_name = 'cart'

urlpatterns = [
    path('', views.cart_detail, name='cart_detail'),
    path('clear/', views.cart_clear, name='cart_clear'),
    #path('add/', views.cart_add, name='cart_add'),
    path('add/<int:variant_id>/', views.cart_add, name='cart_add'),
    path('add/<int:variant_id>/<int:art_id>/', views.cart_add, name='cart_update'),
    path('remove/<uuid:uuid>/', views.cart_remove, name='cart_remove'),
    path('remove_digital/<uuid:pk>/', views.cart_remove_design_for_sale, name='cart_remove_design_for_sale'),
    path('add_blank/<uuid:uuid>/', views.cart_add_blank, name='cart_add_blank'),
    
]
