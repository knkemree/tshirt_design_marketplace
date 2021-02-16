from django.urls import path, include
from .views import SellerProductListView
from . import views
from essentials.api.views import products_list

app_name = "essentials"

urlpatterns = [
    path('', views.product_list, name='product_list'),
    path('search/', views.post_search, name='post_search'),
    path('api/', products_list, name='list'),
    path('ajax/change_size', views.change_size, name='change_size'),
    path('ajax/change_place/', views.change_place, name='change_place'),
    path('ajax/dynamic_canvas', views.dynamic_canvas, name='dynamic_canvas'),
    path('ajax/change_method/', views.change_method, name='change_method'),
    path('ajax/change_color/', views.change_color, name='change_color'),
    path('ajax/get_current_variant/', views.get_current_variant, name='get_current_variant'),
    path('<slug:parent_category>/<slug:subcategory>/<int:id>/<slug:slug>/', views.blank_single_item, name='blank_single_item_two_cats'),
    path('<slug:subcategory>/<int:id>/<slug:slug>/', views.blank_single_item, name='blank_single_item_one_cat'),
    path('<int:id>/<slug:slug>/', views.blank_single_item, name='blank_single_item'),
    path('design/', views.product_design, name='product_design'),
    path('vendor/products/', SellerProductListView.as_view(), name='seller_product_catalog'),
    path('<slug:category_slug>/', views.product_list, name='product_list_by_category'),
    path('<int:id>/<slug:slug>/', views.product_detail, name='product_detail'),
    
    
]



