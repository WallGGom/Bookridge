<template>
  <div id="main">
    <br />

    <!--도서검색결과 있을 시-->
    <h1 style="text-align: center; font-family: HangeulNuri-Bold">
      '{{ searchWord }}'에 대한 검색 결과
    </h1>
    <br />

    <mdb-container>
      <mdb-row>
        <mdb-col col="4" v-for="book in searchData" :item="book" :key="book.id">
          <mdb-card style="height: 700px">
            <mdb-row>
              <mdb-col col="12" class="pic">
                <mdb-view hover class="zoom">
                  <img
                    v-if="book.img_url"
                    :src="book.img_url"
                    alt="bookImage"
                    class="bookimage"
                  />
                  <img
                    v-else
                    src="@/assets/img/no-image.jpg"
                    alt="bookImage"
                    class="bookimage"
                  />
                  <mdb-mask flex-center waves overlay="black-slight">
                    <mdb-btn
                      outline="white"
                      @click="gotoDetail(book.id)"
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
                <mdb-card-body style="text-align: center">
                  <h4 class="do" style="margin: 0 5% 0 5%">
                    {{ book.title }}
                  </h4>

                  <br />
                  <p style="font-family: HangeulNuri-Bold; margin-left: 5%">
                    {{ book.author }}
                  </p>
                  <p style="font-family: HangeulNuri-Bold; margin-left: 5%">
                    출판사 : {{ book.publisher }}
                  </p>
                  <p style="font-family: HangeulNuri-Bold; margin-left: 5%">
                    출판년도 : {{ book.pub_date }}년
                  </p>
                  <div class="d-flex justify-content-center">
                    <v-btn
                      uk-tooltip="책 좋아요"
                      text
                      color="success"
                      @click="like(book)"
                      v-if="!book.like"
                      ><i
                        class="far fa-thumbs-up"
                        style="font-size: x-large"
                      ></i
                    ></v-btn>
                    <v-btn
                      uk-tooltip="책 좋아요 취소"
                      text
                      color="success"
                      @click="like(book)"
                      v-else
                      style="font-family: HangeulNuri-Bold; font-size: x-large"
                      ><i class="fas fa-thumbs-up"></i
                    ></v-btn>
                    <v-btn
                      uk-tooltip="책 싫어요"
                      text
                      color="warning"
                      @click="dislike(book)"
                      v-if="!book.unlike"
                      ><i
                        class="far fa-thumbs-down"
                        style="font-size: x-large"
                      ></i
                    ></v-btn>
                    <v-btn
                      uk-tooltip="책 싫어요 취소"
                      text
                      color="warning"
                      @click="dislike(book)"
                      v-else
                      style="font-family: HangeulNuri-Bold"
                      ><i
                        class="fas fa-thumbs-down"
                        style="font-size: x-large"
                      ></i
                    ></v-btn>
                  </div>
                </mdb-card-body>
              </mdb-row>
            </mdb-row>
          </mdb-card>
        </mdb-col>
      </mdb-row>
      <div v-if="isLoading" class="loading">
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
import axios from "axios";
import VueCookies from "vue-cookies";
import {
  mdbContainer,
  mdbRow,
  mdbCol,
  mdbCard,
  mdbCardBody,
  mdbBtn,
  mdbView,
  mdbMask,
} from "mdbvue";

export default {
  name: "Search",
  data() {
    return {
      likeBooks: null,
      dislikeBooks: null,
      fab: false,
      searchData: null,
      isLoading: false,
      flag: true,
      isDetect: true,
      page: 0,
    };
  },

  components: {
    mdbContainer,
    mdbRow,
    mdbCol,
    mdbCard,
    mdbCardBody,
    mdbBtn,
    mdbView,
    mdbMask,
  },
  created() {
    this.isLoading = true;
    setTimeout(() => {
      this.isLoading = false;
    }, 2000);
    this.searchWord = this.$route.params.search_word;
    this.searchType = this.$route.params.search_type;

    // 책 page0
    axios
      .get(`${process.env.VUE_APP_SERVER_URL}/books/book_search/`, {
        params: {
          page_num: 0,
          search_word: this.searchWord,
          search_type: this.searchType,
        },
        headers: {
          Authorization: VueCookies.get("jwt_token"),
        },
      })
      .then((res) => {
        // console.log("Search 결과");
        // console.log(res);
        if (res.data.result.length) {
          this.searchData = res.data.result;
        } else {
          this.$router.push("/search2");
        }
      })
      // .catch((err) => {
      //   console.log(err);
      // });
    setTimeout(() => {
      this.isLoading = false;
    }, 2000);
  },

  // 무한 스크롤
  mounted() {
    const el = document.querySelector("#main");
    // console.log(el);
    document.addEventListener("scroll", () => {
      const pos = el.scrollHeight - window.scrollY;

      if (pos < 700) {
        if (this.isDetect) {
          this.isDetect = false;
          this.loadMore();
        }
      } else {
        this.isDetect = true;
      }
    });
  },

  methods: {
    like(book) {
      axios
        .get(`${process.env.VUE_APP_SERVER_URL}/accounts/like/`, {
          params: {
            user_pk: VueCookies.get("user_pk"),
            book_pk: book.id,
          },
        })
        .then((res) => {
          // console.log("버튼 결과");
          // console.log(res);
          book.like = res.data.like;
          book.unlike = res.data.unlike;
          // sessionStorage.clear();
          // 좋아요를 누른 상황
        })
        // .catch((err) => {
        //   console.log(err);
        // });
    },
    dislike(book) {
      axios
        .get(`${process.env.VUE_APP_SERVER_URL}/accounts/unlike/`, {
          params: {
            user_pk: VueCookies.get("user_pk"),
            book_pk: book.id,
          },
        })
        .then((res) => {
          // 싫어요를 누른 상황
          // console.log(res);
          book.like = res.data.like;
          book.unlike = res.data.unlike;
          // sessionStorage.clear();
        })
        // .catch((err) => {
        //   console.log(err);
        // });
    },
    onScroll(e) {
      if (typeof window === "undefined") return;
      const top = window.pageYOffset || e.target.scrollTop || 0;
      this.fab = top > 20;
    },
    toTop() {
      this.$vuetify.goTo(0);
    },
    gotoDetail(id) {
      this.$router.push(`/bookdetail/${id}`);
    },
    loadMore() {
      const leng = this.searchData.length;
      if (this.flag && leng % 9 == 0 && !this.isLoading) {
        this.isLoading = true;
        const page = parseInt(this.searchData.length / 9);
        // console.log(page);
        // axios 요청
        axios
          .get(`${process.env.VUE_APP_SERVER_URL}/books/book_search/`, {
            params: {
              page_num: page,
              search_word: this.searchWord,
              search_type: this.searchType,
            },

            headers: {
              Authorization: VueCookies.get("jwt_token"),
            },
          })
          .then((res) => {
            // console.log(res);
            if (this.flag) {
              this.searchData = this.searchData.concat(res.data.result);
            }
            if (res.data.result.length === 0) {
              this.flag = false;
            }
            this.isLoading = false;
          })
          // .catch((err) => {
          //   console.log(err);
          // });
      }
    },
  },
};
</script>

<style scoped>
.pic {
  padding: 5%;
}
.bookimage {
  width: 200px;
  height: 300px;
  display: block;
  margin: 0px auto;
}
@font-face {
  font-family: "MaplestoryOTFBold";
  src: url("https://cdn.jsdelivr.net/gh/projectnoonnu/noonfonts_20-04@2.1/MaplestoryOTFBold.woff")
    format("woff");
  font-weight: 100;
  font-style: normal;
}
@font-face {
  font-family: "HangeulNuri-Bold";
  src: url("https://cdn.jsdelivr.net/gh/projectnoonnu/noonfonts_three@1.0/HangeulNuri-Bold.woff")
    format("woff");
  font-weight: normal;
  font-style: normal;
  font-size: x-large;
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