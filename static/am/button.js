$('body').on('mouseover', '#addButton, #moreInfo, #edit, #search, #backButton, #editButton, #clone', function(){
    $(this).css({"background-color": "#15806B"});
}).on('mouseout', '#addButton, #moreInfo, #edit, #search, #backButton, #editButton, #clone', function(){
    $(this).css({"background-color": "#18a689"});
}).on('mouseover', '#delButton, #del', function () {
    $(this).css({"background-color": "#BB4352"});
}).on('mouseout', '#delButton, #del', function () {
    $(this).css({"background-color": "#ed5565"});
});
