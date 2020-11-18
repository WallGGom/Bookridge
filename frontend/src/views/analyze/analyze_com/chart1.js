export const planetChartData = {
    type: "bar",
    data: {
        labels: ["8~13세", "14~19세", "20대", "30대", "40대", "50대", "60세 이상"],
        datasets: [
            {
                label: "2017년",
                backgroundColor: "#E3F2FD",
                borderColor: "#E3F2FD",
                borderWidth: 1,
                data: [
                    1740097,
                    665113,
                    998345,
                    1736961,
                    2063853,
                    639283,
                    377029
                ]
            },
            {
                label: "2018년",
                backgroundColor: "#D1C4E9",
                borderColor: "#D1C4E9",
                borderWidth: 1,
                data: [
                    1792365,
                    638150,
                    1009021,
                    1859621,
                    2268142,
                    714434,
                    433733
                ]
            },
            {
                label: "2019년",
                backgroundColor: "#FCE4EC",
                borderColor: "#FCE4EC",
                borderWidth: 1,
                data: [
                    1716033,
                    540043,
                    853447,
                    1832649,
                    2391349,
                    759011,
                    451414
                ]
            },
            {
                label: "2020년",
                backgroundColor: "#B2DFDB",
                borderColor: "B2DFDB",
                borderWidth: 1,
                data: [
                    750642,
                    222576,
                    330977,
                    630269,
                    1032266,
                    294698,
                    178640
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