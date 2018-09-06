var full = false;

function updateData() {
	requestNewData();
	connectSocket();
}

function requestNewData() {
	var xhttp;
	var uri = "http://" + location.host + "/stats";
	if (window.XMLHttpRequest) {
		xhttp = new XMLHttpRequest();
	}
	xhttp.onreadystatechange = function() {
		if (this.readyState == 4 && this.status == 200) {
			var obj = JSON.parse(xhttp.responseText);
			console.log(obj);
			displayStats(obj);
		}
	};
	xhttp.open("GET", uri, true);
	xhttp.send();
}

function displayStats(garbageStats) {
	var headerMap = {"total": "<b>Avg Time Until Take-Out:</b> ", "after-full": "<b>Avg Time Left Full:</b> ", "before-full": "<b>Avg Time To Become Full:</b> ", "highest-month": "<b>Month With Most Waste: </b>"};
	var monthMap = {0: "January", 1: "February", 2: "March", 3: "April", 4: "May", 5: "June", 6: "July", 7: "August", 8: "Semptember", 9: "October", 10: "November", 11: "December"};
	for (var key in garbageStats) {
		if (key == "highest-month") {
			document.getElementById(key).innerHTML = headerMap[key] += monthMap[garbageStats[key]];
		} else {
			document.getElementById(key).innerHTML = headerMap[key] += formatTime(garbageStats[key]);
		}
		
	}
}

function formatTime(time) {
	var result = "";
	
	var secs = parseInt(time, 10);
	var days = Math.floor(secs / (3600 * 24));
	secs -= days * (3600 * 24);
	var hrs = Math.floor(secs / 3600);
	secs -= hrs * 3600;
	var mins = Math.floor(secs / 60);
	secs -= mins * 60;
	
	var map = {"day": days, "hour": hrs, "minute": mins};
	for (var key in map) {
		if (map[key] > 0) {
			if (result.length > 0) {
				result += ", "
			}
			result += (map[key] + " " + key);
			if (map[key] > 1) {
				result += "s";
			}
		}
	}
	return result;
}

function connectSocket() {
	console.log("CONNECTING")
	var socket = io.connect("http://" + location.host + "/update");
	
	socket.on("dist", function (data) {
		var percentFull = data.dist
		console.log("Received Data: " + percentFull);
		if (!full || percentFull < 100) {
			move(percentFull);
		}
	});
	
	socket.on("time", function () {
		var lastPickUp = new Date();
		var date = (lastPickUp.getMonth() + 1) + '/' + lastPickUp.getDate() + '/' + lastPickUp.getFullYear();
		var time = (lastPickUp.getHours()) + ':' + lastPickUp.getMinutes();
		document.getElementById("time").innerHTML = "Trash Last Taken Out: " + "<b>" + lastPickUp.toLocaleString() + "</b>";
	});
	
	socket.on("temp", function (temp) {
		document.getElementById("temp").innerHTML = Math.round(temp.temp) + " &#8457";
	});
	
}

function move(percentFull) {
	var elem = document.getElementsByClassName("overlay")[0];
	var text = document.getElementsByClassName("text")[0];
	if (percentFull <= 100) {
		height = percentFull * 4;
		elem.style.height = height + "px";
		text.innerHTML = (percentFull) + "%"
		full = false;
	}
	if (percentFull == 100) {
		setTimeout(function () {
			alert("The Trash Needs To Be Taken Out!")
		}, 750)
		full = true;
	}
}