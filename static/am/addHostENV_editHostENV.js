$().ready(function() {
    $("#commentForm").validate({
        rules: {
            EnvName: {
                required: true,
                remote: {
                    url: "/am/check",
                    type: "post"
                }
            }
        },
        messages: {
            EnvName: {
                required: "请输入环境名称",
                remote: "此名称已经被使用"
            }
        }
    });
});