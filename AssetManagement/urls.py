from django.urls import path
from AssetManagement import views

urlpatterns = [
    path('hostinfo', views.hostinfo),
    path('addhost', views.addhost),
    path('envgroup', views.envgroup),
    path('hostgroup', views.hostgroup),
    path('addhostgroup', views.addhostgroup),
    path('addenvgroup', views.addenvgroup),
    path('edit', views.edithost),
    path('del', views.delhost),
]
