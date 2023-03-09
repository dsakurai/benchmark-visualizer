<template>
    <el-row>
        <el-col :span="22">
            <div id="reebSpace"></div>
        </el-col>
        <el-col :span="2">
            <el-row>
                <el-switch v-model="rotate" active-text="Rotate" inactive-text="Normal" @change="rotateGraph"/>
            </el-row>
            <el-row>
                <el-switch v-model="logScale" active-text="Log" inactive-text="Linear" @change="rotateGraph"/>
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
        treeName: String,
        dimension: Number,
    },
    watch: {
        solverData: function (oldVal, newVal) {
            this.plotSolverData(newVal);
        },
        treeName: function () {
            this.getReebInfo();
        },
        dimension: function () {
            this.getReebInfo();
        },
    },
    data() {
        return {
            reebData: [],
            figureInfo: {
                "width": 800,
                "height": 600,
            },
            margin:{
                left:40,
                right:20,
                top:20,
                bottom:20,
            },
            innerWidth:760,
            innerHeight:760,
            promisedReebData: '',
            treeInfo: '',
            nodeInfo: '',
            svg: '',
            rotate: false,
            logScale: false,
            xScale : '',
            yScale : '',
        }
    },
    created(){
        [this.innerWidth, this.innerHeight] = GraphUtils.marginConvention(this.figureInfo,this.margin);
    },
    mounted() {
        this.getReebInfo();
    },
    methods: {
        plotSolverData(solverData) {
            let coordinatesData = GraphUtils.dataToCoordinates(solverData, this.xScale,this.yScale, this.rotate);
            this.svg.selectAll('circle').remove();
            coordinatesData.forEach(d => {
                this.svg
                    .append("circle")
                    .attr("cx", d.x)
                    .attr("cy", d.y)
                    .attr("r", 3)
                    .attr("transform", `translate(${this.margin.left},${this.margin.top})`);
            })
        },
        getReebInfo() {
            axios.get(`/api/reeb_space?tree_name=${this.treeName}&dimension=${this.dimension}`).then(response => {
                d3.selectAll("svg").remove();
                this.reebData = response.data;
                let reebData = DataUtils.parseReebData(response.data);
                this.$message.success("Reeb space data loaded");
                this.treeInfo = reebData.treeInfo;
                this.nodeInfo = reebData.nodeInfo;
                this.svg = d3.select("#reebSpace").append("svg").attr("width", this.figureInfo.width).attr("height", this.figureInfo.height);
                [this.xScale, this.yScale] = GraphUtils.composeScales(this.treeInfo, {"width":this.innerWidth,"height": this.innerHeight},this.logScale);
                this.drawAxis();
                this.drawSheets();
            }).catch(error => {
                this.$message.error("Reeb space data failed @ " + error.toString());
            });
        },
        rotateGraph() {
            d3.selectAll("svg > *").remove();
            let sheetsCoordinates = GraphUtils.computeSheetsCoordinates(this.treeInfo, this.nodeInfo, this.rotate);
            let boundingBox = GraphUtils.sheetsDataToBox(sheetsCoordinates);
            [this.xScale, this.yScale] = GraphUtils.composeScales(boundingBox, {"width":this.innerWidth,"height": this.innerHeight}, this.logScale);
            this.drawAxis()
            let sheetsScale = GraphUtils.sheetCoordinatesToScale(sheetsCoordinates,this.xScale, this.yScale, this.logScale);
            let sheets = GraphUtils.composeSheets(sheetsScale);
            for (let node_id in sheets) {
                this.svg.append("path")
                    .attr("id", node_id)
                    .attr("d", sheets[node_id])
                    .attr("transform", `translate(${this.margin.left},${this.margin.top})`)
                    .style("fill", '#' + Math.floor(Math.random() * 16777215).toString(16))
                    .style("stroke", "black")
                    .style("opacity", 0.5);
            }
        },
        drawAxis() {
            let {xAxis, yAxis} = GraphUtils.composeAxis(this.xScale, this.yScale);
            this.svg.append("g").attr("transform", `translate(${this.margin.left},${this.margin.top})`).call(yAxis);
            this.svg.append("g").attr("transform", `translate(${this.margin.left},${this.innerHeight + this.margin.top})`).call(xAxis);
        },
        drawSheets() {
            let sheetsCoordinates = GraphUtils.computeSheetsCoordinates(this.treeInfo,this.nodeInfo, this.rotate);
            let sheetsScale = GraphUtils.sheetCoordinatesToScale(sheetsCoordinates,this.xScale, this.yScale, this.logScale);
            let sheets = GraphUtils.composeSheets(sheetsScale);
            for (let node_id in sheets) {
                this.svg.append("path")
                    .attr("id", node_id)
                    .attr("d", sheets[node_id])
                    .attr("transform", `translate(${this.margin.left},${this.margin.top})`)
                    .style("fill", '#' + Math.floor(Math.random() * 16777215).toString(16))
                    .style("stroke", "black")
                    .style("opacity", 0.5);
            }
        },
    },
}
</script>

<style scoped>
#reebSpaceContainer {
    margin-left: 0;
}
</style>