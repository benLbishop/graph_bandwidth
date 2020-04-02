from .bandwidths import BANDWIDTHS
from math import floor

DEVICE_KEY = 'device_id'
TIME_KEY = 'timestamp'
FS_KEY = 'bytes_fs'
TS_KEY = 'bytes_ts'

def getWindowsForDevice(device_uuid, end_time, window_time, num_windows):
        start_idx = getFirstIdxForDevice(device_uuid)
        if (start_idx < 0):
            # didn't find device id. return full empty list
            return makeStartingWindows(end_time, window_time, num_windows)

        completed_windows = []
        
        # account for case where end_time is beyond the last received device timestamp
        last_device_timetsamp = BANDWIDTHS[start_idx][TIME_KEY]
        windows_after_last_device_time = makeEndingWindows(last_device_timetsamp, end_time, window_time, num_windows)
        completed_windows += windows_after_last_device_time

        cur_window_start_time = end_time - window_time * (len(completed_windows) + 1)
        cur_window = makeEmptyWindow(cur_window_start_time)
        cur_idx = getWindowsStartIdx(start_idx, device_uuid, cur_window_start_time + window_time)
        while True:
            # check to see if we've reached num_windows
            if (len(completed_windows) == num_windows):
                break
            if cur_idx == len(BANDWIDTHS):
                break
            cur_data = BANDWIDTHS[cur_idx]
            if (cur_data[DEVICE_KEY] != device_uuid):
                break
            cur_time = cur_data[TIME_KEY]
            if (cur_time < cur_window[TIME_KEY]):
                completed_windows.append(cur_window.copy())
                # reset current window
                cur_window_start_time -= window_time
                cur_window = makeEmptyWindow(cur_window_start_time)
            #append current data
            cur_window[FS_KEY] += cur_data[FS_KEY]
            cur_window[TS_KEY] += cur_data[TS_KEY]
            
            cur_idx += 1

        if (len(completed_windows) < num_windows):
            # first, append current_window
            completed_windows.append(cur_window)
            cur_window_start_time -= window_time
            # append clears on end
            empty_windows = makeStartingWindows(cur_window_start_time, window_time, num_windows - len(completed_windows))
            completed_windows += empty_windows

        completed_windows.reverse()
        return completed_windows

def getFirstIdxForDevice(target_uuid):
    for i in range(len(BANDWIDTHS)):
        elt = BANDWIDTHS[i]
        if elt[DEVICE_KEY] == target_uuid:
            return i
    return -1

def getWindowsStartIdx(start_idx, target_uuid, timestamp):
    cur_idx = start_idx
    while True:
        if cur_idx == len(BANDWIDTHS):
            break
        elt = BANDWIDTHS[cur_idx]
        if elt[DEVICE_KEY] != target_uuid:
            break
        if elt[TIME_KEY] <= timestamp:
            break
        cur_idx += 1
    return cur_idx
        
def makeEndingWindows(last_device_time, end_time, window_time, max_num_windows):
    cur_window_start_time = end_time - window_time
    empty_windows = []
    while cur_window_start_time > last_device_time and len(empty_windows) < max_num_windows:
        empty_window = makeEmptyWindow(cur_window_start_time)
        empty_windows.append(empty_window)

        cur_window_start_time -= window_time

    return empty_windows

def makeStartingWindows(timestamp, window_time, num_windows_to_make):
    cur_window_start_time = timestamp - window_time
    empty_windows = []
    while len(empty_windows) < num_windows_to_make:
        empty_window = makeEmptyWindow(cur_window_start_time)
        empty_windows.append(empty_window)

        cur_window_start_time -= window_time
    return empty_windows

def makeEmptyWindow(timestamp):
    empty_window = dict()
    empty_window[TIME_KEY] = timestamp
    empty_window[FS_KEY] = 0
    empty_window[TS_KEY] = 0

    return empty_window