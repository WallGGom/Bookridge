<template>
  <v-container>
    <v-row class="d-flex justify-content-center">
      <h2 class="my-5" style="font-family: HangeulNuri-Bold">
        👨‍💻{{ this.name }}님의 독서 성향
      </h2>
    </v-row>
    <v-row>
      <v-col lg="6" md="12" sm="12">
        <h4 style="font-family: HangeulNuri-Bold; text-align: center">
          💡{{ name }}님의 선호 장르
        </h4>
        <h6 class="main-font text-center">독서기록 및 책 좋아요 기반</h6>
        <mdb-radar-chart
          :data="radarChartData"
          :options="radarChartOptions"
          :width="600"
          :height="300"
          style="font-family: HangeulNuri-Bold"
        ></mdb-radar-chart>
        <v-divider></v-divider>
        <p class="main-font text-center">선호장르 Best 5</p>
        <v-list nav dense>
          <v-list-item-group
            color="primary"
            style="font-family: HangeulNuri-Bold"
          >
            <v-list-item v-for="(data, idx) in info.slice(0, 5)" :key="idx">
              <v-list-item-content>
                <v-list-item-title style="text-align: center"
                  >{{ idx + 1 }}위</v-list-item-title
                >
              </v-list-item-content>
              <v-list-item-content>
                <v-list-item-title
                  >{{ data[0] }}({{ data[1] }})</v-list-item-title
                >
              </v-list-item-content>
            </v-list-item>
          </v-list-item-group>
        </v-list>
      </v-col>
      <v-col
        lg="6"
        md="12"
        sm="12"
        class="d-flex flex-column justify-content-start"
      >
        <h4 style="font-family: HangeulNuri-Bold" class="text-center">
          📈{{ name }}님의 독서 그래프
        </h4>
        <h6 class="main-font text-center">독서기록 및 리뷰작성 기반</h6>
        <mdb-line-chart
          :data="lineChartData"
          :options="lineChartOptions"
          :width="600"
          :height="300"
        ></mdb-line-chart>
        <v-divider></v-divider>
        <p class="main-font text-center mb-5">{{ name }}님의 독서 계절은?</p>
        <v-list nav dense>
          <h5 class="main-font text-center my-5">{{ comment }}</h5>
          <v-row no-gutters>
            <v-col md="6" offset-md="3">
              <v-divider></v-divider>
            </v-col>
          </v-row>
          <h6 class="main-font my-5 text-center">
            {{ name }}님은 {{ month }}월 "{{ season }}"에 가장 많은 독서를 하고
            있습니다.
          </h6>
        </v-list>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import { mdbRadarChart, mdbLineChart } from "mdbvue";
export default {
  name: "MyChart",
  components: { mdbRadarChart, mdbLineChart },
  data() {
    return {
      comment: "가을은 역시 독서의 계절!!!",
      season: "가을",
      month: null,
      lineChartData: {
        labels: [
          "1월",
          "2월",
          "3월",
          "4월",
          "5월",
          "6월",
          "7월",
          "8월",
          "9월",
          "10월",
          "11월",
          "12월",
        ],
        datasets: [
          {
            label: "2020",
            backgroundColor: "rgba(255, 99, 132, 0.1)",
            borderColor: "rgba(255, 99, 132, 1)",
            borderWidth: 0.7,
            data: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
          },
        ],
      },
      lineChartOptions: {
        responsive: false,
        maintainAspectRatio: false,
        scales: {
          xAxes: [
            {
              gridLines: {
                display: true,
                color: "rgba(0, 0, 0, 0.1)",
              },
            },
          ],
          yAxes: [
            {
              gridLines: {
                display: true,
                color: "rgba(0, 0, 0, 0.1)",
              },
            },
          ],
        },
      },
      radarChartData: {
        labels: [
          "철학",
          "종교",
          "사회과학",
          "순수과학",
          "기술과학",
          "예술",
          "언어",
          "문학",
          "역사",
        ],
        datasets: [
          {
            label: "독서기록 + 책 좋아요",
            backgroundColor: "rgba(255, 99, 132, 0.1)",
            borderColor: "rgba(255, 99, 132, 1)",
            borderWidth: 0.7,
            data: [0, 0, 0, 0, 0, 0, 0, 0, 0],
          },
        ],
      },
      radarChartOptions: {
        responsive: false,
        maintainAspectRatio: false,
      },
    };
  },
  props: {
    radar: {
      type: Array,
    },
    line: {
      type: Array,
    },
    info: {
      type: Array,
    },
    name: {
      type: String,
    },
  },
  created() {
    this.radarChartData.datasets[0].data = this.radar;
    this.lineChartData.datasets[0].data = this.line;
    this.month = this.line.indexOf(Math.max(...this.line)) + 1;
    if (this.month > 12) {
      this.month = 1;
    }
    if (this.month < 3 || this.month == 12) {
      this.season = "겨울";
      this.comment = "겨울엔 따뜻한 집안에서 독서를!!!"
    } else if (this.month < 6) {
      this.season = "봄";
      this.comment = "봄엔 아름다운 꽃과 함께 독서를!!!"
    } else if (this.month < 9) {
      this.season = "여름";
      this.comment = "여름엔 에어컨 바람아래에서 독서를!!!"
    }
  },
};
</script>

<style scoped>
.main-font {
  font-family: "HangeulNuri-Bold";
}
</style>