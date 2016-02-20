/**
 * Append graph to DOM.
 * @param  {{
 *         		label: string,
 *         		selector: string
 *              width: int
 *              height: int
 *              legend: string
 *              marginright: int
 *              marginleft: int
 *              ylegend: string
 *              dateformat: string
 * 				 }} options
 */
function graph(options) {

	options = _.extend({
		json: '',
		label: '',
		selector: 'body',
		width: 960,
		height: 500,
		legend: 480,
		marginright: 80,
		marginleft: 50,
		ylegend: 'price',
		dateformat: '%Y-%m-%d %H:%M:%S'
	}, options);

	var margin = {top: 20, right: options.marginright, bottom: 50, left: options.marginleft},
	    width = options.width - margin.left - margin.right,
	    height = options.height - margin.top - margin.bottom;

	var parseDate = d3.time.format(options.dateformat).parse;

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

var svg = d3.select(options.selector).append("svg")
	    .attr("width", width + margin.left + margin.right)
	    .attr("height", height + margin.top + margin.bottom)
	    .attr("class", "graph-svg-component")
	  .append("g")
	    .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

    // Initialize empty array
    var data = [];

    // Get JSON data and wait for the response
    d3.json("/api/d3/17932", function(error, json) {

      $.each(json, function(d,i){
        data.push({
          timestamp: i.timestamp,
          temperature: i.avgPrice
        })
      })

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
	      .text(options.ylegend)
	      .style("font-size","10px");

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
	      .style("font-size","10px")
	      .text(function(d) { return d.name; });

	  legend = svg.append("g")
	    .attr("class","legend")
	    .attr("transform","translate(50,10)")
	    .style("font-size","10px")
	    .call(d3.legend)

	svg.append("text")
	        .attr("x", (width / 2))
	        .attr("y", options.legend - (margin.top / 2))
	        .attr("text-anchor", "middle")
	        .style("font-size", "14px")
	        .text(options.label);
	});
}

graph({
    width: 580,
    height: 340,
    marginright: 50,
    marginleft: 80,
    selector: '.d3-graph-price-17932',
    json: '/api/d3/17932'
});
