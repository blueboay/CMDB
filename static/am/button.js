$('body').on('mouseover', '#addButton, .get_password_physics, .get_password_network, #edit, #search, #backButton, #editButton', function(){
    $(this).css({"background-color": "#15806B"});
}).on('mouseout', '#addButton, #edit, .get_password_physics, .get_password_network, #search, #backButton, #editButton', function(){
    $(this).css({"background-color": "#18a689"});
}).on('mouseover', '#delButton, #del', function () {
    $(this).css({"background-color": "#BB4352"});
}).on('mouseout', '#delButton, #del', function () {
    $(this).css({"background-color": "#ed5565"});
});
