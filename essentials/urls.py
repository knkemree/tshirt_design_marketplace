from django.urls import path, include
from .views import SellerProductListView
from . import views
from essentials.api.views import products_list

app_name = "essentials"

urlpatterns = [
    path('', views.product_list, name='product_list'),
    path('api/', products_list, name='list'),
    path('ajax/change_place/', views.change_place, name='change_place'),
    path('ajax/change_method/', views.change_method, name='change_method'),
    path('design/', views.product_design, name='product_design'),
    path('vendor/products/', SellerProductListView.as_view(), name='seller_product_catalog'),
    path('<slug:category_slug>/', views.product_list, name='product_list_by_category'),
    path('<int:id>/<slug:slug>/', views.product_detail, name='product_detail'),
    
    
]



