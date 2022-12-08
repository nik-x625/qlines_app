$('#btid').click(function () {
	$.ajax({
		url: "someurl",
		type: "GET",
		dataType: "html",
		success: function (data) {
			$('#dashboard_page_content').html($('#dashboard_page_content', data).html());
		},
	})
})
