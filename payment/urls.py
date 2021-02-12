from django.urls import path
from . import views
app_name = 'payment'
urlpatterns = [
    path('process/', views.payment_process, name='process'),
    path('pay_for_credit/', views.pay_for_credit, name='pay_for_credit'),
    path('pay_order/<int:id>', views.pay_order, name='pay_order'),
    path('done/', views.payment_done, name='done'),
    path('canceled/', views.payment_canceled, name='canceled'),
]
