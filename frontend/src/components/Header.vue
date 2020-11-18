<template>
  <div class="header">
    <v-row>
      <v-col cols="4">
        <h1>
          <router-link :to="'/'">
            <v-img
              src="../assets/img/로고.jpg"
              width="200"
              height="50"
              contain
            ></v-img>
          </router-link>
        </h1>
      </v-col>
      <v-col cols="4">
        <v-btn
          tile
          outlined
          color="white"
          class="mx-2 float-right"
          style="
            font-family: 'HangeulNuri-Bold';
            border-radius: 5%;
            background-color: #1a237e;
          "
          @click="searchWord"
        >
          <v-icon>mdi-magnify</v-icon>
        </v-btn>

        <v-text-field
          v-model="bookKeyword"
          label="검색어를 입력해주세요."
          single-line
          hide-details
          class="pt-0 mx-2 float-right"
          style="
            font-family: 'HangeulNuri-Bold';
            text-align: center;
            width: 170px;
          "
          @keyup.enter="searchWord"
        ></v-text-field>

        <v-select
          :items="items"
          v-model="dropDown"
          class="STS pt-0 float-right"
          style="font-family: 'HangeulNuri-Bold'; text-align: center"
        ></v-select>
      </v-col>
      <v-col cols="4">
        <v-btn
          tile
          outlined
          color="white"
          class="mx-2 float-right jua"
          @click="logout"
          style="
            text-align: center;
            border-radius: 5%;
            background-color: #1a237e;
            font-size: medium;
          "
          >로그아웃</v-btn
        >

        <v-btn
          tile
          outlined
          color="#1A237E"
          class="mx-2 float-right jua"
          @click="goToProfile"
          style="
            text-align: center;
            border-width: 3px;
            border-radius: 5%;
            font-size: medium;
          "
          ><i class="fas fa-user-circle"></i>프로필</v-btn
        >
      </v-col>
    </v-row>
  </div>
</template>

<script>
// import axios from "axios";
import VueCookies from "vue-cookies";
import swal from "sweetalert";

export default {
  name: "Header",
  components: {},
  props: {
    isLogin: {
      type: Boolean,
      default: false,
    },
  },
  created() {},
  watch: {
    dropDown() {
      if (this.dropDown == "제목") {
        this.searchType = 0;
      } else if (this.dropDown == "작가") {
        this.searchType = 1;
      } else {
        this.searchType = 2;
      }
    },
  },
  data() {
    return {
      bookKeyword: "",
      searchType: 0,
      dropDown: "제목",
      items: ["제목", "작가", "출판사"],
    };
  },
  methods: {
    goToProfile() {
      this.$router.push({
        name: "Profile",
      });
    },
    logout() {
      VueCookies.keys().forEach((cookie) => VueCookies.remove(cookie));
      this.closeLoginModal();
      sessionStorage.clear();
      // swal("정상적으로 로그아웃이 되었습니다!", {
      //   buttons: false,
      //   timer: 5000,
      // });
      this.$router.push({ name: "Home" });
      this.$router.go();
    },
    closeLoginModal() {
      this.userId = "";
      this.password = "";
    },
    searchWord(e) {
      e.preventDefault();
      if (this.bookKeyword == "") {
        swal("검색어를 최소 한 자 이상 입력해주세요.");
      } else {
        if (
          this.$router.currentRoute.fullPath !=
          `/search/${this.bookKeyword}/${this.searchType}`
        ) {
          this.$router.push(`/search/${this.bookKeyword}/${this.searchType}`);
        }
      }
    },
    searchList(id) {
      if (id == 0) {
        this.dropDown = "제목";
        this.searchType = id;
      } else if (id == 1) {
        this.dropDown = "작가";
        this.searchType = id;
      } else {
        this.dropDown = "출판사";
        this.searchType = id;
      }
    },
  },
};
</script>

<style scoped>
.STS {
  width: 100px;
}
.v-list.v-select-list.v-sheet.theme--light.theme--light {
  font-family: HangeulNuri-Bold;
}
.jua {
  font-family: "Jua", sans-serif;
}
</style>