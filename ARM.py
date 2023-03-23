from scipy.io import arff
from scipy.io.arff import loadarff
import pandas as pd
import numpy as np
import itertools
import time

def create_ex_df():
    '''
    :return: df that is of the same form of your df after you use loadarff
    '''
    products_data, products_meta = loadarff('basket.arff')
    columns = ['col{}'.format(i+1) for i in range(10)]

    df = pd.DataFrame(data, columns=columns)

    return df

def transform_df_arr_hash(df):
    '''
    :param df: your df
    :return: the df expressed as an array of hash maps or technically in python list of dicts
    '''
    arr_hash = df.to_dict('records')

    return arr_hash

def transform_dict_to_set(dict_vals_0_1):
    '''
    :param dict_vals_0_1: dictionary where the values are 0 and 1 corresponding to if key is present
    :return: set of only those cols that are 'present'
    '''
    return set(key for key, val in dict_vals_0_1.items() if val == 1)

def transform_ah_to_arr_sets(arr_hash):
    '''
    :param arr_hash: the list of dicts returned from transform_df_arr_hash
    :return: a list of sets where each set only contains those columns present in transaction row represents
    '''
    return [transform_dict_to_set(dict_0_1) for dict_0_1 in arr_hash]

def a_subset_b(set_a, set_b):
    '''
    :param set_a: the set that we want to see if it is a subset of set b
    :param set_b: see above
    :return: true if set_a is a subset of set_b, false otherwise
    '''

    # issubset can either be performed via explicit call or <= shorthand
    temp_1 = set_a.issubset(set_b)
    temp_2 = (set_a <= set_b)

    return temp_1


def main():
    ex_df = create_ex_df()
    arr_hash = transform_df_arr_hash(ex_df)
    arr_sets = transform_ah_to_arr_sets(arr_hash)
    print(arr_sets)

    a_subset_b({1,2}, {1,2,3})
    a_subset_b({1, 4}, {1, 2, 3})


if __name__ == '__main__':
    main()
