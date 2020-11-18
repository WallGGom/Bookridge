<template>
  <v-footer dark padless>
    <v-card class="flex" flat tile>
      <v-card-title class="teal d-flex justify-content-center">
        <strong class="subheading main-font"
          >{{ new Date().getFullYear() }} — BOOKRIDGE</strong
        >
      </v-card-title>

      <v-card-text class="py-2 white--text text-center">
        <strong class="main-font">개발자 : 정무성 이종호 엄희관 김희정 강해솔</strong>
      </v-card-text>
    </v-card>
  </v-footer>
</template>

<script>
export default {
  data() {
    return {
    };
  },
};
</script>
<style scoped>
.main-font {
  font-family: "HangeulNuri-Bold";
}
</style>