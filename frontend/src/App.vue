<template class="something">
  <v-app>
    <v-container>
      <Header :isLogin="isLogin" v-if="isLogin" :key="$route.fullPath" />
      <Navbar :isLogin="isLogin" v-if="isLogin" :curRou="$router.currentRoute.name" />
    </v-container>
    <router-view :key="$route.fullPath" @goToAlgorithm="receiveAlgorithm" :algorithm="algorithm" style="min-height: 800px"></router-view>
    <br>
    <br>
    <Footer style=" position:fixed bottom:0 width:100% height:100px;" />
  </v-app>
</template>

<script>
// import axios from 'axios'
import VueCookies from "vue-cookies";
import Header from "./components/Header.vue";
import Navbar from "./components/Navbar.vue";
import Footer from "./components/Footer.vue";
export default {
  name: "App",

  components: {
    Header,
    Navbar,
    Footer
  },
  created() {
    this.checkIsLogin();
  },
  data() {
    return {
      algorithm: null,
      isLogin: false,
      imgUrl: "",
    };
  },
  methods: {
    aboutLoading() {
      this.isLoading = true
    },
    receiveAlgorithm(data) {
      this.algorithm = data
      // console.log(data)
    },
    checkIsLogin() {
      if (VueCookies.get("jwt_token") && VueCookies.get("user_gender") != 2) {
        this.isLogin = true;
      } else {
        this.isLogin = false;
      }
    },
  },
};
</script>

<style>
.something {
  color: var(--v-primary-base);
  background-color: var(--v-accent-lighten2);
}

::-webkit-scrollbar {
  width: 15px;
}

::-webkit-scrollbar-thumb {
  background-color: #4db6ac;
  border-radius: 5px;
  background-clip: padding-box;
  border: 1px solid transparent;
}

::-webkit-scrollbar-track {
  background-color: whitesmoke;
  border-radius: 10px;
  box-shadow: inset 0px 0px 5px white;
}
</style>