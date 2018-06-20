function altRows(id){
    if(document.getElementsByTagName){

        var table = document.getElementById(id);
        var rows = table.getElementsByTagName("tr");

        for(var i=0;i<rows.length;i++){
            if(i % 2 === 0){
                rows[i].className = "evenrowcolor"
            }else{
                rows[i].className = "oddrowcolor"
            }
        }
    }
}

window.onload=function(){
    altRows('alternatecolor');
};

$("#is_checked").change(function () {
    var status = $("#is_checked").prop("checked");
    if (status){
        $("tbody input").prop("checked", true)
    }else {
        $("tbody input").prop("checked", false)
    }
});


