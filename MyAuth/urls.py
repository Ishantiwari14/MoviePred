from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
urlpatterns = [
    path('user/profile/', views.user_profile, name='user_profile'),
    path('register/', views.register, name='register'),
    path('change/password/', views.change_password, name='change_password'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    # Add other URLs as needed
]
