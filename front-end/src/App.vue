<template>
    <el-menu
        :default-active="activeIndex"
        class="el-menu-demo"
        mode="horizontal"
        :ellipsis="false"
        background-color="#2c3e50"
        text-color="#fff"
        active-text-color="#fff"
        @select="handleSelect"
    >
        <el-button type="default" style="margin: 15px 15px 15px 30px;" circle @click="asideExpansion=!asideExpansion">
            <el-icon>
                <Expand/>
            </el-icon>
        </el-button>
        <div class="flex-grow"/>
        <el-menu-item index="1" @click="d3TreeActive=!d3TreeActive">D3Tree</el-menu-item>
        <el-menu-item index="2" @click="d3TreeActive=!d3TreeActive">D3ForceTree</el-menu-item>
    </el-menu>
    <el-container>
        <el-aside width="auto">
           <ComputationMenu :asideExpansion="asideExpansion"></ComputationMenu>
        </el-aside>
        <el-main>
<!--            <D3Tree v-if="d3TreeActive"></D3Tree>-->
<!--            <D3ForceTree v-else></D3ForceTree>-->
          <div v-if="d3TreeActive"><NaiveLogs></NaiveLogs></div>
          <div v-else><ReebSpace></ReebSpace></div>
        </el-main>
    </el-container>
</template>

<script>
// import D3Tree from "@/components/D3Tree";
// import D3ForceTree from "@/components/D3ForceTree";
import ComputationMenu from "@/components/ComputationMenu";
import NaiveLogs from "@/components/NaiveLogs.vue";
import ReebSpace from "@/components/ReebSpace.vue";

export default {
    name: 'App',
    data() {
        return {
            d3TreeActive: true,
            activeIndex: '1',
            asideExpansion: false,
        };
    },
    components: {
      ReebSpace,
      NaiveLogs,
        // D3Tree,
        // D3ForceTree
        ComputationMenu,

    },
    methods: {
        handleSelect(key, keyPath) {
            console.log(key, keyPath);
        },
    }
}
</script>

<style>
html, body, #app {
    font-family: Avenir, Helvetica, Arial, sans-serif;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
    text-align: center;
    color: #000;
    margin-top: 0;
    margin-left: 0;
    margin-right: 0;
}

.flex-grow {
    flex-grow: 1;
}
</style>
