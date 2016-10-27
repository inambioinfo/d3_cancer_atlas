var totalDoubloons = 30;

var investedDoubloons = [0, 0, 0];
var linkRows = [1, 1, 1, 2, 2, 2, 3, 3, 3];
d3.selectAll(".allocation-feedback").data(investedDoubloons);
d3.selectAll(".allocation-box").data(linkRows);
d3.select("#allocation-info-span").text(totalDoubloons);
for (var i = 0; i < investedDoubloons.length; i++) {
	var id = "#allocation-row-" + (i+1);
	d3.select(id).text(function(d) {return d;});
	id = "#reduce-" + (i+1);
	d3.select(id).on("click", function(d) {
		console.log("down: ", d);
		if (investedDoubloons[d-1] > 0) {
			investedDoubloons[d-1] -= 1;
			totalDoubloons += 1;
			d3.select("#allocation-row-" + (d)).text(investedDoubloons[d-1]);
			d3.select("#allocation-info-span").text(totalDoubloons);
		}
	});

	id = "#add-" + (i+1);
	d3.select(id).on("click", function(d) {
		if (totalDoubloons > 0) {
			investedDoubloons[d-1] += 1;
			totalDoubloons -= 1;
			d3.select("#allocation-row-" + d).text(investedDoubloons[d-1]);
			d3.select("#allocation-info-span").text(totalDoubloons);
		}
	});
}

