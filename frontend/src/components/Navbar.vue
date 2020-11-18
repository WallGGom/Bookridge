<template>
  <nav class="my-1">
    <router-link to="/analyze" class="do" style="font-size: large"
      >Analyze</router-link
    >
    <router-link to="/community" class="do" style="font-size: large"
      >Community</router-link
    >
    <router-link
      :to="{ name: 'Activity', params: { pk: userPk } }"
      class="do"
      style="font-size: large"
      >My Activity</router-link
    >

    <div v-if="curRou == 'Analyze'" class="animation start-home"></div>
    <div v-else-if="curRou == 'Community'" class="animation start-about"></div>
    <div v-else-if="curRou == 'Activity'" class="animation start-blog"></div>
  </nav>
</template>

<script>
import VueCookies from "vue-cookies";
export default {
  name: "Navbar",
  components: {},
  // props: {
  //   isLogin: {
  //     type: Boolean,
  //     default: false,
  //   },
  // },
  props: {
    curRou: String,
  },
  created() {
    this.userPk = VueCookies.get("user_pk");
  },
  watch: {},
  methods: {},
  data() {
    return {
      userPk: null,
    };
  },
  mounted() {},
};
</script>

<style scoped>
nav {
  position: relative;
  width: 100%;
  height: 50px;
  background-color: #34495e;
  border-radius: 8px;
  font-size: 0;
}
nav a {
  line-height: 50px;
  height: 100%;
  font-size: 15px;
  display: inline-block;
  position: relative;
  z-index: 1;
  text-decoration: none;
  text-transform: uppercase;
  text-align: center;
  color: white;
  cursor: pointer;
}
nav .animation {
  position: absolute;
  height: 100%;
  top: 0;
  z-index: 0;
  transition: all 0.5s ease 0s;
  border-radius: 8px;
}
a:nth-child(1) {
  width: 33%;
}
a:nth-child(2) {
  width: 33%;
}
a:nth-child(3) {
  width: 33%;
}
/*
a:nth-child(4) {
	width: 20%;
}
a:nth-child(5) {
	width: 20%;
} */
nav .start-home,
a:nth-child(1):hover ~ .animation {
  width: 33%;
  left: 0;
  background-color: #00695c;
}
nav .start-about,
a:nth-child(2):hover ~ .animation {
  width: 33%;
  left: 33%;
  background-color: #00796b;
}
nav .start-blog,
a:nth-child(3):hover ~ .animation {
  width: 34%;
  left: 66%;
  background-color: #009688;
}
/* 
nav .start-portefolio, a:nth-child(4):hover~.animation {
	width: 20%;
	left: 60%;
	background-color: #4DB6AC;
}
nav .start-contact, a:nth-child(5):hover~.animation {
	width: 20%;
	left: 80%;
	background-color: #00BFA5;
} */

body {
  font-size: 12px;
  font-family: sans-serif;
  background: #2c3e50;
}
h1 {
  text-align: center;
  margin: 40px 0 40px;
  text-align: center;
  font-size: 30px;
  color: #ecf0f1;
  text-shadow: 2px 2px 4px #000000;
  font-family: "Cherry Swash", cursive;
}

p {
  position: absolute;
  bottom: 20px;
  width: 100%;
  text-align: center;
  color: #ecf0f1;
  font-family: "Cherry Swash", cursive;
  font-size: 16px;
}

span {
  color: #2bd6b4;
}

.do {
  font-family: "Do Hyeon", sans-serif;
}
</style>