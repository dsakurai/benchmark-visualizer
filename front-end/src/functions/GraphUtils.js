import * as d3 from "d3";

export default {
    composeSheet: composeSheets,
    composeAxis,
}

function composeSheets(treeInfo, figureInfo, nodeData){
    dataToCoordinates(treeInfo, figureInfo, nodeData);

    let points = [{x: 100, y: 100}, {x: 500, y: 100}, {x: 125, y: 150}, {x: 375, y: 150}];
    let p = d3.path();
    p.moveTo(points[0].x,points[0].y);
    p.lineTo(points[1].x,points[1].y);
    p.lineTo(points[3].x,points[3].y);
    p.lineTo(points[2].x,points[2].y);
    p.closePath();
    return p;
}
function composeAxis(treeInfo, figureInfo){
    let minimal = treeInfo.minimal;
    let maximal = treeInfo.maximal;
    let maxTime = treeInfo.maxTime;
    let width = figureInfo.width;
    let height = figureInfo.height;

    let xScale = d3.scaleLinear().domain([0, maxTime]).range([0, width - 100]);
    let yScale = d3.scaleLinear().domain([minimal, maximal ]).range([height / 2, 0]);
    let xAxis = d3.axisBottom().scale(xScale);
    let yAxis = d3.axisLeft().scale(yScale);

    return {"xAxis":xAxis, "yAxis": yAxis};

}

function dataToCoordinates(treeInfo, figureInfo, nodeData){
    let minimal = treeInfo.minimal;
    let maximal = treeInfo.maximal;
    let maxTime = treeInfo.maxTime;
    let width = figureInfo.width;
    let height = figureInfo.height;

    let yRange = maximal - minimal;
    let xRange = maxTime;

    let yInterval = height / yRange;
    let xInterval = width / xRange;

    let sheetData = {};

    nodeData.forEach(node => {
        let points = []
        points.push({"y": (maximal - node.step_back.unrotated_y) * yInterval , "x": node.step_back.unrotated_t * xInterval});
        points.push({"y":(maximal - node.step_back.unrotated_y) * yInterval, "x":maxTime * xInterval});
        points.push({"y": (maximal - node.minimal) * yInterval, "x":maxTime * xInterval});
        points.push({"y": (maximal - node.minimal) * yInterval, "x":node.minimal_time * xInterval})
        sheetData[node.node_id] = points;
    })
    console.log(sheetData);
    console.log(treeInfo);
    return sheetData;

}
