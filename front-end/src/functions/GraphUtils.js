import * as d3 from "d3";

export default {
    composeSheet,
    composeAxis,
}

function composeSheet(nodeData){
    console.log(nodeData);
    // let line = d3.line()
    //     .x(function (d) {
    //         return d.x;
    //     })
    //     .y(function (d) {
    //         return d.y;
    //     });
    let points = [{x: 100, y: 100}, {x: 500, y: 100}, {x: 125, y: 150}, {x: 375, y: 150}];
    let p = d3.path();
    p.moveTo(points[0].x,points[0].y);
    p.lineTo(points[1].x,points[1].y);
    p.lineTo(points[3].x,points[3].y);
    p.lineTo(points[2].x,points[2].y);
    p.closePath();
    nodeData.forEach(node => {
      console.log(node);
    })
    return p;
}
function composeAxis(treeInfo, figureInfo){
    let minimal = treeInfo.minimal;
    let maximal = treeInfo.maximal;
    let maxTime = treeInfo.maxTime;
    // let nodeCount = treeInfo.nodeCount;
    let width = figureInfo.width;
    let height = figureInfo.height;

    let xScale = d3.scaleLinear().domain([0, maxTime]).range([0, width - 100]);
    let yScale = d3.scaleLinear().domain([minimal, maximal ]).range([height / 2, 0]);
    let xAxis = d3.axisBottom().scale(xScale);
    let yAxis = d3.axisLeft().scale(yScale);

    return {"xAxis":xAxis, "yAxis": yAxis};

}
