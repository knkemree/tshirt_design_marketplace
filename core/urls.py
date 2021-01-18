"""core URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))

"""
import debug_toolbar
from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LoginView
from django.contrib.auth import views as auth_views
from .views import HomeView, home_page
from account.views import signup, account_activation_sent, activate, activated, login_request
from core.views import how_it_works
from essentials import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path("", home_page, name='home'),
    path('signup/', signup, name='signup'),
    path('account_activation_sent/', account_activation_sent, name='account_activation_sent'),
    path('activate/<slug:uidb64>/<slug:token>/', activate, name='activate'),
    path('activated/', activated, name='activated'),
    #path('login/', auth_views.LoginView.as_view(redirect_authenticated_user=True), name='login'),
    path('login/', login_request, name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('password_change/', auth_views.PasswordChangeView.as_view(),name='password_change'),
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(), name='password_change_done'),
    # path("register/", register_page, name="register"),
    # path('dashboard/', dashboard, name='dashboard'),
    # path('dashboard/order/<int:order_id>/', order_details, name='order_details'),
    # path('dashboard/allow_change_password/', change_password, name='allow_change_password'),
    #reset password urls
    path('password_reset/',auth_views.PasswordResetView.as_view(),name='password_reset'),
    path('password_reset/done/',auth_views.PasswordResetDoneView.as_view(),name='password_reset_done'),
    path('reset/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(),name='password_reset_confirm'),
    path('reset/done/',auth_views.PasswordResetCompleteView.as_view(),name='password_reset_complete'),
    path('how_it_works/', how_it_works, name='how_it_works'),
    path('cart/', include('cart.urls', namespace='cart')),
    path('orders/', include('orders.urls', namespace='orders')),
    path('payment/', include('payment.urls', namespace='payment')),
    path('coupons/', include('coupons.urls', namespace='coupons')),
    path('essentials/', include("essentials.urls"), name="essentials"),
    path('ajaxcolor/', views.ajaxcolor, name='ajaxcolor'),
    path('__debug__/', include(debug_toolbar.urls)),   
]

if settings.DEBUG == True:
    urlpatterns = urlpatterns + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

admin.site.site_header = "Context Custom Admin"
admin.site.site_title = "Context Custom Admin Portal"
admin.site.index_title = "Contol Panel"

