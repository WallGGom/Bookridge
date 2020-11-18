<template>
  <div class="h-100 d-flex justify-content-center align-items-center">
    <div class="nobook">
      <h1 style="text-align: center;font-family: HangeulNuri-Bold;">검색하신 도서가 존재하지 않습니다.</h1>
    </div>
  </div>
</template>

<script>


export default {
  components: {
    
  },
};
</script>

<style scoped>
.nobook {
  vertical-align: middle;
  background-image: url("/src/assets/img/물음표.png");
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
</style>