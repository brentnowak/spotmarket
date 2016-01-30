/**
 * Append graph to DOM.
 * @param  {{
 *         		csv: string,
 *         		label: string,
 *         		selector: string
 * 				 }} options
 */
function graph(options) {

	options = _.extend({
		csv: '',
		label: '',
		selector: 'body'
	}, options);

	var margin = {top: 20, right: 90, bottom: 50, left: 50},
	    width = 960 - margin.left - margin.right,
	    height = 500 - margin.top - margin.bottom;

	var parseDate = d3.time.format("%Y-%m-%d %H:%M:%S").parse;

	var x = d3.time.scale()
	    .range([0, width]);

	var y = d3.scale.linear()
	    .range([height, 0]);

	var color = d3.scale.category10();

	var xAxis = d3.svg.axis()
	    .scale(x)
	    .ticks(5)
	    .innerTickSize(-height)
	    .outerTickSize(0)
	    .orient("bottom");

	var yAxis = d3.svg.axis()
	    .scale(y)
	    .orient("left");

	var line = d3.svg.line()
	    .interpolate("basis")
	    .x(function(d) { return x(d.timestamp); })
	    .y(function(d) { return y(d.temperature); });

var svg = d3.select("body").append("svg")
	    .attr("width", width + margin.left + margin.right)
	    .attr("height", height + margin.top + margin.bottom)
	    .attr("class", "graph-svg-component")
	  .append("g")
	    .append(function() { return document.createElement("p") })
	    .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

	d3.tsv(options.csv, function(error, data) {
	  if (error) throw error;

	  color.domain(d3.keys(data[0]).filter(function(key) { return key !== "timestamp"; }));

	  data.forEach(function(d) {
	    d.timestamp = parseDate(d.timestamp);
	  });

	  var cities = color.domain().map(function(name) {
	    return {
	      name: name,
	      values: data.map(function(d) {
	        return {timestamp: d.timestamp, temperature: +d[name]};
	      })
	    };
	  });

	  x.domain(d3.extent(data, function(d) { return d.timestamp; }));

	  y.domain([
	    d3.min(cities, function(c) { return d3.min(c.values, function(v) { return v.temperature; }); }),
	    d3.max(cities, function(c) { return d3.max(c.values, function(v) { return v.temperature; }); })
	  ]);

	  svg.append("g")
	      .attr("class", "x axis")
	      .attr("transform", "translate(0," + height + ")")
	      .call(xAxis);

	  svg.append("g")
	      .attr("class", "y axis")
	      .call(yAxis)
	    .append("text")
	      .attr("transform", "rotate(-90)")
	      .attr("y", 6)
	      .attr("dy", ".71em")
	      .style("text-anchor", "end")
	      .text("SUM_factionKills");

	  var city = svg.selectAll(".city")
	      .data(cities)
	    .enter().append("g")
	      .attr("class", "city");

	  city.append("path")
	      .attr("class", "line")
	      .attr("d", function(d) { return line(d.values); })
	      .attr("data-legend",function(d) { return d.name})
	      .style("stroke", function(d) { return color(d.name); });

	  city.append("text")
	      .datum(function(d) { return {name: d.name, value: d.values[d.values.length - 1]}; })
	      .attr("transform", function(d) { return "translate(" + x(d.value.timestamp) + "," + y(d.value.temperature) + ")"; })
	      .attr("x", 3)
	      .attr("dy", ".35em")
	      .text(function(d) { return d.name; });

	  legend = svg.append("g")
	    .attr("class","legend")
	    .attr("transform","translate(50,10)")
	    .style("font-size","12px")
	    .call(d3.legend)

	svg.append("text")
	        .attr("x", (width / 2))
	        .attr("y", 480 - (margin.top / 2))
	        .attr("text-anchor", "middle")
	        .style("font-size", "14px")
	        .text(options.label);

	});

}

graph({
    selector: 'd3-graph-universe',
    csv: 'static/data/npckills_universe.csv',
    label: 'NPC Kill Rates per Security - 12H Resample - 1.5D Window'
});

graph({
    selector: 'd3-graph-angel',
    csv: 'static/data/npckills_regions_angel_cartel.csv',
    label: 'NPC Kill Rates per Region - Angel Cartel - 12H Resample - 1.5D Window'
});

graph({
    selector: 'd3-graph-angel-sum',
    csv: 'static/data/npckills_regions_angel_cartel_sum.csv',
    label: 'NPC Kill Rates for All Regions - Angel Cartel - 12H Resample - 1.5D Window'
});

graph({
    selector: 'd3-graph-blood',
    csv: 'static/data/npckills_regions_blood_raiders.csv',
    label: 'NPC Kill Rates per Region - Blood Raiders - 12H Resample - 1.5D Window'
});

graph({
    selector: 'd3-graph-blood-sum',
    csv: 'static/data/npckills_regions_blood_raiders_sum.csv',
    label: 'NPC Kill Rates for All Regions - Blood Raiders - 12H Resample - 1.5D Window'
});

graph({
    selector: 'd3-graph-guristas',
    csv: 'static/data/npckills_regions_guristas_pirate.csv',
    label: 'NPC Kill Rates per Region - Guristas Pirates - 12H Resample - 1.5D Window'
});

graph({
    selector: 'd3-graph-guristas-sum',
    csv: 'static/data/npckills_regions_guristas_pirates_sum.csv',
    label: 'NPC Kill Rates for All Regions - Guristas Pirates - 12H Resample - 1.5D Window'
});

graph({
    selector: 'd3-graph-sanshas',
    csv: 'static/data/npckills_regions_sanshas_nation.csv',
    label: 'NPC Kill Rates per Region - Sansha’s Nation - 12H Resample - 1.5D Window'
});

graph({
    selector: 'd3-graph-sanshas-sum',
    csv: 'static/data/npckills_regions_sanshas_nation_sum.csv',
    label: 'NPC Kill Rates for All Regions - Sansha’s Nation - 12H Resample - 1.5D Window'
});

graph({
    selector: 'd3-graph-serpentis',
    csv: 'static/data/npckills_regions_serpentis_corporation.csv',
    label: 'NPC Kill Rates per Region - Serpentis Corporation - 12H Resample - 1.5D Window'
});

graph({
    selector: 'd3-graph-serpentis-sum',
    csv: 'static/data/npckills_regions_serpentis_corporation_sum.csv',
    label: 'NPC Kill Rates for All Regions - Serpentis Corporation - 12H Resample - 1.5D Window'
});