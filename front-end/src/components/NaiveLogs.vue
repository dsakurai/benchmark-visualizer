<template>
  <el-container>
    <el-header>
      <el-card>
        <el-slider v-model="currentStep" :step=1 :marks="marks" show-input :show-input-controls="false" :format-tooltip="formatTooltip"/>
      </el-card>
    </el-header>
    <el-main>
      <el-tree-v2 :data="treeData" :props="props"  :height="208">
        <template #default="{ node }">
          <span>{{ node.label }}</span>
            <el-icon ><Location /></el-icon>
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
      allIDs:[],
      marks:{
        0:"0",
        100:"25000",
      },
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
      return val * 250;
    },
    getNaiveLogData(){
      axios.get("/api/demo_data").then(response => {
        this.logData = response.data.solver_log;
        this.treeData = response.data.tree;
      })
    }
  },
}
</script>

<style scoped>

</style>