$(document).ready(function() {
    var socket = io({
        transports: ["websocket"],
        });

    socket.on('connect', function() {
        socket.emit('my_event', {data: 'I\'m connected! - sent from browser'});  // my_event triggers the my_event method in backend
    });

    socket.on('my_response', function(msg, cb) {
        document.getElementById('ts_last_message').innerHTML = msg.user_specific_info;
    });

}
)


