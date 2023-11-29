export function init_chart() {
    var chartDom = document.getElementById('main');
    var myChart = echarts.init(chartDom);
    var option;

    const timestamp = []
    const data_x = []
    const data_y = []
    const data_z = []

    option = {
      title: {
        text: 'Aceleração da base'
      },
      tooltip: {
        trigger: 'axis',
        axisPointer: {
          type: 'cross',
          label: {
            backgroundColor: '#283b56'
          }
        }
      },
      legend: {},
      dataZoom: {
        show: true,
        start: 0,
        end: 100
      },
      xAxis: [
        {
          type: 'category',
          boundaryGap: true,
          data: timestamp
        }
      ],
      yAxis: [
        {
          type: 'value',
          scale: true,
          name: 'G',
          max: 1,
          min: 0,
          boundaryGap: [0.2, 0.2]
        }
      ],
      series: [
        {
          name: 'X',
          type: 'line',
          data: data_x
        },
        {
          name: 'Y',
          type: 'line',
          data: data_y
        },
        {
          name: 'Z',
          type: 'line',
          data: data_z
        }
      ]
    };

    // setInterval(function () {
    //   let axisData = new Date().toLocaleTimeString().replace(/^\D*/, '');
    //
    //   data_x.push(+(Math.random()).toFixed(1));
    //   data_y.push(+(Math.random()).toFixed(1));
    //   data_z.push(+(Math.random()).toFixed(1));
    //
    //   // categories.shift();
    //   timestamp.push(axisData);
    //
    //   myChart.setOption({
    //     xAxis: [
    //       {
    //         data: timestamp
    //       }
    //     ],
    //     series: [
    //       {
    //         data: data_x
    //       },
    //       {
    //         data: data_y
    //       },
    //       {
    //         data: data_z
    //       }
    //     ]
    //   });
    // }, 1000);

    option && myChart.setOption(option);
    return [myChart, option];
}
