function load_page1() {
	var xhttp = new XMLHttpRequest();
	xhttp.onreadystatechange = function () {
		if (this.readyState == 4 && this.status == 200) {
			document.getElementById("dashboard_subpage").innerHTML = this.responseText;
		}
	};
	xhttp.open("GET", "page1", true);
	xhttp.send();
}



function load_page2() {
	var xhttp = new XMLHttpRequest();
	xhttp.onreadystatechange = function () {
		if (this.readyState == 4 && this.status == 200) {
			document.getElementById("dashboard_subpage").innerHTML = this.responseText;
		}
	};
	xhttp.open("GET", "page2", true);
	xhttp.send();
}