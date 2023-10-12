var chartdata1 = [];
var chartname1 = '';
var series2 = [];
var chart_test;
var highchart_object_list = [];
const urlParamsInitial = window.location.href;


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
            name: 'CPU usage - chart1',
            data: []
        }],
        title: {
            text: 'CPU - chart1'
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
            name: 'Memory usage - chart 2',
            data: []
        }],
        title: {
            text: 'Memory - chart 2'
        }
    });

    request_params = {
        client_name: client_name_from_flask,
    };


    


    function fetchAndRenderCharts() {
        $.get('/get_charts', { urlParamsInitial: urlParamsInitial }, function (chart_list) {
            chart_list.forEach(function (chart) {

                const chartDiv = document.createElement('div');
                chartDiv.id = chart.chart_name;
                document.getElementById('chartContainer').appendChild(chartDiv);

                // Convert the JSON string back to a JavaScript object for the chart configuration
                const chartConfig = JSON.parse(chart.chart_config);

                //chart_test = Highcharts.chart(chart.chart_name, chartConfig);
                
                const highchart = Highcharts.chart(chart.chart_name, chartConfig);
                highchart_object_list.push(highchart);
                
            });
            console.log(highchart_object_list)
        });
    };

    fetchAndRenderCharts();



    function fetch_chart_data() {
        $.getJSON('/fetch_chart_data', request_params, function (data_received) {
            if (data_received.data.ts_data) { // check if data_received is not empty
                const param1Data = extractParameterData('param1', data_received.data.ts_data);
                const param2Data = extractParameterData('param2', data_received.data.ts_data);

                // Update chart1 and chart2 with the new data
                chart1.series[0].setData(param1Data);
                chart2.series[0].setData(param1Data);
                //chart_test.series[0].setData(param1Data);
                //chart2.series[0].setData(param2Data);

                // Update other elements as needed
                document.getElementById('cli_result').innerHTML = data_received.data.meta_data.last_cli_response;
                document.getElementById('ts_lastmessage').innerHTML = data_received.data.meta_data.ts_last_message;
            }
        });
    }

    // Function to extract and format the data for a specific parameter
    function extractParameterData(parameterName, data) {
        return data.map((item) => ({
            x: new Date(item.timestamp).getTime(),
            y: parseFloat(item.param_subtree[parameterName]),
        }));
    }

    fetch_chart_data();
    setInterval(fetch_chart_data, 1000);




});







// about CLI commands and PII change
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
            message_type = 'interval_update';
        }

        //const urlParamsInitial = window.location.href;

        // Send the message to the Flask backend
        fetch("/send_to_device", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ message_body, message_type, urlParamsInitial })
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


