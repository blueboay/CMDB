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
        if "Zabbix" in request.POST:
            ZabbixDate = "Yes"
        else:
            ZabbixDate = "NO"
        if "Salt" in request.POST:
            SaltDate = "Yes"
        else:
            SaltDate = "NO"
        if "Jumpserver" in request.POST:
            JumpserverDate = "Yes"
        else:
            JumpserverDate = "NO"
        if "Keepass" in request.POST:
            KeepassDate = "Yes"
        else:
            KeepassDate = "NO"
        models.HostInfo.objects.create(
            ServerName=request.POST["ServerName"],
            IP=request.POST["IP"],
            RemotePort=request.POST["RemotePort"],
            SuperUser=request.POST["SuperUser"],
            SuperUserPass=request.POST["SuperUserPass"],
            Environment=request.POST["Environment"],
            OSType=request.POST["OSType"],
            OSVersion=request.POST["OSVersion"],
            Zabbix=ZabbixDate,
            Salt=SaltDate,
            Jumpserver=JumpserverDate,
            Keepass=KeepassDate,
            Note=request.POST["Note"],
        )
    return render(request, "am/addhost.html", {"envData": envData, "hostGroupData": hostGroupData})

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
        models.HostENV.objects.filter(id=n["id"]).update(
            EnvName=request.POST["EnvName"],
            Note=request.POST["Note"],
        )
        return HttpResponse('OK')

def edithost(request):
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
                return render(request, "am/edithost.html", {"data": data})
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
                models.HostInfo.objects.filter(id=n['host']).delete()
                return HttpResponse("删除成功")
            else:
                return HttpResponse("请求错误")