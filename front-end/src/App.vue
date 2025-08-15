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
    <!-- <el-button
      type="default"
      style="margin: 15px 15px 15px 30px"
      circle
      @click="asideExpansion = !asideExpansion"
    >
      <el-icon>
        <Expand />
      </el-icon>
    </el-button> -->
    <div class="flex-grow" />
    <el-menu-item index="1">Solver VIS</el-menu-item>
  </el-menu>
  <el-container>
    <!-- <el-aside width="auto">
      <ComputationMenu :asideExpansion="asideExpansion"></ComputationMenu>
    </el-aside> -->
    <el-main><NaiveLogs></NaiveLogs> </el-main>
  </el-container>
</template>

<script>
// import ComputationMenu from "@/components/ComputationMenu";
import NaiveLogs from "@/components/NaiveLogs.vue";

export default {
  name: "App",
  data() {
    return {
      activeIndex: "1",
      asideExpansion: false,
    };
  },
  components: {
    NaiveLogs,
    // ComputationMenu,
  },
  methods: {
    handleSelect(key, keyPath) {
      console.log(key, keyPath);
    },
  },
};
</script>

<style>
html,
body,
#app {
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
