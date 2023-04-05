from scipy.io import arff
from scipy.io.arff import loadarff
import pandas as pd
import numpy as np
import itertools
import time

def load_file():
    data, meta = loadarff('basket.arff')
    df = pd.DataFrame(data)
    i = 0
    for dtype in df.dtypes:
        df[df.columns[i]] = df[df.columns[i]].str.decode("utf-8")
        i += 1
    return df

# -------------------------------------------------------------------------------

def transform_df_arr_hash(df):
    arr_hash = df.to_dict('records')
    return arr_hash

# -------------------------------------------------------------------------------

def transform_dict_to_set(dict_vals_0_1):
    return set(key for key, val in dict_vals_0_1.items() if val == '1')

# -------------------------------------------------------------------------------

def transform_ah_to_arr_sets(arr_hash):
    return [transform_dict_to_set(dict_0_1) for dict_0_1 in arr_hash]

# -------------------------------------------------------------------------------

def get_support(arr_sets, length, item):
    count = 0
    for row in arr_sets:
        # print(row)
        if item<=row:
            count += 1
    return count/length

# -------------------------------------------------------------------------------

# def get_confidence(arr_sets, item_a, item_b):
#     count = 0
#     return

# -------------------------------------------------------------------------------

# def get_lift(arr_sets, item_a, item_b):
#     return get_confidence(arr_sets, item_a, item_b) / get_support(arr_sets, item_b)

# -------------------------------------------------------------------------------


# -------------------------------------------------------------------------------

def main():
    df = load_file()
    arr_hash = transform_df_arr_hash(df)
    arr_sets = transform_ah_to_arr_sets(arr_hash)
    arr_sets = sorted(arr_sets)
    


# -------------------------------------------------------------------------------

if __name__ == '__main__':
    main()
