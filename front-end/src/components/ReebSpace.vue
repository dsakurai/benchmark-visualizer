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
            figureWidth: 800,
            figureHeight: 800,
            promisedReebData: '',
            treeInfo: '',
            nodeInfo: '',
            svg:'',
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

                let {xAxis, yAxis} = GraphUtils.composeAxis(this.treeInfo, {
                    "width": this.figureWidth,
                    "height": this.figureHeight
                });

                this.svg = d3.select("#reebSpace").attr("width", this.figureWidth).attr("height", this.figureHeight);
                let xAxisTranslate = this.figureWidth / 2 + 10;
                this.svg.append("g").attr("transform", "translate(50, 10)").call(yAxis);
                this.svg.append("g").attr("transform", "translate(50, " + xAxisTranslate + ")").call(xAxis);
                let sheets = GraphUtils.composeSheets(this.treeInfo, {
                    "width": this.figureWidth,
                    "height": this.figureHeight
                }, this.nodeInfo);

                for (let node_id in sheets) {
                    this.svg.append("path")
                        .attr("id",node_id)
                        .attr("d", sheets[node_id])
                        .attr("transform", "translate(100,0) scale(0.5,0.5) rotate(45)")
                        .style("fill", '#' + Math.floor(Math.random() * 16777215).toString(16))
                        .style("stroke", "black")
                        .style("opacity", 0.5);
                }

            })
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