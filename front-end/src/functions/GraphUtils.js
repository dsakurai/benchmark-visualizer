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
}


function sheetCoordinatesToScale(sheetsData, xScale, yScale, logScale) {
    let sheetsScale = {}
    for (let nodeId in sheetsData) {
        let points = [];
        sheetsData[nodeId].forEach(point => {
            if (logScale && point.y === 0) {
                point.y = -0.1;
            }
            points.push({"x": xScale(point.x), "y": yScale(point.y)});
        })
        sheetsScale[nodeId] = points;
    }
    return sheetsScale;
}

function composeScales(treeInfo, figureInfo, logScale) {
    let [minimal, maximal, minTime, maxTime] = DataUtils.parseTreeData(treeInfo);
    console.log(maximal);
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
    let maxTime = treeInfo.maxTime;
    let sheetsData = {};
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
        sheetsData[node.node_id] = points;
    });
    return sheetsData;
}


function sheetsDataToBox(sheetsData) {
    let [minTime, maxTime] = [0, 0];
    let [maximal, minimal] = [0, -1];
    for (let node_id in sheetsData) {
        let points = sheetsData[node_id];
        points.forEach(point => {
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
    let sheets = {};
    for (let node_id in sheetsData) {
        let p = d3.path();
        let points = sheetsData[node_id]
        p.moveTo(points[0].x, points[0].y);
        p.lineTo(points[1].x, points[1].y);
        p.lineTo(points[2].x, points[2].y);
        p.lineTo(points[3].x, points[3].y);
        p.closePath();
        sheets[node_id] = p;
    }
    return sheets;
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
        let x,y;
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