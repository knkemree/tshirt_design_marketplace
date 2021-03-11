from django.urls import path
from . import views
app_name = 'payment'
urlpatterns = [
    path('process/', views.payment_process, name='process'),
    path('pay_for_credit/', views.pay_for_credit, name='pay_for_credit'),
    path('pay_order/<int:id>', views.pay_order, name='pay_order'),
    path('done/', views.payment_done, name='done'),
    path('pay_order_done/', views.pay_order_done, name='pay_order_done'),
    path('canceled/', views.payment_canceled, name='canceled'),
    path('credit_payment_failed/', views.credit_payment_failed, name='credit_payment_failed'),   
]
