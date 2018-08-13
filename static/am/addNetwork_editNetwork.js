$().ready(function() {
    $("#commentForm").validate({
        rules: {
            Name: {
                required: true
            },
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
            }
        },
        messages: {
            Name: {
                required: "请输入设备型号"
            },
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
            }
        }
    });
});

$(function () {
    $("#id_Name").change(function () {
        console.log();
        var data = $("#id_Name").val();
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