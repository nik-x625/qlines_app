var chartdata1 = [];
var chartname1 = '';
var series2 = [];



$(document).ready(function () {
    // chart 1
    const chart1 = Highcharts.chart('chart-div1', {
        time: {
            useUTC: false
        },

        xAxis: {
            type: 'datetime',
            dateTimeLabelFormats: {
                minute: '%H:%M',
                hour: '%H:%M',
                day: '%e. %b',
                week: '%e. %b',
                month: '%b \'%y',
                year: '%Y'
            }
        },

        series: [{
            name: 'CPU usage',
            data: []
        }],
        title: {
            text: 'CPU'
        }
    });


    // chart 2
    const chart2 = Highcharts.chart('chart-div2', {
        time: {
            useUTC: false
        },

        xAxis: {
            type: 'datetime',
            dateTimeLabelFormats: {
                minute: '%H:%M',
                hour: '%H:%M',
                day: '%e. %b',
                week: '%e. %b',
                month: '%b \'%y',
                year: '%Y'
            }
        },

        series: [{
            name: 'Memory usage',
            data: []
        }],
        title: {
            text: 'Memory'
        }
    });

    request_params = {
        client_name: client_name_from_flask,
    };

    // commented out to be replaced by the websocket (socket.io)
    fetch_new_data();
    setInterval(fetch_new_data, 1000);

    function fetch_new_data() {
        $.getJSON('/fetchdata', request_params, function (data_received) {
            if (data_received.data.ts_data) { // check if data_received is not empty

                console.log(typeof (data_received.data))

                var data = data_received.data
                var data1 = data.ts_data.param1;
                var data2 = data.ts_data.param2;

                var chartdata1 = [];
                var chartdata2 = [];

                for (var i = 0; i < data1.length; i++) {
                    chartdata1.push([
                        Date.parse(data1[i][1]), data1[i][2]
                    ])
                }

                for (var i = 0; i < data2.length; i++) {
                    chartdata2.push([
                        Date.parse(data2[i][1]), data2[i][2]
                    ])
                }

                chart1.series[0].setData(chartdata1)
                chart2.series[0].setData(chartdata2)
                //document.getElementById('ts_registered').innerHTML = data.meta_data.ts_registered;
                //document.getElementById('ts_first_message').innerHTML = data.meta_data.ts_first_message;
                //document.getElementById('ts_last_message').innerHTML = data.meta_data.ts_last_message;
                document.getElementById('cli_result').innerHTML = data.meta_data.last_cli_response;
                document.getElementById('ts_lastmessage').innerHTML = data.meta_data.ts_last_message;
            }
        });
    }




});


document.addEventListener("DOMContentLoaded", function () {

    // Buttons
    const buttonCliSend = document.getElementById("button_cli_send");
    const buttonIntervalSend = document.getElementById("button_interval_send");

    // Inputs
    const inputContentCli = document.getElementById("input_cli");
    const inputContentInterval = document.getElementById("input_interval");

    // Result element
    const resultDiv = document.getElementById("cli_result");

    // Function to send a message
    function sendMessage(inputType) {

        let message_body, message_type;

        if (inputType === 'cli') {
            message_body = inputContentCli.value;
            message_type = 'cli_request';
        } else if (inputType === 'interval') {
            message_body = inputContentInterval.value;
            message_type = 'interval_request';
        }
    
        const urlParams_initial = window.location.href;
    
        // Send the message to the Flask backend
        fetch("/send_to_device", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ message_body, message_type, urlParams_initial })
        })
        .then(response => response.json())
        //.then(data => {
        //    resultDiv.textContent = data.result;
        //})
        .catch(error => {
            console.error("Error:", error);
            resultDiv.textContent = "An error occurred.";
        });
    }

    buttonCliSend.addEventListener("click", function () {
        sendMessage('cli'); // Pass 'cli' as the input type
    });

    buttonIntervalSend.addEventListener("click", function () {
        sendMessage('interval'); // Pass 'interval' as the input type
    });

    // Listen for Enter key press in the input fields
    inputContentCli.addEventListener("keyup", function (event) {
        if (event.key === "Enter") {
            sendMessage('cli'); // Pass 'cli' as the input type
        }
    });

    inputContentInterval.addEventListener("keyup", function (event) {
        if (event.key === "Enter") {
            sendMessage('interval'); // Pass 'interval' as the input type
        }
    });
});


