# pendaftaran/urls.py
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.register, name="register"),
    path('utama/', views.home, name="utama"),
    path('login/', auth_views.LoginView.as_view(template_name="pendaftaran/login.html"), name="login"),
    path("logout/", views.logout_user, name="logout"),
    path('berkas/', views.upload_berkas, name='upload_berkas'),
    path('sukses/', views.sukses_upload, name='sukses_upload'),
]
