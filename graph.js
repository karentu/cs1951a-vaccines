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
      (obj_arr[c].all_immunizations * 1.0) / obj_arr[c].k12_enrollment;
    }

    console.log(obj_arr);

    var svgWidth = 1000, svgHeight = 500, barPadding = 5;
    var barWidth = (svgWidth / obj_arr.length);
    var svg = d3.select('svg')
      .attr("width", svgWidth)
      .attr("height", svgHeight);

    var barChart = svg.selectAll("rect") // select rectangles
      .data(obj_arr) // call data
      .enter()
      .append("rect")
      .attr("y", function(elem,index) {
        return elem.vaccination_percent;
      })
      .attr("height", function(elem,index) {
        return elem.vaccination_percent * 100;
      })
      .attr("width", barWidth - barPadding)
        .attr("transform", function(elem,index) {
          let translate = [barWidth * index, 0]
          return "translate(" + translate + ")";
        });
});
