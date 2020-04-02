from .bandwidths import BANDWIDTHS

DEVICE_KEY = 'device_id'
TIME_KEY = 'timestamp'
FS_KEY = 'bytes_fs'
TS_KEY = 'bytes_ts'

def getWindowsForDevice(device_uuid, end_time, window_time, num_windows):
        earliest_time = end_time - (window_time * num_windows)
        start_idx = getFirstIdxForDevice(device_uuid, end_time, earliest_time)
        if (start_idx < 0):
            # didn't find device id. return full empty list
            return makeEmptyWindows(end_time, window_time, num_windows)

        window_start_time = end_time - window_time
        current_window = dict()
        current_window[TIME_KEY] = window_start_time
        current_window[FS_KEY] = 0
        current_window[TS_KEY] = 0

        completed_windows = []

        cur_idx = start_idx
        while (cur_idx < len(BANDWIDTHS)):
            cur_data = BANDWIDTHS[cur_idx]
            if (cur_data[DEVICE_KEY] != device_uuid):
                break
            cur_time = cur_data[TIME_KEY]
            if (cur_time < current_window[TIME_KEY]):
                completed_windows.append(current_window.copy())
                # check to see if we've reached num_windows
                if (len(completed_windows) == num_windows):
                    break
                # reset current window
                current_window = dict()
                window_start_time -= window_time
                current_window[TIME_KEY] = window_start_time
                current_window[FS_KEY] = 0
                current_window[TS_KEY] = 0
            #append current data
            current_window[FS_KEY] += cur_data[FS_KEY]
            current_window[TS_KEY] += cur_data[TS_KEY]
            
            cur_idx += 1

        if (len(completed_windows) < num_windows):
            # first, append current_window
            completed_windows.append(current_window)
            window_start_time -= window_time
            # append clears on end
            empty_windows = makeEmptyWindows(window_start_time, window_time, num_windows - len(completed_windows))
            completed_windows += empty_windows

        completed_windows.reverse()
        return completed_windows

def getFirstIdxForDevice(target_uuid, end_time, start_time):
    for i in range(len(BANDWIDTHS)):
        elt = BANDWIDTHS[i]
        if elt[DEVICE_KEY] == target_uuid:
            # if (elt[TIME_KEY] < start_time):
            #     # the most recent time for the device is before the earliest possible time we could find.
            #     return -1
            # find the first point where we're earlier than (or at) end_time
            while i < len(BANDWIDTHS) and elt[DEVICE_KEY] == target_uuid:
                elt = BANDWIDTHS[i]
                if (elt[TIME_KEY] <= end_time):
                    return i
                i += 1
            return -1
    return -1

def makeEmptyWindows(cur_time, window_time, num_windows):
    windows_to_make = num_windows
    empty_windows = []
    while (windows_to_make > 0):
        empty_window = dict()
        empty_window[TIME_KEY] = cur_time
        empty_window[FS_KEY] = 0
        empty_window[TS_KEY] = 0
        empty_windows.append(empty_window)

        windows_to_make -= 1
        cur_time -= window_time
    return empty_windows