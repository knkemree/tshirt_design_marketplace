from django.urls import path, include
from .views import SellerProductListView
from . import views
from essentials.api.views import products_list

app_name = "essentials"

urlpatterns = [
    path('api/', products_list, name='list'),
    path('', views.product_list, name='product_list'),
    path('vendor/products/', SellerProductListView.as_view(), name='seller_product_catalog'),
    path('<slug:category_slug>/', views.product_list, name='product_list_by_category'),
    path('<int:id>/<slug:slug>/', views.product_detail, name='product_detail'),
    
]



