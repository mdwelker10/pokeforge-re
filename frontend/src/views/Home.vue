<script>
export default {
  name: "Home",
  methods: {
    async getApiMessage() {
      const response = await fetch("/api/test/");
      const data = await response.json();
      document.getElementById("lbl1").innerHTML = data.message;
    },
    async getAuthApiMessage() {
      const response = await fetch("/api/test/auth");
      const data = await response.json();
      const text = data.message ? data.message : data.error;
      document.getElementById("lbl3").innerHTML = text;
    },
    async login(google = false) {
      console.log("logging in");
      if (google) {
        window.location.href = "/api/login?method=google";
        //TODO figure out how to redirect to a different page after Google login
      } else {
        let res = await fetch("/api/login", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            username: document.getElementById("username").value,
            password: document.getElementById("password").value,
          }),
        });
        if (res.redirected) {
          document.getElementById("lbl2").innerHTML = "You are logged in";
          window.location.href = res.url;
        }
        if (res.status === 200) {
          console.log("no redirect but success");
        } else {
          document.getElementById("lbl2").innerHTML = "Login failed";
        }
      }
      localStorage.setItem("isAuthenticated", JSON.stringify(true));
    },
    async logout() {
      console.log("logging out");
      let res = await fetch("/api/logout");
      document.getElementById("lbl2").innerHTML = "You are logged out";
      localStorage.setItem("isAuthenticated", JSON.stringify(false));
      if (res.redirected) {
        window.location.href = res.url;
      }
    },
    async register() {
      console.log("registering");
      let res = await fetch("/api/register", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          username: document.getElementById("username").value,
          password: document.getElementById("password").value,
        }),
      });
      if (res.redirected) {
        document.getElementById("lbl2").innerHTML = "Registered!";
        window.location.href = res.url;
      }
      if (res.status === 200) {
        console.log("no redirect but success");
      } else {
        document.getElementById("lbl2").innerHTML = "Registration failed";
      }
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
    <button id="btn2" class="btn btn-info" type="button" v-on:click="login(true)">Log in with Google</button>
    <br />
    <button id="btn3" class="btn btn-primary" type="button" v-on:click="getAuthApiMessage">Check Auth Status</button>
    <label id="lbl3"></label>
    <br />
    <br />
    <br />
    <textarea class="me-3" id="username" placeholder="username"></textarea><textarea id="password" placeholder="password"></textarea>
    <br />
    <button id="btn4" class="btn btn-info" type="button" v-on:click="login(false)">Log in</button>
    <button id="btn5" class="btn btn-info" type="button" v-on:click="register">Register</button>
    <br />
    <label id="lbl2"></label>
    <br />
    <button id="btn6" class="btn btn-danger" type="button" v-on:click="logout">Log out</button>
  </div>
</template>

<style scoped>
h1 {
  color: blue;
}
</style>
