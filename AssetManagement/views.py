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
def get_password(data):
    password = models.HostInfo.objects.filter(id=data).values()[0]["SuperUserPass"]
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


# 搜索指定主机
def search(request):
    post_data = request.POST
    if post_data["env_name"] == "" and post_data["group_name"] != "":
        server_name_data = models.HostAndHGroup.objects.filter(GroupName=post_data["group_name"]).values("ServerName")
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
        print(data)
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
        server_name_data = models.HostAndHGroup.objects.filter(GroupName=post_data["group_name"]).values("ServerName")
        for server_name in server_name_data:
            q2.children.append(("ServerName", server_name["ServerName"]))
        search_obj.add(q1, "AND")
        search_obj.add(q2, "AND")
        data = serializers.serialize("json", models.HostInfo.objects.filter(search_obj))
        return HttpResponse(data)


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


# 主页
def index(request):
    return render(request, 'index.html')


# 环境分组
def host_environment_info(request):
    return render(request, 'am/hostENVInfo.html', {'data': get_env_data()})


# 主机分组
def host_group_info(request):
    return render(request, 'am/hostGroupInfo.html', {'data': get_group_data()})


# 资产列表
def host_info(request):
    all_data = render(request, 'am/hostInfo.html', {'data': get_host_data(),
                                                    "hostData": get_group_data(),
                                                    "envData": get_env_data()})
    return all_data


# 资产列表详细信息
def host_more_info(request):
    get_data = request.GET
    host_data = models.HostInfo.objects.filter(id=get_data["host"]).values()
    server_name = get_host_name(get_data["host"])
    group_data = models.HostAndHGroup.objects.filter(ServerName=server_name).values("GroupName")

    # 将获取的密码进行解密，再更改为UTF-8
    decrypt_password = (decrypt_str(get_password(get_data["host"]))).decode("UTF-8")

    return render(request, 'am/hostMoreInfo.html', {"data": host_data,
                                                    "groupData": group_data,
                                                    "password": decrypt_password})


# 添加主机
def add_host(request):
    if request.method == "POST":
        data = request.POST
        group_names = data.getlist("HostGroup")
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
    return render(request, "am/addhost.html", {"envData": get_env_data(), "hostGroupData": get_group_data()})


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


# 添加主机分组
def add_host_group(request):
    if request.method == "POST":
        models.HostGroup.objects.create(
            GroupName=request.POST["GroupName"],
            Note=request.POST["Note"],
        )
    return render(request, "am/addhostgroup.html")


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
    return render(request, "am/addHostENV.html")


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
                return render(request, "am/editHostGroup.html", {"data": data})
            elif i[0] == "hostENVGroup":
                data = models.HostENV.objects.get(id=get_data["hostENVGroup"])
                return render(request, "am/editHostENV.html", {"data": data})
            elif i[0] == "host":
                data = models.HostInfo.objects.get(id=get_data["host"])
                server_name = get_host_name(get_data["host"])
                groups = models.HostAndHGroup.objects.filter(ServerName=server_name).values("GroupName")
                groups_list = []
                for group in groups:
                    groups_list.append(group["GroupName"])
                zabbix_data = models.HostInfo.objects.filter(id=get_data["host"]).values("Zabbix")
                salt_data = models.HostInfo.objects.filter(id=get_data["host"]).values("Salt")
                jumpserver_data = models.HostInfo.objects.filter(id=get_data["host"]).values("Jumpserver")
                keepass_data = models.HostInfo.objects.filter(id=get_data["host"]).values("Keepass")

                # 将获取的密码进行解密，再更改为UTF-8
                decrypt_password = (decrypt_str(get_password(get_data["host"]))).decode("UTF-8")

                return render(request, "am/editHost.html", {"data": data,
                                                            "envData": get_env_data(),
                                                            "hostGroupData": get_group_data(),
                                                            "usegroupdata": groups_list,
                                                            "ZabbixData": zabbix_data,
                                                            "SaltData": salt_data,
                                                            "JumpserverData": jumpserver_data,
                                                            "KeepassData": keepass_data,
                                                            "password": decrypt_password})
            else:
                return HttpResponse("请求错误")


# 册除功能
def delete(request):
    # 单个删除
    if request.method == "GET":
        get_data = request.GET
        for i in get_data.items():
            if i[0] == "hostGroup":
                del_group(get_data['hostGroup'])
                return render(request, 'am/hostGroupInfo.html', {'data': get_group_data()})
            elif i[0] == "hostENVGroup":
                del_env(get_data['hostENVGroup'])
                return render(request, 'am/hostENVInfo.html', {'data': get_env_data()})
            elif i[0] == "host":
                del_host(get_data['host'])
                return render(request,
                              'am/hostInfo.html',
                              {'data': get_host_data(),
                               "hostData": get_group_data(),
                               "envData": get_env_data()})
            else:
                return HttpResponse("请求错误")
    if request.method == "POST":
        # 指定删除
        post_data = request.POST
        for name in post_data:
            if name == "host":
                for nid in post_data.getlist("host"):
                    del_host(nid)
                return HttpResponse("successful")
            elif name == "host_env":
                for nid in post_data.getlist("host_env"):
                    del_env(nid)
                return HttpResponse("successful")
            elif name == "host_group":
                for nid in post_data.getlist("host_group"):
                    del_group(nid)
                return HttpResponse("successful")
            else:
                pass
