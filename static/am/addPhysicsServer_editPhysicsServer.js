$().ready(function() {
    $("#commentForm").validate({
        rules: {
            Model: {
                required: true
            },
            // ManageURL: {
            //     required: true
            // },
            // ManageUsername: {
            //     required: true
            // },
            // ManagePassword: {
            //     required: true
            // },
            Type: {
                required: true
            },
            Brand: {
                required: true
            },
            Owner: {
                required: true
            },
            Position: {
                required: true
            },
            ExpireDate: {
                required: true,
                dateISO:true
            },
            CPU: {
                required: true
            },
            Memory: {
                required: true
            },
            TotalSpace: {
                required: true
            },
            id_Note: {
                required: true
            }
        },
        messages: {
            Model: {
                required: "请输入设备型号"
            },
            // ManageURL: {
            //     required: "请输入管理URL"
            // },
            // ManageUsername: {
            //     required: "请输入访问用户名"
            // },
            // ManagePassword: {
            //     required: "请输入访问密码"
            // },
            Type: {
                required: "请选择设备类型"
            },
            Brand: {
                required: "请选择设备品牌"
            },
            Owner: {
                required: "请选择设备所有者"
            },
            Position: {
                required: "请输入设备位置"
            },
            ExpireDate: {
                required: "选择过期时间",
                dateISO: "必须输入合法的日期"
            },
            CPU: {
                required: "请输入CPU总核数"
            },
            Memory: {
                required: "请输入内存总大小"
            },
            TotalSpace: {
                required: "请输入空间总大小"
            },
            id_Note: {
                required: "请输入设备位置"
            }
        }
    });
});

$(function () {
    $("#id_Model").change(function () {
        var data = $("#id_Model").val();
        if (data.charAt(0) === " "){
            $("#id_error_info").removeClass("error_info");
        }else{
            $("#id_error_info").addClass("error_info");
        }
    })
});

$("#sub").click(function () {
    if (!($("#id_error_info").is(".error_info"))){
        return false;
    }
});