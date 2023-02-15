<template>
    <el-container>
        <el-main>
            <el-row>
                <el-col :span="12">
                    <svg id="reebSpace"></svg>
                </el-col>
            </el-row>
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
            let width = 800;
            let height = 800;
            let data = [10, 15, 20, 25, 30];
            let xScale = d3.scaleLinear().domain([0, d3.max(data)]).range([0, width - 100]);
            let yScale = d3.scaleLinear().domain([0, d3.max(data)]).range([height /2 , 0]);
            this.svg = d3.select("#reebSpace").attr("width", width).attr("height", height);
            let xAxis = d3.axisBottom().scale(xScale);
            let yAxis = d3.axisLeft().scale(yScale);
            this.svg.append("g").attr("transform", "translate(50, 10)").call(yAxis);
            let xAxisTranslate = height/2 + 10;
            this.svg.append("g").attr("transform", "translate(50, " + xAxisTranslate  +")").call(xAxis);
            // this.svg.append("g").call(grid);
        }
    },
}
</script>

<style scoped>
#reebSpaceContainer {
    margin-left: 0;
}
</style>