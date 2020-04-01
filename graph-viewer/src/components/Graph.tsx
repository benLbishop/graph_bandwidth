import React from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend } from 'recharts';
import { BandwidthData } from '../types';
import { retrieveBandwidthData } from '../lib/endpoint';

interface _Props {}

interface State {
  data: BandwidthData[];
}

class Graph extends React.PureComponent<_Props, State> {

  constructor(props: _Props) {
    super(props);
    this.state = {
      data: []
    }
  }

  getUrlParams = () => {
    const queryString = window.location.search;
    const urlParams = new URLSearchParams(queryString);
    return urlParams
}

  getData = async () => {
    const params = this.getUrlParams();
    const uuid = params.get('device_uuid');
    const end_time_str = params.get('end_time');
    const window_time_str = params.get('window_time');
    const num_windows_str = params.get('num_windows');
    let end_time: number | undefined;
    let window_time: number | undefined;
    let num_windows: number | undefined;
    if (end_time_str) {
      end_time = parseInt(end_time_str, 10);
    }
    if (window_time_str) {
      window_time = parseInt(window_time_str, 10);
    }
    if (num_windows_str) {
      num_windows = parseInt(num_windows_str, 10);
    }
    let data = await retrieveBandwidthData(uuid ? uuid : '', end_time, window_time, num_windows);

    this.setState({
      data
    })
  }
  componentDidMount() {
    this.getData()
  }

  render() {
    return <div style={{flex: 1, flexDirection: 'column'}}>
        <LineChart
        width={800}
        height={500}
        data={this.state.data}
      >
        <CartesianGrid strokeDasharray="3 3" />
        <XAxis dataKey="timestamp" />
        <YAxis />
        <Tooltip />
        <Legend />
        <Line type="monotone" dataKey="bytes_fs" stroke="#8884d8" activeDot={{ r: 8 }} />
        <Line type="monotone" dataKey="bytes_ts" stroke="#82ca9d" />
      </LineChart>
    </div>;
  }
}

export default Graph;