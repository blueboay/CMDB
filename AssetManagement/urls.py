from django.urls import path
from AssetManagement import views

urlpatterns = [
    path('hostinfo', views.hostinfo),
    path('addhost', views.addhost),
]
