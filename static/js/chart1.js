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
            name: '',
            data: []
        }]
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
            name: '',
            data: []
        }]
    });

    request_params = {
        client_name: 'cpe1',
    };

    setInterval(fetch_new_data, 1000);

    function fetch_new_data() {
        $.getJSON('/fetchdata', request_params, function (data_received) {

            var data = data_received.data
            var data1 = data.param1;
            var data2 = data.param2;

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
        });
    }

});


