function hide_info() {
    $("#send_fail").css("display", "none");
    $("#verification_fail").css("display", "none");
    $("#repeat").css("display", "none");
    $("#send_success").css("display", "none");
    $("#no_code").css("display", "none");
    $("#valid_code").css("display", "none");
    $("#not_exist").css("display", "none");
}
$('body').on("mouseover", "#get_password, #close, #verification_get", function () {
    $(this).css("background-color", "#8482823b")
}).on("click", ".get_password, .get_password_network, .get_password_physics", function () {
    $("#verification_block").css("display", "inherit");
    $("#verification_div").css("display", "inherit");
    hide_info();
    data_id = $(this).attr("id")
}).on("mouseout", "#get_password, #close, #verification_get", function () {
    $(this).css("background-color", "white")
}).on("click", "#close", function () {
    $("#verification_block").css("display", "none");
    $("#verification_div").css("display", "none");
    $("#verification_code").val("");
    $("#passwd_value").text("");
    $("#username_value").text("");
    $("#webpasswd_value").text("");
    $("#conpasswd_value").text("");
    // $("#user_value").text("");
    // $("#webuser_value").text("");
    // $("#sship_value").text("");
    // $("#weburl_value").text("");
    // $("#conuser_value").text("");
}).on("click", "#verification_code", function () {
    hide_info();
}).on("click", "#verification_get", function () {
    hide_info();
    $.ajax({
        url: "/am/get_login_info",
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
});