from django.urls import path
from AssetManagement import views

urlpatterns = [
    path('host_info', views.host_info, name="hostInfo"),
    path('host_more_info', views.host_more_info, name="hostMoreInfo"),
    path('host_environment_info', views.host_environment_info, name="hostENVInfo"),
    path('host_group_info', views.host_group_info, name="hostGroupInfo"),
    path('network_device_info', views.network_device_info, name="network_device_info"),

    path('add_host', views.add_host, name="addHost"),
    path('add_host_group', views.add_host_group, name="addHostGroup"),
    path('add_host_environment', views.add_host_environment, name="addHostENV"),

    path('edit', views.edit, name="edit"),
    path('delete', views.delete, name="delete"),
    path('search', views.search, name="search"),
    path('check_repeat', views.check_repeat, name="check_repeat"),
    path('check_use', views.check_use, name="check_use"),
    path('check_is_exist', views.check_is_exist, name="check_is_exist"),

    path('change_host_environment', views.change_host_environment, name="changeHostENV"),
    path('change_host_group', views.change_host_group, name="changeHostGroup"),
    path('change_host_info', views.change_host_info, name="changeHostInfo"),
]
