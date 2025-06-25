# accounts/urls.py

from django.urls import path
from .views import AppleLoginView, CheckUserExistView, GoogleLoginView, RegisterView, OTPVerifyView, LoginView, UserProfileView
from rest_framework_simplejwt.views import TokenRefreshView
from django.urls import path, include


urlpatterns = [
    path('grappelli/', include('grappelli.urls')),  # grappelli URLS
    path('register', RegisterView.as_view(), name='register'),
    path('verify-otp', OTPVerifyView.as_view(), name='verify-otp'),
    path('login', LoginView.as_view(), name='login'),
    path('token/refresh', TokenRefreshView.as_view(), name='token_refresh'),
    path('profile', UserProfileView.as_view(), name='user-profile'),
    path('google-login', GoogleLoginView.as_view(), name='google-login'),
    path('apple-login', AppleLoginView.as_view(), name='apple-login'),
    path('check-user-exist', CheckUserExistView.as_view(), name='check-user-exist'),
]
