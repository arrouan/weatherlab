import React, { Component } from 'react';
//import {LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend} from 'recharts';

import { Index, TimeSeries } from "pondjs";
import { Charts, ChartContainer, ChartRow, YAxis, LineChart } from "react-timeseries-charts";

export default class TestChart extends Component {

  constructor() {
    super();
    this.state = {data: []};
  }

  componentDidMount() {
    fetch('http://localhost:5000/noaa/data')
      .then((response) => {
        return response.json();
      })
      .then((data) => {
        this.setState({data: data});
      });
  }

    //convert this data to a Timeseries type
    // cf lines 49-80 in https://github.com/esnet/react-timeseries-charts/blob/master/src/website/examples/cycling/Index.js

    
render() {
    return (
        <ChartContainer timeRange={data.timerange()} width={800}>
            <ChartRow height="200">
                <YAxis id="axis1" label="AUD" min={0.5} max={1.5} width="60" />
                <Charts>
                    <LineChart axis="axis1" series={this.state.data}/>
                </Charts>
            </ChartRow>
        </ChartContainer>
    );
}

      // 	render () {
  // 	return (
  //   	<LineChart width={600} height={300} data={this.state.data}
  //           margin={{top: 5, right: 30, left: 20, bottom: 5}}>
  //      <XAxis dataKey="time"/>
  //      <YAxis/>
  //      <CartesianGrid strokeDasharray="3 3"/>
  //      <Tooltip/>
  //      <Legend />
  //      <Line type="monotone" dataKey="mean" stroke="#8884d8" activeDot={{r: 8}}/>
  //     </LineChart>
  //   );
  // }


}




