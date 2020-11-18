<template>
  <div>
    <canvas id="chart2"></canvas>
  </div>
</template>

<script>
import Chart from "chart.js"
import { planetChartData2 } from "./chart2.js"

export default {
  name: "Test2",
  data() {
    return {
      planetChartData2: planetChartData2
    };
  },
  methods: {
    createChart2(charId, charData) {
      const ctx = document.getElementById(charId);
      const myChart = new Chart(ctx, {
        type: charData.type,
        data: charData.data,
        options: charData.options,
      });
      console.log(myChart)
    }
  },
  mounted() {
    this.createChart2('chart2', this.planetChartData2)
  }
};
</script>

<style scoped>

</style>