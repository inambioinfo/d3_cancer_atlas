var totalDoubloons = 30;

var investedDoubloons = [0, 0, 0];

var ship_names = ["ship_1=", "ship_2=", "ship_3="];

var linkRows = [1, 1, 1, 2, 2, 2, 3, 3, 3];

var makeTheAddReduceFiveRowsWork = [1, 1, 2, 2, 3, 3];

d3.selectAll(".allocation-feedback").data(investedDoubloons);
d3.selectAll(".allocation-box").data(linkRows);
d3.selectAll(".five").data(makeTheAddReduceFiveRowsWork);
d3.select("#allocation-info-span").text(totalDoubloons);
for (var i = 0; i < investedDoubloons.length; i++) {
	var id = "#allocation-row-" + (i+1);
	d3.select(id).text(function(d) {return d;});

	id = "#reduce-" + (i+1);
	d3.select(id).on("click", function(d) {
		// setColours(d, investedDoubloons);
		if (investedDoubloons[d-1] > 0) {
			investedDoubloons[d-1] -= 1;
			totalDoubloons += 1;
			console.log(totalDoubloons);
			console.log(investedDoubloons)
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
			})
		}
	});

	id = "#reduce5-" + (i+1);
	d3.select(id).on("click", function(d) {
		console.log("clicked - 5:", i+1);
		// setColours(d, investedDoubloons);
		if (investedDoubloons[d-1] > 4) {
			investedDoubloons[d-1] -= 5;
			totalDoubloons += 5;
			console.log(totalDoubloons);
			console.log(investedDoubloons)
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
	});

	id = "#add-" + (i+1);
	d3.select(id).on("click", function(d) {
		// setColours(d, investedDoubloons);
		if (totalDoubloons > 0) {
			investedDoubloons[d-1] += 1;
			totalDoubloons -= 1;
			console.log(totalDoubloons);
			console.log(investedDoubloons)
			d3.select("#allocation-row-" + d).text(investedDoubloons[d-1]);
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
			})
		}
	});

	id = "#add5-" + (i+1);
	d3.select(id).on("click", function(d) {
		console.log("clicked + 5:", i+1);
		// setColours(d, investedDoubloons);
		if (totalDoubloons > 4) {
			console.log(d-1, investedDoubloons, investedDoubloons[d-1]);

			investedDoubloons[d-1] += 5;
			totalDoubloons -= 5;
			console.log(totalDoubloons);
			console.log(investedDoubloons)
			d3.select("#allocation-row-" + d).text(investedDoubloons[d-1]);
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
			})
		}
	});
}


d3.select(".next-state-footer").append("a")
	.attr("href", function() {
		var str = "/map-battle?";
		var sum = 0;
		for (var i = 0; i < investedDoubloons.length; i++){
			str += ship_names[i] + investedDoubloons[i] + "&";
			sum += investedDoubloons[i];
		}
		str += "sum=" + sum;
		return str;
	})
	.attr("class", "next-state-button")
	.html("Anchors aweigh");



