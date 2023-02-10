<template>
    <svg id="d3tree"></svg>
</template>

<script>
import axios from 'axios';
import * as d3 from 'd3';


export default {
    name: "SolverVisualizer",
    data() {

    },
    getNaiveLogData() {
        axios.get("/api/demo_data").then(response => {
            this.logData = response.data.solver_log;
            this.treeData = response.data.tree;
            this.totalSteps = this.logData.length;
            this.stepSize = 100 / this.totalSteps;
            this.marks[0] = "0";
            this.marks[100] = this.totalSteps.toString();
            for (let i = 0; i < this.totalSteps; i++) {
                this.solverData[this.logData[i].step] = this.logData[i];
            }
        })
    }
}

</script>

<style scoped>

</style>