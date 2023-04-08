from scipy.io.arff import loadarff
import pandas as pd
import numpy as np
import cProfile
from collections import defaultdict


def load_file():
    '''
    :return: df that is of the same form of past dfs after you use loadarff
    '''
    data, meta = loadarff('basket.arff')
    df = pd.DataFrame(data)
    i = 0
    for dtype in df.dtypes:
        df[df.columns[i]] = df[df.columns[i]].str.decode("utf-8")
        i += 1
    return df

# -------------------------------------------------------------------------------

def transform_df_arr_hash(df):
    '''
    :param df: your df
    :return: the df expressed as an array of hash maps or technically in python
    list of dicts
    '''
    arr_hash = df.to_dict('records')
    return arr_hash

# -------------------------------------------------------------------------------

def transform_dict_to_set(dict_vals_0_1):
    '''
    :param dict_vals_0_1: dictionary where the values are 0 and 1 corresponding to
    if key is present
    :return: set of only those cols that are 'present'
    '''
    return set(key for key, val in dict_vals_0_1.items() if val == '1')

# -------------------------------------------------------------------------------

def transform_ah_to_arr_sets(arr_hash):
    '''
    :param arr_hash: the list of dicts returned from transform_df_arr_hash
    :return: a list of sets where each set only contains those columns present in
    transaction row represents
    '''
    return [transform_dict_to_set(dict_0_1) for dict_0_1 in arr_hash]

# -------------------------------------------------------------------------------

def process_transactions(df):
    '''
    :param df: your df
    :return: a list of sets where each set only contains those columns present in
    transaction row represents
    '''
    arr_hash = transform_df_arr_hash(df)
    arr_sets = transform_ah_to_arr_sets(arr_hash)
    return sorted(arr_sets)

# -------------------------------------------------------------------------------

def get_support(arr_sets, length, item):
    count = 0
    for row in arr_sets:
        if {item} <= row:
            count += 1
    return float(count/length)

# -------------------------------------------------------------------------------

def join_step(num_remaining_frequent_sets, k):
    k_frequent_sets = set()
    k_minus_one_frequent_items = num_remaining_frequent_sets[k - 1]
    for i in range(len(k_minus_one_frequent_items)):
        for j in range(i + 1, len(k_minus_one_frequent_items)):
            if (k_minus_one_frequent_items[i] & k_minus_one_frequent_items[j] not in k_frequent_sets and
                    (k_minus_one_frequent_items[i] & k_minus_one_frequent_items[j]) == k - 2):
                k_frequent_sets.add(k_minus_one_frequent_items[i] & k_minus_one_frequent_items[j])

    return k_frequent_sets

# -------------------------------------------------------------------------------

def prune_step(num_remaining_frequent_sets, k_frequent_sets, k):
    k_frequent_sets_pruned = list()
    if len(k_frequent_sets) == 0:
        return k_frequent_sets_pruned
    k_minus_one_frequent_sets = set()
    for sets in num_remaining_frequent_sets[k - 1]:
        k_minus_one_frequent_sets.add(sets)
    for set in k_frequent_sets:
        for item in set:
            set_minus_item = set - {item}
            if set_minus_item not in k_minus_one_frequent_sets:
                break
        else:
            k_frequent_sets_pruned.add(set)
    return k_frequent_sets_pruned

# -------------------------------------------------------------------------------

def apriori(min_support):
    df = load_file()
    columns = list(df.columns)
    arr_sets = process_transactions(df)
    length = len(arr_sets)
    num_remaining_frequent_sets = defaultdict(list)
    print("K = 1\n")
    for product in range(1, len(columns) + 1):
        support = get_support(arr_sets, length, product)
        if support >= min_support:
            num_remaining_frequent_sets[1].append({product})
    for k in range(2, len(columns) + 1):
        print("K = " + str(k) + "\n")
        k_frequent_sets = join_step(num_remaining_frequent_sets, k)
        k_frequent_sets_pruned = prune_step(num_remaining_frequent_sets, k_frequent_sets, k)
        if len(k_frequent_sets_pruned) == 0:
            break
        for set in k_frequent_sets_pruned:
            support = get_support(arr_sets, length, set)
            if support >= min_support:
                num_remaining_frequent_sets[k].append({set})
    return num_remaining_frequent_sets

# -------------------------------------------------------------------------------

def main():
    min_support = 0.15
    num_remaining_frequent_sets = apriori(min_support)
    for k in num_remaining_frequent_sets:
        print(len(num_remaining_frequent_sets[k]))
    # df = load_file()
    # columns = list(df.columns)
    # arr_sets = process_transactions(df)
    # item_sets = join_step(arr_sets)
    # print(item_sets)

# -------------------------------------------------------------------------------

if __name__ == '__main__':
    # cProfile.run('main()', sort='calls')
    main()