from django.shortcuts import render, HttpResponse
from AssetManagement import models

# Create your views here.
def index(request):
    return render(request, 'index.html')

def envgroup(request):
    data = models.HostENV.objects.all()
    return render(request, 'am/envgroup.html', {'data': data})

def hostgroup(request):
    data = models.HostGroup.objects.all()
    return render(request, 'am/hostgroup.html', {'data': data})

def hostinfo(request):
    data = models.HostInfo.objects.all()
    return render(request, 'am/hostInfo.html', {'data': data})

def hostinfo2(request):
    n = request.GET
    data = models.HostInfo.objects.filter(id=n["name"]).values()
    return render(request, 'am/hostinfo2.html', {"data": data})

def addhost(request):
    envData = models.HostENV.objects.all()
    hostGroupData = models.HostGroup.objects.all()
    if request.method == "POST":
        data = request.POST
        Groups = data.getlist("HostGroup")
        for i in Groups:
            models.HostAndHGroup.objects.create(
                ServerName = request.POST["ServerName"],
                GroupName = i,
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
        return render(request, "am/addhost.html", {"envData": envData, "hostGroupData": hostGroupData})

def changehostinfo(request):
    if request.method == "POST":
        data = request.POST
        n = request.GET
        oldName = models.HostInfo.objects.filter(id=n["id"]).values("ServerName")[0]["ServerName"]
        models.HostAndHGroup.objects.filter(ServerName=oldName).delete()
        Groups = data.getlist("HostGroup")
        for i in Groups:
            models.HostAndHGroup.objects.create(
                ServerName = request.POST["ServerName"],
                GroupName = i,
            )
        models.HostAndHGroup.objects.filter(ServerName=oldName).update(ServerName=request.POST["ServerName"])
        models.HostInfo.objects.filter(id=n["id"]).update(
            ServerName = request.POST["ServerName"],
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

def addhostgroup(request):
    if request.method == "POST":
        data = request.POST
        models.HostGroup.objects.create(
            GroupName=request.POST["GroupName"],
            Note=request.POST["Note"],
        )
    return render(request, "am/addhostgroup.html")

def changehostgroup(request):
    if request.method == "POST":
        data = request.POST
        n = request.GET
        oldName = models.HostGroup.objects.filter(id=n["id"]).values("GroupName")[0]["GroupName"]
        models.HostAndHGroup.objects.filter(GroupName=oldName).update(GroupName=request.POST["GroupName"])
        models.HostGroup.objects.filter(id=n["id"]).update(
            GroupName=request.POST["GroupName"],
            Note=request.POST["Note"],
        )
        return HttpResponse('OK')

def addenvgroup(request):
    if request.method == "POST":
        data = request.POST
        models.HostENV.objects.create(
            EnvName=request.POST["EnvName"],
            Note=request.POST["Note"],
        )
    return render(request, "am/addenvgroup.html")

def changeenvgroup(request):
    if request.method == "POST":
        data = request.POST
        n = request.GET
        oldData = models.HostENV.objects.filter(id=n["id"]).values("EnvName")
        oldData = oldData[0]["EnvName"]
        newData = request.POST["EnvName"]
        models.HostENV.objects.filter(id=n["id"]).update(
            EnvName=request.POST["EnvName"],
            Note=request.POST["Note"],
        )
        if oldData != newData:
            models.HostInfo.objects.filter(Environment=oldData).update(Environment=newData)
        return HttpResponse('OK')

def edit(request):
    if request.method == "GET":
        n = request.GET
        for i in n.items():
            if i[0] == "hgroup":
                data = models.HostGroup.objects.get(id=n["hgroup"])
                return render(request, "am/edithostgroup.html", {"data": data})
            elif i[0] == "envgroup":
                data = models.HostENV.objects.get(id=n["envgroup"])
                return render(request, "am/editenvgroup.html", {"data": data})
            elif i[0] == "host":
                data = models.HostInfo.objects.get(id=n["host"])
                envData = models.HostENV.objects.all()
                groupdata = models.HostGroup.objects.all()
                usegroupdata =  models.HostInfo.objects.filter(id=n["host"]).values("ServerName")
                usegroupdata = usegroupdata[0]["ServerName"]
                usegroupdata = models.HostAndHGroup.objects.filter(ServerName=usegroupdata).values("GroupName")
                list1 = []
                for i in usegroupdata:
                    list1.append(i["GroupName"])
                ZabbixData = models.HostInfo.objects.filter(id=n["host"]).values("Zabbix")
                SaltData = models.HostInfo.objects.filter(id=n["host"]).values("Salt")
                JumpserverData = models.HostInfo.objects.filter(id=n["host"]).values("Jumpserver")
                KeepassData = models.HostInfo.objects.filter(id=n["host"]).values("Keepass")
                return render(request,
                              "am/edithost.html",
                              {"data": data,"envData": envData, "hostGroupData": groupdata, "usegroupdata": list1, "ZabbixData": ZabbixData, "SaltData": SaltData, "JumpserverData": JumpserverData, "KeepassData": KeepassData})
            else:
                return HttpResponse("请求错误")

def delhost(request):
    if request.method == "GET":
        n = request.GET
        for i in n.items():
            if i[0] == "hgroup":
                models.HostGroup.objects.filter(id=n['hgroup']).delete()
                return HttpResponse("删除成功")
            elif i[0] == "envgroup":
                models.HostENV.objects.filter(id=n['envgroup']).delete()
                return HttpResponse("删除成功")
            elif i[0] == "host":
                nm = models.HostInfo.objects.filter(id=n['host']).values("ServerName")[0]["ServerName"]
                models.HostAndHGroup.objects.filter(ServerName=nm).delete()
                models.HostInfo.objects.filter(id=n['host']).delete()
                return HttpResponse("删除成功")
            else:
                return HttpResponse("请求错误")