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
  props: {},
  data() {
    return {
      reebData: [],
      figureWidth: 800,
      figureHeight: 800,
      promisedReebData: '',
    }
  },
  mounted() {
    this.getReebInfo();

  },
  methods: {
    getReebInfo() {
      axios.get("/api/reeb_space").then(response => {
        this.reebData = response.data;
        this.loadInitialGraph();
        let {treeInfo, nodeInfo} = DataUtils.parseReebData(response.data);

        let {xAxis, yAxis} = GraphUtils.composeAxis(treeInfo, {"width": this.figureWidth, "height": this.figureHeight});

        this.svg = d3.select("#reebSpace").attr("width", this.figureWidth).attr("height", this.figureHeight);
        let xAxisTranslate = this.figureWidth / 2 + 10;
        this.svg.append("g").attr("transform", "translate(50, 10)").call(yAxis);
        this.svg.append("g").attr("transform", "translate(50, " + xAxisTranslate + ")").call(xAxis);
        let sheets = GraphUtils.composeSheets(treeInfo, {
          "width": this.figureWidth,
          "height": this.figureHeight
        }, nodeInfo);



        for (let node_id in sheets) {
          this.svg.append("path")
              .attr("d", sheets[node_id])
              .attr("transform", "translate(50, " + 10 + ")")
              .style("fill", '#' + Math.floor(Math.random() * 16777215).toString(16))
              .style("stroke", "black")
              .style("opacity", 0.5).call(d3.drag());
              // .on('start', dragStart)
              // .on('drag', dragging)
              // .on('end', dragEnd));
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