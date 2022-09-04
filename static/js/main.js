$(document).ready(function() {
    $('#login-btn').click(function() {
        $('#login-form').submit( function(event) {
            event.preventDefault();
            var form = $(this);
            $.ajax({
                url: form.prop("action"),
                method: form.prop("method"),
                data: form.serialize(),
                timeout: 5000,
                dataType: "html",
            })
            .done( function(data) {
                var out_html = $($.parseHTML(data));
                try {
                    localStorage.setItem("token", out_html.filter('#token')[0].innerHTML);
                    localStorage.setItem("userid", out_html.filter('#userid')[0].innerHTML);
                } catch(error) {}
                $('body').html(out_html);
            })
            .fail(function() {
                $('#login-fail-area').text('ログインに失敗しました');
            });
        });        
    });

    $('body').on('click', '#go-btn', function(){
        $('#main-form').submit( function(event) {
            event.preventDefault();
            var form = $(this);
            var serverData = mainLogicSendData(form);
            $.ajax({
                url: form.prop("action"),
                method: form.prop("method"),
                data: serverData,
                timeout: 5000,
                dataType: "html",
            })
            .done( function(data) {
                var out_html = $($.parseHTML(data));
                $('body').html(out_html);
            })
            .fail(function() {
                $('#main-fail-area').text('業務エラーです。');
            });
        });
    });

    $('body').on('click', '#refresh-btn', function(){
        $('#main-form').submit( function(event) {
            event.preventDefault();
            var form = $(this);
            var serverData = mainLogicSendData(form);
            $.ajax({
                url: form.prop("action"),
                method: form.prop("method"),
                data: serverData,
                timeout: 5000,
                dataType: "html",
            })
            .done( function(data) {
                var out_html = $($.parseHTML(data));
                $('body').html(out_html);
                $("body").find('#error-tag').hide();
            })
            .fail(function() {});
        });
    });
});

function mainLogicSendData(formData) {
    var serverData = formData.serialize();
    for (let i = 0; i < 50; i++) {
        serverData = serverData.replace('ken-select=', 'ken-select' + i.toString(10) + '=');
        serverData = serverData.replace('md-item-select=', 'md-item-select' + i.toString(10) + '=');
    }

    var token = localStorage.getItem("token");
    var userid = localStorage.getItem("userid");

    var tokenSendData = "token="+token;
    var useridSendData = "userid="+userid;

    serverData = serverData+"&"+tokenSendData+"&"+useridSendData;

    return serverData;
}
