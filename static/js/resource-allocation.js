var totalDoubloons = 30;

var investedDoubloons = [0, 0, 0];

var ship_names = ["ship_1=", "ship_2=", "ship_3="];

var linkRows = [1, 1, 1, 2, 2, 2, 3, 3, 3];

var makeTheAddReduceFiveRowsWork = [1, 1, 2, 2, 3, 3];

var eventData = [];
recordEvent("LOAD", true);

var dataDumpURL = "/log_submit";

function next() {
		var str = "/map-battle?";
		var sum = 0;
		for (var i = 0; i < investedDoubloons.length; i++){
			str += ship_names[i] + investedDoubloons[i] + "&";
			sum += investedDoubloons[i];
		}
		str += "sum=" + sum;
		str += "&time=" + Date.now();
		
		//Export click data here, the page may be left...
		for (var i = 0; i < eventData.length; ++i) {
			console.log(JSON.stringify(eventData[i]));
			var req = new XMLHttpRequest();
			req.open("POST", dataDumpURL, true);
			req.setRequestHeader("Content-type", "application/json"); //This should be easily parsed.
			req.send(JSON.stringify(eventData[i]));
			//In case of mouseover without click, the page will still be loaded, but we have sent some of the data already...
		}
		eventData = [];
		//Page change event will need handling at the server end.
		
		return str;
	}

function recordEvent(event, success) {
	obj = {event: event, time: Date.now(), success: success}
	eventData.push(obj);//JSON-friendly
	console.log(obj.event + "\t" + obj.success + "\t" + obj.time);
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
		setColours(d, investedDoubloons);
		if (investedDoubloons[d-1] > 0) {
			recordEvent("REDUCE_" + d, true);
			investedDoubloons[d-1] -= 1;
			totalDoubloons += 1;
			d3.select("#allocation-row-" + (d)).text(investedDoubloons[d-1]);
			d3.select("#allocation-info-span").text(totalDoubloons);

			d3.select(".next-state-button")
			.attr("href", next)
		}
		else {
			recordEvent("REDUCE_" + d, false);
		}
	});

	id = "#reduce5-" + (i+1);
	d3.select(id).on("click", function(d) {
		setColours(d, investedDoubloons);
		if (investedDoubloons[d-1] > 4) {
			recordEvent("REDUCE_FIVE)" + d, true);
			investedDoubloons[d-1] -= 5;
			totalDoubloons += 5;
			d3.select("#allocation-row-" + (d)).text(investedDoubloons[d-1]);
			d3.select("#allocation-info-span").text(totalDoubloons);

			d3.select(".next-state-button")
			.attr("href", function() {
				var str = "/map-battle?";
				var sum = 0;
				for (var i = 0; i < investedDoubloons.length; i++){
					str += ship_names[i] + investedDoubloons[i] + "&";
					sum += investedDoubloons[i];
				}
				str += "sum=" + sum;
				return str;
			});
		}
		else {
			recordEvent("REDUCE_FIVE_" + d, false);
		}
	});

	id = "#add-" + (i+1);
	d3.select(id).on("click", function(d) {
		setColours(d, investedDoubloons);
		if (totalDoubloons > 0) {
			recordEvent("ADD_" + d, true);
			investedDoubloons[d-1] += 1;
			totalDoubloons -= 1;
			d3.select("#allocation-row-" + d).text(investedDoubloons[d-1]);
			d3.select("#allocation-info-span").text(totalDoubloons);

			d3.select(".next-state-button")
			.attr("href", next)
		}
		else {
			recordEvent("ADD_" + d, false);
		}
	});

	id = "#add5-" + (i+1);
	d3.select(id).on("click", function(d) {
		setColours(d, investedDoubloons);
		if (totalDoubloons > 4) {
			console.log(d-1, investedDoubloons, investedDoubloons[d-1]);
			recordEvent("ADD_FIVE_" + d, true);
			investedDoubloons[d-1] += 5;
			totalDoubloons -= 5;
			d3.select("#allocation-row-" + d).text(investedDoubloons[d-1]);
			d3.select("#allocation-info-span").text(totalDoubloons);

			d3.select(".next-state-button")
			.attr("href", next)
		}
		else {
			recordEvent("ADD_FIVE_" + d, false);
		}
	});
}


d3.select(".next-state-footer").append("a")
	.attr("href", next)
	.attr("class", "next-state-button")
	.html("Anchors aweigh");