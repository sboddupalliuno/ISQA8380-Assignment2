from django.conf.urls import url
from . import views
from django.urls import path, register_converter
from rest_framework.urlpatterns import format_suffix_patterns
from . import converter
# from .views import PasswordResetConfirmView,ChangePasswordResetDoneSuccessView, ChangePasswordResetDoneView,PasswordResetView,PasswordResetCompleteView, PasswordResetDoneView, PasswordResetConfirmView

register_converter(converter.FloatUrlParameterConverter, 'float')
app_name = 'portfolio'
urlpatterns = [
    path('', views.home, name='home'),
    url(r'^home/$', views.home, name='home'),
    path('customer/new/', views.customer_new, name='customer_new'),
    path('customer_list', views.customer_list, name='customer_list'),
    path('customer/<int:pk>/edit/', views.customer_edit, name='customer_edit'),
    path('customer/<int:pk>/delete/', views.customer_delete, name='customer_delete'),
    path('stock_list', views.stock_list, name='stock_list'),
    path('stock/<int:pk>/edit/', views.stock_edit, name='stock_edit'),
    path('stock/<int:pk>/delete/', views.stock_delete, name='stock_delete'),
    path('stock/new/', views.stock_new, name='stock_new'),
    path('investment_list', views.investment_list, name='investment_list'),
    path('investment/<int:pk>/edit/', views.investment_edit, name='investment_edit'),
    path('investment/<int:pk>/delete/', views.investment_delete, name='investment_delete'),
    path('investment/new/', views.investment_new, name='investment_new'),
    path('customer/<int:pk>/portfolio/', views.portfolio, name='portfolio'),
    url(r'^customers_json/', views.CustomerList.as_view()),
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('accountpreferences/', views.CustomUserChangeForm, name='accountpreferences'),
    path('reset_confirmation/<uidb64>/<token>', views.PasswordResetConfirmView.as_view(), name='reset_password_confirmation'),
    path('reset_password/', views.PasswordResetView.as_view(), name='reset_password'),
    path('reset_password/done/', views.PasswordResetDoneView.as_view(), name='reset_password_done'),
    path('reset/done/', views.PasswordResetCompleteView.as_view(), name='reset_password_complete'),
    path('password_change/', views.ChangePasswordResetDoneView.as_view(), name='password_change'),
    path('password/', views.ChangePasswordResetDoneView.as_view(), name='password'),
    path('change_password_done/', views.ChangePasswordResetDoneSuccessView.as_view(), name='change_password_done'),
    path('account_profile', views.account_profile, name='account_profile'),
    path('account_profile_edit/<int:pk>', views.account_profile_edit, name='account_profile_edit'),
    path(r'broadcast/<int:pk>/<str:phonenumber>/<float:initalstock>/<float:currentstock>/<float:initalinvestment>/<float:currentinvestment>/send/', views.broadcast_sms, name="broadcast"),
    path('sendpdfEmail/<int:pk>/portfolio/', views.sendpdfEmail, name='sendpdfEmail'),
    path('downloadPDF/<int:pk>/portfolio/', views.downloadPDF, name='downloadPDF'),
    path('customer/<int:pk>/', views.CustomerByNumber.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)