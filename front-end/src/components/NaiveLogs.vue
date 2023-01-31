<template>
    <el-container>
        <el-main>
            <el-card class="box-card" header="Visualization Controls">
                <el-row :gutter="20">
                    <el-col :gutter="20" :span="24">
                        <el-slider v-model="sliderStep" range :step="stepSize" :marks="marks"
                                   :format-tooltip="formatTooltip"
                                   @input="filterRange"/>
                    </el-col>
                </el-row>
                <el-row :gutter="20">
                    <el-col :gutter="20" :span="2">
                        <el-button type="primary" @click="startAutoPlay">Play</el-button>
                    </el-col>
                    <el-col :gutter="20" :span="2">
                        <el-button type="primary" @click="pause">Pause</el-button>
                    </el-col>
                    <el-col :gutter="20" :span="1">
                        <el-switch
                            v-model="isPlaying"
                            class="ml-2"
                            style="--el-switch-on-color: #13ce66; --el-switch-off-color: #ff4949"
                        />
                    </el-col>
                    <el-col :gutter="20" :span="3">
                        <span>Playback Speed:</span>
                    </el-col>
                    <el-col :gutter="20" :span="6">
                        <el-slider v-model="playbackSpeed" show-input @change="changePlaybackSpeed"></el-slider>
                    </el-col>
                    <el-col :span="3">
                        <el-checkbox v-model="lockRange" label="Lock Range"/>
                    </el-col>
                    <el-col :span="3"><span>Current Range Size:</span></el-col>
                    <el-col :span="2">
                        <el-input-number v-model="stepRange" @change="changeStepRange"></el-input-number>
                    </el-col>
                </el-row>
                <el-row :gutter="20">
                    <el-col :gutter="20" :span="8">
                        <span>Population Size:</span> <el-input-number v-model="populationSize"></el-input-number>
                    </el-col>
                </el-row>
            </el-card>
            <el-tree-v2 :data="treeData" :props="props" :height="208">
                <template #default="{ node ,data}">
                  <div class="tree-node">
                    <el-space wrap :size="50">
                        <span>{{ node.label }}</span>
                        <span style="color: #4281b9"> Stays: {{ data.id in nodeStats ? nodeStats[data.id] : 0}}</span>
                    </el-space>
                      <div class="progress-bar">
                      <el-progress :stroke-width="20" :percentage="(nodeStats[data.id] *100 / (stepRange*populationSize)).toFixed(2)" style="width:600px;"><span style="width: 10px" v-text="nodaMinima[data.id].toFixed(2)"> </span></el-progress>
                      </div>

                  </div>
                </template>
            </el-tree-v2>
        </el-main>
    </el-container>
</template>

<script>
import axios from 'axios';

export default {
    name: "NaiveLogs",
    data() {
        return {
            logData: '',
            treeData: '',
            sliderStep: [0, 100],
            totalSteps: 100,
            stepSize: 100,
            populationSize:100,
            nodaMinima:{},
            allIDs: [],
            solverData: [],
            filteredSolverData: [],
            currentStep: 0,
            playbackSpeed: 1,
            marks: {},
            nodeStats: {},
            playInstance: '',
            isPlaying: false,
            lockRange: false,
            stepRange: 0,
            filterOffset: 0,
            props: {
                value: 'id',
                label: 'label',
                children: 'children',
            }
        }

    },
    created() {
        this.getNaiveLogData();
    },
    methods: {
        updateTailSlider() {
            let range = this.stepRange * this.stepSize;
            console.log(range);
            if (this.sliderStep[0] + range < 100) {
                console.log(this.sliderStep[0]);
                console.log(this.sliderStep[1]);
                this.sliderStep[1] = this.sliderStep[0] + range;
                console.log(this.sliderStep[1]);
            }
        },
        changeStepRange() {
            this.sliderStep[1] = this.sliderStep[0] + Math.round(this.stepRange * this.stepSize);
        },
        updateStep() {
            if (Math.round(this.sliderStep[0] / this.stepSize) < this.totalSteps) {
                this.sliderStep[0] += this.stepSize;
            }
            if (this.lockRange && (this.sliderStep[1] < 100)) {
                this.sliderStep[1] += this.stepSize;
            } else {
                this.stepRange = Math.round((this.sliderStep[1] - this.sliderStep[0]) / this.stepSize);
            }
            this.stepRange = Math.round((this.sliderStep[1] - this.sliderStep[0]) / this.stepSize);
            let startStep = Math.round(this.sliderStep[0] * this.populationSize / this.stepSize);
            let endStep = Math.round(this.sliderStep[1] * this.populationSize / this.stepSize);
            this.filterOffset = startStep;
            this.filteredSolverData = this.solverData.slice(startStep, endStep);
            this.getStats();
        },
        startAutoPlay() {
            clearInterval(this.playInstance);
            this.playInstance = setInterval(this.updateStep, Math.round(1000 / this.playbackSpeed));
            this.isPlaying = true;
        },
        changePlaybackSpeed() {
            clearInterval(this.playInstance);
            if (this.isPlaying) {
                this.playInstance = setInterval(this.updateStep, Math.round(1000 / this.playbackSpeed));
            }
        },
        pause() {
            clearInterval(this.playInstance);
            this.isPlaying = false;
        },
        formatTooltip(val) {
            return Math.round(val / 100 * this.totalSteps / this.populationSize);
        },
        getNaiveLogData() {
            axios.get("/api/demo_data").then(response => {
                this.logData = response.data.solver_log;
                this.treeData = response.data.tree;
                this.totalSteps = this.logData.length;
                this.stepSize = 100 / this.totalSteps * this.populationSize;
                this.marks[0] = "0";
                this.marks[100] = this.totalSteps.toString();
                this.stepRange = Math.round(this.totalSteps / this.populationSize);
                for (let i = 0; i < this.totalSteps; i++) {
                    this.solverData[this.logData[i].step] = this.logData[i];
                }
                this.filteredSolverData = this.solverData;
                this.getStats();
            })
        },
        getStats() {
            let range = this.filteredSolverData.length;
            let nodeCounts = {};
            let nodeMinima = {};
            for (let i = 0; i < range; i++) {
                let key = this.filteredSolverData[i].eval_node_id;
                if (!(key in nodeMinima)){
                nodeMinima[key] = this.filteredSolverData[i].y2;
                }
                else{
                    if (nodeMinima[key] > this.filteredSolverData[i].y2){
                        nodeMinima[key] = this.filteredSolverData[i].y2
                    }
                }
                if (!(key in nodeCounts)) {
                    nodeCounts[key] = 1;
                } else {
                    nodeCounts[this.filteredSolverData[i].eval_node_id] += 1;
                }
            }
            this.nodeStats = nodeCounts;
            this.nodaMinima = nodeMinima;
        },
        filterRange(input) {
            this.sliderStep[0] = input[0];
            this.sliderStep[1] = input[1];
            this.stepRange = Math.round((this.sliderStep[1] - this.sliderStep[0]) / this.stepSize);
            let startStep = Math.round(this.sliderStep[0] * this.populationSize / this.stepSize);
            let endStep = Math.round(this.sliderStep[1] * this.populationSize / this.stepSize);
            this.filterOffset = startStep;
            this.filteredSolverData = this.solverData.slice(startStep, endStep);
            console.log(this.filteredSolverData);
            if (this.lockRange) {
                // TODO: Tail slider not updated!!
                this.updateTailSlider();
            }
            this.getStats();
        },
    },
}
</script>

<style scoped>
.el-row {
    margin-top: 10px;
    margin-bottom: 0px;
}
.tree-node{
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: space-between;
  font-size: 20px;
  padding-right: 400px;
}
</style>