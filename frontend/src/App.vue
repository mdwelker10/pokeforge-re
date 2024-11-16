<template>
  <div id="app">
    <HelloWorld msg="You did it!" />
    <router-view> </router-view>
  </div>
</template>

<script>
import HelloWorld from "./components/HelloWorld.vue";
export default {
  name: "App",
  components: {
    HelloWorld,
  },
};
</script>

<style scoped>
#app {
  text-align: center;
}
</style>
