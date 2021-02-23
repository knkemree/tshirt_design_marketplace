from django.urls import path
from . import views
from orders.views import DownloadsListView, design_download

app_name = 'orders'
urlpatterns = [
    path('order/', views.order_list, name='order_list'),
    #path('order/<int:order_id>/', views.order_detail, name='order_detail'),
    path('create/', views.order_create, name='order_create'),
    path('cancel/<int:order_id>/', views.order_cancel, name='order_cancel'),
    path('admin/order/<int:order_id>/', views.admin_order_detail, name='admin_order_detail'),
    path('admin/orderitem/<int:order_id>/', views.admin_order_item_detail, name='admin_order_item_detail'),
    path('admin/order/<int:order_id>/pdf/',views.admin_order_pdf,name='admin_order_pdf'),
    path('downloads/', DownloadsListView.as_view(), name='downloads-list'),
    path('download/<uuid:pk>/', design_download, name='design-download')
]