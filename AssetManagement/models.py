from django.db import models

# Create your models here.

class HostInfo(models.Model):
    ServerName = models.CharField('服务器名称', max_length=32)
    IP = models.CharField('IP地址', max_length=64)
    RemotePort = models.IntegerField('远程端口')
    SuperUser = models.CharField('超级用户名', max_length=32)
    SuperUserPass = models.CharField('超级用户密码', max_length=64)
    Environment = models.CharField('使用环境', max_length=32)
    OSType = models.CharField('操作系统类型', max_length=32)
    OSVersion = models.CharField('操作系统版本', max_length=32)
    Zabbix = models.CharField('是否加入监控', max_length=32)
    Salt = models.CharField('是否加入自动化运维', max_length=32)
    Jumpserver = models.CharField('是否加入堡垒机', max_length=32)
    Keepass = models.CharField('是否记录密码', max_length=32)
    Note = models.CharField('备注信息', max_length=1024, null=True, blank=True)

    def __str__(self):
        return self.ServerName

    class Meta:
        verbose_name_plural = "主机信息"
        verbose_name = "主机信息"

class HostENV(models.Model):
    EnvName = models.CharField("环境名称", max_length=32)
    Note = models.CharField('备注信息', max_length=1024, null=True, blank=True)

class HostGroup(models.Model):
    GroupName = models.CharField("分组名称", max_length=32, default="")
    Note = models.CharField('备注信息', max_length=1024, null=True, blank=True)

class HostAndHGroup(models.Model):
    ServerName = models.CharField('服务器名称', max_length=32)
    GroupName = models.CharField("分组名称", max_length=32)