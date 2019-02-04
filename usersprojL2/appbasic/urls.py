from django.urls import path
from appbasic import views

app_name = 'appbasic'
urlpatterns = [
    path('', views.registerView, name='register'),
    path('login/', views.loginView, name='login_site'),
]
