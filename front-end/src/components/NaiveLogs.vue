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
                    <el-space wrap :size="30">
                        <span>{{ node.label }}</span>
                        <span style="color: #ff4949"> Eval-Minimal: {{locatedMinima[data.id].toFixed(2)}}</span>
                        <span style="color: #4281b9"> Count: {{ data.id in nodeStats ? nodeStats[data.id] : 0}}</span>
                    </el-space>
                      <div class="progress-bar">
                      <el-progress :stroke-width="15" :percentage="(nodeStats[data.id] *100 / (stepRange*populationSize))" style="width:600px;"><span style="width: 10px" v-text="locatedMinima[data.id].toFixed(2)"> </span></el-progress>
                      </div>

                  </div>
                </template>
            </el-tree-v2>
            <ReebSpace></ReebSpace>
        </el-main>
    </el-container>
</template>

<script>
import axios from 'axios';
import computeUtils from "@/functions/ComputeUtils";
import ReebSpace from "@/components/ReebSpace.vue";

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
            locatedMinima:{},
            nodaMinima:{},
            elapsedData:[],
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
    components:{
        ReebSpace,
    },
    created() {
        this.getNaiveLogData();
    },
    methods: {
        updateTailSlider() {
            let range = this.stepRange * this.stepSize;
            if (this.sliderStep[0] + range < 100) {
                this.sliderStep[1] = this.sliderStep[0] + range;
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
                this.allIDs = response.data.all_ids;
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
            this.locatedMinima = computeUtils.computeElapsedMinimal(this.elapsedData, this.allIDs);
            this.nodeStats = computeUtils.computeNodeCounts(this.filteredSolverData, this.allIDs);
        },
        filterRange(input) {
            this.sliderStep[0] = input[0];
            this.sliderStep[1] = input[1];
            this.stepRange = Math.round((this.sliderStep[1] - this.sliderStep[0]) / this.stepSize);
            let startStep = Math.round(this.sliderStep[0] * this.populationSize / this.stepSize);
            let endStep = Math.round(this.sliderStep[1] * this.populationSize / this.stepSize);
            this.filterOffset = startStep;
            this.filteredSolverData = this.solverData.slice(startStep, endStep);
            this.elapsedData = this.solverData.slice(0, endStep);

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
    margin-bottom: 0;
}
.tree-node{
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: space-between;
  font-size: 18px;
  padding-right: 50px;
}
</style>