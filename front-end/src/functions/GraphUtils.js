import * as d3 from "d3";

export default {
    composeSheets,
    composeAxis,
    dataToCoordinates,
}

function composeSheets(treeInfo, figureInfo, nodeData){
    let minimal = treeInfo.minimal;
    // Maximal = -1
    let maximal = treeInfo.maximal;
    let maxTime = treeInfo.maxTime;
    let width = figureInfo.width;
    let height = figureInfo.height;

    let yRange = maximal - minimal;
    let xRange = maxTime;


    let yInterval = height / yRange / 2;
    let xInterval = width / xRange;

    let sheetsData = {};

    nodeData.forEach(node => {
        let points = []
        points.push({"y": (maximal - node.step_back.unrotated_y) * yInterval , "x": node.step_back.unrotated_t * xInterval});
        points.push({"y":(maximal - node.step_back.unrotated_y) * yInterval, "x":maxTime * xInterval});
        points.push({"y": (maximal - node.minimal) * yInterval, "x":maxTime * xInterval});
        points.push({"y": (maximal - node.minimal) * yInterval, "x":node.minimal_time * xInterval})
        sheetsData[node.node_id] = points;
    })

    let sheets = {}
    for (let node_id in sheetsData){
        let p = d3.path();
        let points = sheetsData[node_id]
        p.moveTo(points[0].x,points[0].y);
        p.lineTo(points[1].x,points[1].y);
        p.lineTo(points[2].x,points[2].y);
        p.lineTo(points[3].x,points[3].y);
        p.closePath();
        sheets[node_id] = p;
    }
    return sheets;
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
function dataToCoordinates(treeInfo, figureInfo, solverData){
    let minimal = treeInfo.minimal;
    // Maximal = -1
    let maximal = treeInfo.maximal;
    let maxTime = treeInfo.maxTime;
    let width = figureInfo.width;
    let height = figureInfo.height;

    let yRange = maximal - minimal;
    let xRange = maxTime;


    let yInterval = height / yRange / 2;
    let xInterval = width / xRange;

    let coordinates = [];

    solverData.forEach(dataPoint => {
        let x = dataPoint.t1 * xInterval;
        let y = (maximal - dataPoint.y_org) * yInterval;
        coordinates.push({"x":x, "y":y});
    })
    return coordinates;
}
