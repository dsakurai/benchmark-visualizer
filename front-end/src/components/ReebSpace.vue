<template>
    <el-row>
        <el-col :span="22">
            <svg id="reebSpace"></svg>
        </el-col>
        <el-col :span="2">
            <el-row>
                <el-switch v-model="rotate" active-text="Rotate" inactive-text="Normal" @change="rotateGraph"/>
            </el-row>
            <el-row>
                <el-switch v-model="logScale" active-text="Log" inactive-text="Linear"/>
            </el-row>
        </el-col>
    </el-row>
</template>

<script>
import * as d3 from 'd3';
import axios from 'axios';
import GraphUtils from "@/functions/GraphUtils";
import DataUtils from "@/functions/DataUtils";

export default {
    name: "ReebSpace",
    props: {
        solverData: Array,
    },
    watch: {
        solverData: function (oldVal, newVal) {
            this.plotSolverData(newVal);
        },
    },
    data() {
        return {
            reebData: [],
            figureInfo: {
                "width": 800,
                "height": 800,
            },
            promisedReebData: '',
            treeInfo: '',
            nodeInfo: '',
            svg: '',
            rotate: false,
            logScale: false,
        }
    },
    mounted() {
        this.getReebInfo();

    },
    methods: {
        plotSolverData(solverData) {
            let coordinatesData = GraphUtils.dataToCoordinates(this.treeInfo, {
                "width": this.figureWidth,
                "height": this.figureHeight
            }, solverData);
            this.svg.selectAll('circle').remove();
            coordinatesData.forEach(d => {
                this.svg
                    .append("circle")
                    .attr("cx", d.x)
                    .attr("cy", d.y)
                    .attr("r", 3)
            })
        },
        getReebInfo() {
            axios.get("/api/reeb_space").then(response => {
                this.reebData = response.data;
                this.loadInitialGraph();
                let reebData = DataUtils.parseReebData(response.data);
                this.treeInfo = reebData.treeInfo;
                this.nodeInfo = reebData.nodeInfo;



                let {xAxis, yAxis} = GraphUtils.composeAxis(this.treeInfo, this.figureInfo, this.rotate);

                this.svg = d3.select("#reebSpace").attr("width", this.figureInfo.width).attr("height", this.figureInfo.height);
                let xAxisTranslate = this.figureInfo.width / 2 + 10;
                this.svg.append("g").attr("transform", "translate(50, 10)").call(yAxis);
                this.svg.append("g").attr("transform", "translate(50, " + xAxisTranslate + ")").call(xAxis);
                let sheets = GraphUtils.composeSheets(this.treeInfo, this.figureInfo, this.nodeInfo, this.rotate);

                for (let node_id in sheets) {
                    this.svg.append("path")
                        .attr("id", node_id)
                        .attr("d", sheets[node_id])
                        .attr("transform", "translate(100,10)")
                        .style("fill", '#' + Math.floor(Math.random() * 16777215).toString(16))
                        .style("stroke", "black")
                        .style("opacity", 0.5);
                }

            })
        },
        rotateGraph() {
            d3.selectAll("svg > *").remove();
            let sheetsCoordinates = GraphUtils.computeSheetsCoordinates(this.treeInfo, this.figureInfo, this.nodeInfo, this.rotate);
            let viewBox = GraphUtils.sheetsDataToBox(sheetsCoordinates);
            let {xAxis, yAxis} = GraphUtils.composeAxisBySheets(this.figureInfo, viewBox);
            let sheets = GraphUtils.composeSheetsV2(viewBox,this.figureInfo,sheetsCoordinates);
            this.svg = d3.select("#reebSpace").attr("width", this.figureInfo.width).attr("height", this.figureInfo.height);
            let xAxisTranslate = this.figureInfo.width / 2 + 10;
            this.svg.append("g").attr("transform", "translate(50, 10)").call(yAxis);
            this.svg.append("g").attr("transform", "translate(50, " + xAxisTranslate + ")").call(xAxis);
            for (let node_id in sheets) {
                this.svg.append("path")
                    .attr("id", node_id)
                    .attr("d", sheets[node_id])
                    .attr("transform", "translate(0,10)")
                    .style("fill", '#' + Math.floor(Math.random() * 16777215).toString(16))
                    .style("stroke", "black")
                    .style("opacity", 0.5);
            }
        },
        drawAxis() {

        },
        drawSheets() {

        },
        loadInitialGraph() {
            this.drawAxis();
            this.drawSheets();
        }
    },
}
</script>

<style scoped>
#reebSpaceContainer {
    margin-left: 0;
}
</style>