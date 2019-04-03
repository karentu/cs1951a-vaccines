const file = "/Users/jennifernino/cs1951-proj/cs1951a-vaccines/complete.csv";
d3.csv("https://raw.githubusercontent.com/karentu/cs1951a-vaccines/master/complete.csv",
  function(data) {
    // console.log(data[0]);
    let year = '2015';
    let counties_2015 = new Set();
    let obj_arr = [];

    for (let i = 0; i < data.length; i += 1) {
      if (year === data[i].school_year) {
        // console.log(data[i].school_year)
        if (counties_2015.has(data[i].county)) {
          for (let k = 0; k < obj_arr.length; k += 1) {
            if (obj_arr[k].county === data[i].county) {

              obj_arr[k].k12_enrollment += parseInt(data[i].k12_enrollment);
              obj_arr[k].all_immunizations += parseInt(data[i].all_immunizations);
            }
          }
        } else {
          counties_2015.add(data[i].county);
          obj_arr.push(
            {
              county:data[i].county,
              k12_enrollment:parseInt(data[i].k12_enrollment), // TODO: not a number,
              all_immunizations:parseInt(data[i].all_immunizations),
              vaccination_percent:0 // TODO: calculate after
            }
          );
        }
      }
    }

    for (let c = 0; c < obj_arr.length; c += 1) {
      obj_arr[c].vaccination_percent =
      (obj_arr[c].all_immunizations * 100.0) / obj_arr[c].k12_enrollment;
    }

    console.log(obj_arr);

    // set the dimensions and margins of the graph
    var margin = {top: 20, right: 20, bottom: 30, left: 40},
        width = 1500 - margin.left - margin.right,
        height = 500 - margin.top - margin.bottom;

    // set the ranges
    var x = d3.scaleBand()
              .range([0, width])
              .padding(0.1);
    var y = d3.scaleLinear()
              .range([height, 0]);

    // append the svg object to the body of the page
    // append a 'group' element to 'svg'
    // moves the 'group' element to the top left margin
    var svgWidth = 1000, svgHeight = 300, barPadding = 5;
    var barWidth = (svgWidth / obj_arr.length);
    var svg = d3.select("body").append("svg")
        .attr("width", width + margin.left + margin.right)
        .attr("height", height + margin.top + margin.bottom)
      .append("g")
        .attr("transform",
              "translate(" + margin.left + "," + margin.top + ")");

      // Scale the range of the data in the domains
      x.domain(obj_arr.map(function(d) { return d.county; }));
      y.domain([0, 100]);
      //y.domain([0, d3.max(obj_arr, function(d) { return d.vaccination_percent; })]);

      // append the rectangles for the bar chart
      // var barChart = svg.selectAll("rect") // select rectangles
      //   .data(obj_arr) // call data
      //   .enter()
      //   .append("rect")
      //   .attr("y", function(elem,index) {
      //     return svgHeight - (elem.vaccination_percent * 100);
      //   })
      //   .attr("height", function(elem,index) {
      //     return elem.vaccination_percent * 100;
      //   })
      //   .attr("width", barWidth - barPadding)
      //   .attr("transform", function(elem,index) {
      //     let translate = [barWidth * index, 0]
      //     return "translate(" + translate + ")";
      //   });

      svg.selectAll(".bar")
          .data(obj_arr)
          .enter()
          .append("rect")
          .attr("class", "bar")
          .attr("x", function(d,i) { return x(d.county); })
          .attr("width", x.bandwidth())
          .attr("y", function(d,i) { console.log(y(d.vaccination_percent));
            return y(d.vaccination_percent); })
          .attr("height", function(d,i) { return height - y(d.vaccination_percent); });

      // add the x Axis
      svg.append("g")
          .attr("transform", "translate(0," + height + ")")
          .call(d3.axisBottom(x));

      // add the y Axis
      svg.append("g")
          .call(d3.axisLeft(y));

    // var svgWidth = 1000, svgHeight = 300, barPadding = 5;
    // var barWidth = (svgWidth / obj_arr.length);
    // var svg = d3.select('svg')
    //   .attr("width", svgWidth)
    //   .attr("height", svgHeight);
    //
    // var barChart = svg.selectAll("rect") // select rectangles
    //   .data(obj_arr) // call data
    //   .enter()
    //   .append("rect")
    //   .attr("y", function(elem,index) {
    //     return svgHeight - (elem.vaccination_percent * 100);
    //   })
    //   .attr("height", function(elem,index) {
    //     return elem.vaccination_percent * 100;
    //   })
    //   .attr("width", barWidth - barPadding)
    //   .attr("transform", function(elem,index) {
    //     let translate = [barWidth * index, 0]
    //     return "translate(" + translate + ")";
    //   });
});
