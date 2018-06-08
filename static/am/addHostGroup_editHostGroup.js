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