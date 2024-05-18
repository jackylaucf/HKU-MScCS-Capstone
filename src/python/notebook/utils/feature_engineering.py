import pandas as pd
import numpy as np

def add_return_data(
        raw_dataset: pd.DataFrame,
        return_days: int,
    ):
    dataset = raw_dataset.copy()
    return_dates = []
    return_values = []
    for i in range(len(dataset)):
        # # get expect return date and find the closest record 
        # return_date = dataset.iloc[i]['date'] + np.timedelta64(return_days,'D')
        # return_data_df = dataset.loc[dataset['date'] >= return_date].sort_values(by=['date'])
        # # return null if there is no return_data_df
        # if len(return_data_df) < 1:
        #     return_dates.append(None)
        #     return_values.append(None)
        #     continue

        # return_data = return_data_df.iloc[0]
        # return_value = return_data['close'] / dataset.iloc[i]['close'] - 1
        # return_dates.append(return_data['date'])
        # return_values.append(return_value)

        # if we just search for the [i+return_days] row
        if (i + return_days >= len(dataset)): 
            return_dates.append(None)
            return_values.append(None)
            continue
        return_data = dataset.iloc[i + return_days]
        return_value = return_data['close'] / dataset.iloc[i]['close'] - 1
        return_dates.append(return_data['date'])
        return_values.append(return_value)

    dataset[f'return_{return_days}_date'] = return_dates
    dataset[f'return_{return_days}_value'] = return_values
    
    return dataset


def add_simple_moving_average(
        raw_dataset: pd.DataFrame,
        ma_days: int, # 50, 100, 200 or any value
    ):
    dataset = raw_dataset.copy()
    queue = [] # an array storing last x day's value (if ma_days = 50, there will be 50 value in this array)
    ma_values = []
    for i in range(len(dataset)):
        if (len(queue) < ma_days): 
            # not enough data to calc the moving average
            queue.append(dataset.iloc[i]['close'])
            ma_values.append(None)
            continue
        # got enough data, start appending
        ma_values.append(sum(queue) / ma_days)
        # append current date's close value to queue
        queue.append(dataset.iloc[i]['close'])
        # pop the earliest record from queue
        queue.pop(0)

    dataset[f'ma_{ma_days}d'] = ma_values
    
    return dataset

# Function to generate daily ohlc chart
# https://stackoverflow.com/questions/434583/what-is-the-fastest-way-to-draw-an-image-from-discrete-pixel-values-in-python
# https://stackoverflow.com/questions/57545125/attributeerror-module-scipy-misc-has-no-attribute-toimage
def generate_daily_ohlc_chart(
        size: int,          # height of the bitmap
        min: float,         # the minimum value in that period (5d etc)
        max: float,         # the maximum value in that period (5d etc)
        o: float,           # open
        h: float,           # high
        l: float,           # low
        c: float,           # close
        color = 255,        # 255 or [255, 255, 255] if we want to use RGB
        bgColor = 0         # 0 or [0, 0, 0] if we want to use RGB
    ) -> np.ndarray:
    # initize the data
    data = np.empty((size, 3), dtype=np.uint8) # (size, 3) or (size, 3, 3) if we want to use RGB
    # background color
    data[:,:] = bgColor
    # calculation
    _step = (max - min) / size
    # open
    _open = int((o - min) / _step) # will floor the number
    if _open == size: # -1 if its the maximum value
        _open -= 1
    data[_open,0] = color
    # high-low
    _high = int((h - min) / _step) # will floor the number
    _low = int((l - min) / _step) # will floor the number
    if _high == size: # -1 if its the maximum value
        _high -= 1
    if _low == size: # -1 if its the maximum value
        _low -= 1
    data[_low:_high + 1,1] = color
    # close
    _close = int((c - min) / _step) # will floor the number
    if _close == size: # -1 if its the maximum value
        _close -= 1
    data[_close,2] = color

    return np.flip(data, 0)

# Function to generate moving average chart
def generate_ma_chart(
        size: int,          # height of the bitmap
        min: float,         # the minimum value in that period (5d etc)
        max: float,         # the maximum value in that period (5d etc)
        rawData: list,      # array of data
        color = 255,        # 255 or [255, 255, 255] if we want to use RGB
        bgColor = 0         # 0 or [0, 0, 0] if we want to use RGB
    ) -> np.ndarray:
    # initize the data
    data = np.empty((size, len(rawData) * 3), dtype=np.uint8) # (height, width) or (height, width, 3) if we want to use RGB
    # background color
    data[:,:] = bgColor
    # calculation
    _step = (max - min) / size

    for index, value in enumerate(rawData):
        # col 1,4,7,... is  the exact value
        # col between (2 & 3, 5 & 6, ....)will be calculated linearly
        # index 0 -> get col 1,4 data and update col 1,2,3
        # index 1 -> get col 4,7 data and update col 4,5,6
        # index n -> get col n*3+1, (n+1)*3+1 data and update n*3+1 , n*3+2, n*3+3
        # if no n+1, meaning it is the last and no need to update n*3+2, n*3+3

        _value = int((value - min) / _step) # will floor the number
        if _value == size: # -1 if its the maximum value
            _value -= 1
        data[_value, index * 3 + 1] = color
        # check if this is last one -> no need to get the middle points
        if index == len(rawData) - 1:
            continue
        _mid_step = (rawData[index + 1] - value) / 3
        _mid_1 = int((value + _mid_step - min) / _step)
        _mid_2 = int((value + _mid_step * 2 - min) / _step)
        # midpoint would not be max
        data[_mid_1, index * 3 + 2] = color
        data[_mid_2, index * 3 + 3] = color

    return np.flip(data, 0)

# Function to generate daily volume barchart
def generate_daily_volume_chart(
        size: int,          # height of the bitmap
        min: float,         # the minimum value in that period (5d etc)
        max: float,         # the maximum value in that period (5d etc)
        v: float,           # open
        color = 255,
        bgColor = 0
    ) -> np.ndarray:
    # initize the data
    data = np.empty((size, 3), dtype=np.uint8)
    # background color
    data[:,:] = bgColor
    # calculation
    _step = (max - min) / size
    # no volume data
    if _step == 0:
        return data
    # drawing volume bar
    _volume = int((v - min) / _step) # will floor the number
    if (_volume != 0):
        data[0:_volume,1] = color

    # print(_step)
    # print(v)
    # print(_volume)

    return np.flip(data, 0)

# Function to generate a gap
def generate_gap(
        height: int,          # height of the bitmap
        width: int,          # height of the bitmap
        bgColor = 0
    ) -> np.ndarray:
    # initize the data
    data = np.empty((height, width), dtype=np.uint8)
    # background color
    data[:,:] = bgColor
    return data

# Function to generate one image data
def generate_image_data(
        dataset: pd.DataFrame,
        ohlc_height: int,
        volume_height: int, # set this to 0 if we don't want volume barchart
        gap_height: int, # set this to 0 if we don't want volume barchart
        include_ma_50d = False,
        include_ma_100d = False,
        include_ma_200d = False,
    ) -> np.ndarray:
    data = []
    _chart_min = float(dataset.min()['low'])
    _chart_max = float(dataset.max()['high'])
    # check ma's min max
    if include_ma_50d:
        _chart_min = min(_chart_min, float(dataset.min()['ma_50d']))
        _chart_max = max(_chart_max, float(dataset.max()['ma_50d']))
    if include_ma_100d:
        _chart_min = min(_chart_min, float(dataset.min()['ma_100d']))
        _chart_max = max(_chart_max, float(dataset.max()['ma_100d']))
    if include_ma_200d:
        _chart_min = min(_chart_min, float(dataset.min()['ma_200d']))
        _chart_max = max(_chart_max, float(dataset.max()['ma_200d']))
    for index, row in dataset.iterrows():
        _ohlc = generate_daily_ohlc_chart(
            ohlc_height,
            _chart_min,
            _chart_max,
            float(row['open']),
            float(row['high']),
            float(row['low']),
            float(row['close']),
        )
        if volume_height == 0:
            data.append(_ohlc)
        else:
            _gap = generate_gap(
                gap_height,
                3,
            )
            _volume = generate_daily_volume_chart(
                volume_height,
                0, # 0 or float(dataset.min()['volume'])
                float(dataset.max()['volume']),
                float(row['volume']),
            )
            _data = np.concatenate([_ohlc, _gap, _volume], axis=0)
            data.append(_data)

    imgData = np.concatenate(data, axis=1)

    # add 50d_ma
    if include_ma_50d:
        _ma_50d = generate_ma_chart(
            ohlc_height, # height
            _chart_min,
            _chart_max,
            dataset['ma_50d'].tolist()
        )
        _ma_gap = generate_gap(
            volume_height + gap_height,
            len(dataset.index) * 3
        )
        ma_50d_imgData = np.concatenate([_ma_50d, _ma_gap], axis=0)
        imgData = merge_image(imgData, ma_50d_imgData)

    # add 100d_ma
    if include_ma_100d:
        _ma_100d = generate_ma_chart(
            ohlc_height, # height
            _chart_min,
            _chart_max,
            dataset['ma_100d'].tolist()
        )
        _ma_gap = generate_gap(
            volume_height + gap_height,
            len(dataset.index) * 3
        )
        ma_100d_imgData = np.concatenate([_ma_100d, _ma_gap], axis=0)
        imgData = merge_image(imgData, ma_100d_imgData)

    # add 200d_ma
    if include_ma_200d:
        _ma_200d = generate_ma_chart(
            ohlc_height, # height
            _chart_min,
            _chart_max,
            dataset['ma_200d'].tolist()
        )
        _ma_gap = generate_gap(
            volume_height + gap_height,
            len(dataset.index) * 3
        )
        ma_200d_imgData = np.concatenate([_ma_200d, _ma_gap], axis=0)
        imgData = merge_image(imgData, ma_200d_imgData)
        
    return imgData

# Function to merge two image data
# if one of the pixel is 255 -> return 255
# if both pixel is 0 -> return 0
def merge_image(
        x: np.ndarray,
        y: np.ndarray,
    ):
    if (x.shape != y.shape):
        raise Exception(f'Array shape not match: {x.shape} / {y.shape}')
    return (x + y).astype('bool').astype(np.uint8) * 255
    # def array_merge(a, b):
    #     return 255 if a == 255 or b == 255 else 0
    # array_merge = np.frompyfunc(array_merge, 2, 1)
    # out = array_merge(x, y) as np
    # out = 
    # return out

