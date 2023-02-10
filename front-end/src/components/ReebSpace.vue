<template>
    <el-container>
        <el-main>
            <svg id="reebSpace"></svg>
        </el-main>
    </el-container>
</template>

<script>
import * as d3 from 'd3';

export default {
    name: "ReebSpace",
    data() {
        return {}
    },
    mounted() {
        this.loadInitialGraph();
    },
    methods: {
        loadInitialGraph() {
            let width = 400;
            let height = 100;
            let data = [10, 20, 30, 40, 50];
            let scale = d3.scaleLinear().domain([d3.min(data), d3.max(data)]).range([0, width - 100]);
            this.svg = d3.select("#reebSpace").attr('viewBox', [0, 0, width, height]);
            let xAxis = d3.axisBottom().scale(scale);
            let yAxis = d3.axisLeft().scale(scale);
            this.svg.append("g").call(xAxis);
            this.svg.append("g").call(yAxis);
            // this.svg.append("g").call(grid);
        }
    },
}
</script>

<style scoped>

</style>