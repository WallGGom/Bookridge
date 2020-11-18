export const planetChartData3 = {
    type: "line",
    data: {
        labels: ["1월", "2월", "3월", "4월", "5월", "6월", "7월", "8월", "9월", "10월", "11월", "12월"],
        datasets: [
            {
                label: "2017년",
                borderColor: "pink",
                borderWidth: 5,
                fill: false,
                data: [
                    754839,
                    683096,
                    642284,
                    622694,
                    600138,
                    627882,
                    776412,
                    865567,
                    722580,
                    599058,
                    635209,
                    690922
                ]
            },
            {
                label: "2018년",
                borderColor: "lightblue",
                borderWidth: 5,
                fill: false,
                data: [
                    863240,
                    656291,
                    696251,
                    676560,
                    679269,
                    685080,
                    840826,
                    868046,
                    685648,
                    667710,
                    676990,
                    719555
                ]
            },
            {
                label: "2019년",
                borderColor: "#FFCC80",
                borderWidth: 5,
                fill: false,
                data: [
                    853300,
                    722025,
                    725144,
                    668374,
                    651547,
                    690283,
                    801636,
                    844545,
                    649801,
                    592043,
                    653511,
                    691737
                ]
            },
            {
                label: "2020년",
                borderColor: "#C5CAE9",
                borderWidth: 5,
                fill: false,
                data: [
                    780292,
                    516273,
                    116225,
                    215846,
                    427170,
                    333148,
                    540912,
                    510202,
                    0,
                    0,
                    0,
                    0
                ]
            }
        ],
    },
    options: {
        responsive: true,
        legend: {
            position: "top"
        },
        title: {
            display: true,
            //text: "연도별 대여횟수"
        },
        scales: {
            yAxes: [{
                ticks: {
                    beginAtZero: true,
                    callback: function (value, index, values) {
                        if (values[0].toString().length > 9 && value != 0) return (Math.floor(value / 100000000)).toLocaleString("ko-KR") + "억";
                        else if (values[0].toString().length == 9 && value != 0) return (value / 100000000).toFixed(1) + "억";
                        else if (values[0].toString().length > 6 && value != 0) return (Math.floor(value / 10000)).toLocaleString("ko-KR") + "만";
                        else if (values[0].toString().length == 6 && value != 0) return (value / 10000).toFixed(1) + "만";
                        else return value.toLocaleString("ko-KR");
                    }
                }
            }]
        }
    }
}