<template>
  <div id="main">
    <br />
    <div style="text-align: center">
      <v-row no-gutters>
        <v-col md="6" offset-md="3">
          <v-divider></v-divider>
        </v-col>
      </v-row>
      <h1 class="do">도서 리뷰</h1>
      <v-row no-gutters>
        <v-col md="6" offset-md="3">
          <v-divider></v-divider>
        </v-col>
      </v-row>
      <br />
      <mdb-form-inline
        class="active-green active-green-4 d-flex justify-content-end"
        style="margin-right: 12%"
      >
        <input
          class="form-control mr-sm-2"
          type="text"
          placeholder="검색어를 입력해주세요."
          aria-label="Search"
          v-model="searchWord"
          style="
            font-family: HangeulNuri-Bold;
            text-align: center;
            height: 50.88px;
          "
          @keydown.enter="search"
        />
        <mdb-dropdown>
          <mdb-dropdown-toggle
            slot="toggle"
            color="teal"
            style="
              font-family: 'HangeulNuri-Bold';
              text-align: center;
              font-size: medium;
            "
            >{{ dropDown }}</mdb-dropdown-toggle
          >
          <mdb-dropdown-menu>
            <mdb-dropdown-item
              style="
                font-family: 'HangeulNuri-Bold';
                text-align: center;
                color: black;
              "
              @click="searchList(0)"
              >리뷰제목</mdb-dropdown-item
            >
            <mdb-dropdown-item
              style="
                font-family: 'HangeulNuri-Bold';
                text-align: center;
                color: black;
              "
              @click="searchList(3)"
              >리뷰내용</mdb-dropdown-item
            >
            <mdb-dropdown-item
              style="
                font-family: 'HangeulNuri-Bold';
                text-align: center;
                color: black;
              "
              @click="searchList(1)"
              >리뷰작성자</mdb-dropdown-item
            >
            <mdb-dropdown-item
              style="
                font-family: 'HangeulNuri-Bold';
                text-align: center;
                color: black;
              "
              @click="searchList(2)"
              >책이름</mdb-dropdown-item
            >
          </mdb-dropdown-menu>
        </mdb-dropdown>
        <mdb-btn @click="search" color="default"
          ><mdbIcon icon="search" style="color: white; text-align: center"
        /></mdb-btn>
      </mdb-form-inline>
    </div>
    <br />
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

    <div class="container">
      <div class="row" v-if="reviews != '검색 결과가 없습니다.'">
        <div
          class="col-lg-6 col-sm-12"
          v-for="review of reviewData"
          :item="review"
          :key="review.id"
          style="width: 48%"
        >
          <v-card>
            <v-row style="height: 470px">
              <v-col cols="5" style="margin-left: 2%">
                <div class="card">
                  <v-card class="d-inline-block" style="width: 100%">
                    <v-container>
                      <v-row justify="space-between">
                        <v-col cols="12" style="width: 100%" class="cursor">
                          <v-img
                            v-if="review.book_img_url"
                            height="100%"
                            width="100%"
                            :src="review.book_img_url"
                          ></v-img>
                          <v-img
                            v-else
                            height="100%"
                            width="100%"
                            src="@/assets/img/no-image.jpg"
                          ></v-img>
                          <div class="details" @click="gotoDetail(review.book)">
                            <h6 class="do" style="font-size: large">
                              {{ review.book_title }} 자세히보기
                            </h6>
                          </div>
                        </v-col>
                      </v-row>
                      <v-row
                        class="d-flex justify-content-center"
                        style="margin-left: 2%"
                      >
                        <h4 v-if="review.book_title.length > 9" class="do">
                          {{ review.book_title.slice(0, 9) }}...
                        </h4>
                        <h4 v-else class="do">
                          {{ review.book_title }}
                        </h4>
                      </v-row>
                    </v-container>
                  </v-card>
                </div>
              </v-col>
              <v-col cols="6" class="d-flex flex-column">
                <div>
                  <v-list-item
                    uk-tooltip="사용자 프로필 가기"
                    @click="goToActivity(review.user)"
                  >
                    <v-row>
                      <v-col cols="4">
                        <div>
                          <v-img
                            :src="review.profile_url"
                            class="rounded-circle"
                          >
                          </v-img>
                        </div>
                      </v-col>
                      <v-col>
                        <h5
                          style="
                            font-family: HangeulNuri-Bold;
                            font-size: large;
                          "
                        >
                          {{ review.user_name }}
                        </h5>
                      </v-col>
                    </v-row>
                  </v-list-item>
                </div>
                <div>
                  <v-card-text style="margin-left: 2%">
                    <h4
                      v-if="review.title.length > 8"
                      style="color: #1a237e"
                      class="do"
                    >
                      제목 : {{ review.title.slice(0, 8) }}...
                    </h4>
                    <h4 v-else style="color: #1a237e" class="do">
                      제목 : {{ review.title }}
                    </h4>
                    <hr />
                    <p
                      v-if="review.content.length > 22"
                      style="font-family: HangeulNuri-Bold; font-size: large"
                    >
                      내용 : {{ review.content.slice(0, 22) }}...
                    </p>
                    <p
                      v-else
                      style="font-family: HangeulNuri-Bold; font-size: large"
                    >
                      내용 : {{ review.content }}
                    </p>
                    <hr />

                    <p style="font-family: HangeulNuri-Bold">
                      내용 평점 :
                      <span v-for="num in review.content_score" :key="num.id">
                        <i class="fas fa-star" style="color: yellow"></i>
                      </span>
                    </p>
                    <p style="font-family: HangeulNuri-Bold">
                      디자인 평점 :
                      <span v-for="num in review.design_score" :key="num.id">
                        <i class="fas fa-star" style="color: yellow"></i>
                      </span>
                    </p>
                  </v-card-text>
                </div>

                <div class="bottomIcon">
                  <v-list-item-subtitle
                    style="font-family: HangeulNuri-Bold; font-size: medium"
                    class="d-flex justify-content-end"
                    >{{ review.created_at.slice(0, 10) }}
                    {{ review.created_at.slice(11, 16) }}
                  </v-list-item-subtitle>

                  <v-row class="d-flex justify-content-end">
                    <v-btn
                      icon
                      @click="reviewLike(review)"
                      v-if="!review.review_like_state"
                    >
                      <v-icon color="red" uk-tooltip="리뷰 좋아요"
                        >mdi-heart-outline</v-icon
                      >
                    </v-btn>
                    <v-btn icon @click="reviewLike(review)" v-else>
                      <v-icon
                        color="red"
                        icon="heart-broken"
                        uk-tooltip="좋아요 취소"
                      >
                        mdi-heart
                      </v-icon>
                    </v-btn>
                    <p
                      style="
                        font-family: HangeulNuri-Bold;
                        font-size: large;
                        margin: 3% 0 0 0;
                      "
                    >
                      {{ review.review_like_count }}
                    </p>
                    <v-btn icon @click="gotoReviewDetail(review.id)">
                      <i
                        class="fas fa-plus"
                        uk-tooltip="리뷰 자세히보기"
                        style="color: #00bfa5"
                      ></i>
                    </v-btn>
                  </v-row>
                </div>
              </v-col>
            </v-row>
          </v-card>
          <br />
        </div>
      </div>
      <div class="row no-review" v-else>
        <h4 style="font-family: HangeulNuri-Bold">
          '{{ searchWord }}' 에 대한 검색결과가 없습니다.
        </h4>
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
  </div>
</template>

<script>
import VueCookies from "vue-cookies";
import swal from "sweetalert";
import {
  mdbIcon,
  mdbBtn,
  mdbFormInline,
  mdbDropdown,
  mdbDropdownItem,
  mdbDropdownMenu,
  mdbDropdownToggle,
} from "mdbvue";
import axios from "axios";

export default {
  components: {
    mdbIcon,
    mdbFormInline,
    mdbDropdown,
    mdbDropdownItem,
    mdbDropdownMenu,
    mdbDropdownToggle,
    mdbBtn,
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
      reviews: [],
      nextItem: 0,
      searchWord: null,
      searchType: 0,

      isDetect: true,
      isLoading: false,
      // 스크롤
      fab: false,
      dialog: [],
      star: null,
      reviewData: [],
      dropDown: "리뷰제목",
      btnTitle: "리뷰수정",
      contentStar: 3,
    };
  },
  created() {
    this.isLoading = true;
    // 리뷰 불러오는 코드
    axios
      .get(`${process.env.VUE_APP_SERVER_URL}/reviews/community/`, {
        params: {
          user_pk: VueCookies.get("user_pk"),
        },
        // Back에서 원하는 데이터
        headers: { Authorization: VueCookies.get("jwt_token") },
      })
      .then((res) => {
        this.reviews = res.data.result;
        this.nextItem = 0;
        this.reviewData = [];
        this.isLoading = false;
        this.loadMore();
      })

  },
  // 무한 스크롤
  mounted() {
    const el = document.querySelector("#main");
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
    reviewLike(review) {
      axios
        .get(`${process.env.VUE_APP_SERVER_URL}/reviews/like/`, {
          params: {
            user_pk: VueCookies.get("user_pk"),
            review_pk: review.id,
          },
        })
        .then((res) => {
          review.review_like_state = !review.review_like_state;
          review.review_like_count = res.data.review_like_count;
        })

    },
    loadMore() {
      this.isLoading = true;
      if (this.reviews.length - this.nextItem > 9) {
        for (let i = 0; i < 10; i++) {
          let nextReview = this.reviews[this.nextItem++];
          this.reviewData.push(nextReview);
        }
      } else if (this.reviews.length - this.nextItem == 0) {
        this.isLoading = false;
      } else {
        for (let i = 0; i <= this.reviews.length - this.nextItem; i++) {
          let nextReview = this.reviews[this.nextItem++];
          this.reviewData.push(nextReview);
        }
      }
      this.isLoading = false;
    },

    // 검색하는 함수
    search() {
      axios
        .get(`${process.env.VUE_APP_SERVER_URL}/reviews/community/`, {
          params: {
            user_pk: VueCookies.get("user_pk"),
            search_word: this.searchWord,
            search_type: this.searchType,
          },
          headers: {
            Authorization: VueCookies.get("jwt_token"),
          },
        })
        .then((res) => {
          this.reviewData = [];
          this.nextItem = 0;
          this.reviews = res.data.result;
          this.loadMore();

        })
    },
    searchList(id) {
      if (id == 0) {
        this.dropDown = "리뷰제목";
        this.searchType = id;
      } else if (id == 1) {
        this.dropDown = "리뷰작성자";
        this.searchType = id;
      } else if (id == 3) {
        this.dropDown = "리뷰내용";
        this.searchType = id;
      } else {
        this.dropDown = "책이름";
        this.searchType = id;
      }
    },
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
    gotoDetail(id) {
      this.$router.push(`bookdetail/${id}`);
    },
    goToActivity(id) {
      this.$router.push(`/activity/${id}`);
    },
    gotoReviewDetail(id) {
      this.$router.push({
        name: "ReviewDetail",
        params: {
          pk: id,
        },
      });
    },
  },
};
</script>

<style scoped>
.cursor {
  cursor: pointer;
}
#main {
  height: inherit;
  width: 1080px;
  margin: 0 auto;
}

.no-review {
  vertical-align: middle;
  background-image: url("/src/assets/img/물음표.png");
  text-align: center;
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

.active-green-2 input[type="text"]:focus:not([readonly]) {
  border: 1px solid#2BBBAD;
  box-shadow: 0 1px 0 0 #2bbbad;
}
.active-green input[type="text"] {
  border: 1px solid #2bbbad;
  box-shadow: 0 1px 0 0 #2bbbad;
  text-align: center;
}
.active-cyan .fa,
.active-cyan-2 .fa {
  color: #2bbbad;
}
@font-face {
  font-family: "HangeulNuri-Bold";
  src: url("https://cdn.jsdelivr.net/gh/projectnoonnu/noonfonts_three@1.0/HangeulNuri-Bold.woff")
    format("woff");
  font-weight: normal;
  font-style: normal;
  font-size: x-large;
}
.bottomIcon {
  align-self: flex-end;
}

.card {
  left: 50%;
  top: 50%;
  transform: translate(-50%, -50%);
  background: #262626;
  overflow: hidden;
}
.card .imgBx,
.card .details {
  position: absolute;
  box-sizing: border-box;
  transition: 0.5s;
}

.card .details {
  background: #1a237e;
  top: 0;
  left: 100%;
  padding: 30px 20px;
  width: 100%;
  height: 100%;
}
.card:hover .details {
  width: 100%;
  height: 100%;
  top: 0;
  left: 0%;
}
.card .details h6 {
  color: #fff;
  text-align: center;
  padding: 0 0 10px;
  margin-top: 50%;
}
.do {
  font-family: "Do Hyeon", sans-serif;
}

.btn.btn-default.ripple-parent {
  padding: 1.5% 2% 1.5% 2%;
}
.card {
  max-height: 430px;
}
</style>
