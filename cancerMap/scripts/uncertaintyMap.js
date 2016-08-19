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
	.scale(2000)
	.translate([-svgDimensions.width * 5.33, -svgDimensions.height  *1.4])
	.precision(1);

var path = d3.geoPath()
	.projection(projection);

// define the svg size
svg.attr("width", svgDimensions.width)
	.attr("height", svgDimensions.height);

// add a group where the map will live
mapCanvas = svg.append("g");

// expose the data to the browser, while testing
var r;

// load some data
d3.json("data/qld_slas.json", function(error, regions) 
{
	if (error) return (console.log(error));
	
	var r = regions;
	// add a new set of objects to draw on the map
	r.objects.selected_slas = {"type": "GeometryCollection", "geometries":[]};

	// s = regions;
	// for each feature that we selected to show...
	for (var i = 0; i < selectedFeatures.length; i++)
	{
		// console.log("checking for " + selectedFeatures[i])
		// check the list of features...
		for (var j = 0; j < r.objects.qld_slas.geometries.length; j++)
		{
			// and if we have the right one...
			if (selectedFeatures[i] === r.objects.qld_slas.geometries[j].id)
			{
				// console.log("found matching area!");
				// push it onto the list of regions we want to show
				r.objects.selected_slas.geometries = r.objects.qld_slas.geometries[j];
				r.objects.selected_slas.geometries.id = i;

				// draw this region to the page.
				mapCanvas.insert("path", "mapRegion")
					.datum(topojson.feature(r, r.objects.selected_slas.geometries))
					.attr("class", "mapRegion")
					.attr("d", path);
			}
		}
	}
	d3.select(".vis").style("border", "1px #222 solid");
	d3.selectAll(".mapRegion")
		.on("mouseover", function(d){
			console.log(selectedFeatures[d.id] + ": " + d.id);
	})
});

