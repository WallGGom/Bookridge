<template>
  <div></div>
</template>

<script>
import axios from "axios";
import VueCookies from "vue-cookies";
import swal from "sweetalert";
export default {
  name: "OauthGoogle",
  created() {
    const code = this.$route.query.code;
    if (code) {
      // console.log(code);
      axios
        .get(`${process.env.VUE_APP_SERVER_URL}/accounts/oauth2?code=` + code)
        .then((res) => {
          // console.log(response)
          VueCookies.set("jwt_token", res["data"]["token"], "1h");
          VueCookies.set("user_pk", res["data"]["user_pk"], "1h");
          VueCookies.set("social_id", res["data"]["social_id"], "1h");
          VueCookies.set("user_gender", res["data"]["user_gender"], "6h");
          if (res.data.user_gender == 2) {
            this.$router.push({
              name: "Signup",
              params: {
                name: res.data.name,
                email: res.data.email,
                social: res.data.social,
              },
            });
          } else {
            swal(`${res.data.name}님 북릿지에 오신걸 환영합니다. `);
            this.$router.replace("/main");
            this.$router.go();
          }
        })
        .catch((err) => {
          this.err = err;
        });
    } else {
      // this.$router.replace("/")
    }
  },
};
</script>

<style scoped>
</style>