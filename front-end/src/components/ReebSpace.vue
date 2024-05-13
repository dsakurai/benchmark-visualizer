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
                <el-switch v-model="displayFronts" active-text="Fronts" inactive-text="Normal" @change="rotateGraph"></el-switch>
            </el-row>
            <el-row>

            </el-row>
<!--            <el-row>-->
<!--                <el-switch v-model="logScale" active-text="Log" inactive-text="Linear" @change="rotateGraph"/>-->
<!--            </el-row>-->
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
        allIds: Array,
    },
    watch: {
        solverData: function (oldVal, newVal) {
            console.log(this.colorShapeMap);

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
            displayFronts: false,
            xScale : '',
            yScale : '',
            dataPointShapes:["circle","hollow-circle", "hollow-rect", "rect"],
            colorCodes: [
                "#DC143C",  // Crimson
                "#FF7F50",  // Coral
                "#4169E1",  // Royal Blue
                "#228B22",  // Forest Green
                "#DAA520",  // Goldenrod
                "#DDA0DD",  // Plum
                "#708090",  // Slate Gray
                "#FF8C00",  // Dark Orange
                "#40E0D0",  // Turquoise
                "#CD853F"   // Peru
            ],
            colorShapeMap: {},
        }
    },
    created(){
        [this.innerWidth, this.innerHeight] = GraphUtils.marginConvention(this.figureInfo,this.margin);
        this.createColorMap();

    },
    mounted() {
        this.getReebInfo();
        
    },
    methods: {
        createColorMap(){
            let combinations = [];
            for (let i = 0; i < this.dataPointShapes.length; i++) {
                for (let j = 0; j < this.colorCodes.length; j++) {
                    combinations.push([this.colorCodes[j], this.dataPointShapes[(i+j) % 4]]);
                }
            }
            this.allIds.forEach((id,index) => {
                this.colorShapeMap[id] = combinations[index];
            })
        },
        plotSolverData(solverData) {
            let coordinatesData = GraphUtils.dataToCoordinates(solverData, this.xScale,this.yScale, this.rotate);
            this.svg.selectAll('circle').remove();
            this.svg.selectAll('rect').remove();
            for (const [eval_node_id, coordinateData] of Object.entries(coordinatesData)){
                let [colorCode, shape] = this.colorShapeMap[eval_node_id];
                let shapeFill = colorCode;
                let strokeWidth = 0;
                if (shape.charAt(6) === "-"){
                    shape = shape.substring(7);
                    shapeFill = "none";
                    strokeWidth = 2;
                }
                // this.svg.selectAll(shape).remove();
                coordinateData.forEach(d => {
                    this.svg
                        .append(shape)
                        .attr("cx", d.x)
                        .attr("cy", d.y)
                        .attr("r", 3)
                        .attr("fill", shapeFill)
                        .attr("stroke", colorCode)
                        .attr("stroke-width", strokeWidth)
                        .attr("transform", `translate(${this.margin.left},${this.margin.top})`);
                })
            }

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

            this.renderSheets(sheets);

            if (this.rotate && this.displayFronts) {
                this.drawParetoFronts(sheetsScale);
            }
        },
        drawAxis() {
            let {xAxis, yAxis} = GraphUtils.composeAxis(this.xScale, this.yScale);
            this.svg.append("g").attr("transform", `translate(${this.margin.left},${this.margin.top})`).call(yAxis);
            this.svg.append("g").attr("transform", `translate(${this.margin.left},${this.innerHeight + this.margin.top})`).call(xAxis);
        },
        drawParetoFronts(sheetsScale) {
            let paretoFronts = GraphUtils.getParetoFronts(sheetsScale);
            let line = d3.line()
                .x(function(d) { return d.x; })
                .y(function(d) { return d.y; });
            this.svg.selectAll(".line")
                .append("g")
                .data(paretoFronts)
                .enter().append("path")
                .attr("class", "line")
                .attr("d", line)
                .attr("transform", `translate(${this.margin.left},${this.margin.top})`)
                .style("stroke-width", 2.5)
                .style("stroke", "red")
                .style("opacity", 0.8);
        },
        drawSheets() {
            let sheetsCoordinates = GraphUtils.computeSheetsCoordinates(this.treeInfo,this.nodeInfo, this.rotate);
            let sheetsScale = GraphUtils.sheetCoordinatesToScale(sheetsCoordinates,this.xScale, this.yScale, this.logScale);
            let sheets = GraphUtils.composeSheets(sheetsScale);
            this.renderSheets(sheets);
        },
        renderSheets(sheets){
            for (let [node_id,sheet] of sheets.entries()) {
                let strokeColor = this.colorShapeMap[node_id][0];
                this.svg.append("path")
                    .attr("id", node_id)
                    .attr("d", sheet)
                    .attr("transform", `translate(${this.margin.left},${this.margin.top})`)
                    .style("fill","none")
                    // .style("fill", '#' + Math.floor(Math.random() * 16777215).toString(16))
                    .style("stroke", strokeColor)
                    // .style("stroke", '#' + Math.floor(Math.random() * 16777215).toString(16))
                    .style("stroke-width", 2.5)
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