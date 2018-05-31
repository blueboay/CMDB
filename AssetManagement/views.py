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
        if "Zabbix" in request.POST:
            ZabbixDate = True
        else:
            ZabbixDate = False

        if "Salt" in request.POST:
            SaltDate = True
        else:
            SaltDate = False

        if "Jumpserver" in request.POST:
            JumpserverDate = True
        else:
            JumpserverDate = False

        if "Keepass" in request.POST:
            KeepassDate = True
        else:
            KeepassDate = False

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

def addenvgroup(request):
    if request.method == "POST":
        data = request.POST
        models.HostENV.objects.create(
            EnvName=request.POST["EnvName"],
            Note=request.POST["Note"],
        )
    return render(request, "am/addenvgroup.html")

def edithost(request):
    if request.method == "GET":
        n = request.GET
        data = models.HostGroup.objects.get(id=n["hgroup"])
        return render(request, "am/edithost.html", {"data": data})

def delhost(request):
    return HttpResponse("Not")