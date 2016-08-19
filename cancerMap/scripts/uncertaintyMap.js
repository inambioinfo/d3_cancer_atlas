// 
// 
// 
// 		D3 Cancer Atlas research
// 			Code: Phil Gough <phillip.gough@qut.edu.au>
// 			Design: Jessie Roberts, Phil Gough
// 			
// 			
// 
// 


//********************//
//  SVG/MAP VARIABLES //
//********************//


// append an svg to the .vis div
var svg = d3.select(".vis").append("svg");

// extract the dimensions of the div element
var svgDimensions = d3.select(".vis").node().getBoundingClientRect();

// define the internal padding of the svg
var svgPadding =
{
	"top" : 10,
	"bottom" : 10,
	"left" : 10,
	"right" : 10
}

// select the projection the map will use
var projection = d3.geoMercator()
	.scale(2800)
	.translate([-svgDimensions.width * 7.45, -svgDimensions.height  *1.35])
	.precision(1);

var path = d3.geoPath()
	.projection(projection);

// define the svg size
svg.attr("width", svgDimensions.width)
	.attr("height", svgDimensions.height);

// add a group where the map will live
mapCanvas = svg.append("g");




//****************************************//
//	UNCERTAINTY VISUALISATION VARIABLES   //
//****************************************//

var uncertaintyLimits = {
	"lower" : 45,
	"upper" : 400
};

var regionColours = d3.scaleOrdinal()
    .domain([1, 4])
    .range(["steelblue", "mediumseagreen", "darkorange", "brown"]);



//****************************************//
//	Load and parse the uncertainty data   //
//****************************************//

d3.json("data/qld_slas.json", function(error, regions) 
{
	if (error) return (console.log(error));
	
	// add a new set of objects to draw on the map
	regions.objects.selected_slas = {"type": "GeometryCollection", "geometries":[]};

	// s = regions;
	// for each feature that we selected to show...
	for (var i = 0; i < selectedFeatures.length; i++)
	{
		// console.log("checking for " + selectedFeatures[i])
		// check the list of features...
		for (var j = 0; j < regions.objects.qld_slas.geometries.length; j++)
		{
			// and if we have the right one...
			if (selectedFeatures[i] === regions.objects.qld_slas.geometries[j].id)
			{
				// console.log("found matching area!");
				// push it onto the list of regions we want to show
				regions.objects.selected_slas.geometries = regions.objects.qld_slas.geometries[j];
				regions.objects.selected_slas.geometries.id = i;

				// draw this region to the page.
				mapCanvas.insert("path", "mapRegion")
					.datum(topojson.feature(regions, regions.objects.selected_slas.geometries))
					.attr("class", "mapRegion")
					.attr("d", path);
			}
		}
	}
	d3.select(".vis").style("border", "1px #222 solid");
	d3.selectAll(".mapRegion")
		// Move the region we are hovering over to the front
		.on("mouseover", function(d) {
			svg.selectAll("path").sort(function (a, b) { // select the parent and sort the path's
				if (a.id != d.id) return -1;               // a is not the hovered element, send "a" to the back
				else return 1;                             // a is the hovered element, bring "a" to the front
			});
		})
		// click to show a box with info
		.on("click", function(d) {
			updateFeedback(d.id);
		});

		// change the colours of the regions
		d3.selectAll("path")
		.style("fill", function(d) {
			region = getName(d.id);
			uncertainty = getUncertainty(parsed_data[region].high_uncertainty, parsed_data[region].low_uncertainty);
			return regionColours(uncertainty.urgency);
		})
});



//*********************//
//	Custom functions   //
//*********************//



//
//	Get various values:
//		getName
//		getUncertainty
//		getUrgency
//



// get the name of a region based on its index, stored in the id of the path data
var getName = function(index) {
	return selectedFeatures[index];
}

// calculate the uncertainty values of a region
var getUncertainty = function(upper, lower) {
	var mean = (upper + lower)/2;
	var confidence = upper - lower;
	return {"lower" : lower,
			"upper" : upper,
			"mean" : mean,
			"confidence" : upper - lower,
			"urgency" : getUrgency(confidence, mean)
		}
}

// calculate the urgency value we are using to colour the region
var getUrgency = function(confidence, mean) {
	// how urgent is the action?
	var urgency;

	confidenceRatio = .3;
	uncertaintyRatio = .6;

	if (confidence > uncertaintyLimits.upper * confidenceRatio) {
		// low confidence and low mean
		if (mean < uncertaintyLimits.upper * uncertaintyRatio) {
			urgency = 2
		}
		// low confidence and high mean
		else {
			urgency = 3
		}
	}
	else {
		// high confidence and low mean
		if (mean < uncertaintyLimits.upper * uncertaintyRatio) {
			urgency = 1
		}
		// high confidence and high mean
		else {
			urgency = 4
		}	
	}
	return urgency;
}



//
//	Update displays etc:
//		updateFeedback
//


// update the feedback on a region when clicked
var updateFeedback = function(index) {
	console.log("clicked " + selectedFeatures[index]);
}