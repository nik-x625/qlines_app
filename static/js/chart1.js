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

    fetch_new_data();
    setInterval(fetch_new_data, 1000);

    function fetch_new_data() {
        $.getJSON('/fetchdata', request_params, function (data_received) {
            if (data_received.data.ts_data) { // check if data_received is not empty

                console.log(typeof(data_received.data))

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
                document.getElementById('ts_registered').innerHTML = data.meta_data.ts_registered;
                document.getElementById('ts_first_message').innerHTML = data.meta_data.ts_first_message;
                document.getElementById('ts_last_message').innerHTML = data.meta_data.ts_last_message;
            }
        });
    }

});


