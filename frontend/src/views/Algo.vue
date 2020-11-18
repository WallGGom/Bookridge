<template>
  <mdb-container>
    <!-- <p class="do" style="text-align: center">알고리즘 설명</p> -->
    <br /><br />
    <h1 v-show="temp" style="font-family: HangeulNuri-Bold; text-align: center">
      {{ algorithms.theme }}
    </h1>
    <h6 v-show="temp" style="font-family: HangeulNuri-Bold; text-align: center">추천 도서 리스트에서 원하는 책을 클릭해보세요!</h6>

    <br /><br />
    <v-system-bar dark color="#34495e" v-show="temp">
      <v-spacer></v-spacer>
    </v-system-bar>
    <h3 v-show="temp" style="font-family: HangeulNuri-Bold; text-align: center" class="my-5">📖 도서 추천 리스트 📖</h3>
    <v-system-bar dark color="#34495e" v-show="temp">
      <v-spacer></v-spacer>
    </v-system-bar>
    <mdb-row v-if="temp">
      <mdb-col
        col="3"
        lg="3"
        md="4"
        sm="6"
        v-for="alg of algorithms.algo"
        :item="alg"
        :key="alg.id"
      >
        <mdb-card style="height: 680px">
          <mdb-row>
            <mdb-col col="12" class="pic pb-0">
              <mdb-view hover class="zoom">
                <img
                  v-if="alg.img_url"
                  :src="alg.img_url"
                  alt="bookImage"
                  class="bookimage"
                />
                <img
                  v-else
                  src="@/assets/img/no-image.jpg"
                  alt="bookImage"
                  class="bookimage"
                />
                <mdb-mask flex-center waves overlay="black-strong">
                  <mdb-btn
                    outline="white"
                    @click="gotoDetail(alg.id)"
                    style="
                      width: 220px;
                      height: 300px;
                      font-size: large;
                      font-family: HangeulNuri-Bold;
                    "
                    >자세히 보기</mdb-btn
                  >
                </mdb-mask>
              </mdb-view>
            </mdb-col>
            <mdb-row>
              <mdb-card-body style="text-align: center" class="pt-0 mb-5">
                <h4 class="do" style="margin: 0 5% 0 5%">
                  {{ alg.title }}
                </h4>

                <br />
                <p style="font-family: HangeulNuri-Bold; margin-left: 5%">
                  {{ alg.author }}
                </p>
                <p style="font-family: HangeulNuri-Bold; margin-left: 5%">
                  출판사 : {{ alg.publisher }}
                </p>
                <p style="font-family: HangeulNuri-Bold; margin-left: 5%">
                  출판년도 : {{ alg.pub_date }}년
                </p>
              </mdb-card-body>
            </mdb-row>
          </mdb-row>
        </mdb-card>
      </mdb-col>
    </mdb-row>
    <div v-if="!temp" class="loading">
      <div class="spinner-grow text-primary" role="status">
        <span class="sr-only">Loading...</span>
      </div>
      <div class="spinner-grow text-secondary" role="status">
        <span class="sr-only">Loading...</span>
      </div>
      <div class="spinner-grow text-success" role="status">
        <span class="sr-only">Loading...</span>
      </div>
      <div class="spinner-grow text-danger" role="status">
        <span class="sr-only">Loading...</span>
      </div>
      <div class="spinner-grow text-warning" role="status">
        <span class="sr-only">Loading...</span>
      </div>
      <div class="spinner-grow text-info" role="status">
        <span class="sr-only">Loading...</span>
      </div>
      <div class="spinner-grow text-light" role="status">
        <span class="sr-only">Loading...</span>
      </div>
      <div class="spinner-grow text-dark" role="status">
        <span class="sr-only">Loading...</span>
      </div>
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
      <v-icon>mdi-arrow-up-thick</v-icon>
    </v-btn>
  </mdb-container>
</template>

<script>
import {
  mdbContainer,
  mdbRow,
  mdbCol,
  mdbMask,
  mdbBtn,
  mdbView,
  mdbCard,
  mdbCardBody,
} from "mdbvue";
import axios from "axios";
import VueCookies from "vue-cookies";

export default {
  name: "Algo",
  data() {
    return {
      name: null,
      age: null,
      gender: null,

      urlName: null,
      algorithms: {},
      isLoading: false,
      fab: false,
      temp: false,
    };
  },
  components: {
    mdbContainer,
    mdbRow,
    mdbCol,
    mdbMask,
    mdbBtn,
    mdbView,
    mdbCard,
    mdbCardBody,
  },
  props: {
    algorithm: Object,
  },

  created() {
    this.$vuetify.goTo(0);
    if (!this.algorithm) {
      if (this.$route.params.pk == 0) {
        axios
          .get(`${process.env.VUE_APP_SERVER_URL}/analyze/feature_temp/`, {
            // Back에서 원하는 데이터
            headers: { Authorization: VueCookies.get("jwt_token") },
          })

          .then((res) => {
            // this.age = parseInt(res.data.info.age / 365);
            this.age = res.data.info.age;
            var rest = this.age % 10;
            this.age = this.age - rest;
            if (res.data.info.gender == 0) {
              this.gender = "남성";
            } else {
              this.gender = "여성";
            }
            this.name = res.data.info.name;

            if (this.age != 0) {
              this.algorithms["theme"] =
                this.age + "대" + this.gender + "을 위한 책";
            } else {
              this.algorithms["theme"] = "어린이를 위한 책";
            }

            this.algorithms["algo"] = res.data.feature;
          })
          // .catch((err) => {
          //   console.log(err);
          // });
        setTimeout(() => {
          this.temp = true;
        }, 2000);
      } else {
        if (this.$route.params.pk == 1) {
          this.urlName = "desc_temp";
          this.algorithms["theme"] = "좋아요한 도서의 줄거리기반 추천";
        } else if (this.$route.params.pk == 2) {
          this.urlName = "review_temp";
          this.algorithms["theme"] = "작성한 리뷰 기반의 도서 추천";
        } else if (this.$route.params.pk == 3) {
          this.urlName = "title_temp";
          this.algorithms["theme"] = "좋아요한 도서와 비슷한 주제의 도서 추천";
        } else {
          this.urlName = "recommend_temp";
          this.algorithms["theme"] = "나와 비슷한 사용자들이 읽은 책 추천";
        }
        axios
          .get(`${process.env.VUE_APP_SERVER_URL}/analyze/${this.urlName}/`, {
            // Back에서 원하는 데이터
            headers: { Authorization: VueCookies.get("jwt_token") },
          })
          .then((res) => {
            this.algorithms["algo"] = res.data.data;
          })
          // .catch((err) => {
          //   console.log(err);
          // });
        setTimeout(() => {
          this.temp = true;
        }, 4000);
      }
    } else {
      this.algorithms = this.algorithm;
      this.temp = true;
    }
  },
  methods: {
    loadAlgo() {},
    gotoDetail(id) {
      this.$router.push(`/bookdetail/${id}`);
    },
    onScroll(e) {
      if (typeof window === "undefined") return;
      const top = window.pageYOffset || e.target.scrollTop || 0;
      this.fab = top > 20;
    },
    toTop() {
      this.$vuetify.goTo(0);
    },
  },
};
</script>

<style scoped>
@font-face {
  font-family: "HangeulNuri-Bold";
  src: url("https://cdn.jsdelivr.net/gh/projectnoonnu/noonfonts_three@1.0/HangeulNuri-Bold.woff")
    format("woff");
  font-weight: normal;
  font-style: normal;
  font-size: x-large;
}
.bookimage {
  width: 200px;
  height: 300px;
  display: block;
  margin: 0px auto;
}
.pic {
  padding: 5%;
}
.loading {
  text-align: center;
  color: black;
  z-index: 2;
  padding: 8px 18px;
  border-radius: 5px;
  left: calc(50% - 105px);
  top: calc(50% - 45px);
}

.pic.col-12 {
  height: 365px;
}

.do {
  font-family: "Do Hyeon", sans-serif;
}
</style>