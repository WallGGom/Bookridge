<template>
  <v-row justify="center">
    <v-dialog
      v-model="loginDialog"
      @click:outside="closeLoginModal"
      class="my-2"
      width="70%"
    >
      <div id="wrapper">
        <div id="container" class="p-0">
          <section class="open-book">
            <header>
              <h1>BookRidge</h1>
              <h6>SSAFY</h6>
            </header>
            <article>
              <h4 class="chapter-title" style="font-family: TmonMonsori;">로그인</h4>

              <v-container>
                <v-row justify="center">
                  <v-col cols="12" class="py-0">
                    <v-text-field
                      class="do"
                      ref="emailInput"
                      v-model="email"
                      label="아이디"
                      required
                      color="#009688"
                      style='font-size:x-large'
                    ></v-text-field>
                    <!-- <p class="hint-size caption">'아이디@bookridge.com' 형식으로 입력해주세요.</p> -->
                  </v-col>
                  <v-col cols="12" class="py-0">
                    <v-text-field
                      class="do"
                      color="#009688"
                      ref="passwordInput"
                      v-model="password"
                      label="비밀번호"
                      type="password"
                      hint
                      required
                      style="font-size:x-large"
                      @keydown.enter="login"
                    ></v-text-field>
                  </v-col>
                  <v-spacer></v-spacer>
                  <div class="d-flex justify-center">
                    <v-btn
                      class="main-font do"
                      color="green darken-1"
                      @click="login"
                      outlined
                      >로그인</v-btn
                    >
                  </div>
                </v-row>
              </v-container>
              <h6 class="text-center highlight main-font">
                아직 회원이 아니신가요?
                <v-btn
                  color="green darken-1"
                  text
                  @click="closeLoginModal"
                  to="/signup"
                  >회원가입</v-btn
                >
              </h6>

              <h4 class="chapter-title"  style="font-family: TmonMonsori;">SNS 로그인</h4>
              <v-card-text class="pt-5">
                <v-row>
                  <v-col cols="3">
                    <img
                      class="tempLogin"
                      src="@/assets/img/kakao_btn.png"
                      height="45px"
                      width="45px"
                    />
                  </v-col>
                  <v-col cols="9">
                    <v-btn text :href="kakaoRedirect"
                      ><h6 class="main-font" style="font-size:large;">카카오 로그인</h6></v-btn
                    >
                  </v-col>
                </v-row>
                <v-row>
                  <v-col cols="3">
                    <img
                      class="tempLogin"
                      src="@/assets/img/google_btn.png"
                      height="45px"
                      width="45px"
                    />
                  </v-col>
                  <v-col cols="9">
                    <v-btn text :href="googleRedirect"
                      ><h6 class="main-font" style="font-size:large;">구글 로그인</h6></v-btn
                    >
                  </v-col>
                </v-row>
              </v-card-text>
              <v-spacer></v-spacer>
              <v-card-actions class="justify-content-end mt-5">
                <v-btn
                  class="mt-5 main-font do"
                  color="green darken-1"
                  text
                  outlined
                  @click="closeLoginModal"
                  style="font-size:medium"
                  >닫기</v-btn
                >
              </v-card-actions>
            </article>
            <footer>
              <ol id="page-numbers">
                <li>1</li>
                <li>2</li>
              </ol>
            </footer>
          </section>
        </div>
      </div>
    </v-dialog>
  </v-row>
</template>

<script>
import swal from "sweetalert";
import axios from "axios";
import VueCookies from "vue-cookies";

export default {
  name: "LoginDialog",
  props: {
    loginDialog: Boolean,
  },
  data() {
    return {
      kakaoRedirect: `${process.env.VUE_APP_SERVER_URL}/accounts/kakao_login/`,
      googleRedirect: `${process.env.VUE_APP_SERVER_URL}/accounts/google_login/`,

      ///////////
      email: "",
      password: "",
    };
  },
  methods: {
    login() {
      axios
        .post(`${process.env.VUE_APP_SERVER_URL}/accounts/login/`, {
          email: this.email + "@bookridge.com",
          password: this.password,
        })
        .then((res) => {
          if (res.data.error) {
            swal("아이디 비밀번호를 확인해주세요!");
          } else {
            VueCookies.set("jwt_token", res["data"]["token"], "6h");
            VueCookies.set("user_pk", res["data"]["user_pk"], "6h");
            VueCookies.set("social_id", 0, "6h");

            this.closeLoginModal();
            this.$router.push("/main");
            this.$router.go();
            this.dialog3 = true;
          }
        })
        .catch((err) => {
          this.err = err;
          alert("아이디 또는 비밀번호를 확인해주세요.");
        });
    },
    closeLoginModal() {
      this.email = "";
      this.password = "";
      this.$emit("closeLoginModal");
    },
    loginInputEnter() {
      if (this.email !== "" && this.password === "") {
        this.$refs.passwordInput.focus();
      } else if (this.password !== "" && this.email === "") {
        this.$refs.emailInput.focus();
      } else {
        this.login();
      }
    },
  },
};
</script>

<style scoped>
.main-font {
  font-family: "HangeulNuri-Bold";
}

.tempLogin {
  height: 40px;
}
a {
  border-radius: 5px;
}
a:hover {
  opacity: 0.7;
}
.hint-size {
  font-size: 12px;
}
/*  */

@import url(https://fonts.googleapis.com/css?family=Crimson+Text:400,700,900,400italic,700italic,900italic|Playfair+Display:400,700,900,400italic,700italic,900italic|Rock+Salt:400);

*,
:before,
:after {
  box-sizing: border-box;
}

body {
  background-color: #1d1f20;
  color: #e5e5e5;
  font: 16px/1.25 "Crimson Text", sans-serif;
  margin: 0;
}

#wrapper {
  width: 100%;
  padding: 5px;
}

#container {
  margin-left: auto;
  margin-right: auto;
}

/*** OPEN BOOK ***/
.open-book {
  background: #fff;
  box-shadow: rgba(0, 0, 0, 0.5) 0 1em 3em;
  color: #000;
  padding: 2em;
}

.open-book * {
  position: relative;
}

/* Highlight */
.open-book *::-moz-selection {
  background: rgba(222, 255, 0, 0.75);
}

.open-book *::selection {
  background: rgba(222, 255, 0, 0.75);
}

/* Header/Footer */
.open-book header {
  padding-bottom: 1em;
}

.open-book header *,
.open-book footer * {
  font: 700 1em/1.25 "Playfair Display", sans-serif;
  letter-spacing: 0.125em;
  margin: 0;
}

.open-book header * {
  font-size: 0.75em;
  text-transform: uppercase;
}

.open-book footer {
  padding-top: 1em;
}

.open-book footer #page-numbers {
  display: none;
  list-style: none;
  padding: 0;
  text-align: left;
}

.open-book footer #page-numbers > li:last-child {
  text-align: right;
}

/* Chapter Title */
.open-book .chapter-title {
  background: url(data:image/svg+xml;base64,PD94bWwgdmVyc2lvbj0iMS4wIiBlbmNvZGluZz0idXRmLTgiPz4NCjxzdmcgdmVyc2lvbj0iMS4xIiBpZD0iTGF5ZXJfMSIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIiB4bWxuczp4bGluaz0iaHR0cDovL3d3dy53My5vcmcvMTk5OS94bGluayIgeD0iMHB4IiB5PSIwcHgiDQoJIHZpZXdCb3g9IjAgMCA2NCA2NCIgc3R5bGU9ImVuYWJsZS1iYWNrZ3JvdW5kOm5ldyAwIDAgNjQgNjQ7IiB4bWw6c3BhY2U9InByZXNlcnZlIj4NCiAgICA8Zz4NCiAgICAJPHBhdGggZD0iTTAsMzJMMzIsMGwzMiwzMkwzMiw2NEwwLDMyeiBNOCwzMmwyNCwyNGwyNC0yNEwzMiw4TDgsMzJ6IE0xNiwzMmwxNi0xNmwxNiwxNkwzMiw0OEwxNiwzMnogTTI0LDMybDgsOGw4LThsLTgtOEwyNCwzMnoiIC8+DQogICAgPC9nPg0KPC9zdmc+)
    bottom center no-repeat;
  background-size: 0.5em 0.5em;
  font: 700 7vw/1.25 "HangeulNuri-Bold", sans-serif;
  letter-spacing: 0.125em;
  margin: 0 0 1em 0;
  padding: 1em 0;
  position: relative;
  text-align: center;
  text-transform: uppercase;
}

.open-book .chapter-title:before,
.open-book .chapter-title:after {
  border: solid 0 #000;
  border-width: 0.05em 0;
  bottom: calc((0.125em / 2) * 3);
  content: "";
  height: 0.15em;
  position: absolute;
  width: calc(50% - (1em / 2));
}

.open-book .chapter-title:before {
  left: 0;
}

.open-book .chapter-title:after {
  right: 0;
}

/* Body Copy */
.open-book article {
  line-height: 1.5;
}

.open-book article *:not(.chapter-title):not(hr):not(dl) {
  margin: 0 auto;
  max-width: 28.125em;
}

.open-book article p {
  text-indent: 2em;
}

.open-book .chapter-title + p:first-of-type {
  text-indent: 0;
}

.open-book .chapter-title + p:first-of-type:first-letter {
  float: left;
  font: 700 3em/0.65 "HangeulNuri-Bold", sans-serif;
  padding: 0.15em 0.05em 0 0;
  text-transform: uppercase;
}

/*** MEDIA QUERIES ***/
@media only screen and (min-width: 50em) {
  .open-book {
    margin: 1em;
    position: relative;
  }

  .open-book:before {
    background-color: #8b4513;
    border-radius: 0.25em;
    bottom: -1em;
    content: "";
    left: -1em;
    position: absolute;
    right: -1em;
    top: -1em;
    z-index: -1;
  }

  .open-book:after {
    background: linear-gradient(
      to right,
      transparent 0%,
      rgba(0, 0, 0, 0.2) 46%,
      rgba(0, 0, 0, 0.5) 49%,
      rgba(0, 0, 0, 0.6) 50%,
      rgba(0, 0, 0, 0.5) 51%,
      rgba(0, 0, 0, 0.2) 52%,
      transparent 100%
    );
    bottom: -1em;
    content: "";
    left: 50%;
    position: absolute;
    top: -1em;
    transform: translate(-50%, 0);
    width: 4em;
    z-index: 1;
  }

  .open-book > * {
    column-count: 2;
    column-gap: 6em;
    position: relative;
    z-index: 1;
  }

  /* Header/Footer */
  .open-book header:before,
  .open-book header:after,
  .open-book footer:before,
  .open-book footer:after {
    background: #fff;
    border-radius: 25%;
    content: "";
    height: 2em;
    position: absolute;
    z-index: -1;
    width: calc(50% + 2em);
  }

  .open-book header:before,
  .open-book footer:before,
  .open-book footer:after {
    border-top-left-radius: 0;
  }

  .open-book header:after,
  .open-book footer:before,
  .open-book footer:after {
    border-top-right-radius: 0;
  }

  .open-book header:before,
  .open-book header:after,
  .open-book footer:after {
    border-bottom-right-radius: 0;
  }

  .open-book header:before,
  .open-book header:after,
  .open-book footer:before {
    border-bottom-left-radius: 0;
  }

  .open-book header:before,
  .open-book header:after {
    top: -2.65em;
  }

  .open-book header:before,
  .open-book footer:before {
    right: 50%;
  }

  .open-book header:before {
    transform: rotate(-2deg);
  }

  .open-book header:after,
  .open-book footer:after {
    left: 50%;
  }

  .open-book header:after {
    transform: rotate(2deg);
  }

  .open-book footer:before,
  .open-book footer:after {
    bottom: -2.65em;
  }

  .open-book footer:before {
    transform: rotate(2deg);
  }

  .open-book footer:after {
    transform: rotate(-2deg);
  }

  .open-book header > *:last-child,
  .open-book footer > *:last-child {
    text-align: right;
  }

  .open-book footer #page-numbers {
    display: block;
  }

  /* Chapter Title */
  .open-book .chapter-title {
    font-size: 2em;
  }

  .open-book .chapter-title:before,
  .open-book .chapter-title:after {
    height: 0.125em;
  }
}

.do {
  font-family: "Do Hyeon", sans-serif;
}

@font-face {
  font-family: "TmonMonsori";
  src: url("https://cdn.jsdelivr.net/gh/projectnoonnu/noonfonts_two@1.0/TmonMonsori.woff")
    format("woff");
  font-weight: lighter;
  font-style: normal;
}
</style>