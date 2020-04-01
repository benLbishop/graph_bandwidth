import axios, { AxiosResponse } from 'axios';
import { BandwidthData, BandwidthDataWrapper } from '../types';

const handleError = (err: any) => {
    console.log(err);
}

export const retrieveBandwidthData = async (
    device_uuid: string,
    end_time?: number,
    window_time?: number,
    num_windows?: number
): Promise<BandwidthData[]> => {
    let paramsString = `?device_uuid=${device_uuid}`;
    // TODO: move url to constants
    if (end_time) {
        paramsString += `&end_time=${end_time}`;  
    }
    if (window_time) {
        paramsString += `&window_time=${window_time}`
    }
    if (num_windows) {
        paramsString += `&num_windows=${num_windows}`
    }
    const url = 'http://127.0.0.1:5000/bandwidths' + paramsString;
    
    let res: AxiosResponse;

    try {
        res = await axios.get(url);
    } catch (err) {
        handleError(err);
        return [];
    }

    const rawData = res.data as BandwidthDataWrapper;
    console.log(rawData.data)
    return rawData.data;
}