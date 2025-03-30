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
    increaseBrightness,
}

function increaseBrightness(color, percent) {
    // Parse the color (assuming it's in hex format, e.g., "#ff5733")
    const r = parseInt(color.slice(1, 3), 16);
    const g = parseInt(color.slice(3, 5), 16);
    const b = parseInt(color.slice(5, 7), 16);

    // Convert RGB to HSL
    const { h, s, l } = rgbToHsl(r, g, b);

    // Increase lightness by the specified percentage
    const newL = Math.min(100, l + percent);

    // Convert HSL back to RGB
    const { r: newR, g: newG, b: newB } = hslToRgb(h, s, newL);

    // Return new color in hex format
    return `#${((1 << 24) + (newR << 16) + (newG << 8) + newB).toString(16).slice(1)}`;
}

function rgbToHsl(r, g, b) {
    r /= 255;
    g /= 255;
    b /= 255;
    const max = Math.max(r, g, b);
    const min = Math.min(r, g, b);
    let h, s, l = (max + min) / 2;

    if (max === min) {
        h = s = 0; // achromatic
    } else {
        const d = max - min;
        s = l > 0.5 ? d / (2 - max - min) : d / (max + min);
        switch (max) {
            case r: h = (g - b) / d + (g < b ? 6 : 0); break;
            case g: h = (b - r) / d + 2; break;
            case b: h = (r - g) / d + 4; break;
        }
        h /= 6;
    }
    return { h: h * 360, s: s * 100, l: l * 100 };
}

function hslToRgb(h, s, l) {
    h /= 360;
    s /= 100;
    l /= 100;
    let r, g, b;

    if (s === 0) {
        r = g = b = l; // achromatic
    } else {
        const hue2rgb = (p, q, t) => {
            if (t < 0) t += 1;
            if (t > 1) t -= 1;
            if (t < 1 / 6) return p + (q - p) * 6 * t;
            if (t < 1 / 2) return q;
            if (t < 2 / 3) return p + (q - p) * (2 / 3 - t) * 6;
            return p;
        };
        const q = l < 0.5 ? l * (1 + s) : l + s - l * s;
        const p = 2 * l - q;
        r = hue2rgb(p, q, h + 1 / 3);
        g = hue2rgb(p, q, h);
        b = hue2rgb(p, q, h - 1 / 3);
    }
    return { r: Math.round(r * 255), g: Math.round(g * 255), b: Math.round(b * 255) };
}




function sheetCoordinatesToScale(sheetsData, xScale, yScale, logScale) {
    /**
     * Convert coordinates to d3 scale
     * **/
    let sheetsScale = new Map();
    for (let [nodeId, sheetData] of sheetsData.entries()) {
        let points = [];
        sheetData.forEach(point => {
            // This is to avoid inf problem in log scale
            // Since we don't use log scale display, this doesn't matter
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
        if (parseFloat(points[3].x.toFixed(10)) > parseFloat(points[0].x.toFixed(10))){
            fronts.push([{x: points[0].x, y: points[0].y} , {x: points[3].x,y:points[3].y}])
        }
    }
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
    let coordinates = {};

    solverData.forEach(dataPoint => {
        let eval_node_id = dataPoint.eval_node_id;
        if(!coordinates[eval_node_id]){
            coordinates[eval_node_id] = [];
        }
        let x, y;
        if (rotate) {
            x = xScale(dataPoint.y1);
            y = yScale(dataPoint.y2);
        } else {
            x = xScale(dataPoint.t);
            y = yScale(dataPoint.y_org);

        }
        coordinates[eval_node_id].push({"x": x, "y": y});
    })
    return coordinates;
}
