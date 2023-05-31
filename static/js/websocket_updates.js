// window.addEventListener("DOMContentLoaded", () => {

//     const websocket = new WebSocket("ws://localhost:8001/");
//     websocket.addEventListener("message", ({ data }) => {
//         const event = JSON.parse(data);
//         switch (event.type) {

//             case "field_update":
//                 document.getElementById('ts_last_message').innerHTML = event.value;
//                 break;

//             default:
//                 throw new Error(`Some error for event type: ${event.type}.`);

//         }
//     });
// });


$(document).ready(function() {
    var socket = io({
        transports: ["websocket"],
        });

    socket.on('connect', function() {
        socket.emit('my_event', {data: 'I\'m connected!'});
    });

    socket.on('my_response', function(msg, cb) {
        document.getElementById('ts_last_message').innerHTML = msg.user_specific_info;
    });

}
)


