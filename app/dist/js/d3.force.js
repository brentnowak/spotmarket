/**
 * Append graph to DOM.
 * @param  {{
 *         		label: string,
 *         		selector: string
 * 				 }} options
 */
function graphForce(options) {

	options = _.extend({
		json: '',
		label: '',
		selector: 'body'
	}, options);

    var width = 620,
        height = 340

    var svg = d3.select(options.selector).append("svg")
        .attr("width", width)
        .attr("height", height);

    var force = d3.layout.force()
        .gravity(0.05)
        .distance(35)
        .charge(-25)
        .size([width, height]);

    d3.json(options.json, function(error, json) {
      if (error) throw error;

      force
          .nodes(json.nodes)
          .links(json.links)
          .start();

      var link = svg.selectAll(".link")
          .data(json.links)
        .enter().append("line")
          .attr("class", "link");

      var node = svg.selectAll(".node")
          .data(json.nodes)
        .enter().append("g")
          .attr("class", "node")
          .call(force.drag);

      node.append("image")
          .attr("xlink:href", "/dist/images/circle-outline-16.gif")
          .attr("x", -8)
          .attr("y", -8)
          .attr("width", 16)
          .attr("height", 16);

      node.append("text")
          .attr("dx", 12)
          .attr("dy", ".35em")
          .text(function(d) { return d.name });

      force.on("tick", function() {
        link.attr("x1", function(d) { return d.source.x; })
            .attr("y1", function(d) { return d.source.y; })
            .attr("x2", function(d) { return d.target.x; })
            .attr("y2", function(d) { return d.target.y; });

        node.attr("transform", function(d) { return "translate(" + d.x + "," + d.y + ")"; });
      });
    });

}
