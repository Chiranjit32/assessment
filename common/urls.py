from django.urls import path, re_path
from . import views

urlpatterns = [
    re_path(r'^$', views.home, name='home'),
    path('signup/', views.signup, name='signup'),
    path('signin/', views.signin, name='signin'),
    path('signout/', views.signout, name='signout'),
    path('add_ip/<int:user_id>/', views.addIp, name='addIp'),
    path('dashboard/', views.dashboard, name='dashboard'),
]