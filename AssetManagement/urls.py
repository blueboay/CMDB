from django.urls import path
from AssetManagement import views

urlpatterns = [
    path('hostInfo', views.hostInfo, name="hostInfo"),
    path('hostMoreInfo', views.hostMoreInfo, name="hostMoreInfo"),
    path('hostENVInfo', views.hostENVInfo, name="hostENVInfo"),
    path('hostGroupInfo', views.hostGroupInfo, name="hostGroupInfo"),

    path('addHost', views.addHost, name="addHost"),
    path('addHostGroup', views.addHostGroup, name="addHostGroup"),
    path('addHostENV', views.addHostENV, name="addHostENV"),

    path('edit', views.edit, name="edit"),
    path('delete', views.delete, name="delete"),
    path('search', views.search, name="search"),

    path('changeHostENV', views.changeHostENV, name="changeHostENV"),
    path('changeHostGroup', views.changeHostGroup, name="changeHostGroup"),
    path('changeHostInfo', views.changeHostInfo, name="changeHostInfo"),
]
