from django.urls import path, re_path

from sms import views

urlpatterns = [
    re_path('prod', views.prod, name="prod"),
]
