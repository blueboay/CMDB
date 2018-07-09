$("#verification_get").mouseover(function () {
    $(this).css("background-color", "#8482823b")
}).mouseout(function () {
    $(this).css("background-color", "white")
}).click(function () {
    console.log("3")
});
$("#close").click(function () {
   $("#verification_block").css("display", "none");
   $("#verification_form").css("display", "none")
});