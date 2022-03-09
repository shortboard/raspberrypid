import React, { useEffect, useState } from 'react';
import useInterval from '../hooks/UseInterval';
import ReactApexChart from 'react-apexcharts';
import { Card, CardHeader, Box } from '@mui/material';
const axios = require('axios');

const TempGraph = () => {
  const [state, setState] = useState({
    options: {
      chart: {
        id: "basic-bar"
      },
      xaxis: {
        categories: []
      }
    },
    series: [
      {
        name: "series-1",
        data: []
      }
    ]
  })
  
  useEffect(() => {
    getData()
  }, [])

  useInterval(async () => {
    getData()
  }, 5000)

  const getData = () => {
    axios.get("http://192.168.20.62:9000/tempgraph").then(response => {
      setState({
        options: {
          chart: {
            id: "basic-bar"
          },
          xaxis: {
            categories: response.data.map(x => x.time)
          }
        },
        series: [
          {
            name: "series-1",
            data: response.data.map(x => x.temp)
          }
        ]
      })
})
  }

  return (
    <Card>
      <CardHeader title="Temperature" subheader="Last 100 readings" />
      <Box sx={{ p: 3, pb: 1 }} dir="ltr">
        <ReactApexChart type="line" series={state.series} options={state.options} height={364} />
      </Box>
    </Card>
  );
}

export default TempGraph;