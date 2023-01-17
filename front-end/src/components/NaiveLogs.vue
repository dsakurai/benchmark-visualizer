<template>
  <el-container>
    <el-header>
      <el-card>
        <el-row>
          <el-slider v-model="sliderStep" :step="stepSize" :marks="marks" :format-tooltip="formatTooltip"/>
        </el-row>
        <el-row>
          <el-col>
<!--            <el-button type="primary" :icon="VideoPlay" circle></el-button>-->
          </el-col>
        </el-row>
      </el-card>
    </el-header>
    <el-main>
      <el-tree-v2 :data="treeData" :props="props"  :height="208">
        <template #default="{ node ,data}">
          <span>{{ node.label }}</span>
            <span v-if="data.id===solverData[Math.round(this.sliderStep / this.stepSize)].eval_node_id">
              <el-icon color="green"><Location /></el-icon>{{solverData[Math.round(this.sliderStep / this.stepSize)]}}</span>
           </template>
      </el-tree-v2>
    </el-main>
  </el-container>
</template>

<script>
import axios from 'axios';
export default {
  name: "NaiveLogs",
  data(){
    return {
      logData:'',
      treeData:'',
      sliderStep:0,
      totalSteps:100,
      stepSize:1,
      allIDs:[],
      solverData:[],
      currentStep:0,
      marks:{},
      props : {
        value: 'id',
        label: 'label',
        children: 'children',
      }
    }

  },
  created() {
    this.getNaiveLogData();
  },
  methods:{
    formatTooltip(val){
      return val * this.totalSteps / 100;
    },
    getNaiveLogData(){
      axios.get("/api/demo_data").then(response => {
        this.logData = response.data.solver_log;
        this.treeData = response.data.tree;
        this.totalSteps = this.logData.length;
        this.stepSize = 100 / this.totalSteps;
        this.marks[0] = "0";
        this.marks[100] = this.totalSteps.toString();
        for (let i = 0;i<this.totalSteps;i++){
          this.solverData[this.logData[i].step] = this.logData[i];
        }
      })
    }
  },
}
</script>

<style scoped>

</style>