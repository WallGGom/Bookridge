<template>
  <div>
    <vue-datamaps
      :scope="scope"
      :setProjection="setProjection('korea')"
      :fills="fills"
      :data="data"
      popupTemplate
      @custom:popup="popupTemplate"
      ><div slot="hoverinfo" class="hoverinfo" style="white-space: pre-line">
        {{ popupData }}
      </div></vue-datamaps
    >
  </div>
</template>

<script>
import { VueDatamaps } from "vue-datamaps";
export default {
  components: {
    "vue-datamaps": VueDatamaps,
  },
  data() {
    return {
      popupData: "",
      scope: "kor",
      fills: {
        color1: "#FAF3DD",
        color2: "#C8D5B9",
        color3: "#8FC0A9",
        color4: "#68B0AB",
        color5: "#696D7D",
        color6: "#F6F6E2",
        color7: "#CDCDBF",
        color8: "#A4A4AE",
        color9: "#8787AC",
        color10: "#6A6A79",
        color11: "#F9E6E7",
        color12: "#C8C5C6",
        color13: "#91B2B3",
        color14: "#6BADAD",
        color15: "#697675",
        color16: "#7598AB",
        color17: "#696B7B",
      },
      data: {
        "KR.SO": {
          fillKey: "color1",
          count: 628411,
        },
        "KR.PU": {
          fillKey: "color2",
          count: 273940,
        },
        "KR.TG": {
          fillKey: "color3",
          count: 139800,
        },
        "KR.IN": {
          fillKey: "color4",
          count: 84053,
        },
        "KR.KJ": {
          fillKey: "color5",
          count: 71993,
        },
        "KR.TJ": {
          fillKey: "color6",
          count: 108220,
        },
        "KR.UL": {
          fillKey: "color7",
          count: 113490,
        },
        "KR.SJ": {
          fillKey: "color8",
          count: 18446,
        },
        "KR.KG": {
          fillKey: "color9",
          count: 1129399,
        },
        "KR.KW": {
          fillKey: "color10",
          count: 91613,
        },
        "KR.GB": {
          fillKey: "color11",
          count: 129146,
        },
        "KR.GN": {
          fillKey: "color12",
          count: 110563,
        },
        "KR.CB": {
          fillKey: "color13",
          count: 107546,
        },
        "KR.JN": {
          fillKey: "color14",
          count: 136435,
        },
        "KR.KB": {
          fillKey: "color15",
          count: 146993,
        },
        "KR.KN": {
          fillKey: "color16",
          count: 158725,
        },
        "KR.CJ": {
          fillKey: "color17",
          count: 74859,
        },
      },
    };
  },
  methods: {
    popupTemplate({ geography, datum }) {
      this.popupData = `${geography.properties.name}\n대여 횟수: ${datum.count}`;
    },
    setProjection(type) {
      const createProjection = {
        korea: function (d3, element) {
          const projection = d3
            .geoMercator()
            .center([0, 0])
            .rotate([-128, -36])
            .scale(element.offsetWidth * 6)
            .translate([element.offsetWidth / 2, element.offsetHeight / 2]);
          const path = d3.geoPath().projection(projection);
          return { projection, path };
        },
        zoom: function (d3, element) {
          var projection = d3
            .geoEquirectangular()
            .center([23, -3])
            .rotate([4.4, 0])
            .scale(element.offsetHeight * 0.6)
            .translate([element.offsetWidth / 2, element.offsetHeight / 2]);
          var path = d3.geoPath().projection(projection);
          return { path: path, projection: projection };
        },
      };
      return createProjection[type];
    },
  },
};
</script>

<style scoped>
</style>