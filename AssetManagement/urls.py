from django.urls import path
from AssetManagement import views

urlpatterns = [
    path('hostinfo', views.hostinfo),
    path('envgroup', views.envgroup),
    path('hostgroup', views.hostgroup),

    path('addhost', views.addhost),
    path('addhostgroup', views.addhostgroup),
    path('addenvgroup', views.addenvgroup),

    path('edit', views.edit),
    path('del', views.delhost),

    path('changeenvgroup', views.changeenvgroup),
    path('changehostgroup', views.changehostgroup),
]
