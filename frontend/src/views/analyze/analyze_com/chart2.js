export const planetChartData2 = {
    type: "line",
    data: {
        labels: ["2017년", "2018년", "2019년", "2020년"],
        datasets: [
            {
                label: "여성",
                borderColor: "pink",
                borderWidth: 5,
                fill: false,
                data: [
                    5074864,
                    5441450,
                    5407720,
                    2214439
                
                ]
            },
            {
                label: "남성",
                borderColor: "lightblue",
                borderWidth: 5,
                fill: false,
                data: [
                    3145817,
                    3274016,
                    3136226,
                    1225629
                ]
            },
        ],
    },
    options: {
        responsive: true,
        legend: {
            position: "top"
        },
        title: {
            display: true,
            //text: "남/여 대여횟수"
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