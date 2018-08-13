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
    ServerType = models.CharField('类型', max_length=32, blank=True)
    Brand = models.CharField('品牌', max_length=32, blank=True)
    Owner = models.CharField('所有者', max_length=32, blank=True)
    Position = models.CharField('位置', max_length=32, blank=True)
    Zabbix = models.CharField('是否加入监控', max_length=32)
    Salt = models.CharField('是否加入自动化运维', max_length=32)
    Jumpserver = models.CharField('是否加入堡垒机', max_length=32)
    Keepass = models.CharField('是否记录密码', max_length=32)
    Use = models.CharField('是否使用', max_length=32, null=True, blank=True)
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


class UserInfo(models.Model):
    UserName = models.CharField('用户名', max_length=32)
    Password = models.CharField('密码', max_length=128)
    Alias = models.CharField('别名', max_length=32)
    # Permission = models.CharField('权限', max_length=32)
    PhoneNumber = models.IntegerField('手机', null=True, blank=True)
    Email = models.EmailField('邮箱', max_length=32, null=True, blank=True)
    Note = models.CharField('备注信息', max_length=1024, null=True, blank=True)


class NetworkDevice(models.Model):
    Name = models.CharField('型号名称', max_length=32)
    ManageUser = models.CharField('SSH远程管理用户', max_length=64, null=True, blank=True)
    ManageIP = models.CharField('SSH远程管理IP', max_length=64, null=True, blank=True)
    Password = models.CharField('SSH远程密码', max_length=128, null=True, blank=True)
    WebManageUser = models.CharField('Web远程管理用户', max_length=64, null=True, blank=True)
    WebManageIP = models.CharField('Web远程管理IP', max_length=64, null=True, blank=True)
    WebPassword = models.CharField('Web远程管理密码', max_length=128, null=True, blank=True)
    ConsolePassword = models.CharField('Console管理密码', max_length=128, null=True, blank=True)
    Type = models.CharField('类型', max_length=32)
    # HomeNetwork = models.CharField('所属网络', max_length=32)
    Brand = models.CharField('品牌', max_length=32)
    Owner = models.CharField('所有者', max_length=32)
    Position = models.CharField('位置', max_length=32)
    Note = models.CharField('备注信息', max_length=1024, null=True, blank=True)


class PhysicalServer(models.Model):
    Model = models.CharField('型号', max_length=32)
    Type = models.CharField('类型', max_length=32)
    SN = models.CharField('序列号', max_length=32, null=True, blank=True)
    Brand = models.CharField('品牌', max_length=32)
    Position = models.CharField('位置', max_length=32)
    Owner = models.CharField('所有者', max_length=32, null=True, blank=True)
    ManageURL = models.CharField('登录URL', max_length=32, null=True, blank=True)
    ManageUsername = models.CharField('管理用户名', max_length=32, null=True, blank=True)
    ManagePassword = models.CharField('管理密码', max_length=32, null=True, blank=True)
    ExpireDate = models.DateField('维保过期时间', max_length=32)
    CPU = models.CharField('CPU', max_length=32)
    Memory = models.CharField('内存', max_length=32)
    TotalSpace = models.CharField('总空间', max_length=32)
    Note = models.CharField('备注信息', max_length=1024, null=True, blank=True)