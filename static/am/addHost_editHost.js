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
                required: "请输入主机名称"
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
                required: "请选择使用环境"
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

$(function () {
    var old_data = $("#id_ServerName").val();
    $("#id_ServerName").change(function () {
        var data = $("#id_ServerName").val();
        if (data !== old_data){
            $.ajax({
                url: "/am/check",
                type: "post",
                data: {"host_name": data},
                success: function (arg) {
                    if (arg === "Error"){
                        $("#id_error_info").removeClass("error_info");
                        return false;
                    }else if (arg === "OK") {
                        $("#id_error_info").addClass("error_info");
                    }else{
                        console.log("OK");
                    }
                },
                fail: function () {
                }
            })
        }else {
            $("#id_error_info").addClass("error_info");
        }
    })
});

$("#sub").click(function () {
    if ($("#id_error_info").is(".error_info")){
        console.log("OK");
    }else {
        return false;
    }
});