<template>
  <mdb-container>
    <mdb-btn
      v-if="!isWritten"
      color="indigo"
      style="
        color: white;
        float: right;
        font-family: HangeulNuri-Bold;
        border-radius: 5%;
      "
      @click.native="header = true"
      >{{ btnTitle }}
    </mdb-btn>
    <mdb-btn
      v-else
      disabled
      color="blue-grey"
      style="
        color: white;
        float: right;
        font-family: HangeulNuri-Bold;
        border-radius: 5%;
      "
      >리뷰 작성 완료
    </mdb-btn>

    <mdb-modal :show="header" @close="cancel" warning>
      <mdb-modal-header class="text-center" style="background-color: #00bfa5">
        <mdb-modal-title tag="h4" bold class="w-100" style="color: white; font-family: HangeulNuri-Bold;"
          >리뷰 작성</mdb-modal-title
        >
      </mdb-modal-header>
      <mdb-modal-body class="mx-3">
        <div>
          <mdb-input
            disabled
            label="책 제목"
            v-model="book.book_title"
            class="mb-5"
            iconClass="text"
            style="font-family: HangeulNuri-Bold; "
          />
        </div>
        <mdb-input
          label="리뷰제목"
          v-model="reviewdata.title"
          class="mb-5"
          iconClass="text"
          style="font-family: HangeulNuri-Bold;"
        />
        <mdb-input
          type="textarea"
          outline
          v-model="reviewdata.content"
          :rows="4"
          label="리뷰내용"
          style="font-family: HangeulNuri-Bold;color:#757575"
        />
        <mdb-row>
          <mdb-col col="4">
            <span style="font-family: HangeulNuri-Bold; color:#757575"
              >내용 평점 :
            </span></mdb-col
          >
          <mdb-col col="8">
            <mdb-rating v-model="reviewdata.content_score" />
          </mdb-col>
        </mdb-row>

        <mdb-row>
          <mdb-col col="4">
            <span style="font-family: HangeulNuri-Bold; color:#757575"
              >디자인 평점 :
            </span>
          </mdb-col>
          <mdb-col col="8">
            <mdb-rating v-model="reviewdata.design_score" />
          </mdb-col>
        </mdb-row>
        <br />
      </mdb-modal-body>
      <mdb-modal-footer center>
        <mdb-btn
          @click="sendReview"
          outline="warning"
          style="font-family: HangeulNuri-Bold;"
          >저장 <mdb-icon icon="paper-plane" class="ml-1"
        /></mdb-btn>
        <mdb-btn
          @click="cancel"
          outline="danger"
          style="font-family: HangeulNuri-Bold;"
          >취소 <mdb-icon icon="times" class="ml-1" style="color: red"
        /></mdb-btn>
      </mdb-modal-footer>
    </mdb-modal>
  </mdb-container>
</template>

<script>
import swal from "sweetalert";
import {
  mdbContainer,
  mdbBtn,
  mdbModal,
  mdbModalHeader,
  mdbModalBody,
  mdbInput,
  mdbModalFooter,
  mdbModalTitle,
  mdbIcon,
  mdbRow,
  mdbCol,
  mdbRating,
} from "mdbvue";

import axios from "axios";
import VueCookies from "vue-cookies";

export default {
  components: {
    mdbContainer,
    mdbBtn,
    mdbModal,
    mdbModalHeader,
    mdbModalBody,
    mdbInput,
    mdbModalFooter,
    mdbModalTitle,
    mdbIcon,
    mdbRating,
    mdbRow,
    mdbCol,
  },
  data() {
    return {
      header: false,
      reviewdata: {
        title: null,
        content: null,
        content_score: null,
        design_score: null,
        book_pk: null,
        value: 0,
      },
    };
  },
  methods: {
    cancel() {
      this.header = false;
      this.reviewdata.title = "";
      this.reviewdata.content = "";
      this.reviewdata.content_score = "";
      this.reviewdata.design_score = "";
    },
    sendReview() {
      this.reviewdata.book_pk = this.book.book_pk;
      // console.log(this.reviewdata);
      if (this.reviewdata.content_score && this.reviewdata.design_score) {
        axios
          .put(
            `${process.env.VUE_APP_SERVER_URL}/reviews/review/`,
            this.reviewdata,
            {
              headers: { Authorization: VueCookies.get("jwt_token") },
            }
          )
          .then(() => {
            // console.log(res);
            this.$emit("sendReview");
            this.header = false;
            swal("리뷰작성이 완료되었습니다.");
            sessionStorage.clear();
            this.cancel();
          })
          // .catch((err) => {
          //   console.log(err);
          // });
      } else {
        swal("점수를 입력해 주십시오.");
      }
      this.reviewdata.content = "";
    },
  },
  props: {
    book: Object,
    btnTitle: String,
    isWritten: Boolean,
  },
};
</script>

<style scoped>
@font-face {
  font-family: "MaplestoryOTFBold";
  src: url("https://cdn.jsdelivr.net/gh/projectnoonnu/noonfonts_20-04@2.1/MaplestoryOTFBold.woff")
    format("woff");
  font-weight: 100;
  font-style: normal;
}
i.fas.prefix.fa-clipboard.text::before {
  color: #00bfa5;
}
.fa-clipboard:before {
  color: #00bfa5;
}
</style>
