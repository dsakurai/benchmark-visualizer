import axios from "axios";

export default {
    getDemoData,
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