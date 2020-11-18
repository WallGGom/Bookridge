<template>
  <div>
    <canvas id="chart3"></canvas>
  </div>
</template>

<script>
import Chart from "chart.js"
import { planetChartData3 } from "./chart3.js"

export default {
  name: "Test3",
  data() {
    return {
      planetChartData3: planetChartData3
    };
  },
  methods: {
    createChart3(charId, charData) {
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
    this.createChart3('chart3', this.planetChartData3)
  }
};
</script>

<style scoped>

</style>