from django.shortcuts import render, HttpResponse
from django.core import serializers
from AssetManagement import models
from django.db.models import Q
import pyDes
import base64

# Create your views here.
Key = "Gogenius"
Iv = "Gogen123"


# 加密
def encrypt_str(data):
    # 加密方法
    method = pyDes.des(Key, pyDes.CBC, Iv, pad=None, padmode=pyDes.PAD_PKCS5)
    # 执行加密码
    k = method.encrypt(data)
    # 转base64编码并返回
    return base64.b64encode(k)


# 解密
def decrypt_str(data):
    method = pyDes.des(Key, pyDes.CBC, Iv, pad=None, padmode=pyDes.PAD_PKCS5)
    # 对base64编码解密
    k = base64.b64decode(data)
    # 再执行Des解码并返回
    return method.decrypt(k)


# 获取主机超级用户密码并改成bytes类型
def get_host_password(data):
    password = models.HostInfo.objects.filter(id=data).values()[0]["SuperUserPass"]
    return password.encode("UTF-8")


# 获取网络设备密码
def get_network_device_password(data):
    password = models.NetworkDevice.objects.filter(id=data).values()[0]["Password"]
    return password.encode("UTF-8")


# 获取主机信息所有数据
def get_host_data():
    return models.HostInfo.objects.all()


# 获取主机环境所有数据
def get_group_data():
    return models.HostGroup.objects.all()


# 获取主机分组表所有数据
def get_env_data():
    return models.HostENV.objects.all()


# 获取网络设备表所有数据
def get_network_device_data():
    return models.NetworkDevice.objects.all()


# 获取主机名
def get_host_name(host_id):
    server_name = models.HostInfo.objects.filter(id=host_id).values("ServerName")[0]["ServerName"]
    return server_name


# 获取分组名
def get_group_name(group_id):
    group_name = models.HostGroup.objects.filter(id=group_id).values("GroupName")[0]["GroupName"]
    return group_name


# 检查主机名，分组名，环境名是否重复
def check_repeat(request):
    post_data = request.POST
    for i in post_data:
        name = post_data[i]
        if i == "host_name":
            if models.HostInfo.objects.filter(ServerName=name):
                return HttpResponse("Error")
            else:
                return HttpResponse("OK")
        elif i == "group_name":
            if models.HostGroup.objects.filter(GroupName=name):
                return HttpResponse("Error")
            else:
                return HttpResponse("OK")
        elif i == "env_name":
            if models.HostENV.objects.filter(EnvName=name):
                return HttpResponse("Error")
            else:
                return HttpResponse("OK")
        else:
            pass


# 检查是否有主机分组或者环境
def check_is_exist(request):
    group_data = get_group_data()
    env_data = get_env_data()
    if group_data.__len__() == 0:
        return HttpResponse("1")
    elif env_data.__len__() == 0:
        return HttpResponse("2")
    else:
        return HttpResponse("OK")


# 检查分组和环境是否被主机使用
def check_use(request):
    get_data = request.GET
    for i in get_data:
        if i == "host_group":
            group_name = get_group_name(get_data["host_group"])
            data = models.HostAndHGroup.objects.filter(GroupName=group_name)
            if data.__len__() == 0:
                return HttpResponse("OK")
            else:
                return HttpResponse("E")
        else:
            if i == "host_env":
                env_name = models.HostENV.objects.filter(id=get_data["host_env"]).values("EnvName")[0]["EnvName"]
                data = models.HostInfo.objects.filter(Environment=env_name)
                if data.__len__() == 0:
                    return HttpResponse("OK")
                else:
                    return HttpResponse("E")


# 搜索指定服务器
def search_server(request):
    post_data = request.POST
    for i in post_data:
        if i == "other":
            search_obj = Q()
            search_obj.add(Q(ServerName__icontains=post_data["other"]) | Q(IP__contains=post_data["other"]), Q.OR)
            data = serializers.serialize("json", models.HostInfo.objects.filter(search_obj))
            return HttpResponse(data)
        else:
            if post_data["env_name"] == "" and post_data["group_name"] != "":
                server_name_data = models.HostAndHGroup.objects.filter(GroupName=post_data["group_name"]).\
                    values("ServerName")
                if server_name_data.__len__() == 0:
                    # 如果没有需要查询的数据就返回空，这里模拟查询一个不存在的ServerName，主要是以空格开头，创建主机的时候不允许以空格开头
                    # 必须返回json格式，否则前端无法接收
                    data = serializers.serialize("json", models.HostInfo.objects.filter(ServerName=" test"))
                    return HttpResponse(data)
                else:
                    # 使用Django数据的Q类来实现复杂查询
                    search_obj = Q()
                    # 指定表达式的连接方式运算符，可以是OR AND NOT
                    search_obj.connector = "OR"
                    for server_name in server_name_data:
                        # 添加表达式
                        search_obj.children.append(("ServerName", server_name["ServerName"]))
                    data = serializers.serialize("json", models.HostInfo.objects.filter(search_obj))
                    return HttpResponse(data)
            elif post_data["env_name"] != "" and post_data["group_name"] == "":
                # 返回Json数据格式给前端
                data = serializers.serialize("json", models.HostInfo.objects.filter(Environment=post_data["env_name"]))
                return HttpResponse(data)
            elif post_data["env_name"] == "" and post_data["group_name"] == "":
                data = serializers.serialize("json", models.HostInfo.objects.all())
                return HttpResponse(data)
            else:
                search_obj = Q()
                q1 = Q()
                q1.connector = "AND"
                q1.children.append(("Environment", post_data["env_name"]))
                q2 = Q()
                q2.connector = "OR"
                server_name_data = models.HostAndHGroup.objects.filter(GroupName=post_data["group_name"]).\
                    values("ServerName")
                for server_name in server_name_data:
                    q2.children.append(("ServerName", server_name["ServerName"]))
                search_obj.add(q1, "AND")
                search_obj.add(q2, "AND")
                data = serializers.serialize("json", models.HostInfo.objects.filter(search_obj))
                return HttpResponse(data)


# 搜索指定网络设备
def search_network_device(request):
    post_data = request.POST
    for i in post_data:
        if i == "other":
            search_obj = Q()
            search_obj.add(Q(Name__icontains=post_data["other"]) | Q(ManageIP__contains=post_data["other"]) | Q(Position__contains=post_data["other"]), Q.OR)
            data = serializers.serialize("json", models.NetworkDevice.objects.filter(search_obj))
            return HttpResponse(data)
    else:
        if post_data["network_device_type"] == "" and post_data["network_device_owner"] == "" and post_data["network_device_brand"] == "":
            data = serializers.serialize("json", models.NetworkDevice.objects.all())
            return HttpResponse(data)
        elif post_data["network_device_type"] != "" and post_data["network_device_owner"] != "" and post_data["network_device_brand"] != "":
            q1 = Q()
            q1.connector = "AND"
            q1.children.append(("Type", post_data["network_device_type"]))
            q1.children.append(("Brand", post_data["network_device_brand"]))
            q1.children.append(("Owner", post_data["network_device_owner"]))
            data = serializers.serialize("json", models.NetworkDevice.objects.filter(q1))
            return HttpResponse(data)
        elif post_data["network_device_type"] == "" and post_data["network_device_owner"] == "" and post_data["network_device_brand"] != "":
            data = serializers.serialize("json", models.NetworkDevice.objects.filter(Brand=post_data["network_device_brand"]))
            return HttpResponse(data)
        elif post_data["network_device_type"] == "" and post_data["network_device_owner"] != "" and post_data["network_device_brand"] == "":
            data = serializers.serialize("json", models.NetworkDevice.objects.filter(Owner=post_data["network_device_owner"]))
            return HttpResponse(data)
        elif post_data["network_device_type"] != "" and post_data["network_device_owner"] == "" and post_data["network_device_brand"] == "":
            data = serializers.serialize("json", models.NetworkDevice.objects.filter(Type=post_data["network_device_type"]))
            return HttpResponse(data)
        elif post_data["network_device_type"] != "" and post_data["network_device_owner"] != "" and post_data["network_device_brand"] == "":
            q1 = Q()
            q1.connector = "AND"
            q1.children.append(("Type", post_data["network_device_type"]))
            q1.children.append(("Owner", post_data["network_device_owner"]))
            data = serializers.serialize("json", models.NetworkDevice.objects.filter(q1))
            return HttpResponse(data)
        elif post_data["network_device_type"] != "" and post_data["network_device_owner"] == "" and post_data["network_device_brand"] != "":
            q1 = Q()
            q1.connector = "AND"
            q1.children.append(("Type", post_data["network_device_type"]))
            q1.children.append(("Brand", post_data["network_device_brand"]))
            data = serializers.serialize("json", models.NetworkDevice.objects.filter(q1))
            return HttpResponse(data)
        elif post_data["network_device_type"] == "" and post_data["network_device_owner"] != "" and post_data["network_device_brand"] != "":
            q1 = Q()
            q1.connector = "AND"
            q1.children.append(("Brand", post_data["network_device_brand"]))
            q1.children.append(("Owner", post_data["network_device_owner"]))
            data = serializers.serialize("json", models.NetworkDevice.objects.filter(q1))
            return HttpResponse(data)
        else:
            pass


# 删除主机
def del_host(nid):
    server_name = get_host_name(nid)
    models.HostAndHGroup.objects.filter(ServerName=server_name).delete()
    models.HostInfo.objects.filter(id=nid).delete()
    return "successful"


# 删除分组
def del_group(nid):
    group_name = get_group_name(nid)
    models.HostAndHGroup.objects.filter(GroupName=group_name).delete()
    models.HostGroup.objects.filter(id=nid).delete()
    return "successful"


# 删除环境
def del_env(nid):
    models.HostENV.objects.filter(id=nid).delete()
    return "successful"


# 删除网络设备
def del_network_device(nid):
    models.NetworkDevice.objects.filter(id=nid).delete()
    return "successful"


# 主页
def index(request):
    return render(request, 'index.html')


# 环境分组
def host_environment_info(request):
    return render(request, 'am/host_env_info.html', {'data': get_env_data()})


# 网络设备列表
def network_device_info(request):
    data = models.NetworkDevice.objects.all()
    return render(request, "am/network_device_info.html", {"data": data})


# 主机分组
def host_group_info(request):
    return render(request, 'am/host_group_info.html', {'data': get_group_data()})


# 资产列表
def host_info(request):
    all_data = render(request, 'am/host_info.html', {'data': get_host_data(),
                                                    "hostData": get_group_data(),
                                                    "envData": get_env_data()})
    return all_data


# 获取密码
def get_password(request):
    return HttpResponse("此功能还未开发")


# 添加主机
def add_host(request):
    if request.method == "POST":
        post_data = request.POST
        group_names = post_data.getlist("HostGroup")
        for group_name in group_names:
            models.HostAndHGroup.objects.create(
                ServerName=request.POST["ServerName"],
                GroupName=group_name,
            )
        models.HostInfo.objects.create(
            ServerName=request.POST["ServerName"],
            IP=request.POST["IP"],
            RemotePort=request.POST["RemotePort"],
            SuperUser=request.POST["SuperUser"],
            #  存入数据库前先进行加密，再更改为UTF-8
            SuperUserPass=(encrypt_str(request.POST["SuperUserPass"])).decode("UTF-8"),
            Environment=request.POST["Environment"],
            OSType=request.POST["OSType"],
            OSVersion=request.POST["OSVersion"],
            Zabbix=request.POST["Zabbix"],
            Salt=request.POST["Salt"],
            Jumpserver=request.POST["Jumpserver"],
            Keepass=request.POST["Keepass"],
            Note=request.POST["Note"],
        )
    return render(request, "am/add_host.html", {"envData": get_env_data(), "hostGroupData": get_group_data()})


# 添加网络设备
def add_network_device(request):
    if request.method == "POST":
        models.NetworkDevice.objects.create(
            Name=request.POST["Name"],
            ManageIP=request.POST["IP"],
            #  存入数据库前先进行加密，再更改为UTF-8
            Password=(encrypt_str(request.POST["Password"])).decode("UTF-8"),
            Type=request.POST["Type"],
            Brand=request.POST["Brand"],
            Owner=request.POST["Owner"],
            Position=request.POST["Position"],
            Note=request.POST["Note"],
        )
    return render(request, "am/add_network_device.html")


# 编辑主机信息
def change_host_info(request):
    if request.method == "POST":
        post_data = request.POST
        get_data = request.GET
        old_host_name = get_host_name(get_data["id"])
        models.HostAndHGroup.objects.filter(ServerName=old_host_name).delete()
        group_names = post_data.getlist("HostGroup")
        for group_name in group_names:
            models.HostAndHGroup.objects.create(
                ServerName=request.POST["ServerName"],
                GroupName=group_name,
            )
        models.HostAndHGroup.objects.filter(ServerName=old_host_name).update(ServerName=request.POST["ServerName"])
        models.HostInfo.objects.filter(id=get_data["id"]).update(
            ServerName=request.POST["ServerName"],
            IP=request.POST["IP"],
            RemotePort=request.POST["RemotePort"],
            SuperUser=request.POST["SuperUser"],
            #  存入数据库前先进行加密，再更改为UTF-8
            SuperUserPass=(encrypt_str(request.POST["SuperUserPass"])).decode("UTF-8"),
            Environment=request.POST["Environment"],
            OSType=request.POST["OSType"],
            OSVersion=request.POST["OSVersion"],
            Zabbix=request.POST["Zabbix"],
            Salt=request.POST["Salt"],
            Jumpserver=request.POST["Jumpserver"],
            Keepass=request.POST["Keepass"],
            Note=request.POST["Note"],
        )
        return HttpResponse("OK")


# 编辑网络设备信息
def change_network_device_info(request):
    if request.method == "POST":
        get_data = request.GET
        models.NetworkDevice.objects.filter(id=get_data["id"]).update(
            Name=request.POST["Name"],
            ManageIP=request.POST["IP"],
            #  存入数据库前先进行加密，再更改为UTF-8
            Password=(encrypt_str(request.POST["Password"])).decode("UTF-8"),
            Type=request.POST["Type"],
            Brand=request.POST["Brand"],
            Owner=request.POST["Owner"],
            Position=request.POST["Position"],
            Note=request.POST["Note"],
        )
        return HttpResponse("OK")


# 添加主机分组
def add_host_group(request):
    if request.method == "POST":
        models.HostGroup.objects.create(
            GroupName=request.POST["GroupName"],
            Note=request.POST["Note"],
        )
    return render(request, "am/add_host_group.html")


# 更改主机分组
def change_host_group(request):
    if request.method == "POST":
        get_data = request.GET
        old_group_name = models.HostGroup.objects.filter(id=get_data["id"]).values("GroupName")[0]["GroupName"]
        models.HostAndHGroup.objects.filter(GroupName=old_group_name).update(GroupName=request.POST["GroupName"])
        models.HostGroup.objects.filter(id=get_data["id"]).update(
            GroupName=request.POST["GroupName"],
            Note=request.POST["Note"],
        )
        return HttpResponse('OK')


# 添加环境
def add_host_environment(request):
    if request.method == "POST":
        models.HostENV.objects.create(
            EnvName=request.POST["EnvName"],
            Note=request.POST["Note"],
        )
    return render(request, "am/add_host_env.html")


# 更改环境
def change_host_environment(request):
    if request.method == "POST":
        get_data = request.GET
        old_env_data = models.HostENV.objects.filter(id=get_data["id"]).values("EnvName")[0]["EnvName"]
        new_env_data = request.POST["EnvName"]
        models.HostENV.objects.filter(id=get_data["id"]).update(
            EnvName=request.POST["EnvName"],
            Note=request.POST["Note"],
        )
        if old_env_data != new_env_data:
            models.HostInfo.objects.filter(Environment=old_env_data).update(Environment=new_env_data)
        return HttpResponse('OK')


# 编辑功能
def edit(request):
    if request.method == "GET":
        get_data = request.GET
        for i in get_data.items():
            if i[0] == "hostGroup":
                data = models.HostGroup.objects.get(id=get_data["hostGroup"])
                return render(request, "am/edit_host_group.html", {"data": data})
            elif i[0] == "hostENVGroup":
                data = models.HostENV.objects.get(id=get_data["hostENVGroup"])
                return render(request, "am/edit_host_env.html", {"data": data})
            elif i[0] == "editHost":
                data = models.HostInfo.objects.get(id=get_data["editHost"])
                server_name = get_host_name(get_data["editHost"])
                groups = models.HostAndHGroup.objects.filter(ServerName=server_name).values("GroupName")
                groups_list = []
                for group in groups:
                    groups_list.append(group["GroupName"])
                zabbix_data = models.HostInfo.objects.filter(id=get_data["editHost"]).values("Zabbix")
                salt_data = models.HostInfo.objects.filter(id=get_data["editHost"]).values("Salt")
                jumpserver_data = models.HostInfo.objects.filter(id=get_data["editHost"]).values("Jumpserver")
                keepass_data = models.HostInfo.objects.filter(id=get_data["editHost"]).values("Keepass")

                # 将获取的密码进行解密，再更改为UTF-8
                decrypt_password = (decrypt_str(get_host_password(get_data["editHost"]))).decode("UTF-8")
                return render(request, "am/edit_host.html", {"data": data,
                                                             "envData": get_env_data(),
                                                             "hostGroupData": get_group_data(),
                                                             "usegroupdata": groups_list,
                                                             "ZabbixData": zabbix_data,
                                                             "SaltData": salt_data,
                                                             "JumpserverData": jumpserver_data,
                                                             "KeepassData": keepass_data,
                                                             "password": decrypt_password})
            elif i[0] == "cloneHost":
                data = models.HostInfo.objects.get(id=get_data["cloneHost"])
                server_name = get_host_name(get_data["cloneHost"])
                groups = models.HostAndHGroup.objects.filter(ServerName=server_name).values("GroupName")
                groups_list = []
                for group in groups:
                    groups_list.append(group["GroupName"])
                zabbix_data = models.HostInfo.objects.filter(id=get_data["cloneHost"]).values("Zabbix")
                salt_data = models.HostInfo.objects.filter(id=get_data["cloneHost"]).values("Salt")
                jumpserver_data = models.HostInfo.objects.filter(id=get_data["cloneHost"]).values("Jumpserver")
                keepass_data = models.HostInfo.objects.filter(id=get_data["cloneHost"]).values("Keepass")

                # 将获取的密码进行解密，再更改为UTF-8
                decrypt_password = (decrypt_str(get_host_password(get_data["cloneHost"]))).decode("UTF-8")
                return render(request, "am/clone_host.html", {"data": data,
                                                             "envData": get_env_data(),
                                                             "hostGroupData": get_group_data(),
                                                             "usegroupdata": groups_list,
                                                             "ZabbixData": zabbix_data,
                                                             "SaltData": salt_data,
                                                             "JumpserverData": jumpserver_data,
                                                             "KeepassData": keepass_data,
                                                             "password": decrypt_password})
            elif i[0] == "network_device":
                data = models.NetworkDevice.objects.get(id=get_data["edit_network_device"])
                # 将获取的密码进行解密，再更改为UTF-8
                decrypt_password = (decrypt_str(get_network_device_password(get_data["edit_network_device"]))).decode("UTF-8")
                return render(request, "am/edit_network_device.html", {"data": data,
                                                             "password": decrypt_password})
            else:
                pass


# 册除功能
def delete(request):
    # 单个删除
    if request.method == "GET":
        get_data = request.GET
        for i in get_data.items():
            if i[0] == "hostGroup":
                del_group(get_data['hostGroup'])
                return render(request, 'am/host_group_info.html', {'data': get_group_data()})
            elif i[0] == "hostENVGroup":
                del_env(get_data['hostENVGroup'])
                return render(request, 'am/host_env_info.html', {'data': get_env_data()})
            elif i[0] == "host":
                del_host(get_data['host'])
                return render(request,
                              'am/host_info.html',
                              {'data': get_host_data(),
                               "hostData": get_group_data(),
                               "envData": get_env_data()})
            elif i[0] == "network_device":
                del_network_device(get_data['network_device'])
                return render(request, 'am/network_device_info.html', {'data': get_network_device_data()})
            else:
                pass
    if request.method == "POST":
        # 指定删除
        post_data = request.POST
        for name in post_data:
            if name == "host":
                for nid in post_data.getlist("host"):
                    del_host(nid)
                return HttpResponse("successful")
            elif name == "host_env":
                env_name_list = []
                q1 = Q()
                q1.connector = "OR"
                for nid in post_data.getlist("host_env"):
                    env_name_list.append(models.HostENV.objects.filter(id=nid).values("EnvName")[0]["EnvName"])
                for n in env_name_list:
                    q1.children.append(("Environment", n))
                data = models.HostInfo.objects.filter(q1)
                if data.__len__() != 0:
                    return HttpResponse("error")
                if data.__len__() == 0:
                    for nid in post_data.getlist("host_env"):
                        del_env(nid)
                    return HttpResponse("successful")
            elif name == "host_group":
                group_name_list = []
                q1 = Q()
                q1.connector = "OR"
                for nid in post_data.getlist("host_group"):
                    group_name_list.append(get_group_name(nid))
                for n in group_name_list:
                    q1.children.append(("GroupName", n))
                data = models.HostAndHGroup.objects.filter(q1)
                if data.__len__() != 0:
                    return HttpResponse("error")
                if data.__len__() == 0:
                    for nid in post_data.getlist("host_group"):
                        del_group(nid)
                    return HttpResponse("successful")
            elif name == "network_device":
                for nid in post_data.getlist("network_device"):
                    del_network_device(nid)
                return HttpResponse("successful")
            else:
                pass
