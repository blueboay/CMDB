$().ready(function() {
    $("#commentForm").validate({
        rules: {
            GroupName: {
                required: true
            }
        },
        messages: {
            GroupName: {
                required: "请输入分组名称"
            }
        }
    });
});

$(function () {
    var old_data = $("#id_GroupName").val();
    $("#id_GroupName").change(function () {
        var data = $("#id_GroupName").val();
        if (data.charAt(0) === " "){
            $("#id_error_info2").removeClass("error_info");
        }else{
            $("#id_error_info2").addClass("error_info");
        }
        if (data !== old_data){
            $.ajax({
                url: "/am/check",
                type: "post",
                data: {"group_name": data},
                success: function (arg) {
                    if (arg === "Error"){
                        $("#id_error_info1").removeClass("error_info");
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
    if ($("#id_error_info1， #id_error_info2").is(".error_info")){
        console.log("OK");
    }else {
        return false;
    }
});