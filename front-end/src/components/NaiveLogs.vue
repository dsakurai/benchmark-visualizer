<template>
  <el-container>
    <el-header>
      <el-card>
        <el-slider v-model="currentStep" :step="stepSize" :marks="marks" :format-tooltip="formatTooltip"/>
      </el-card>
    </el-header>
    <el-main>
      <el-tree-v2 :data="treeData" :props="props"  :height="208">
        <template #default="{ node }">
          <span>{{ node.label }}</span>
            <el-icon ><Location /></el-icon><span v-if="node.value!==solver_data[currentStep / stepSize].eval_node_id"> !!{{solver_data[currentStep / stepSize]}} </span>
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
      currentStep:0,
      totalSteps:100,
      stepSize:1,
      allIDs:[],
      solver_data:{},
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
          this.solver_data[this.logData[i].step] = this.logData[i];
        }
      })
    }
  },
}
</script>

<style scoped>

</style>