
<template>
  <div id="app">
    <mdb-container>
      <br /><br />
      <v-row no-gutters>
        <v-col md="6" offset-md="3">
          <v-divider></v-divider>
        </v-col>
      </v-row>
      <h1 class="main-font text-center">전국 도서관 도서대여 통계</h1>

      <h6 style="font-family: HangeulNuri-Bold; text-align: center">
        2017.01~2020.08 기준
      </h6>
      <v-row no-gutters>
        <v-col md="6" offset-md="3">
          <v-divider></v-divider>
        </v-col>
      </v-row>
      <br />
      <span class="main-font d-flex justify-content-center"
        >전국 도서관의 데이터를 종합하여 연령별, 성별, 연도별, 지역별 대여횟수에
        대한 분석을 확인하실 수 있습니다.</span
      >
      <br /><br />
      <v-system-bar dark color="#34495e" class="my-5">
        <v-spacer></v-spacer>
      </v-system-bar>
      <br /><br />
      <v-row>
        <v-col lg="6" sm="12">
          <h2 style="font-family: HangeulNuri-Bold; text-align: center">
            연령별 대여횟수
          </h2>
          <h6 class="main-font text-center">
            연령별 연간 대여횟수를 확인하실 수 있습니다.
          </h6>
          <v-divider></v-divider>
          <Test class="my-5" />
        </v-col>
        <v-col lg="6" sm="12">
          <h2 style="font-family: HangeulNuri-Bold; text-align: center">
            남/여 대여횟수
          </h2>
          <h6 class="main-font text-center">
            성별 연간 대여횟수를 확인하실 수 있습니다.<small class="main-font"
              >(100만 단위)</small
            >
          </h6>
          <v-divider></v-divider>
          <Test2 class="my-5" />
        </v-col>
      </v-row>
      <br /><br />
      <v-system-bar dark color="#34495e" class="my-5">
        <v-spacer></v-spacer>
      </v-system-bar>
      <br /><br />
      <v-row>
        <v-col lg="6" sm="12">
          <h2 style="font-family: HangeulNuri-Bold; text-align: center">
            연도별 대여횟수
          </h2>
          <h6 class="main-font text-center">
            연도별 대여횟수를 확인하실 수 있습니다.
          </h6>
          <v-divider></v-divider>
          <Test3 class="my-5" />
        </v-col>
        <v-col lg="6" sm="12">
          <h2 style="font-family: HangeulNuri-Bold; text-align: center">
            지역별 대여횟수
          </h2>
          <h6 class="main-font text-center">
            지역별 대여횟수를 확인하실 수 있습니다.
          </h6>
          <v-divider></v-divider>
          <Test4 class="my-5" />
        </v-col>
      </v-row>
      <v-system-bar dark color="#34495e" class="my-5">
        <v-spacer></v-spacer>
      </v-system-bar>
      <br />
      <br />
    </mdb-container>
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
      <v-icon>mdi-arrow-up-thick</v-icon>
    </v-btn>
  </div>
</template>

<script>
import VueCookies from "vue-cookies";
import swal from "sweetalert";

import Test from "./analyze_com/Test.vue";
import Test2 from "./analyze_com/Test2.vue";
import Test3 from "./analyze_com/Test3.vue";
import Test4 from "./analyze_com/Test4.vue";

import { mdbContainer } from "mdbvue";

export default {
  name: "Analyze",
  components: {
    mdbContainer,

    // mapChart,
    Test,
    Test2,
    Test3,
    Test4,
  },

  beforeRouteEnter(to, from, next) {
    if (!VueCookies.get("jwt_token")) {
      next("/");
      swal("잘못된 접근입니다.");
    } else {
      next();
    }
  },
  data() {
    return {
      // 스크롤
      fab: false,
      reg_total: {
        경기: 1129399,
        서울: 628411,
        부산: 273940,
        경남: 158725,
        경북: 146993,
        대구: 139800,
        전남: 136435,
        충북: 129146,
        울산: 113490,
        충남: 110563,
        대전: 108220,
        전북: 107546,
        강원: 91613,
        인천: 84053,
        제주: 74859,
        광주: 71993,
        세종: 18446,
      },
    };
  },
  created() {
    this.container = document.getElementById("chart-area");
  },
  methods: {
    // 스크롤(Top)
    onScroll(e) {
      if (typeof window === "undefined") return;
      const top = window.pageYOffset || e.target.scrollTop || 0;
      this.fab = top > 20;
    },

    // 최상단으로 이동하기
    toTop() {
      this.$vuetify.goTo(0);
    },
  },
};
</script>

<style scoped>
.main-font {
  font-family: "HangeulNuri-Bold";
}
.col-lg-8 {
  text-align: center;
}
@font-face {
  font-family: "HangeulNuri-Bold";
  src: url("https://cdn.jsdelivr.net/gh/projectnoonnu/noonfonts_three@1.0/HangeulNuri-Bold.woff")
    format("woff");
  font-weight: normal;
  font-style: normal;
  font-size: x-large;
}
.do {
  font-family: "Do Hyeon", sans-serif;
}
</style>