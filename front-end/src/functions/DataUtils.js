import axios from "axios";
import ComputeUtils from "@/functions/ComputeUtils";

export default {
    getDemoData,
    parseReebData,
    parseTreeData,
}

function parseReebData(reebData){
    let nodeInfo = reebData.nodeInfo;
    let treeInfo = reebData.treeInfo;
    return {"nodeInfo":nodeInfo, "treeInfo":treeInfo}
}

function getDemoData(){
    axios.get("/api/demo_data").then(response => {
        this.logData = response.data.solver_log;
        this.allIDs = response.data.all_ids;
        this.treeData = response.data.tree;
        this.totalSteps = this.logData.length;
        this.stepSize = 100 / this.totalSteps * this.populationSize;
        this.marks[0] = "0";
        this.marks[100] = this.totalSteps.toString();
        this.stepRange = Math.round(this.totalSteps / this.populationSize);
        for (let i = 0; i < this.totalSteps; i++) {
            this.solverData[this.logData[i].step] = this.logData[i];
        }
        this.filteredSolverData = this.solverData;
        this.getStats();
    })
}

/**
 *
 * @param {Dictionary} treeInfo
 * @param {Boolean} rotate
 * @returns {{maxTime: *, minimal: *, minTime: *, maximal: *}}
 */
function parseTreeData(treeInfo, rotate){
    let minimal = treeInfo.minimal;
    let maximal = treeInfo.maximal;
    let minTime = treeInfo.minTime;
    let maxTime = treeInfo.maxTime;

    if (rotate){
        minimal = ComputeUtils.rotateValues(maxTime,minimal)[1];
        maxTime = ComputeUtils.rotateValues(maxTime,0)[0];
        let temp = minTime;
        minTime = ComputeUtils.rotateValues(minTime,minimal)[0];
        maximal = ComputeUtils.rotateValues(temp,maximal)[1];
    }


    return [minimal,maximal,minTime,maxTime]
}