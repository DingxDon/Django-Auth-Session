from django.urls import path
from .views import  RegistrationView, ActivateView, ActivationConfirm, GetCSRFToken, LoginView, LogoutView, UserDetailView, ChangePasswordView, DeleteView, ResetPasswordEmailView, ResetPasswordView, ResetPasswordConfirmView

urlpatterns = [
    path('accounts/csrf_token/', GetCSRFToken.as_view(), name='csrf_cookie'),
    path('accounts/registration/', RegistrationView.as_view(), name='registration'),
    path('accounts/activate/<str:uid>/<str:token>/', ActivateView.as_view(), name='activate'),
    path('accounts/activate/', ActivationConfirm.as_view(), name='activation_confirm'),
    path('accounts/login/', LoginView.as_view(), name='login'),
    path('accounts/user/', UserDetailView.as_view(), name='user_detail'),
    path('accounts/change_password/', ChangePasswordView.as_view(), name='change_password'),
    path('accounts/reset_password/<str:uid>/<str:token>/', ResetPasswordView.as_view(), name='reset_password'),
    path('accounts/reset_password_confirm/<str:uid>/<str:token>/', ResetPasswordConfirmView.as_view(), name='reset_password_confirm'),
    path('accounts/reset_password/', ResetPasswordEmailView.as_view(), name='reset_password_email'),
    path('accounts/logout/', LogoutView.as_view(), name='logout'),
    path('accounts/delete/', DeleteView.as_view(), name='delete'),
    
    
    
    
    
    
    
    
]
