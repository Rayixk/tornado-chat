/**
 * Created by Administrator on 2017/11/17.
 */

$(document).ready(function () {
    if (!window.console) window.console = {};
    if (!window.console.log) window.console.log = function () {
    };

    $("#messageform").live("submit", function () {
        newMessage($(this));
        return false;
    });
    $("#messageform").live("keypress", function (e) {
        if (e.keyCode == 13) {
            newMessage($(this));
            return false;
        }
    });
    $("#message").select();
    updater.start();
});

function newMessage(form) {
    var message = form.formToDict();
    console.log(JSON.stringify(message))
    updater.socket.send(JSON.stringify(message));
    form.find("#message").val("").select();
}

jQuery.fn.formToDict = function () {
    var fields = this.serializeArray();
    var json = {}
    for (var i = 0; i < fields.length; i++) {
        json[fields[i].name] = fields[i].value;
    }
    if (json.next) delete json.next;
    return json;
};

var updater = {
    socket: null,

    start: function () {
        var url = "ws://" + location.host + "/chatsocket";
        updater.socket = new WebSocket(url);
        console.log("1111111111111")
        updater.socket.onmessage = function (event) {
            console.log("2222222222222")
            updater.showMessage(JSON.parse(event.data));
        }
    },

    showMessage: function (message) {
        var node = $(message.html)
        node.hide()
        $("#inbox").append(node)
        node.slideDown()
        // del(message.client_id);
        // if (message.type != "offline") {
        //     add(message.client_id, message.username);
        //     if (message.body == "") return;
        //     var existing = $("#m" + message.id);
        //     if (existing.length > 0) return;
        //     var node = $(message.html);
        //     node.hide();
        //     $("#inbox").append(node);
        //     node.slideDown();
        // }
    }
};