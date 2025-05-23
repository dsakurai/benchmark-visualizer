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
                    <el-col :span="5">
                        <span>Population Size:</span>
                        <el-input-number v-model="populationSize"></el-input-number>
                    </el-col>
                    <el-col :span="4">
                        <span>Solver: </span>
                        <el-select-v2
                            v-model="solverType"
                            :options="solverOptions"
                            @change="getNaiveLogData"
                        />
                    </el-col>
                    <el-col :span="4">
                        <span>Tree: </span>
                        <el-select-v2
                            v-model="treeType"
                            :options="treeOptions"
                            @change="getNaiveLogData"
                        />
                    </el-col>
                    <el-col :span="5">
                        <span>Dimension: </span>
                        <el-select-v2
                            v-model="dimension"
                            :options="dimensionOptions"
                            @change="getNaiveLogData"
                        />
                    </el-col>
                    <el-col :span="6">
                        <span>Stopping Criterion: </span>
                        <el-select-v2
                            v-model="stoppingCriterion"
                            :options="stoppingCriterionOptions"
                            @change="getNaiveLogData"
                        />
                    </el-col>
                </el-row>
            </el-card>
            <el-row>
                <el-col :span="24">
                <el-tree-v2 :data="treeData" :props="props">
                    <template #default="{ node ,data}">
                        <div class="tree-node">
                            <el-space wrap :size="30">
                                <span>{{ node.label }}</span>
                                <span
                                    style="color: #ff4949">Best in selection: {{nodeMinima[data.id].toFixed(2)}}, Best record:{{ locatedMinima[data.id].toFixed(2) }}</span>
<!--                                <span-->
<!--                                    style="color: #4281b9"> Count: {{data.id in nodeStats ? nodeStats[data.id] : 0}}</span>-->
                            </el-space>
                            <div class="progress-bar">
                                <el-progress :stroke-width="15"
                                             :percentage="(nodeStats[data.id] *100 / (stepRange*populationSize))"
                                             style="width:600px;"><span style="width: 10px"
                                                                        v-text="(nodeStats[data.id] *100 / (stepRange*populationSize)).toFixed(2)"> </span>
                                </el-progress>
                            </div>
                        </div>
                    </template>
                </el-tree-v2>
                </el-col>
            </el-row>
            <el-row>
                <ReebSpace :solver-data="filteredSolverData" :tree-name="treeType" :dimension="dimension" :all-ids="allIDs"></ReebSpace>
            </el-row>
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
            treeData: [],
            sliderStep: [0, 1],
            totalSteps: 100,
            stepSize: 100,
            populationSize: 100,
            locatedMinima: {},
            nodeMinima: {},
            elapsedData: [],
            allIDs: [],
            solverData: [],
            filteredSolverData: [],
            currentStep: 0,
            playbackSpeed: 1,
            marks: {},
            nodeStats: {},
            stepMinimals:{},
            playInstance: '',
            isPlaying: false,
            lockRange: false,
            stepRange: 2,
            filterOffset: 0,
            solverType: "NSGAII",
            treeType: "breadth_base_1",
            dimension: 5,
            stoppingCriterion: "StoppingByEvaluations",
            solverOptions: [{value: "GDE3", label: "GDE3"}, {value: "IBEA", label: "IBEA"},{value: "NSGAII", label: "NSGA-II"}, {
                value: "MOEAD",
                label: "MOEAD"
            }, {value: "OMOPSO", label: "OMOPSO"}
            ],
            treeOptions: [
                {value: "sample", label: "Sample"},
                {value: "diverse_tree", label: "Diverse"},
                {value: "depth_base_1", label: "Depth 1"},
                {value: "depth_base_2", label: "Depth 2"},
                {value: "depth_base_3", label: "Depth 3"},
                {value: "depth_base_4", label: "Depth 4"},
                {value: "depth_base_5", label: "Depth 5"},
                {value: "depth_base_6", label: "Depth 6"},
                // {value: "breadth", label: "Breadth"},
                {value: "breadth_base_1", label: "Breadth 1"},
                {value: "breadth_base_2", label: "Breadth 2"},
                {value: "breadth_base_3", label: "Breadth 3"},
                {value: "breadth_base_4", label: "Breadth 4"},
                {value: "breadth_base_5", label: "Breadth 5"},
                {value: "breadth_base_6", label: "Breadth 6"},
            ],
            dimensionOptions: [{value: 2, label: 2},
                {value: 3, label: 3},
                {value: 4, label: 4},
                {value: 5, label: 5},
                {value: 6, label: 6},
                {value: 7, label: 7},
                {value: 8, label: 8},
                {value: 9, label: 9},
                {value: 10, label: 10},
                {value: 11, label: 11},
                {value: 12, label: 12},
                {value: 20, label: 20},
                {value: 100, label: 100}, {
                value: 1000,
                label: 1000
            }],
            stoppingCriterionOptions: [{value: "StoppingByTime", label: "By Time"}, {
                value: "StoppingByEvaluations",
                label: "By Evaluations"
            }],
            props: {
                value: 'id',
                label: 'label',
                children: 'children',
            }
        }

    },
    components: {
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
            this.getStats(endStep);
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
            axios.get(`/api/demo_data?solver=${this.solverType}&tree_name=${this.treeType}&dimension=${this.dimension}&termination=${this.stoppingCriterion}`).then(response => {
                this.logData = response.data.solver_log;
                this.allIDs = response.data.all_ids;
                this.treeData = response.data.tree;
                this.$message.success("Solver data loaded");
                this.totalSteps = this.logData.length;
                this.stepSize = 100 / this.totalSteps * this.populationSize;
                this.marks[0] = "0";
                this.marks[100] = this.totalSteps.toString();
                // this.stepRange = Math.round(this.totalSteps / this.populationSize);
                for (let i = 0; i < this.totalSteps; i++) {
                    this.solverData[this.logData[i].step] = this.logData[i];
                }
                this.stepMinimals = computeUtils.computeStepMinimal(this.solverData,this.allIDs);
                this.filteredSolverData = this.solverData;
                let endStep = Math.round(this.sliderStep[1] * this.populationSize / this.stepSize);
                this.getStats(endStep);
            }).catch(error => {
                this.$message.error("Solver data failed @ " + error.toString());
            });
        },
        getStats(endStep) {
            // this.locatedMinima = computeUtils.computeElapsedMinimal(this.elapsedData, this.allIDs);
            this.locatedMinima = computeUtils.getLocatedMinima(this.stepMinimals,endStep,this.allIDs)
            this.nodeMinima = computeUtils.computeElapsedMinimal(this.filteredSolverData, this.allIDs);
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
            this.getStats(endStep);
        },
    },
}
</script>

<style scoped>
.el-row {
    margin-top: 10px;
    margin-bottom: 0;
}

.tree-node {
    flex: 1;
    display: flex;
    align-items: center;
    justify-content: space-between;
    font-size: 18px;
    padding-right: 50px;
}
</style>