queue()
    .defer(d3.json, "/noaa/data")
    // .defer(d3.json, "static/geojson/us-states.json")
    .await(makeGraphs);

function makeGraphs(error, noaaJson) {
	
	//Clean projectsJson data
	var mynoaadata = noaaJson;
	var dateFormat = d3.time.format("%Y%m%d%H%M");
	mynoaadata.forEach(function(d) {
		d["ts"] = dateFormat.parse(d["ts"]);
	});

	//Create a Crossfilter instance
	var ndx = crossfilter(mynoaadata);

	//Define Dimensions
	var dateDim = ndx.dimension(function(d) { return d["ts"]; });
	var tempDim = ndx.dimension(function(d) { return d["TEMP"]; });

    var loctemp = dateDim.group().reduceSum(function(d) { return d["TEMP"]; }); 

    
	//Define values (to be used in charts)
	var minDate = dateDim.bottom(1)[0]["ts"];
	var maxDate = dateDim.top(1)[0]["ts"];

    	var minTemp = tempDim.bottom(1)[0]["TEMP"];
	var maxTemp = tempDim.top(1)[0]["TEMP"];
    console.log(loctemp.size());
    
    //Charts
	var timeChart = dc.barChart("#time-chart");
	timeChart
		.width(600)
		.height(160)
	.margins({top: 10, right: 50, bottom: 30, left: 50})
		.dimension(dateDim)
	.group(loctemp)
	.valueAccessor(function (d) {
            return d.value;
        })
	.transitionDuration(0)
	.mouseZoomable(true)
		 .x(d3.time.scale().domain([minDate, maxDate]))
		//.x(d3.time.scale().domain([minTemp, maxTemp]))
	// 	// .elasticY(true)
	.xAxisLabel("Year");
	// .yAxis().ticks(4);


    dc.renderAll();

};
