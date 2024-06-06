import React, { useState } from 'react'
import EChartsReact from 'echarts-for-react';
const GenreComponent = (props) => {
    const { genreCount, genreName } = props;
    const resultArray = genreCount.map((value, index) => ({
      value: value,
      name: genreName[index]
    }));


  // ECharts 데이터로 변환
  console.log(props.genreCount, props.genreName)
  const option = {
    tooltip: {
      trigger: 'item'
    },
    legend: {
      top: '0%',
      bottom:'10',
      textStyle: {
        color: '#ffff'
      },
      left: 'center',
    },
    series: [
      {
        name: 'Prefer genre',
        type: 'pie',
        radius: ['40%', '70%'],
        avoidLabelOverlap: false,
        itemStyle: {
          borderRadius: 10,
          borderColor: '#fff',
          borderWidth: 2
        },
        // label: {
        //   show: false,
        //   position: 'center'
        // },
        emphasis: {
          label: {
            show: true,
            fontSize: 40,
            fontWeight: 'bold',
          }
        },
        labelLine: {
          show: false
        },
        data: resultArray
      }
    ]
  };
  return (
    <EChartsReact 
        option={option}
        opts={{ renderer: 'svg', width: 'auto', height: 'auto' }}
    />
  )
}

export default GenreComponent