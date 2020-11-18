<template>
  <div>
    <canvas id="chart5"></canvas>
  </div>
</template>

<script>
import Chart from "chart.js"
import { planetChartData5 } from "./chart5.js"

export default {
  name: "Test5",
  data() {
    return {
      planetChartData5: planetChartData5
    };
  },
  methods: {
    createChart5(charId, charData) {
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
    this.createChart5('chart5', this.planetChartData5)
  }
};
</script>

<style scoped>

</style>