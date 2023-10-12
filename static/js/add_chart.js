$(function () {
	$(document).ready(function () {
		$("#add_chart_submit").click(function () {
			$.ajax({
				'async': true,
				'type': "POST",
				'global': false,
				'dataType': 'html',
				'url': $SCRIPT_ROOT + "/add_chart",
				'data': {
					chart_name: $('input[name="chart_name"]').val(),
					chart_config: $('input[name="chart_config"]').val(),
					urlParamsInitial: urlParamsInitial, // Include urlParams_initial here
					//username: $('input[name="username"]').val(),
					//password: $('input[name="password"]').val(),
					//title: $('input[name="title"]').val(),
					//customer: $('input[name="customer"]').val(),
					//version: $('input[name="version"]').val()
				},
				'success': function (data) {
					$("#result_add_chart").html(data);
					$("#wait_add_chart").css("display", "none");
				},
				'beforeSend': function (x) {
					$("#wait_add_chart").css("display", "inline");
					$("#result_add_chart").html('Waiting for the result...');
				},
			});
		});
	});
});



