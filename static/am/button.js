$('body').on('mouseover', '#addButton, .get_password_physics, .get_password_network, #edit, #search, #backButton, #editButton', function(){
    $(this).css({"background-color": "#15806B"});
}).on('mouseout', '#addButton, #edit, .get_password_physics, .get_password_network, #search, #backButton, #editButton', function(){
    $(this).css({"background-color": "#18a689"});
}).on('mouseover', '#delButton, #del, #updata_passwd', function () {
    $(this).css({"background-color": "#BB4352"});
}).on('mouseout', '#delButton, #del, #updata_passwd', function () {
    $(this).css({"background-color": "#ed5565"});
}).on("mouseover", "#queren", function () {
    $(this).css({"background-color": "#ddd"});
}).on("mouseout", "#queren", function () {
    $(this).css({"background-color": "white"});
}).on("click", "#queren", function () {
    $("#load_block").css("display", "none");
    $("#change_result").css("display", "none");
});
