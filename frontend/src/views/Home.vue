<script>
export default {
  name: "Home",
  methods: {
    async getApiMessage() {
      const response = await fetch("http://localhost:5000/api/test");
      const data = await response.text();
      document.getElementById("lbl1").innerHTML = data;
    },
  },
};
</script>

<template>
  <div>
    <h1>Home Page</h1>
    <p>Welcome to the Home Page!</p>
    <router-link to="/about">Go to About</router-link>
    <br />
    <button id="btn1" class="btn btn-primary" type="button" v-on:click="getApiMessage">Click to get API message</button>
    <label id="lbl1"></label>
  </div>
</template>

<style scoped>
h1 {
  color: blue;
}
</style>
