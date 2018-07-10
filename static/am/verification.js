function hide_info() {
    $("#send_fail").css("display", "none");
    $("#verification_fail").css("display", "none");
    $("#repeat").css("display", "none");
    $("#send_success").css("display", "none");
    $("#no_code").css("display", "none");
    $("#valid_code").css("display", "none");
    $("#not_exist").css("display", "none");
}
$(".get_password").click(function () {
    $("#verification_block").css("display", "inherit");
    $("#verification_div").css("display", "inherit");
    $("#verification_code").val("");
    $("#passwd_value").text("");
    hide_info();
    host_id = $(this).attr("id")
});
$('body').on("mouseover", "#get_password, #close, #verification_get", function () {
    $(this).css("background-color", "#8482823b")
}).on("mouseout", "#get_password, #close, #verification_get", function () {
    $(this).css("background-color", "white")
}).on("click", "#close", function () {
    $("#verification_block").css("display", "none");
    $("#verification_div").css("display", "none")
}).on("click", "#verification_get", function () {
    hide_info();
    $.ajax({
        url: "/am/get_password",
        data: {"phone_number": "13357110502"},
        type: "post",
        dataType: "json",
        success: function (arg) {
            if (arg.code === 200){
                $("#send_success").css("display", "inherit")
            }else if(arg.code === 501){
                $("#repeat").css("display", "inherit")
            }else {
                $("#send_fail").css("display", "inherit")
            }
        }
    })
}).on("click", "#verification_code", function () {
    hide_info();
}).on("click", "#get_password", function () {
    var code_number = $("#verification_code").val();
    if (code_number.length === 0){
        hide_info();
        $("#no_code").css("display", "inherit")
    }else if(isNaN(Number(code_number))){
        hide_info();
        $("#valid_code").css("display", "inherit")
    }else {
        $.ajax({
            url: "/am/get_password",
            data: {"code_number": code_number, "host_id": host_id},
            type: "get",
            success: function (arg) {
                if (arg === "404"){
                    $("#not_exist").css("display", "inherit")
                }else if (arg === "403"){
                    $("#verification_fail").css("display", "inherit")
                }else {
                    $("#passwd_value").text(arg)
                }
            }
        })
    }
});