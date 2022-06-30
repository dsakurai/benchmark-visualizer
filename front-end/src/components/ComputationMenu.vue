<template>
    <el-menu
        default-active="1"
        :collapse="asideExpansion"
        @open="handleOpen"
        @close="handleClose"
        v-if="algListLoaded"
    >
        <el-sub-menu index="1">
            <template #title>
                <el-icon>
                    <cpu/>
                </el-icon>
                <span>Solvers</span>
            </template>
            <el-menu-item-group title="Multi-Objective">
                <span class="algorithmCategory">Evolutionary Algorithms</span>
                <div v-for="(alg, alg_index) in solvers.multi_objective.evolutionary_algorithms" :key="alg.name">
                    <el-popover
                        placement="right"
                        title="Parameters"
                        :width="300"
                        trigger="hover"
                    >
                        <template #reference>
                            <el-menu-item :index="'1-1-'+alg_index.toString()">{{ alg.name }}</el-menu-item>
                        </template>
                        <el-row :gutter="20" v-for="(parameter, para_name) in alg.parameters" :key="alg.name+para_name">
                            <el-col :span="12"><span v-text="para_name"></span></el-col>
                            <el-col :span="12">
                                <el-input-number
                                    v-model="solvers.multi_objective.evolutionary_algorithms[alg_index].parameters[para_name]"
                                    :precision="2" :step="0.1" size="small"/>
                            </el-col>
                        </el-row>
                    </el-popover>
                </div>
                <span class="algorithmCategory">PSO Algorithms</span>
                <div v-for="(alg, alg_index) in solvers.multi_objective.PSO_algorithms" :key="alg.name">
                    <el-popover
                        placement="right"
                        title="Parameters"
                        :width="300"
                        trigger="hover"
                    >
                        <template #reference>
                            <el-menu-item :index="'1-2-'+alg_index.toString()">{{ alg.name }}</el-menu-item>
                        </template>
                        <el-row :gutter="20" v-for="(parameter, para_name) in alg.parameters" :key="alg.name+para_name">
                            <el-col :span="12"><span v-text="para_name"></span></el-col>
                            <el-col :span="12">
                                <el-input-number
                                    v-model="solvers.multi_objective.PSO_algorithms[alg_index].parameters[para_name]"
                                    :precision="2" :step="0.1" size="small"/>
                            </el-col>
                        </el-row>
                    </el-popover>
                </div>
            </el-menu-item-group>
            <el-menu-item-group title="Single-Objective">
                <div v-for="(alg, alg_index) in solvers.single_objective" :key="alg.name">
                    <el-popover
                        placement="right"
                        title="Parameters"
                        :width="300"
                        trigger="hover"
                    >
                        <template #reference>
                            <el-menu-item :index="'1-3-'+alg_index.toString()">{{ alg.name }}</el-menu-item>
                        </template>
                        <el-row :gutter="20" v-for="(parameter, para_name) in alg.parameters" :key="alg.name+para_name">
                            <el-col :span="12"><span v-text="para_name"></span></el-col>
                            <el-col :span="12">
                                <el-input-number
                                    v-model="solvers.single_objective[alg_index].parameters[para_name]"
                                    :precision="2" :step="0.1" size="small"/>
                            </el-col>
                        </el-row>
                    </el-popover>
                </div>
            </el-menu-item-group>
        </el-sub-menu>
        <el-menu-item index="2">
            <el-icon>
                <operation/>
            </el-icon>
            <template #title>Filters</template>
        </el-menu-item>
    </el-menu>
</template>

<script>
import axios from "axios";

export default {
    name: "ComputationMenu",
    data() {
        return {
            solvers: '',
            algListLoaded: false
        };
    },
    props: {
        asideExpansion: Boolean,
    },
    created() {
        this.getAlgorithms();
    },
    methods: {
        handleOpen(){},
        handleClose(){},
        getAlgorithms() {
            axios.get("/api/get_all_solvers/").then(response => {
                this.solvers = response.data;
                this.algListLoaded = true;
            });
        }
    }
}
</script>

<style scoped>
span.algorithmCategory {
    color: #4281b9;
    font-size: small;
    text-align: right;
}
.el-row {
    margin-bottom: 10px;
}
</style>