<template>
  <div>
    <canvas id="chart1"></canvas>
  </div>
</template>

<script>
import Chart from "chart.js"
import { planetChartData } from "./chart1.js"

export default {
  name: "Test",
  data() {
    return {
      planetChartData: planetChartData
    };
  },
  methods: {
    createChart(charId, charData) {
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
    this.createChart('chart1', this.planetChartData)
  }
};
</script>

<style scoped>

</style>