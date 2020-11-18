<template>
  <div>
    <div id="map"></div>
  </div>
</template>

<script>
import axios from "axios";
import VueCookies from "vue-cookies";

export default {
  name: "Map",
  created() {
  },
  data() {
    return {
      myLocation: null,
      libraries: [], // 추가로 불러올 라이브러리
      map: null, // 지도 객체. 지도가 로드되면 할당됨.
    };
  },
  mounted() {
    // 도서관 위치 정보 가져오기
    axios
      .get(`${process.env.VUE_APP_SERVER_URL}/books/library/`, {
        params: {
          book_pk: this.$route.params.pk,
          user_pk: VueCookies.get("user_pk"),
        },
      })
      .then((res) => {
        // console.log("도서관 위치 가져오기");
        // console.log(res.data.result);
        this.libraryList = res.data.result["libs"];
        this.myLocation = res.data.result["user"];
        // console.log(this.myLocation);

        if (window.kakao && window.kakao.maps) {
          // console.log("나 여깃엉");
          setTimeout(() => {
            this.initMap();
          }, 1000);
        } else {
          const script = document.createElement("script");
          /* global kakao */
          script.onload = () => kakao.maps.load();
          script.src =
            "http://dapi.kakao.com/v2/maps/sdk.js?autoload=false&appkey=74f2063cad707b3796dacfe976496318";
          document.head.appendChild(script);
        }
      })
      // .catch((err) => {
      //   console.log(err);
      // });
  },
  methods: {
    initMap() {
      var imageSrc =
        "https://t1.daumcdn.net/localimg/localimages/07/mapapidoc/markerStar.png";

      var imageSize = new kakao.maps.Size(24, 35);

      // 마커 이미지를 생성합니다
      var markerImage = new kakao.maps.MarkerImage(imageSrc, imageSize);

      var mapContainer = document.getElementById("map"), // 지도를 표시할 div
        mapOption = {
          center: new kakao.maps.LatLng(
            this.myLocation["longitude"],
            this.myLocation["latitude"]
          ), // 지도의 중심좌표
          level: 8, // 지도의 확대 레벨
        };

      var map = new kakao.maps.Map(mapContainer, mapOption); // 지도를 생성합니다
      // console.log("드루와부렷엉3");
      // 마커를 표시할 위치와 내용을 가지고 있는 객체 배열입니다
      var positions = [];
      // 마커를 생성합니다

      var myMap_obj = new Object();
      myMap_obj.content = `<div>나의 위치</div>`;
      myMap_obj.latlng = new kakao.maps.LatLng(
        this.myLocation["longitude"],
        this.myLocation["latitude"]
      );
      myMap_obj.image = markerImage;
      // console.log("지도 위치");
      // console.log(positions);
      positions.push(myMap_obj);
      if (this.libraryList.length <= 10) {
        for (let j = 0; j < this.libraryList.length; j++) {
          var map_obj = new Object();
          map_obj.content = `<div>${this.libraryList[j]["lib"]["libName"]}</div>`;
          map_obj.latlng = new kakao.maps.LatLng(
            this.libraryList[j]["lib"]["latitude"],
            this.libraryList[j]["lib"]["longitude"]
          );
          positions.push(map_obj);
        }

        for (var i = 0; i < positions.length; i++) {
          if (i == 0) {
            var marker = new kakao.maps.Marker({
              map: map,
              position: positions[i].latlng,
              image: positions[i].image,
            });

            // 마커에 표시할 인포윈도우를 생성합니다
            var infowindow = new kakao.maps.InfoWindow({
              content: positions[i].content,
            });
          } else {
            // 마커를 생성합니다
            marker = new kakao.maps.Marker({
              map: map, // 마커를 표시할 지도
              position: positions[i].latlng, // 마커의 위치
            });

            // 마커에 표시할 인포윈도우를 생성합니다
            infowindow = new kakao.maps.InfoWindow({
              content: positions[i].content, // 인포윈도우에 표시할 내용
            });
          }
          // 마커에 mouseover 이벤트와 mouseout 이벤트를 등록합니다
          // 이벤트 리스너로는 클로저를 만들어 등록합니다
          // for문에서 클로저를 만들어 주지 않으면 마지막 마커에만 이벤트가 등록됩니다
          kakao.maps.event.addListener(
            marker,
            "mouseover",
            this.makeOverListener(map, marker, infowindow)
          );
          kakao.maps.event.addListener(
            marker,
            "mouseout",
            this.makeOutListener(infowindow)
          );
        }
      } else {
        this.libraryList = [];
      }
    },
    displayMarker(markerPositions) {
      if (this.markers.length > 0) {
        this.markers.forEach((marker) => marker.setMap(null));
      }

      const positions = markerPositions.map(
        (position) => new kakao.maps.LatLng(...position)
      );

      if (positions.length > 0) {
        this.markers = positions.map(
          (position) =>
            new kakao.maps.Marker({
              map: this.map,
              position,
            })
        );

        const bounds = positions.reduce(
          (bounds, latlng) => bounds.extend(latlng),
          new kakao.maps.LatLngBounds()
        );

        this.map.setBounds(bounds);
      }
    },
  },
};
</script>

<style>
</style>