<script>
sessionStorage.clear(); //TODO TAKE OUT AFTER LOGIN WORKS
export default {
  name: "Home",
  methods: {
    async getApiMessage() {
      const response = await fetch("/api/test/");
      const data = await response.text();
      document.getElementById("lbl1").innerHTML = data;
    },
    async getAuthApiMessage() {
      const response = await fetch("/api/test/auth");
      const data = await response.json();
      document.getElementById("lbl3").innerHTML = data.message;
    },
    async handleClick() {
      localStorage.setItem("isAuthenticated", JSON.stringify(false));
      // login or logout depending on authentication status
      if (localStorage.getItem("isAuthenticated") === "true") {
        this.logout();
      } else {
        this.login();
      }
    },
    async login() {
      console.log("logging in");
      window.location.href = "/api/login";
      // document.getElementById("lbl2").innerHTML = `${sessionStorage.getItem("email")} - ${sessionStorage.getItem("name")}`;
      document.getElementById("btn2").innerHTML = "Logout";
      // localStorage.setItem("isAuthenticated", JSON.stringify(true));
    },
    async logout() {
      console.log("logging out");
      const response = await fetch("/api/logout");
      // const data = await response.json();
      // console.log(data.message);
      document.getElementById("lbl2").innerHTML = "You are logged out";
      document.getElementById("btn2").innerHTML = "Log in with Google";
      localStorage.setItem("isAuthenticated", JSON.stringify(false));
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
    <br />
    <button id="btn2" class="btn btn-info" type="button" v-on:click="handleClick">Log in with Google</button>
    <label id="lbl2"></label>
    <br />
    <button id="btn3" class="btn btn-info" type="button" v-on:click="getAuthApiMessage">Check Auth Status</button>
    <label id="lbl3"></label>
  </div>
</template>

<style scoped>
h1 {
  color: blue;
}
</style>
