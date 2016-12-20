var totalDoubloons = 30;

var investedDoubloons = [0, 0, 0];

var ship_names = ["ship_1=", "ship_2=", "ship_3="];

var linkRows = [1, 1, 1, 2, 2, 2, 3, 3, 3];

var makeTheAddReduceFiveRowsWork = [1, 1, 2, 2, 3, 3];

var dataDumpURL = "/log_submit";

//console.log("ResAlloc");

recordEvent("LOAD", true);

function next() {
		var str = "/decision_comfort?";
		var sum = 0;
		for (var i = 0; i < investedDoubloons.length; i++){
			str += ship_names[i] + investedDoubloons[i] + "&";
			sum += investedDoubloons[i];
		}
		str += "sum=" + sum;
		str += "&time=" + Date.now();
		
		document.location.assign(str);//Hopefully this will work...
		return false;
	}
	
function recordEvent(event, success) {
	obj = {event: event, time: Date.now(), success: success}
	console.log(JSON.stringify(obj));
	var req = new XMLHttpRequest();
	req.open("POST", dataDumpURL, true);
	req.setRequestHeader("Content-type", "application/json"); //This should be easily parsed.
	req.send(JSON.stringify(obj));//JSON-friendly
}

d3.selectAll(".allocation-feedback").data(investedDoubloons);
d3.selectAll(".allocation-box").data(linkRows);
d3.selectAll(".allocation-box-five").data(makeTheAddReduceFiveRowsWork);
d3.select("#allocation-info-span").text(totalDoubloons);
for (var i = 0; i < investedDoubloons.length; i++) {
	var id = "#allocation-row-" + (i+1);
	d3.select(id).text(function(d) {return d;});

	id = "#reduce-" + (i+1);
	d3.select(id).on("click", function(d) {
		if (investedDoubloons[d-1] > 0) {
			recordEvent("REDUCE_" + d, true);
			investedDoubloons[d-1] -= 1;
			totalDoubloons += 1;
			d3.select("#allocation-row-" + (d)).text(investedDoubloons[d-1]);
			d3.select("#allocation-info-span").text(totalDoubloons);
		}
		else {
			recordEvent("REDUCE_" + d, false);
		}
		setColours(d, investedDoubloons);
	});

	id = "#reduce5-" + (i+1);
	d3.select(id).on("click", function(d) {
		if (investedDoubloons[d-1] > 4) {
			recordEvent("REDUCE_FIVE)" + d, true);
			investedDoubloons[d-1] -= 5;
			totalDoubloons += 5;
			d3.select("#allocation-row-" + (d)).text(investedDoubloons[d-1]);
			d3.select("#allocation-info-span").text(totalDoubloons);
		}
		else {
			recordEvent("REDUCE_FIVE_" + d, false);
		}
		setColours(d, investedDoubloons);
	});

	id = "#add-" + (i+1);
	d3.select(id).on("click", function(d) {
		if (totalDoubloons > 0) {
			recordEvent("ADD_" + d, true);
			investedDoubloons[d-1] += 1;
			totalDoubloons -= 1;
			d3.select("#allocation-row-" + d).text(investedDoubloons[d-1]);
			d3.select("#allocation-info-span").text(totalDoubloons);
		}
		else {
			recordEvent("ADD_" + d, false);
		}
		setColours(d, investedDoubloons);
	});

	id = "#add5-" + (i+1);
	d3.select(id).on("click", function(d) {
		if (totalDoubloons > 4) {
			console.log(d-1, investedDoubloons, investedDoubloons[d-1]);
			recordEvent("ADD_FIVE_" + d, true);
			investedDoubloons[d-1] += 5;
			totalDoubloons -= 5;
			d3.select("#allocation-row-" + d).text(investedDoubloons[d-1]);
			d3.select("#allocation-info-span").text(totalDoubloons);
		}
		else {
			recordEvent("ADD_FIVE_" + d, false);
		}
		setColours(d, investedDoubloons);
	});
}


d3.select(".next-state-footer").append("a")
	.attr("href", function() {return "javascript:next()"})
	.attr("class", "next-state-button")
	.html("Anchors aweigh");