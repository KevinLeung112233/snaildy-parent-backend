# accounts/urls.py

from django.urls import path
from .views import RegisterView, OTPVerifyView, LoginView, BindStudentView, UserProfileView
from rest_framework_simplejwt.views import TokenRefreshView
from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('grappelli/', include('grappelli.urls')),  # grappelli URLS
    path('register/', RegisterView.as_view(), name='register'),
    path('verify-otp/', OTPVerifyView.as_view(), name='verify-otp'),
    path('login/', LoginView.as_view(), name='login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('bind-student/', BindStudentView.as_view(), name='bind_student'),
    path('profile/', UserProfileView.as_view(), name='user-profile'),

]
