from django.shortcuts import render, HttpResponse
from AssetManagement import models

# Create your views here.

# 获取主机信息，主机环境，主机分组表所有数据
hostInfoData = models.HostInfo.objects.all()
HostGroupData = models.HostGroup.objects.all()
HostENVData = models.HostENV.objects.all()


# 主页
def index(request):
    return render(request, 'index.html')


# 环境分组
def host_environment_info(request):
    return render(request, 'am/hostENVInfo.html', {'data': HostENVData})


# 主机分组
def host_group_info(request):
    return render(request, 'am/hostGroupInfo.html', {'data': HostGroupData})


# 资产列表
def host_info(request):
    data = request.POST
    if request.method == "POST":
        if data["ENVName"] != "环境" or data["GroupName"] != "分组" or data["Other"] != "":
            return HttpResponse("OK")
        else:
            return HttpResponse("Error")
    else:
        return render(request, 'am/hostInfo.html', {'data': hostInfoData,
                                                    "hostData": HostGroupData,
                                                    "envData": HostENVData})


# 资产列表详细信息
def host_more_info(request):
    n = request.GET
    data = models.HostInfo.objects.filter(id=n["host"]).values()
    servername = models.HostInfo.objects.filter(id=n["host"]).values("ServerName")[0]["ServerName"]
    group_data = models.HostAndHGroup.objects.filter(ServerName=servername).values("GroupName")
    return render(request, 'am/hostMoreInfo.html', {"data": data, "groupData": group_data})


# 添加主机
def add_host(request):
    if request.method == "POST":
        data = request.POST
        groups = data.getlist("HostGroup")
        for i in groups:
            models.HostAndHGroup.objects.create(
                ServerName=request.POST["ServerName"],
                GroupName=i,
            )
        models.HostInfo.objects.create(
            ServerName=request.POST["ServerName"],
            IP=request.POST["IP"],
            RemotePort=request.POST["RemotePort"],
            SuperUser=request.POST["SuperUser"],
            SuperUserPass=request.POST["SuperUserPass"],
            Environment=request.POST["Environment"],
            OSType=request.POST["OSType"],
            OSVersion=request.POST["OSVersion"],
            Zabbix=request.POST["Zabbix"],
            Salt=request.POST["Salt"],
            Jumpserver=request.POST["Jumpserver"],
            Keepass=request.POST["Keepass"],
            Note=request.POST["Note"],
        )
    return render(request, "am/addhost.html", {"envData": HostENVData, "hostGroupData": HostGroupData})


# 编辑主机信息
def change_host_info(request):
    if request.method == "POST":
        data = request.POST
        n = request.GET
        old_name = models.HostInfo.objects.filter(id=n["id"]).values("ServerName")[0]["ServerName"]
        models.HostAndHGroup.objects.filter(ServerName=old_name).delete()
        groups = data.getlist("HostGroup")
        for i in groups:
            models.HostAndHGroup.objects.create(
                ServerName=request.POST["ServerName"],
                GroupName=i,
            )
        models.HostAndHGroup.objects.filter(ServerName=old_name).update(ServerName=request.POST["ServerName"])
        models.HostInfo.objects.filter(id=n["id"]).update(
            ServerName=request.POST["ServerName"],
            IP=request.POST["IP"],
            RemotePort=request.POST["RemotePort"],
            SuperUser=request.POST["SuperUser"],
            SuperUserPass=request.POST["SuperUserPass"],
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
        n = request.GET
        old_name = models.HostGroup.objects.filter(id=n["id"]).values("GroupName")[0]["GroupName"]
        models.HostAndHGroup.objects.filter(GroupName=old_name).update(GroupName=request.POST["GroupName"])
        models.HostGroup.objects.filter(id=n["id"]).update(
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
        n = request.GET
        old_data = models.HostENV.objects.filter(id=n["id"]).values("EnvName")
        old_data = old_data[0]["EnvName"]
        new_data = request.POST["EnvName"]
        models.HostENV.objects.filter(id=n["id"]).update(
            EnvName=request.POST["EnvName"],
            Note=request.POST["Note"],
        )
        if old_data != new_data:
            models.HostInfo.objects.filter(Environment=old_data).update(Environment=new_data)
        return HttpResponse('OK')


# 编辑功能
def edit(request):
    if request.method == "GET":
        n = request.GET
        for i in n.items():
            if i[0] == "hostGroup":
                data = models.HostGroup.objects.get(id=n["hostGroup"])
                return render(request, "am/editHostGroup.html", {"data": data})
            elif i[0] == "hostENVGroup":
                data = models.HostENV.objects.get(id=n["hostENVGroup"])
                return render(request, "am/editHostENV.html", {"data": data})
            elif i[0] == "host":
                data = models.HostInfo.objects.get(id=n["host"])
                usegroupdata =  models.HostInfo.objects.filter(id=n["host"]).values("ServerName")
                usegroupdata = usegroupdata[0]["ServerName"]
                usegroupdata = models.HostAndHGroup.objects.filter(ServerName=usegroupdata).values("GroupName")
                list1 = []
                for x in usegroupdata:
                    list1.append(x["GroupName"])
                zabbix_data = models.HostInfo.objects.filter(id=n["host"]).values("Zabbix")
                salt_data = models.HostInfo.objects.filter(id=n["host"]).values("Salt")
                jumpserver_data = models.HostInfo.objects.filter(id=n["host"]).values("Jumpserver")
                keepass_data = models.HostInfo.objects.filter(id=n["host"]).values("Keepass")
                return render(request, "am/editHost.html", {"data": data,
                                                            "envData": HostENVData,
                                                            "hostGroupData": HostGroupData,
                                                            "usegroupdata": list1,
                                                            "ZabbixData": zabbix_data,
                                                            "SaltData": salt_data,
                                                            "JumpserverData": jumpserver_data,
                                                            "KeepassData": keepass_data})
            else:
                return HttpResponse("请求错误")


# 册除功能
def delete(request):
    if request.method == "GET":
        n = request.GET
        for i in n.items():
            if i[0] == "hostGroup":
                models.HostGroup.objects.filter(id=n['hostGroup']).delete()
                return HttpResponse("删除成功")
            elif i[0] == "hostENVGroup":
                models.HostENV.objects.filter(id=n['hostENVGroup']).delete()
                return HttpResponse("删除成功")
            elif i[0] == "host":
                nm = models.HostInfo.objects.filter(id=n['host']).values("ServerName")[0]["ServerName"]
                models.HostAndHGroup.objects.filter(ServerName=nm).delete()
                models.HostInfo.objects.filter(id=n['host']).delete()
                return HttpResponse("删除成功")
            else:
                return HttpResponse("请求错误")
