$().ready(function() {
    $("#commentForm").validate({
        rules: {
            EnvName: {
                required: true
            }
        },
        messages: {
            EnvName: {
                required: "请输入环境名称"

            }
        }
    });
});

$(function () {
    var old_data = $("#id_EnvName").val();
    $("#id_EnvName").change(function () {
        var data = $("#id_EnvName").val();
        if (data.charAt(0) === " "){
            $("#id_error_info2").removeClass("error_info");
        }else{
            $("#id_error_info2").addClass("error_info");
        }
        if (data !== old_data){
            $.ajax({
                url: "/am/check_repeat",
                type: "post",
                data: {"env_name": data},
                success: function (arg) {
                    if (arg === "Error"){
                        $("#id_error_info1").removeClass("error_info");
                        return false;
                    }else if (arg === "OK") {
                        $("#id_error_info1").addClass("error_info");
                    }else{
                        console.log("OK");
                    }
                },
                fail: function () {
                }
            })
        }else {
            $("#id_error_info1").addClass("error_info");
        }
    })
});

$("#sub").click(function () {
    if ($("#id_error_info1").is(".error_info")){
        console.log("OK");
    }else {
        return false;
    }
    if ($("#id_error_info2").is(".error_info")){
        console.log("OK");
    }else {
        return false;
    }
});