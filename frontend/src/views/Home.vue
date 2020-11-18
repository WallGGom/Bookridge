<template>
  <v-app>
    <div class="home">
      <div class="container do">
        <section class="my-5">
          <div
            class="mb-5"
            uk-scrollspy="cls: uk-animation-slide-bottom; target: .uk-card; delay: 300; repeat: false"
          >
            <div>
              <div
                class="uk-card uk-card-default uk-card-body"
                uk-scrollspy-class="uk-animation-slide-top"
              >
                <p class="d-flex justify-content-start" style="width: 20%">
                  <v-img
                    class=""
                    src="../assets/img/로고.jpg"
                    width="25%"
                    contain
                  ></v-img>
                </p>
                <v-system-bar dark color="#34495e" class="mb-5">
                  <v-spacer></v-spacer>
                </v-system-bar>
                <h2 class="h1-responsive font-weight-bold text-center my-5">
                  Why the BOOKRIDGE?
                </h2>

                <p class="lead grey-text w-responsive text-center mx-auto mb-5">
                  책과 사람을 이어주다.
                </p>
              </div>
            </div>
          </div>

          <div class="uk-child-width-1-2@m uk-grid-match" uk-grid>
            <div>
              <div
                class="uk-card uk-card-default uk-card-body"
                uk-scrollspy="cls: uk-animation-slide-left; repeat: false"
              >
                <v-img class="img-fluid" src="../assets/img/home2.jpg" contain>
                </v-img>
              </div>
            </div>
            <div style="background-color: #009688;" class="py-5 px-5">
              <div
                
                class="uk-card uk-card-default uk-card-body"
                uk-scrollspy="cls: uk-animation-slide-right; repeat: false"
              >
                <h5 class="font-weight-bold mb-3 do" style="font-size: x-large">
                  📖 01. 읽은 책을 기록하고 나누고
                </h5>
                <p class="grey-text" style="font-size: large">
                  지금 어떤 책을 읽고 있는지 기록하고, 다 읽고 난 후에 평점과
                  리뷰를 남기세요. 한 눈에 볼 수 있도록 'BOOKRIDGE'가 잘
                  정리해드립니다.
                </p>
                <br />
                <h5 class="font-weight-bold mb-3 do" style="font-size: x-large">
                  📖 02. 나의 서재로 관리하고
                </h5>
                <p class="grey-text" style="font-size: large">
                  책을 읽다가 기억하고 싶은 글귀를 만났다면, 글로 기록하세요.
                  ‘BOOKRIDGE’가 책 별/페이지 별로 기억해줍니다.
                </p>
                <br />
                <h5 class="font-weight-bold mb-3 do" style="font-size: x-large">
                  📖 03. 활동 내용을 기반으로 추천받고
                </h5>
                <p class="grey-text" style="font-size: large">
                  'BOOKRIDGE'에서의 모든 활동을 기반으로 실시간 도서를
                  추천해드립니다. 다양한 추천방식으로 제공되는 독서의 재미를
                  느껴보세요.
                </p>
              </div>

            </div>
          </div>
          <div class="uk-child-width-1-2@m uk-grid-match" uk-grid>
            <div style="background-color: #009688" class="px-5 py-5">
              <div
                class="uk-card uk-card-default uk-card-body"
                uk-scrollspy="cls: uk-animation-slide-right; repeat: false"
              >
                <h5 class="font-weight-bold mb-3 do" style="font-size: x-large">
                  👍 장르기반 추천
                </h5>
                <p class="grey-text" style="font-size: large">
                  개인정보에 입력하신 장르를 기반으로 도서를 추천해드립니다.
                </p>
                <br />
                <h5 class="font-weight-bold mb-3 do" style="font-size: x-large">
                  👍 나를 위한 추천
                </h5>
                <p class="grey-text" style="font-size: large">
                  개인정보에 입력하신 성별, 생년월일을 기반하여 도서를
                  추천해드립니다.
                </p>
                <br />
                <h5 class="font-weight-bold mb-3 do" style="font-size: x-large">
                  👍 줄거리 기반 도서 추천
                </h5>
                <p class="grey-text" style="font-size: large">
                  선호하는 책에 '좋아요'를 표시해보세요! 좋아하는 줄거리의
                  도서를 <br>추천해드립니다.
                </p>
                <h5 class="mt-5 do" style="font-size: large">
                  이외에도 BOOKRIDGE내의 다양한 활동으로
                </h5>
                <h5 class="ml-5 do" style="font-size: large">
                  도서 추천 서비스와 도서에 대한 다양한 정보를 얻을 수
                  있습니다 😊
                </h5>
              </div>
            </div>
            <div class="pl-0">
              <div
                class="uk-card uk-card-default uk-card-body"
                uk-scrollspy="cls: uk-animation-slide-left; repeat: false"
              >
                <v-img class="img-fluid" src="../assets/img/main.jpg" contain>
                </v-img>
              </div>
            </div>
          </div>
          <div
            class="mt-5"
            uk-scrollspy="cls: uk-animation-slide-bottom; target: .uk-card; delay: 300; repeat: false"
          >
            <div>
              <div class="uk-card uk-card-default uk-card-body">
                <p class="lead grey-text w-responsive text-center mx-auto mb-5">
                  지금 당장 BOOKRIDGE에 가입하세요~
                </p>
                <p class="d-flex justify-content-center">
                  <v-btn
                    class="do mt-5"
                    uk-tooltip="북릿지 시작하기"
                    style="display: block; font-size:20px"
                    v-show="!isLogin"
                    x-large
                    color="#2bbbad"
                    dark
                    @click="loginDialog = true"
                    >로그인</v-btn
                  >
                </p>
                <v-system-bar dark color="#34495e" class="mb-5">
                  <v-spacer></v-spacer>
                </v-system-bar>
              </div>
            </div>
          </div>
        </section>
      </div>
      <v-btn
        v-scroll="onScroll"
        v-show="fab"
        fab
        dark
        fixed
        bottom
        right
        color="#34495e"
        @click="toTop"
      >
        <i class="fas fa-arrow-up" style="color: white"></i>
      </v-btn>
      <!-- login dialog -->
      <LoginDialog
        :loginDialog="loginDialog"
        @closeLoginModal="closeLoginModal"
      />
    </div>
  </v-app>
</template>

<script>
import VueCookies from "vue-cookies";
// import swal from "sweetalert";
import LoginDialog from "../components/LoginDialog";
// import { mdbContainer, mdbRow, mdbCol, mdbIcon } from "mdbvue";

export default {
  name: "Home",
  components: {
    LoginDialog,
    // mdbContainer,
    // mdbRow,
    // mdbCol,
    // mdbIcon,
  },
  beforeRouteEnter(to, from, next) {
    // console.log(VueCookies.get('jwt_token'))
    if (VueCookies.get("jwt_token")) {
      next({ path: "/main" });
      // swal("잘못된 접근입니다.2");
    } else {
      next();
    }
  },
  created() {
    this.isLogin = VueCookies.get("jwt_token") ? true : false;
  },
  methods: {
    // 스크롤(Top)
    onScroll(e) {
      if (typeof window === "undefined") return;
      const top = window.pageYOffset || e.target.scrollTop || 0;
      this.fab = top > 20;
    },
    toTop() {
      this.$vuetify.goTo(0);
    },
    closeLoginModal() {
      this.loginDialog = false;
    },
  },
  data() {
    return {
      loginDialog: false,
      // 스크롤(Top)
      fab: false,

      model: 0,
      isLogin: false,
    };
  },
  mounted() {},
};
</script>

<style scoped>
.do {
  font-family: "Do Hyeon", sans-serif;
}
</style>