//container is the selected element into which the content is to be loaded
var container = document.querySelector('#dashboard_page_content'),
	//these are the selectors for your links
	linkPage1 = document.querySelector('#link_page1'),
	linkPage2 = document.querySelector('#link_page2');
//function that loads content
function loadContent(content) {
	// AJAX request
	var xhr = new XMLHttpRequest();
	xhr.open('POST', content, true);
	xhr.onload = function () {
		var el = document.createElement('div');
		el.innerHTML = this.response;
		container.empty()
		container.prepend(el);
	}
	xhr.send();
}
//After clicking the selector it will start the function loading the content. Enter the URL to your files in the appropriate place
linkPage1.addEventListener('click', function (e) {
	loadContent('static/templates/page1.html');
	e.preventDefault();
});
linkPage2.addEventListener('click', function (e) {
	loadContent('static/templates/page2.html');
	e.preventDefault();
});

