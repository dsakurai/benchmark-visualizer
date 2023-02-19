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

export default {
  name: "ReebSpace",
  props: {},
  data() {
    return {
      reebData: [],
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
      })
    },
    drawAxis() {
      let width = 800;
      let height = 800;
      let data = [10, 15, 20, 25, 30];
      let xScale = d3.scaleLinear().domain([0, d3.max(data)]).range([0, width - 100]);
      let yScale = d3.scaleLinear().domain([0, d3.max(data)]).range([height / 2, 0]);
      this.svg = d3.select("#reebSpace").attr("width", width).attr("height", height);
      let xAxis = d3.axisBottom().scale(xScale);
      let yAxis = d3.axisLeft().scale(yScale);
      this.svg.append("g").attr("transform", "translate(50, 10)").call(yAxis);
      let xAxisTranslate = height / 2 + 10;
      this.svg.append("g").attr("transform", "translate(50, " + xAxisTranslate + ")").call(xAxis);
    },
    drawSheets() {
      this.reebData.forEach(node => {
        console.log(node);
        let line = d3.line()
            .x(function (d) {
              return d.x;
            })
            .y(function (d) {
              return d.y;
            });
        let points = [{x: 100, y: 100}, {x: 500, y: 100}, {x: 375, y: 150}, {x: 125, y: 150}];
        this.svg.append("path").attr("d", line(points) + 'Z')
            .style("fill", "orange")
            .style("stroke", "black");

      })
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