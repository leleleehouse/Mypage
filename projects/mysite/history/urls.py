from django.urls import path
from . import views

app_name = 'history'

urlpatterns = [
    path('', views.history, name = 'history'),
]


