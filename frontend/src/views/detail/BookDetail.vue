<template>
  <div id="main">
    <mdb-container>
      <mdb-row>
        <mdb-col col="3">
          <img v-if="image" :src="image" style="width: 200px; height: 270px" />
          <img v-else src="@/assets/img/no-image.jpg" />
          <div style="margin-top: 5%">
            <img
              class="cursor"
              uk-tooltip="교보문고 바로가기"
              src="@/assets/img/교보문고.jpg"
              @click="kyobo"
              style="
                border-radius: 50%;
                width: 50px;
                height: 50px;
                margin: 0 5% 0 5%;
              "
              alt
            />
            <img
              class="cursor"
              uk-tooltip="yes24 바로가기"
              src="@/assets/img/yes24.jpg"
              @click="yes24"
              style="
                border-radius: 50%;
                width: 50px;
                height: 50px;
                margin: 0 5% 0 0;
              "
              alt
            />
            <img
              class="cursor"
              uk-tooltip="알라딘 바로가기"
              src="@/assets/img/알라딘.jpg"
              @click="aladin"
              style="
                border-radius: 50%;
                width: 50px;
                height: 50px;
                margin: 0 5% 0 0;
              "
              alt
            />
          </div>
        </mdb-col>
        <mdb-col col="8" style="margin-left: 5px">
          <h1 class="do">{{ title }}</h1>
          <h5 v-if="author" class="do">{{ author }}</h5>
          <h5 v-else class="do">이 책은 작가 정보가 없습니다.</h5>
          <br />
          <h5 v-if="publisher" class="do" style="font-weight: 500">
            출판사 : {{ publisher }}
          </h5>
          <h5 v-else class="do" style="font-weight: 500">
            이 책은 출판사 정보가 없습니다.
          </h5>
          <br />
          <h6
            v-if="description"
            v-html="description"
            style="font-family: InfinitySans-RegularA1"
          ></h6>
          <h6 v-else style="font-family: InfinitySans-RegularA1">
            이 책은 줄거리 정보가 없습니다.
          </h6>
          <br />
          <v-btn icon @click="like" v-if="!isLiked" color="success">
            <i
              class="far fa-thumbs-up"
              uk-tooltip="책 좋아요"
              style="font-size: x-large"
            ></i>
            {{ like_count }}
          </v-btn>
          <v-btn icon @click="like" color="success" v-else>
            <i
              class="fas fa-thumbs-up"
              uk-tooltip="책 좋아요 취소"
              style="font-size: x-large"
            ></i>
            {{ like_count }}
          </v-btn>

          <v-btn
            icon
            @click="dislike"
            v-if="!isDisliked"
            style="padding-left: 2%"
            color="warning"
          >
            <i
              class="far fa-thumbs-down"
              uk-tooltip="책 싫어요"
              style="font-size: x-large"
            ></i>
            {{ unlike_count }}
          </v-btn>
          <v-btn
            icon
            @click="dislike"
            v-else
            style="padding-left: 2%"
            color="warning"
          >
            <i
              class="fas fa-thumbs-down"
              uk-tooltip="책 싫어요 취소"
              style="font-size: x-large"
            ></i>
            {{ unlike_count }}
          </v-btn>
          <span class="do" style="margin-left: 3%">내용 평점 : </span>
          <span v-if="content_score_average">
            <span v-for="num in content_score_average" :key="num.id">
              <i class="fas fa-star" style="color: yellow"></i>
            </span>
          </span>
          <span v-else>
            <span class="do">내용 평점이 없습니다.</span>
          </span>

          <span class="do" style="margin-left: 3%">디자인 평점 : </span>
          <span v-if="design_score_average">
            <span v-for="num2 in design_score_average" :key="num2.id">
              <i class="fas fa-star" style="color: yellow"></i>
            </span>
          </span>
          <span v-else>
            <span class="do">디자인 평점이 없습니다.</span>
          </span>
          <p v-show="score" class="mt-5 main-font">
            나의 취향 :
            <span class="main-font" style="color: green"
              >{{ score }}% 일치</span
            >
          </p>
        </mdb-col>
      </mdb-row>
      <br /><br />
      <mdb-row class="scrollme1" style="display: block">
        <mdb-row style="height: 40px">
          <h3 class="do">📚이 책을 읽은 사람들이 본 책</h3>
          <br />
          <br />
        </mdb-row>

        <mdb-row
          v-if="
            otherLikeBooks != '다른 사용자가 좋아요한 책이 존재하지 않습니다'
          "
        >
          <mdb-col col="12">
            <br /><br />
            <div class="rounded z-depth-2 mb-lg-0 mb-4" hover>
              <div
                class="uk-position-relative uk-visible-toggle uk-light"
                tabindex="-1"
                uk-slider
              >
                <ul
                  class="uk-slider-items uk-child-width-1-2 uk-child-width-1-3@s uk-child-width-1-4@m"
                >
                  <li
                    v-for="book of otherLikeBooks"
                    :item="book"
                    :key="book.id"
                  >
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
                      <mdb-mask flex-center waves overlay="black-strong">
                        <mdb-btn
                          v-if="book.title.length > 50"
                          outline="white"
                          @click="gotoDetail(book.id)"
                          style="
                            width: 220px;
                            height: 300px;
                            font-size: large;
                            font-family: HangeulNuri-Bold;
                          "
                          >{{ book.title.slice(0, 50) }} ... 자세히
                          보기</mdb-btn
                        >
                        <mdb-btn
                          v-else
                          outline="white"
                          @click="gotoDetail(book.id)"
                          style="
                            width: 220px;
                            height: 300px;
                            font-size: large;
                            font-family: HangeulNuri-Bold;
                          "
                          >{{ book.title }} - 자세히 보기</mdb-btn
                        >
                      </mdb-mask>
                    </mdb-view>

                    <div class="uk-position-center uk-panel"></div>
                  </li>
                </ul>

                <a
                  class="uk-position-center-left uk-position-small uk-hidden-hover"
                  style="color: black"
                  href="#"
                  uk-slidenav-previous
                  uk-slider-item="previous"
                ></a>
                <a
                  class="uk-position-center-right uk-position-small uk-hidden-hover"
                  style="color: black"
                  href="#"
                  uk-slidenav-next
                  uk-slider-item="next"
                ></a>
              </div>
            </div>
          </mdb-col>
        </mdb-row>
        <mdb-row v-else class="d-flex justify-content-center">
          <p class="do" style="font-size: large">
            다른 사용자가 좋아요한 책이 존재하지 않습니다.
          </p>
        </mdb-row>
      </mdb-row>
      <hr />
      <br /><br />
      <div id="seeChart" class="scrollme2">
        <BookChart :popular="popular" v-if="temp" />
      </div>
      <div id="seeLibrary" class="scrollme3">
        <v-row v-if="libraryList">
          <v-col cols="12">
            <div id="map" style="width: 100%"></div>
          </v-col>
          <v-col cols="4">
            <h6 class="font-weight-bold mb-3 do">📖대출 가능한 도서관📖</h6>
            <h3 class="font-weight-bold mb-3 p-0 do">
              <strong>내 주변 도서관</strong>
            </h3>
            <p class="do">개인정보에 입력하신 주소지를 기준으로</p>
            <p class="do">대출 가능한 도서관 목록을 보여드립니다.</p>
          </v-col>

          <v-col cols="8" style="padding: 0">
            <v-subheader inset class="ml-0"
              ><h4 class="do">🏬 도서대여가능 도서관</h4></v-subheader
            >
            <v-list subheader two-line style="overflow-y: auto; height: 250px">
              <v-list-item v-for="lib in libraryList" :key="lib.id">
                <v-list-item-content>
                  <v-list-item-title
                    v-text="lib['lib']['libName']"
                    style="font-size: large"
                    class="main-font"
                  ></v-list-item-title>

                  <v-list-item-subtitle
                    v-text="lib['lib']['address']"
                    class="main-font"
                  ></v-list-item-subtitle>

                  <v-list-item-subtitle class="main-font">{{
                    lib["lib"]["operatingTime"]
                  }}</v-list-item-subtitle>
                </v-list-item-content>

                <v-list-item-action>
                  <v-btn
                    icon
                    uk-tooltip="도서관 바로가기"
                    @click="goToLibrary(lib['lib']['homepage'])"
                  >
                    <v-icon color="#00BFA5">mdi-library</v-icon>
                  </v-btn>
                </v-list-item-action>
              </v-list-item>
            </v-list>
          </v-col>
        </v-row>
        <v-row v-else>
          <v-col>
            <h3 class="main-font text-center">
              대출 가능한 도서관이 없습니다.
            </h3>
          </v-col>
        </v-row>
      </div>
      <v-row> </v-row>

      <hr class="my-3" />

      <div id="seePhrase" class="scrollme4">
        <mdb-row>
          <mdb-col>
            <span style="font-size: xx-large" class="do">📌글귀</span>
            <PhraseForm @sendPhrase="getPhraseList" :booktitle2="title" />
          </mdb-col>
        </mdb-row>

        <div v-if="phraseList.length != 0">
          <v-carousel>
            <v-carousel-item
              v-for="(phrase, i) in phraseList"
              :key="i"
              :src="
                require('@/assets/img/phrase/phrase' +
                  String(phrase.id % 13) +
                  '.jpg')
              "
              reverse-transition="fade-transition"
              transition="fade-transition"
            >
              <div class="jb-text">
                <div class="jb-text-table">
                  <div class="jb-text-table-row">
                    <div class="jb-text-table-cell">
                      <p
                        class="do"
                        style="font-size: xx-large; color: black; opacity: 0.8"
                      >
                        {{ phrase.content }}
                      </p>
                      <p
                        class="do"
                        style="font-size: large; color: black; opacity: 0.8"
                      >
                        p. {{ phrase.page }}
                      </p>
                      <p
                        class="do"
                        style="font-size: large; color: black; opacity: 0.8"
                      >
                        by {{ phrase.username }}
                      </p>
                    </div>
                  </div>
                </div>
              </div>
            </v-carousel-item>
          </v-carousel>
        </div>

        <div v-else class="d-flex justify-content-center">
          <h3 class="do">등록된 문장이 없습니다.</h3>
        </div>
      </div>

      <hr class="my-3" />

      <mdb-row id="seeReview" class="scrollme5">
        <mdb-col>
          <span style="font-size: xx-large" class="do">📝리뷰</span>
          <ReviewForm
            @sendReview="getReviewList"
            :book="book"
            :btnTitle="btnTitle"
            :isWritten="isWritten"
          />
          <br /><br />
          <mdb-row v-if="reviewData.length">
            <mdb-col
              col="6"
              lg="6"
              sm="12"
              v-for="review in reviewData"
              :item="review"
              :key="review.id"
            >
              <mdb-card hover waves overlay="white-slight" style="width: 400px">
                <mdb-card-body>
                  <div class="label" @click="goToActivity(review.user.id)">
                    <!-- <img
                      src="https://cdn.vuetifyjs.com/images/john.jpg"
                      class="rounded-circle z-depth-1-half"
                      style="width: 60px; height: 60px; margin-right: 2%"
                    /> -->
                    <v-img
                      :src="`${review.profile_url}`"
                      class="rounded-circle z-depth-1-half"
                      style="border-color: black"
                      width="15%"
                      height="15%"
                    >
                    </v-img
                    ><br />
                    <span class="do" style="font-size: large"
                      >&nbsp;작성자 : {{ review.user.name }}
                    </span>
                  </div>
                  <br />
                  <mdb-card-title
                    v-if="review.review.title.length > 15"
                    class="name do"
                    style="color: black; font-size: x-large"
                    >{{ review.review.title.slice(0, 15) }}...</mdb-card-title
                  >
                  <mdb-card-title
                    v-else
                    class="name do"
                    style="color: black; font-size: x-large"
                    >{{ review.review.title }}</mdb-card-title
                  >
                  <hr />
                  <mdb-card-text>
                    <p
                      v-if="review.review.content.length > 25"
                      class="do"
                      style="font-size: medium"
                    >
                      내용 : {{ review.review.content.slice(0, 25) }}...
                    </p>
                    <p v-else class="do" style="font-size: medium">
                      내용 : {{ review.review.content }}
                    </p>

                    <p class="do">
                      내용 평점 :
                      <span
                        v-for="num in review.review.content_score"
                        :key="num.id"
                      >
                        <i class="fas fa-star" style="color: yellow"></i>
                      </span>
                    </p>

                    <p class="do">
                      디자인 평점 :
                      <span
                        v-for="num in review.review.design_score"
                        :key="num.id"
                      >
                        <i class="fas fa-star" style="color: yellow"></i>
                      </span>
                    </p>
                    <p class="date do" style="color: grey">
                      작성일 : {{ review.review.created_at.slice(0, 10) }}
                    </p>
                  </mdb-card-text>
                  <div class="text-right">
                    <mdb-btn
                      class="do"
                      style="
                        background-color: #00bfa5;
                        color: white;
                        font-size: medium;
                        padding: 3% 2% 3% 2%;
                        border-radius: 7%;
                      "
                      @click="goToReview(review.review.id)"
                      >자세히보기</mdb-btn
                    >
                  </div>
                </mdb-card-body> </mdb-card
              ><br />
            </mdb-col>
          </mdb-row>

          <mdb-row v-else class="d-flex justify-content-center">
            <h3 class="do">등록된 리뷰가 없습니다.</h3>
          </mdb-row>
        </mdb-col>
      </mdb-row>
    </mdb-container>
    <!-- 리모콘 -->
    <v-speed-dial
      v-model="fab"
      direction="top"
      transition="slide-y-reverse-transition"
      class="temp_spy"
    >
      <template v-slot:activator>
        <v-btn v-model="fab" dark fab color="blue-grey">
          <v-icon v-if="fab">mdi-close</v-icon>
          <v-icon v-else>mdi-view-grid</v-icon>
        </v-btn>
      </template>
      <v-btn
      
        v-scroll="onScroll"
        text
        class="do"
        style="font-size: large; background-color: #F5F5F5"
        @click="toTop"
      >
        <h5>⬆</h5>
        위로
      </v-btn>
      <v-btn
        text
        :class="{ active: isActive4 }"
        @click="goToSomewhere('seeReview')"
        class="do"
        style="font-size: large; background-color: #F5F5F5"
        >📝리뷰</v-btn
      >
      <v-btn
        text
        :class="{ active: isActive3 }"
        @click="goToSomewhere('seePhrase')"
        class="do"
        style="font-size: large; background-color: #F5F5F5"
        >📌글귀</v-btn
      >
      <v-btn
        text
        :class="{ active: isActive2 }"
        @click="goToSomewhere('seeLibrary')"
        class="do"
        style="font-size: large; background-color: #F5F5F5"
        >🏬도서관</v-btn
      >
      <v-btn
        text
        :class="{ active: isActive1 }"
        @click="goToSomewhere('seeChart')"
        class="do"
        style="font-size: large; background-color: #F5F5F5"
        >📊차트</v-btn
      >
    </v-speed-dial>
  </div>
</template>

<script>
import VueCookies from "vue-cookies";
import swal from "sweetalert";
import _ from "lodash";
import ReviewForm from "@/views/form/ReviewForm";
import PhraseForm from "@/views/form/PhraseForm";
import BookChart from "@/views/detail/BookChart";
// import Map from "./Map.vue";

import {
  mdbContainer,
  mdbRow,
  mdbCol,
  mdbCard,
  mdbCardBody,
  mdbCardTitle,
  mdbCardText,
  mdbBtn,
  mdbMask,
  mdbView,
} from "mdbvue";

import axios from "axios";

export default {
  name: "BookDetail",
  components: {
    mdbContainer,
    mdbRow,
    mdbCol,
    ReviewForm,
    PhraseForm,
    BookChart,
    mdbCard,
    mdbCardBody,
    mdbCardTitle,
    mdbCardText,
    mdbBtn,
    mdbMask,
    mdbView,
    // Map,
  },
  destroyed() {
    window.removeEventListener("scroll", this.handleScroll);
  },

  created() {
    this.toTop();
    this.imgNum = _.random(0, 13);

    window.addEventListener("scroll", this.handleScroll);

    if (VueCookies.get("user_gender") == 2) {
      swal("잘못된 접근입니다.", "회원가입이 완료되지 않았습니다.");
      this.$router.push("/signup");
    }

    // 도서 정보 가져오기
    axios
      .get(
        `${process.env.VUE_APP_SERVER_URL}/books/book_detail/${this.$route.params.pk}/`,
        {
          params: { user_pk: VueCookies.get("user_pk") },
        }
      )
      .then((res) => {
        this.tempData = res.data;
        this.author = res.data.author;
        this.description = res.data.description;
        this.book_pk = res.data.id;
        this.image = res.data.img_url;
        this.isbn = res.data.isbn;
        this.like_users = res.data.like_users;
        this.price = res.data.price;
        this.pub_date = res.data.pub_date;
        this.publisher = res.data.publisher;
        this.title = res.data.title;
        this.book = { book_pk: this.book_pk, book_title: this.title };
        this.isLiked = res.data.like;
        this.isDisliked = res.data.unlike;
        this.like_count = res.data.like_count;
        this.unlike_count = res.data.unlike_count;
        this.score = res.data.score;
        if (this.score) {
          this.score = parseInt(this.score * 100);
        }
        if (res.data.popular !== undefined) {
          this.popular = res.data.popular;
        }
        if (res.data.error !== undefined) {
          this.error = res.data.error;
        }
        // this.error = res.data.error
        // this.popular = res.data.popular
      })

    // 리뷰 가져오기
    axios
      .get(`${process.env.VUE_APP_SERVER_URL}/reviews/review/`, {
        params: { book_pk: String(this.$route.params.pk) },
        headers: { Authorization: VueCookies.get("jwt_token") },
      })
      .then((res) => {
        if (res.data.status == "리뷰가 있어") {
          this.isWritten = true;
        } else {
          this.isWritten = false;
        }
        this.reviews = res.data.result;
        this.reviewData = res.data.result.slice(0, 4);

        this.content_score_average = res.data.score[0].content_score_average;
        this.design_score_average = res.data.score[0].design_score_average;
      })


    // 글귀 가져오기
    axios
      .get(`${process.env.VUE_APP_SERVER_URL}/reviews/phrase/`, {
        params: {
          book_pk: this.$route.params.pk,
        },
        headers: { Authorization: VueCookies.get("jwt_token") },
      })
      .then((res) => {
        this.phraseList = res.data.result;
      })

    // 타인이 좋아하는 책
    axios
      .get(`${process.env.VUE_APP_SERVER_URL}/books/other_like_book/`, {
        params: {
          book_pk: this.$route.params.pk,
          user_pk: VueCookies.get("user_pk"),
        },
      })
      .then((res) => {
        this.otherLikeBooks = res.data.result;
      })

    setTimeout(() => {
      this.temp = true;
    }, 1000);
  },
  mounted() {
    // // 도서관 위치 정보 가져오기
    axios
      .get(`${process.env.VUE_APP_SERVER_URL}/books/library/`, {
        params: {
          book_pk: this.$route.params.pk,
          user_pk: VueCookies.get("user_pk"),
        },
      })
      .then((res) => {
        this.libraryList = res.data.result["libs"];
        this.myLocation = res.data.result["user"];

        if (window.kakao && window.kakao.maps) {
          this.initMap();
        } else {
          const script = document.createElement("script");
          /* global kakao */
          script.onload = () => kakao.maps.load();
          script.src =
            "http://dapi.kakao.com/v2/maps/sdk.js?autoload=false&appkey=74f2063cad707b3796dacfe976496318";
          document.head.appendChild(script);
        }
      })
      // .catch((err) => {
      //   console.log(err);
      // });
    // 무한 스크롤
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
      score: null,
      isWritten: false,
      imgNum: 1,
      nextItem: 4,
      isDetect: true,
      isLoading: false,

      myLocation: null,
      libraries: [], // 추가로 불러올 라이브러리
      map: null, // 지도 객체. 지도가 로드되면 할당됨.
      isLiked: false,
      isDisliked: false,
      // 스크롤
      fab: false,
      temp: false,
      feedback: null,

      tempData: {},
      author: null,
      description: null,
      image: null,
      isbn: null,
      like_users: null,
      price: null,
      pub_date: null,
      publisher: null,
      title: null,
      error: null,
      popular: null,
      basicRating: "",
      book_pk: null,
      book: {},

      reviews: [],
      reviewData: [],

      phraseList: [],
      libraryList: [],
      otherLikeBooks: null,
      content_score_average: 0,
      design_score_average: 0,
      like_count: 0,
      unlike_count: 0,

      btnTitle: "리뷰 작성",

      isActive1: false,
      isActive2: false,
      isActive3: false,
      isActive4: false,
      isActive5: false,
    };
  },
  methods: {
    gotoDetail(id) {
      this.$router.push(`/bookdetail/${id}`);
    },
    loadMore() {
      this.isLoading = true;
      if (this.reviews.length - this.nextItem > 3) {
        for (let i = 0; i < 4; i++) {
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

    goToSomewhere(item) {
      window.scrollTo(0, document.getElementById(item).offsetTop);
    },
    handleScroll() {
      const els = document.querySelectorAll(".scrollme1");

      els.forEach((el) => {
        const elTop = el.getBoundingClientRect().top;
        const elBottom = el.getBoundingClientRect().bottom;
        if (elTop >= 0 || elBottom <= 0) {
          this.isActive1 = false;
        }
        if (elTop <= 0 && elBottom >= 0) {
          this.isActive1 = true;
        }
      });
      const els2 = document.querySelectorAll(".scrollme2");
      els2.forEach((el2) => {
        const elTop2 = el2.getBoundingClientRect().top;
        const elBottom2 = el2.getBoundingClientRect().bottom;
        if (elTop2 >= 0 || elBottom2 <= 0) {
          this.isActive2 = false;
        }
        if (elTop2 <= 0 && elBottom2 >= 0) {
          this.isActive2 = true;
        }
      });
      const els3 = document.querySelectorAll(".scrollme3");
      els3.forEach((el3) => {
        const elTop3 = el3.getBoundingClientRect().top;
        const elBottom3 = el3.getBoundingClientRect().bottom;
        if (elTop3 >= 0 || elBottom3 <= 0) {
          this.isActive3 = false;
        }
        if (elTop3 <= 0 && elBottom3 >= 0) {
          this.isActive3 = true;
        }
      });
      const els4 = document.querySelectorAll(".scrollme4");
      els4.forEach((el4) => {
        const elTop4 = el4.getBoundingClientRect().top;
        const elBottom4 = el4.getBoundingClientRect().bottom;
        if (elTop4 >= 0 || elBottom4 <= 0) {
          this.isActive4 = false;
        }
        if (elTop4 <= 0 && elBottom4 >= 0) {
          this.isActive4 = true;
        }
      });
      const els5 = document.querySelectorAll(".scrollme5");
      els5.forEach((el5) => {
        const elTop5 = el5.getBoundingClientRect().top;
        const elBottom5 = el5.getBoundingClientRect().bottom;
        if (elTop5 >= 0 || elBottom5 <= 0) {
          this.isActive5 = false;
        }
        if (elTop5 <= 0 && elBottom5 >= 0) {
          this.isActive5 = true;
        }
      });
    },

    goToLibrary(link) {
      window.open(link);
    },

    goToActivity(id) {
      this.$router.push(`/activity/${id}`);
    },

    goToReview(id) {
      this.$router.push(`/reviewdetail/${id}`);
    },

    makeOverListener(map, marker, infowindow) {
      return function () {
        infowindow.open(map, marker);
      };
    },

    // 인포윈도우를 닫는 클로저를 만드는 함수입니다
    makeOutListener(infowindow) {
      return function () {
        infowindow.close();
      };
    },
    initMap() {
      var imageSrc =
        "https://t1.daumcdn.net/localimg/localimages/07/mapapidoc/markerStar.png";

      var imageSize = new kakao.maps.Size(24, 35);

      // 마커 이미지를 생성합니다
      var markerImage = new kakao.maps.MarkerImage(imageSrc, imageSize);

      var mapContainer = document.getElementById("map"), // 지도를 표시할 div
        mapOption = {
          center: new kakao.maps.LatLng(
            this.myLocation["longitude"],
            this.myLocation["latitude"]
          ), // 지도의 중심좌표
          level: 8, // 지도의 확대 레벨
        };

      var map = new kakao.maps.Map(mapContainer, mapOption); // 지도를 생성합니다
      // 마커를 표시할 위치와 내용을 가지고 있는 객체 배열입니다
      var positions = [];
      // 마커를 생성합니다

      var myMap_obj = new Object();
      myMap_obj.content = `<div>나의 위치</div>`;
      myMap_obj.latlng = new kakao.maps.LatLng(
        this.myLocation["longitude"],
        this.myLocation["latitude"]
      );
      myMap_obj.image = markerImage;
      positions.push(myMap_obj);

      if (this.libraryList.length <= 10) {
        for (let j = 0; j < this.libraryList.length; j++) {
          var map_obj = new Object();
          map_obj.content = `<div>${this.libraryList[j]["lib"]["libName"]}</div>`;
          map_obj.latlng = new kakao.maps.LatLng(
            this.libraryList[j]["lib"]["latitude"],
            this.libraryList[j]["lib"]["longitude"]
          );
          positions.push(map_obj);
        }

        for (var i = 0; i < positions.length; i++) {
          if (i == 0) {
            var marker = new kakao.maps.Marker({
              map: map,
              position: positions[i].latlng,
              image: positions[i].image,
            });

            // 마커에 표시할 인포윈도우를 생성합니다
            var infowindow = new kakao.maps.InfoWindow({
              content: positions[i].content,
            });
          } else {
            // 마커를 생성합니다
            marker = new kakao.maps.Marker({
              map: map, // 마커를 표시할 지도
              position: positions[i].latlng, // 마커의 위치
            });

            // 마커에 표시할 인포윈도우를 생성합니다
            infowindow = new kakao.maps.InfoWindow({
              content: positions[i].content, // 인포윈도우에 표시할 내용
            });
          }
          // 마커에 mouseover 이벤트와 mouseout 이벤트를 등록합니다
          // 이벤트 리스너로는 클로저를 만들어 등록합니다
          // for문에서 클로저를 만들어 주지 않으면 마지막 마커에만 이벤트가 등록됩니다
          kakao.maps.event.addListener(
            marker,
            "mouseover",
            this.makeOverListener(map, marker, infowindow)
          );
          kakao.maps.event.addListener(
            marker,
            "mouseout",
            this.makeOutListener(infowindow)
          );
        }
      } else {
        this.libraryList = [];
      }
    },

    displayMarker(markerPositions) {
      if (this.markers.length > 0) {
        this.markers.forEach((marker) => marker.setMap(null));
      }

      const positions = markerPositions.map(
        (position) => new kakao.maps.LatLng(...position)
      );

      if (positions.length > 0) {
        this.markers = positions.map(
          (position) =>
            new kakao.maps.Marker({
              map: this.map,
              position,
            })
        );

        const bounds = positions.reduce(
          (bounds, latlng) => bounds.extend(latlng),
          new kakao.maps.LatLngBounds()
        );

        this.map.setBounds(bounds);
      }
    },

    like() {
      axios
        .get(`${process.env.VUE_APP_SERVER_URL}/accounts/like/`, {
          params: {
            user_pk: VueCookies.get("user_pk"),
            book_pk: this.$route.params.pk,
          },
        })
        .then((res) => {
          // sessionStorage.clear();
          this.isLiked = res.data.like;
          if (res.data.like) {
            this.like_count = this.like_count + 1;
          } else {
            this.like_count = this.like_count - 1;
          }
          this.isDisliked = res.data.unlike;
          if (res.data.unlike === false) {
            this.unlike_count = this.unlike_count - 1;
          }
        })
    },
    dislike() {
      axios
        .get(`${process.env.VUE_APP_SERVER_URL}/accounts/unlike/`, {
          params: {
            user_pk: VueCookies.get("user_pk"),
            book_pk: this.$route.params.pk,
          },
        })
        .then((res) => {
          // sessionStorage.clear();
          this.isLiked = res.data.like;
          if (res.data.like === false) {
            this.like_count = this.like_count - 1;
          }
          this.isDisliked = res.data.unlike;
          if (res.data.unlike) {
            this.unlike_count = this.unlike_count + 1;
          } else {
            this.unlike_count = this.unlike_count - 1;
          }
        })
    },
    beforeEnter(el) {
      this.elHeight = el.scrollHeight;
    },
    enter(el) {
      el.style.height = this.elHeight + "px";
    },
    beforeLeave(el) {
      el.style.height = 0;
    },
    getReviewList() {
      axios
        .get(`${process.env.VUE_APP_SERVER_URL}/reviews/review/`, {
          params: { book_pk: String(this.$route.params.pk) },
          headers: { Authorization: VueCookies.get("jwt_token") },
        })
        .then((res) => {
          this.reviews = res.data.result;
          this.reviewData = this.reviews.slice(0, 5);
          this.isWritten = true;
        })

    },
    getPhraseList() {
      axios
        .get(`${process.env.VUE_APP_SERVER_URL}/reviews/phrase/`, {
          params: {
            book_pk: this.$route.params.pk,
          },
          headers: { Authorization: VueCookies.get("jwt_token") },
        })
        .then((res) => {
          this.phraseList = res.data.result;
        })

    },
    kyobo() {
      window.open(
        `https://search.kyobobook.co.kr/web/search?vPstrKeyWord=${this.isbn}`
      );
    },
    yes24() {
      window.open(
        `http://www.yes24.com/SearchCorner/Search?domain=BOOK&query=${this.isbn}`
      );
    },
    aladin() {
      //window.open(`https://www.aladin.co.kr/weeklyeditorialmeeting/detail.aspx?&isbn=${this.isbn}`);
      window.open(
        `https://www.aladin.co.kr/shop/wproduct.aspx?isbn=${this.isbn}`
      );
      //window.open(`https://www.aladin.co.kr/search/wsearchresult.aspx?SearchTarget=Book&SearchWord=${this.title}`);
    },

    toTop() {
      this.$vuetify.goTo(0);
    },

    // 스크롤(Top)
    onScroll(e) {
      if (typeof window === "undefined") return;
      const top = window.pageYOffset || e.target.scrollTop || 0;
      this.fab = top > 20;
    },
  },
};
</script>

<style scoped>
.cursor {
  cursor: pointer;
}
.main-font {
  font-family: "HangeulNuri-Bold";
}

#map {
  width: 400px;
  height: 400px;
  text-align: center;
}

.button-group {
  margin: 10px 0px;
}

button {
  margin: 0 3px;
}

.text-black {
  color: black;
}
.phrase-img {
  opacity: 0.5;
  width: 850px;
  height: 300px;
  margin-right: 2%;
}
.yellow-text-dark-2 {
  color: #d7c952 !important;
}
.yellow-text-dark-3 {
  color: #9b9247 !important;
}
.yellow-text-dark-4 {
  color: #827c47 !important;
}
.yellow-text-dark-1 {
  color: #e9d947 !important;
}
.collapse-item {
  overflow: hidden;
  height: 0;
  padding: 0;
  transition: height 0.5s;
}
.do {
  font-family: "Do Hyeon", sans-serif;
}
.jua {
  font-family: "Jua", sans-serif;
}
.poor {
  font-family: "Poor Story", cursive;
}
.nanum {
  font-family: "Nanum Pen Script", cursive;
}
.lucky {
  font-family: "Luckiest Guy", cursive;
}
.godic {
  font-family: "Nanum Gothic", sans-serif;
}
@font-face {
  font-family: "InfinitySans-RegularA1";
  src: url("https://cdn.jsdelivr.net/gh/projectnoonnu/noonfonts_20-04@2.1/InfinitySans-RegularA1.woff")
    format("woff");
  font-weight: normal;
  font-style: normal;
}
@font-face {
  font-family: "MaplestoryOTFBold";
  src: url("https://cdn.jsdelivr.net/gh/projectnoonnu/noonfonts_20-04@2.1/MaplestoryOTFBold.woff")
    format("woff");
  font-weight: 100;
  font-style: normal;
}
@font-face {
  font-family: "BMEULJIRO";
  src: url("https://cdn.jsdelivr.net/gh/projectnoonnu/noonfonts_twelve@1.0/BMEULJIRO.woff")
    format("woff");
  font-weight: lighterl;
  font-style: normal;
}
@font-face {
  font-family: "TmonMonsori";
  src: url("https://cdn.jsdelivr.net/gh/projectnoonnu/noonfonts_two@1.0/TmonMonsori.woff")
    format("woff");
  font-weight: lighter;
  font-style: normal;
}

.temp_spy {
  display: flex;
  flex-direction: column;
  position: fixed;
  right: 2%;
  bottom: 5%;
  font-size: 1em;
}
.active {
  font-size: 2em;
}
.bookimage {
  width: 200px;
  height: 300px;
  display: block;
  margin: 0px auto;
}
li.uk-active {
  width: 220px;
}
.rounded {
  margin-left: auto;
  margin-right: auto;
  width: 100%;
}

.uk-position-relative.uk-visible-toggle.uk-light.uk-slider.uk-slider-container {
  width: 100%;
}

.jb-wrap {
  width: 40%;
  margin: 0px auto;
  position: relative;
}
.jb-wrap img {
  width: 100%;
  vertical-align: middle;
}
.jb-text {
  position: absolute;
  top: 0px;
  width: 100%;
  height: 100%;
}
.jb-text-table {
  display: table;
  width: 100%;
  height: 100%;
}
.jb-text-table-row {
  display: table-row;
}
.jb-text-table-cell {
  display: table-cell;
  vertical-align: middle;
}
.jb-text p {
  margin: 0px 40px;
  padding: 10px;
  background-color: #ffffff;
  text-align: center;
}
</style>
