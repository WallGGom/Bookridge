<template>
  <div id="main" class="mx-auto" style="max-width: 80%; min-width: 65%">
    <v-container>
      <v-row class="d-flex justify-content-center">
        <v-list three-line subheader>
          <v-subheader
            v-if="!updateReviewNow"
            style="font-size: xx-large; color: black"
            class="do"
          >
            "{{ reviewData.title }}"</v-subheader
          >
          <v-text-field
            v-model="reviewTitle"
            counter="20"
            label="리뷰 제목을 입력하세요."
            style="font-family: HangeulNuri-Bold; font-size: x-large"
            outlined
            v-if="updateReviewNow"
          ></v-text-field>
          <hr />
          <v-list-item>
            <v-list-item-content>
              <br /><br />
              <v-row>
                <v-col cols="4">
                  <img
                    :src="image"
                    style="width: 200px; height: 270px"
                    alt=""
                    uk-tooltip="책 바로가기"
                    @click="gotoDetail(reviewData.book)"
                    class="cursor"
                  />
                </v-col>
                <v-col cols="8">
                  <v-row>
                    <v-col cols="2">
                      <div uk-tooltip="프로필 바로가기">
                        <v-img
                          @click="goToActivity(reviewData.user)"
                          :src="reviewData.profile_url"
                          class="rounded-circle cursor"
                          style="width: 70px; height: auto"
                        ></v-img>
                      </div>
                    </v-col>
                    <v-col cols="5">
                      <h5 style="font-family: HangeulNuri-Bold">
                        {{ reviewData.review_user_name }}
                      </h5>
                    </v-col>
                  </v-row>

                  <p style="font-family: HangeulNuri-Bold; color: gray">
                    {{ createdAt.slice(0, 10) }}
                    {{ createdAt.slice(11, 16) }} | 조회수 :
                    {{ reviewData.hitcount }} |
                    <v-btn
                      icon
                      @click="reviewLike(reviewData)"
                      v-if="!reviewData.review_like_state"
                    >
                      <v-icon color="red" uk-tooltip="리뷰 좋아요"
                        >mdi-heart-outline</v-icon
                      >
                    </v-btn>
                    <v-btn icon @click="reviewLike(reviewData)" v-else>
                      <v-icon
                        color="red"
                        icon="heart-broken"
                        uk-tooltip="좋아요 취소"
                      >
                        mdi-heart
                      </v-icon>
                    </v-btn>
                    {{ reviewData.review_like_count }}개
                  </p>
                  <br /><br />

                  <v-list-item-title
                    style="font-family: HangeulNuri-Bold; font-size: large"
                    v-show="!updateReviewNow"
                    >내용</v-list-item-title
                  ><br />
                  <v-list-item-content
                    style="font-family: HangeulNuri-Bold"
                    v-show="!updateReviewNow"
                    >{{ reviewData.content }}</v-list-item-content
                  >
                  <v-textarea
                    outlined
                    name="input-7-4"
                    label="내용"
                    style="font-family: HangeulNuri-Bold; font-size: large"
                    v-show="updateReviewNow"
                    v-model="reviewContent"
                  ></v-textarea>

                  <br /><br /><br />
                  <v-list-item-title
                    style="font-family: HangeulNuri-Bold; font-size: large"
                    >평점</v-list-item-title
                  ><br />
                  <p
                    style="font-family: HangeulNuri-Bold"
                    v-show="!updateReviewNow"
                  >
                    내용 평점 :
                    <span v-for="num in reviewData.content_score" :key="num.id">
                      <i class="fas fa-star" style="color: yellow"></i>
                    </span>
                  </p>
                  <p
                    style="font-family: HangeulNuri-Bold"
                    v-show="!updateReviewNow"
                  >
                    디자인 평점 :
                    <span v-for="num in reviewData.design_score" :key="num.id">
                      <i class="fas fa-star" style="color: yellow"></i>
                    </span>
                  </p>
                  <v-row v-show="updateReviewNow">
                    <v-col col="4">
                      <span style="font-family: HangeulNuri-Bold"
                        >내용 평점 :
                      </span></v-col
                    >
                    <v-col col="5">
                      <v-rating
                        v-model="reviewData.content_score"
                        background-color="grey lighten-1"
                        color="yellow accent-4"
                        dense
                        hover
                        size="23"
                      ></v-rating>
                    </v-col>
                  </v-row>

                  <v-row v-show="updateReviewNow">
                    <v-col col="4">
                      <span style="font-family: HangeulNuri-Bold"
                        >디자인 평점 :
                      </span></v-col
                    >
                    <v-col col="8">
                      <v-rating
                        v-model="reviewData.design_score"
                        background-color="grey lighten-1"
                        color="yellow accent-4"
                        dense
                        hover
                        size="23"
                      ></v-rating>
                    </v-col>
                  </v-row>
                </v-col>
              </v-row>
            </v-list-item-content>
          </v-list-item>
          <div style="text-align: right; margin-right: 5%" v-show="isYou">
            <v-btn
              class="mx-2 jua"
              dark
              medium
              color="cyan"
              @click="updateReviewNow = true"
              v-show="!updateReviewNow && isYou"
            >
              수정
            </v-btn>

            <v-btn
              class="mx-2 jua"
              dark
              medium
              color="cyan"
              v-show="updateReviewNow"
              @click="completeReviewModify"
            >
              제출
            </v-btn>

            <v-btn
              class="mx-2 jua"
              dark
              medium
              color="red"
              v-show="updateReviewNow"
              @click="cancelReview"
            >
              취소
            </v-btn>

            <v-btn
              v-show="!updateReviewNow && isYou"
              class="mx-2 jua"
              dark
              medium
              color="green"
              @click="gotoReviewDelete(reviewData.id)"
            >
              삭제
            </v-btn>
          </div>
        </v-list>
      </v-row>
      <br /><br />
      <v-row>
        <v-col cols="2" class="text-center">
          <v-avatar color="indigo">
            <v-icon dark>mdi-account-circle</v-icon>
          </v-avatar>
        </v-col>
        <v-col cols="8" class="p-0">
          <v-textarea
            v-model="comment"
            label="댓글을 입력해주세요."
            style="font-family: HangeulNuri-Bold"
            maxlength="45"
            counter="45"
            auto-grow
            outlined
            rows="1"
            row-height="30"
            @keypress.enter="createComment"
          ></v-textarea>
        </v-col>
        <v-col cols="2">
          <mdb-btn
            color="secondary"
            :disabled="comment == '' || comment.length > 45"
            style="
              font-family: HangeulNuri-Bold;
              color: white;
              font-size: small;
              border-radius: 10%;
            "
            @click="createComment"
            >등록</mdb-btn
          >
        </v-col>
      </v-row>
      <v-row
        v-if="comments == '해당 review 의 comments 가 없습니다'"
        class="d-flex justify-content-center"
      >
        <h4 class="main-font my-5">리뷰에 등록된 댓글이 없습니다.</h4>
      </v-row>
      <v-row v-else v-for="com in commentData" :key="com.id">
        <v-col cols="2" class="text-center">
          <div
            @click="goToActivity(com.user)"
            uk-tooltip="프로필 바로가기"
            class="cursor"
          >
            <v-img
              :src="com.profile_url"
              class="rounded-circle mx-auto"
              width="25%"
              height="25%"
            ></v-img>
          </div>
          <p style="font-family: HangeulNuri-Bold">{{ com.user_name }}</p>
        </v-col>

        <v-col cols="8" class="p-0">
          <v-textarea
            @keypress.enter="updateComment(com)"
            v-show="user_pk == com.user && com.edit"
            v-model="com.content"
            label="댓글을 입력해주세요."
            style="font-family: HangeulNuri-Bold"
            maxlength="45"
            counter="45"
            auto-grow
            outlined
            rows="1"
            row-height="15"
          ></v-textarea>
          <div
            v-show="!com.edit"
            class="pa-6 lighten-2 rounded-xl"
            style="font-family: HangeulNuri-Bold; background-color: whitesmoke"
          >
            {{ com.content }}
          </div>
          <v-row>
            <v-col class="p-0">
              <v-row class="d-flex justify-content-end pr-3">
                <p
                  style="font-family: HangeulNuri-Bold"
                  class="d-flex justify-content-end pr-3 pt-3"
                >
                  {{ com.created_at.slice(0, 10) }}
                  {{ com.created_at.slice(11, 16) }}
                </p></v-row
              >
              <v-row class="d-flex justify-content-end pr-3 pb-3">
                <v-btn
                  class="mx-2 jua"
                  dark
                  medium
                  color="cyan"
                  @click="beforeUpdateComment(com)"
                  v-show="user_pk == com.user && !com.edit"
                >
                  수정
                </v-btn>
                <v-btn
                  class="mx-2 jua"
                  dark
                  medium
                  color="green"
                  @click="deleteComment(com.id)"
                  v-show="user_pk == com.user && !com.edit"
                >
                  삭제
                </v-btn>
                <v-btn
                  class="mx-2 jua"
                  dark
                  medium
                  color="green"
                  :disabled="com.content == '' || com.content.length > 45"
                  @click="updateComment(com)"
                  v-show="user_pk == com.user && com.edit"
                >
                  제출
                </v-btn>
                <v-btn
                  class="mx-2 jua"
                  dark
                  medium
                  color="red"
                  @click="cancelComment(com)"
                  v-show="isYou && com.edit"
                >
                  취소
                </v-btn>
              </v-row>
            </v-col>
          </v-row>
        </v-col>
      </v-row>
    </v-container>
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
import swal from "sweetalert";
// import { VueFeedbackReaction, VueReactionEmoji } from "vue-feedback-reaction";
import { mdbBtn } from "mdbvue";

export default {
  name: "ReviewDetail",
  components: {
    // VueReactionEmoji,
    // VueFeedbackReaction,
    mdbBtn,
  },
  data() {
    return {
      nowLength: 0,
      // 스크롤
      fab: false,
      isDetect: true,
      isLoading: false,

      tempComment: "",
      user_pk: null,
      createdAt: "",
      comment: "",
      comments: [],

      nextItem: 5,
      commentData: [],

      reviewData: {},
      image: null,
      updateReviewNow: false,
      updateCommentNow: false,
      isYou: false,
      reaction1: "natural",
      reaction2: "natural",
      isActive1: true,
      isActive2: true,
      reviewTitle: null,
      reviewContent: null,
      reviewContentScore: null,
      reviewDesignScore: null,
    };
  },
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

  created() {
    this.$vuetify.goTo(0);
    // 리뷰 디테일 불러오기
    this.user_pk = VueCookies.get("user_pk");
    axios
      .get(`${process.env.VUE_APP_SERVER_URL}/reviews/review_detail/`, {
        params: {
          review_pk: this.$route.params.pk,
          user_pk: VueCookies.get("user_pk"),
        },
      })
      .then((res) => {
        // console.log("가져온 리뷰");
        // console.log(res);
        this.reviewData = res.data.result;
        if (this.reviewData.review_user_pk == VueCookies.get("user_pk")) {
          this.isYou = true;
        }
        this.createdAt = this.reviewData.created_at;
        this.reviewTitle = this.reviewData.title;
        this.reviewContent = this.reviewData.content;
        this.reviewContentScore = this.reviewData.content_score;
        this.reviewDesignScore = this.reviewData.design_score;
        this.image = this.reviewData.book_img_url;

        if (this.reviewData.content_score == 1) {
          this.reaction1 = "hate";
        } else if (this.reviewData.content_score == 2) {
          this.reaction1 = "disappointed";
        } else if (this.reviewData.content_score == 3) {
          this.reaction1 = "natural";
        } else if (this.reviewData.content_score == 4) {
          this.reaction1 = "good";
        } else {
          this.reaction1 = "excellent";
        }

        if (this.reviewData.design_score == 1) {
          this.reaction2 = "hate";
        } else if (this.reviewData.design_score == 2) {
          this.reaction2 = "disappointed";
        } else if (this.reviewData.design_score == 3) {
          this.reaction2 = "natural";
        } else if (this.reviewData.design_score == 4) {
          this.reaction2 = "good";
        } else {
          this.reaction2 = "excellent";
        }
      });
    // 댓글 가져오기
    axios
      .get(`${process.env.VUE_APP_SERVER_URL}/reviews/comment/`, {
        headers: {
          Authorization: VueCookies.get("jwt_token"),
        },
        params: {
          review_pk: this.$route.params.pk,
        },
      })
      .then((res) => {
        // console.log("댓글 가져오기");
        // console.log(res);
        if (res.data.result.length) {
          this.comments = res.data.result.reverse();
          this.commentData = this.comments.slice(0, 5);
        } else {
          this.comments = "해당 review 의 comments 가 없습니다";
        }
      });
    // .catch((err) => {
    //   console.log(err);
    // });
  },
  watch: {
    commentData() {
      // console.log(this.commentData.length);
      this.nowLength = this.commentData.length;
    },
    comment() {
      if (this.comment.length > 45) {
        swal("댓글은 45자 이내로 입력해주세요.");
      }
    },
  },
  methods: {
    // 최상단으로 이동하기
    toTop() {
      this.$vuetify.goTo(0);
    },
    // 스크롤(Top)
    onScroll(e) {
      if (typeof window === "undefined") return;
      const top = window.pageYOffset || e.target.scrollTop || 0;
      this.fab = top > 20;
    },
    loadMore() {
      this.isLoading = true;
      if (this.comments.length - this.nextItem > 5) {
        for (let i = 0; i < 5; i++) {
          let nextComment = this.comments[this.nextItem++];
          this.commentData.push(nextComment);
        }
      } else if (this.comments.length - this.nextItem == 0) {
        this.isLoading = false;
      } else {
        for (let i = 0; i <= this.comments.length - this.nextItem; i++) {
          let nextComment = this.comments[this.nextItem++];
          this.commentData.push(nextComment);
        }
      }
      // console.log(this.reviewData)
      this.isLoading = false;
    },

    // 프로필 이동
    goToActivity(id) {
      this.$router.push(`/activity/${id}`);
    },
    // 책 detail로 이동
    gotoDetail(id) {
      this.$router.push(`/bookdetail/${id}`);
    },
    // 댓글 생성
    createComment() {
      axios
        .put(
          `${process.env.VUE_APP_SERVER_URL}/reviews/comment/`,
          {
            content: this.comment,
            review_pk: this.$route.params.pk,
          },
          {
            headers: {
              Authorization: VueCookies.get("jwt_token"),
            },
          }
        )
        .then((res) => {
          // console.log("댓글 생성 후 결과");
          // console.log(res);
          this.comment = "";
          this.comments = res.data.result.reverse();
          this.commentData = this.comments.slice(0, 5);
        });
      // .catch((err) => {
      //   console.log(err);
      // });
    },
    // 댓글 수정 전
    beforeUpdateComment(com) {
      let num = 0;
      for (num; num < this.comments.length; num++) {
        if (this.comments[num]["edit"]) {
          this.comments[num]["content"] = this.tempComment;
        }
        this.comments[num]["edit"] = false;
        // console.log(this.comments[num]["edit"]);
      }
      this.tempComment = com.content;
      com.edit = !com.edit;
    },
    // 댓글 수정
    updateComment(com) {
      axios
        .post(
          `${process.env.VUE_APP_SERVER_URL}/reviews/comment/`,
          {
            content: com.content,
            comment_pk: com.id,
            review_pk: this.$route.params.pk,
          },
          {
            headers: {
              Authorization: VueCookies.get("jwt_token"),
            },
          }
        )
        .then((res) => {
          // console.log("댓글 수정 후 결과");
          // console.log(res);
          this.comments = res.data.result.reverse();
          com.edit = !com.edit;
          this.updateCommentNow = false;
        });
      // .catch((err) => {
      //   console.log(err);
      // });
    },
    // 댓글 수정 취소
    cancelComment(com) {
      com.content = this.tempComment;
      com.edit = !com.edit;
      this.tempComment = "";
    },
    // 댓글 삭제
    deleteComment(pk) {
      axios
        .delete(`${process.env.VUE_APP_SERVER_URL}/reviews/comment/`, {
          params: {
            comment_pk: pk,
            review_pk: this.$route.params.pk,
          },
          headers: {
            Authorization: VueCookies.get("jwt_token"),
          },
        })
        .then((res) => {
          // console.log("댓글 삭제 후 결과");
          // console.log(res);
          if (res.data.result == "해당 review 의 comments 가 없습니다") {
            this.comments = res.data.result;
          } else {
            this.comments = res.data.result.reverse();
            this.commentData = this.comments.slice(0, this.nowLength);
          }
        });
      // .catch((err) => {
      //   console.log(err);
      // });
    },

    // 리뷰 수정
    completeReviewModify() {
      axios
        .post(
          `${process.env.VUE_APP_SERVER_URL}/reviews/review/`,
          {
            review_pk: this.reviewData.id,
            book_pk: this.reviewData.book,
            title: this.reviewTitle,
            content: this.reviewContent,
            content_score: this.reviewData.content_score,
            design_score: this.reviewData.design_score,
          },
          {
            headers: { Authorization: VueCookies.get("jwt_token") },
          }
        )
        .then((res) => {
          // console.log(res);
          this.updateReviewNow = false;
          this.reviewTitle = res.data.result.title;
          this.reviewData.title = res.data.result.title;
          this.reviewContent = res.data.result.content;
          this.reviewData.content = res.data.result.content;
        });
      // .catch((err) => {
      //   console.log(err);
      // });
    },

    cancelReview() {
      this.reviewTitle = this.reviewData.title;
      this.reviewContent = this.reviewData.content;
      this.reviewContentScore = this.reviewData.content_score;
      this.reviewDesignScore = this.reviewData.design_score;
      this.updateReviewNow = false;
    },
    gotoReviewDelete(id) {
      axios
        .delete(`${process.env.VUE_APP_SERVER_URL}/reviews/review/`, {
          params: { review_pk: id },
          headers: { Authorization: VueCookies.get("jwt_token") },
        })
        .then(() => {
          swal("리뷰가 삭제되었습니다.", {
            button:false,
            timer: 1500
          })
          // console.log(res);
          this.$router.push("/community");
          
        });
      // .catch((err) => {
      //   console.log(err);
      // });
    },
    reviewLike(review) {
      axios
        .get(`${process.env.VUE_APP_SERVER_URL}/reviews/like/`, {
          params: {
            user_pk: VueCookies.get("user_pk"),
            review_pk: review.id,
          },
        })
        .then((res) => {
          // console.log("좋아요 결과");
          // console.log(res);
          review.review_like_state = !review.review_like_state;
          review.review_like_count = res.data.review_like_count;
        });
      // .catch((err) => {
      //   console.log(err);
      // });
    },
  },
};
</script>

<style scoped>
.main-font {
  font-family: "HangeulNuri-Bold";
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

.jua {
  font-family: "Jua", sans-serif;
}
.col.col-2 {
  padding: 0;
}
.do {
  font-family: "Do Hyeon", sans-serif;
}
.v-list.v-sheet.theme--light.v-list--subheader.v-list--three-line {
  width: 100%;
}
.cursor {
  cursor: pointer;
}
</style>
