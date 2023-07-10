import * as d3 from "d3";
import DataUtils from "@/functions/DataUtils";
import ComputeUtils from "@/functions/ComputeUtils";

export default {
    composeSheets,
    composeAxis,
    computeSheetsCoordinates,
    sheetsDataToBox,
    dataToCoordinates,
    composeScales,
    marginConvention,
    sheetCoordinatesToScale,
    getParetoFronts,
}


function sheetCoordinatesToScale(sheetsData, xScale, yScale, logScale) {
    /**
     * Convert coordinates to d3 scale
     * **/
    let sheetsScale = new Map();
    for (let [nodeId, sheetData] of sheetsData.entries()) {
        let points = [];
        sheetData.forEach(point => {
            if (logScale && point.y === 0) {
                point.y = -0.1;
            }
            points.push({"x": xScale(point.x), "y": yScale(point.y)});
        })
        sheetsScale.set(nodeId, points);
    }
    return sheetsScale;
}

function composeScales(treeInfo, figureInfo, logScale) {
    /**
     * Compose the scales of the d3 graph
     * **/
    let [minimal, , minTime, maxTime] = DataUtils.parseTreeData(treeInfo);
    let xScale, yScale;
    if (logScale) {
        // xScale = d3.scaleLog().domain([1, maxTime]).range([0, figureInfo.width]);
        xScale = d3.scaleLinear().domain([minTime, maxTime]).range([0, figureInfo.width]);
        yScale = d3.scaleLog().domain([minimal, -0.1]).range([figureInfo.height, 0]);
    } else {
        xScale = d3.scaleLinear().domain([minTime, maxTime]).range([0, figureInfo.width]);
        yScale = d3.scaleLinear().domain([minimal, 0]).range([figureInfo.height, 0]);
    }

    return [xScale, yScale];
}

function computeSheetsCoordinates(treeInfo, nodeData, rotate) {
    /**
     * Convert each node to corner points of the sheets
     * **/
    let maxTime = treeInfo.maxTime;
    let sheetsData = new Map();
    nodeData.forEach(node => {
        let points = [];
        let [x, y] = rotate ? ComputeUtils.rotateValues(node.step_back.unrotated_t, node.step_back.unrotated_y) : [node.step_back.unrotated_t, node.step_back.unrotated_y];
        points.push({"x": x, "y": y});
        [x, y] = rotate ? ComputeUtils.rotateValues(maxTime, node.step_back.unrotated_y) : [maxTime, node.step_back.unrotated_y];
        points.push({"x": x, "y": y});
        [x, y] = rotate ? ComputeUtils.rotateValues(maxTime, node.minimal) : [maxTime, node.minimal];
        points.push({"x": x, "y": y});
        [x, y] = rotate ? ComputeUtils.rotateValues(node.minimal_time, node.minimal) : [node.minimal_time, node.minimal];
        points.push({"x": x, "y": y});
        // sheetsData[node.node_id] = points;
        sheetsData.set(node.node_id, points);
    });
    return sheetsData;
}


function sheetsDataToBox(sheetsData) {
    /**
     * Get the bounding box of the graph
     * **/
    let [minTime, maxTime] = [0, 0];
    let [maximal, minimal] = [0, -1];
    for (let sheetData of sheetsData.values()) {
        sheetData.forEach(point => {
            if (point.x < minTime) {
                minTime = point.x;
            }
            if (point.x > maxTime) {
                maxTime = point.x;
            }
            if (point.y > maximal) {
                maximal = point.y;
            }
            if (point.y < minimal) {
                minimal = point.y;
            }
        })
    }
    return {"minimal": minimal, "maximal": maximal, "minTime": minTime, "maxTime": maxTime}
}

function composeSheets(sheetsData) {
    /**
     * Compose sheets path from d3 scales
     * **/
    let sheets = new Map();
    for (let [node_id,sheetData] of sheetsData.entries()) {
        let p = d3.path();
        let points = sheetData;
        p.moveTo(points[0].x, points[0].y);
        p.lineTo(points[1].x, points[1].y);
        p.lineTo(points[2].x, points[2].y);
        p.lineTo(points[3].x, points[3].y);
        p.closePath();
        sheets.set(node_id,p);
        // sheets[node_id] = p;
    }
    return sheets;
}

function getParetoFronts(sheetsData){
    /**
     * Compute the pareto fronts.
     * Line from point 2 to point 3 is automatically a Pareto front,
     * Line from point 3 to point 0 is determined by slope
     * **/
    let fronts = [];
    for (let [,sheetData] of sheetsData.entries()) {
        let points = sheetData;
        fronts.push([{x: points[2].x, y: points[2].y} , {x: points[3].x,y:points[3].y}])
        if (points[3].x > points[0].x){
            fronts.push([{x: points[0].x, y: points[0].y} , {x: points[3].x,y:points[3].y}])
        }
    }
    console.log(fronts)
    return fronts;
}

function composeAxis(xScale, yScale) {
    let xAxis = d3.axisBottom().scale(xScale);
    let yAxis = d3.axisLeft().scale(yScale);
    return {"xAxis": xAxis, "yAxis": yAxis};
}

function marginConvention(figureInfo, margin) {
    let innerWidth = figureInfo.width - margin.left - margin.right;
    let innerHeight = figureInfo.height - margin.top - margin.bottom;
    return [innerWidth, innerHeight]
}

function dataToCoordinates(solverData, xScale, yScale, rotate) {
    let coordinates = [];

    solverData.forEach(dataPoint => {
        let x, y;
        if (rotate) {
            x = xScale(dataPoint.y1);
            y = yScale(dataPoint.y2);
        } else {
            x = xScale(dataPoint.t);
            y = yScale(dataPoint.y_org);

        }
        coordinates.push({"x": x, "y": y});
    })
    return coordinates;
}
