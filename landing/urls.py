from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='landing'),  # root URL untuk landing page
]
