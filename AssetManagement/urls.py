from django.urls import path
from AssetManagement import views

urlpatterns = [
    path('hostInfo', views.host_info, name="hostInfo"),
    path('hostMoreInfo', views.host_more_info, name="hostMoreInfo"),
    path('hostENVInfo', views.host_environment_info, name="hostENVInfo"),
    path('hostGroupInfo', views.host_group_info, name="hostGroupInfo"),

    path('addHost', views.add_host, name="addHost"),
    path('addHostGroup', views.add_host_group, name="addHostGroup"),
    path('addHostENV', views.add_host_environment, name="addHostENV"),

    path('edit', views.edit, name="edit"),
    path('delete', views.delete, name="delete"),
    path('check', views.check, name="check"),

    path('changeHostENV', views.change_host_environment, name="changeHostENV"),
    path('changeHostGroup', views.change_host_group, name="changeHostGroup"),
    path('changeHostInfo', views.change_host_info, name="changeHostInfo"),
]
