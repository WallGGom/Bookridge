<template>
  <mdb-container>
    <!-- <mdb-btn color="default" @click.native="header = true">Phrase 쓰기 <i class="fas fa-edit"></i></mdb-btn> -->
    <mdb-btn
      class="indigo"
      style="
        color: white;
        float: right;
        font-family: HangeulNuri-Bold;
        border-radius: 5%;
      "
      @click.native="header = true"
      >글귀 작성</mdb-btn
    >
    <mdb-modal :show="header" @close="cancel" warning>
      <mdb-modal-header class="text-center" style="background-color: #00bfa5">
        <mdb-modal-title
          tag="h4"
          bold
          class="w-100"
          style="color: white; font-family: HangeulNuri-Bold"
          >글귀 작성</mdb-modal-title
        >
      </mdb-modal-header>
      <mdb-modal-body class="mx-3">
        <div v-if="bookTitle == null">
          <mdb-input
            disabled
            label="책 제목"
            v-model="booktitle2"
            class="mb-5"
            iconClass="text"
            style="font-family: HangeulNuri-Bold; color: black"
          />
        </div>
        <div v-else>
          <h2 style="font-family: HangeulNuri-Bold">{{ bookTitle }}</h2>
        </div>
        <mdb-input
          label="책 페이지"
          v-model="page"
          class="mb-5"
          style="font-family: HangeulNuri-Bold"
        />
        <mdb-input
          type="textarea"
          outline
          :rows="2"
          label="글귀(45자이내)"
          v-model="content"
          style="font-family: HangeulNuri-Bold"
        />
      </mdb-modal-body>
      <mdb-modal-footer center>
        <!-- {{ checked }} -->
        <div v-if="checked">
          <mdb-btn
            @click="createPhrase"
            outline="warning"
            style="font-family: HangeulNuri-Bold; font-size: small"
            >제출 <mdb-icon icon="paper-plane" class="ml-1"
          /></mdb-btn>
        </div>
        <div v-else>
          <mdb-btn
            color="mdb-color"
            outline="warning"
            style="font-family: HangeulNuri-Bold; font-size: small"
            >제출 <mdb-icon icon="paper-plane" class="ml-1"
          /></mdb-btn>
        </div>
        <mdb-btn
          @click="cancel"
          outline="danger"
          style="font-family: HangeulNuri-Bold"
          >취소 <mdb-icon icon="times" class="ml-1" style="color: red"
        /></mdb-btn>
      </mdb-modal-footer>
    </mdb-modal>
  </mdb-container>
</template>

<script>
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
} from "mdbvue";
import axios from "axios";
import VueCookies from "vue-cookies";
import swal from "sweetalert";

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
  },
  data() {
    return {
      checked: true,
      header: false,
      bookTitle: null,
      content: null,
      page: null,
    };
  },
  watch: {
    content() {
      if (this.content.length >= 45) {
        this.checked = false;
        this.content = this.content.slice(0, 45);
        // swal("45자")
      } else {
        this.checked = true;
      }
      // console.log(this.content.length);
    },
  },
  methods: {
    cancel() {
      this.header = false;
      this.page = "";
      this.content = "";
    },

    createPhrase() {
      if (!isNaN(Number(this.page)) && this.page) {
        if (this.page && this.content) {
          axios
            .put(
              `${process.env.VUE_APP_SERVER_URL}/reviews/phrase/`,
              {
                book_pk: this.$route.params.pk,
                page: this.page,
                content: this.content,
              },
              {
                headers: {
                  Authorization: VueCookies.get("jwt_token"),
                },
              }
            )
            .then(() => {
              // console.log("글 귀 생성");
              // console.log(res);
              this.header = false;
              this.$emit("sendPhrase");
              this.cancel();
            })
            // .catch((err) => {
            //   console.log(err);
            // });
        } else {
          swal("page 및 content 를 입력해주십시오.");
        }
      } else {
        swal("책 페이지는 숫자값으로 넣어주세요.");
      }
    },
  },
  props: {
    booktitle2: String,
  },
};
</script>

<style scoped>
label.acitve.mr-5 {
  color: black;
}
</style>
