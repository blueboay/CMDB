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