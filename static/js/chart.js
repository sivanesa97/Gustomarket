$(document).ready(function () {


    var options = {
        series: [{
            name: 'Unique Words',
            data: [76, 85, 101, 98, 87, 105, 91]
        }],
        colors: ["#B5E4CA"],
        chart: {
            type: 'bar',
            height: 355
        },
        plotOptions: {
            bar: {
                horizontal: false,
                columnWidth: '32%',
                endingShape: 'rounded'
            },
        },
        dataLabels: {
            enabled: false
        },
        stroke: {
            show: true,
            width: 2,
            colors: ['transparent']
        },
        xaxis: {
            categories: ['22', '23', '24', '25', '26', '27', '28'],
        },
        yaxis: {
            title: {
                text: '$ (thousands)'
            }
        },
        fill: {
            opacity: 1
        },
        tooltip: {
            y: {
                formatter: function (val) {
                    return "$ " + val + " thousands"
                }
            }
        }
    };

    var chart = new ApexCharts(document.querySelector("#productsales-chart"), options);
    chart.render();

    var options = {
        series: [{
            name: 'Unique Words',
            data: [76, 45, 101, 98, 87, 25, 91]
        }],
        colors: ["#B5E4CA"],
        chart: {
            type: 'bar',
            height: 355
        },
        plotOptions: {
            bar: {
                horizontal: false,
                columnWidth: '32%',
                endingShape: 'rounded'
            },
        },
        dataLabels: {
            enabled: false
        },
        stroke: {
            show: true,
            width: 2,
            colors: ['transparent']
        },
        xaxis: {
            categories: ['22', '23', '24', '25', '26', '27', '28'],
        },
        yaxis: {
            title: {
                text: '$ (thousands)'
            }
        },
        fill: {
            opacity: 1
        },
        tooltip: {
            y: {
                formatter: function (val) {
                    return "$ " + val + " thousands"
                }
            }
        }
    };

    var chart = new ApexCharts(document.querySelector("#productsales-chart1"), options);
    chart.render();

    var options = {
        series: [{
            name: 'Unique Words',
            data: [20, 85, 101, 50, 87, 105, 31]
        }],
        colors: ["#B5E4CA"],
        chart: {
            type: 'bar',
            height: 355
        },
        plotOptions: {
            bar: {
                horizontal: false,
                columnWidth: '32%',
                endingShape: 'rounded'
            },
        },
        dataLabels: {
            enabled: false
        },
        stroke: {
            show: true,
            width: 2,
            colors: ['transparent']
        },
        xaxis: {
            categories: ['22', '23', '24', '25', '26', '27', '28'],
        },
        yaxis: {
            title: {
                text: '$ (thousands)'
            }
        },
        fill: {
            opacity: 1
        },
        tooltip: {
            y: {
                formatter: function (val) {
                    return "$ " + val + " thousands"
                }
            }
        }
    };

    var chart = new ApexCharts(document.querySelector("#productsales-chart2"), options);
    chart.render();
});
