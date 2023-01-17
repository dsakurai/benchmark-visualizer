<template>
    <el-container>
        <el-main>
            <el-card class="box-card">
                <el-row :gutter="20">
                    <el-col :gutter="20" :span="24">
                    <el-slider v-model="sliderStep" :step="stepSize" :marks="marks" :format-tooltip="formatTooltip"/>
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
                    <el-col :gutter="20" :span="11">
                        <el-slider v-model="playbackSpeed" show-input @change="changePlaybackSpeed"></el-slider>
                    </el-col>
                </el-row>
            </el-card>
            <el-tree-v2 :data="treeData" :props="props" :height="208">
                <template #default="{ node ,data}">
                    <span>{{ node.label }}</span>
                    <span v-if="data.id===solverData[Math.round(this.sliderStep / this.stepSize)].eval_node_id">
              <el-icon color="green"><Location/></el-icon>{{ solverData[Math.round(this.sliderStep / this.stepSize)] }}</span>
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
            sliderStep: 0,
            totalSteps: 100,
            stepSize: 1,
            allIDs: [],
            solverData: [],
            currentStep: 0,
            playbackSpeed: 1,
            marks: {},
            playInstance: '',
            isPlaying: false,
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
        updateStep() {
            if (this.currentStep < this.totalSteps) {
                this.currentStep++;
                this.sliderStep = this.currentStep * this.stepSize
            }
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
            return Math.round(val * this.totalSteps / 100);
        },
        getNaiveLogData() {
            axios.get("/api/demo_data").then(response => {
                this.logData = response.data.solver_log;
                this.treeData = response.data.tree;
                this.totalSteps = this.logData.length;
                this.stepSize = 100 / this.totalSteps;
                this.marks[0] = "0";
                this.marks[100] = this.totalSteps.toString();
                for (let i = 0; i < this.totalSteps; i++) {
                    this.solverData[this.logData[i].step] = this.logData[i];
                }
            })
        }
    },
}
</script>

<style scoped>

</style>