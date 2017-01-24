import React, { Component } from 'react';
import {LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend} from 'recharts';

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

	render () {
  	return (
    	<LineChart width={600} height={300} data={this.state.data}
            margin={{top: 5, right: 30, left: 20, bottom: 5}}>
       <XAxis dataKey="time"/>
       <YAxis/>
       <CartesianGrid strokeDasharray="3 3"/>
       <Tooltip/>
       <Legend />
       <Line type="monotone" dataKey="mean" stroke="#8884d8" activeDot={{r: 8}}/>
      </LineChart>
    );
  }
}




