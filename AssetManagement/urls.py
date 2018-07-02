from django.urls import path
from AssetManagement import views

urlpatterns = [
    path('host_info', views.host_info, name="hostInfo"),
    path('host_environment_info', views.host_environment_info, name="hostENVInfo"),
    path('host_group_info', views.host_group_info, name="hostGroupInfo"),
    path('network_device_info', views.network_device_info, name="network_device_info"),
    path('physics_server_info', views.physics_server_info, name="physics_server_info"),

    path('add_host', views.add_host, name="addHost"),
    path('add_host_group', views.add_host_group, name="addHostGroup"),
    path('add_host_environment', views.add_host_environment, name="addHostENV"),
    path('add_network_device', views.add_network_device, name="add_network_device"),
    path('add_physics_server', views.add_physics_server, name="add_physics_server"),

    path('edit', views.edit, name="edit"),
    path('delete', views.delete, name="delete"),
    path('search_server', views.search_server, name="search_server"),
    path('search_network_device', views.search_network_device, name="search_network_device"),
    path('check_repeat', views.check_repeat, name="check_repeat"),
    path('check_use', views.check_use, name="check_use"),
    path('check_is_exist', views.check_is_exist, name="check_is_exist"),
    path('get_password', views.get_password, name="get_password"),

    path('change_host_environment', views.change_host_environment, name="changeHostENV"),
    path('change_host_group', views.change_host_group, name="changeHostGroup"),
    path('change_host_info', views.change_host_info, name="changeHostInfo"),
    path('change_network_device_info', views.change_network_device_info, name="change_network_device_info"),
]
