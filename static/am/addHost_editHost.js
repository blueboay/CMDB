$().ready(function() {
    $("#commentForm").validate({
        rules: {
            ServerName: {
                required: true
            },
            IP: {
                required: true
            },
            RemotePort: {
                required: true,
                digits: true
            },
            SuperUser: {
                required: true
            },
            SuperUserPass: {
                required: true
            },
            OSType: {
                required: true
            },
            OSVersion: {
                required: true
            },
            Environment: {
                required: true
            },
            HostGroup: {
                required: true
            },
            Zabbix: {
                required: true
            },
            Salt: {
                required: true
            },
            Jumpserver: {
                required: true
            },
            Keepass: {
                required: true
            }
        },
        messages: {
            ServerName: {
                required: "请输入主机显示名称"
            },
            IP: {
                required: "请输入主要对应IP地址"
            },
            RemotePort: {
                required: "请输入远程访问主机端口",
                digits: "请输入合法的端口，必须为正整数"
            },
            SuperUser: {
                required: "请输入远程访问主机超级用户名"
            },
            SuperUserPass: {
                required: "请输入远程访问主机超级用户密码"
            },
            OSType: {
                required: "请输入主机操作系统类型，如：Windows,Linux"
            },
            OSVersion: {
                required: "请输入主机操作系统版本"
            },
            Environment: {
                required: "123"
            },
            HostGroup: {
                required: "请至少选中一项"
            },
            Zabbix: {
                required: "请至少任选其一"
            },
            Salt: {
                required: "请至少任选其一"
            },
            Jumpserver: {
                required: "请至少任选其一"
            },
            Keepass: {
                required: "请至少任选其一"
            }
        }
    });
});