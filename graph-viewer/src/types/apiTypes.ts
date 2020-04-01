export interface BandwidthData {
    timestamp: number;
    bytes_ts: number;
    bytes_fs: number;
}

export interface BandwidthDataWrapper {
    data: BandwidthData[];
}