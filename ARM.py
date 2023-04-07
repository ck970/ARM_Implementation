from scipy.io.arff import loadarff
import pandas as pd
import numpy as np
import cProfile

min_support = 0.15
min_confidence = 0.5
length = 4000


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
    # NEED TO SEE IF THERE IS A FASTER WAY TO EXECUTE LINES 14-16
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

# def generate_frequent_itemsets_size_one(columns, arr_sets, min_support):
#     frequent_sets_size_one = set()
#     # length = len(arr_sets)
#     for item in columns:
#         item_support = get_support(arr_sets, length, item)
#         # print(str(item) + "'s Support: " + str(item_support))
#         if item_support >= min_support:
#             frequent_sets_size_one.add(item)
#     return frequent_sets_size_one

# -------------------------------------------------------------------------------

def join_step(num_remaining_frequent_sets, arr_sets):
    k_frequent_sets = set()
    k_minus_one_frequent_items = num_remaining_frequent_sets[k - 1]
    for i in range(len(k_minus_one_frequent_items)):
        for j in range(i + 1, len(k_minus_one_frequent_items)):
            if (k_minus_one_frequent_items[i] & k_minus_one_frequent_items[j] not in k_frequent_sets and
                    (k_minus_one_frequent_items[i] & k_minus_one_frequent_items[j]) == k - 2):
                k_frequent_sets.add(k_minus_one_frequent_items[i] & k_minus_one_frequent_items[j])
    return k_frequent_sets

# -------------------------------------------------------------------------------

# def prune_step(k_frequent_sets, arr_sets, min_support):
#     k_frequent_sets_pruned = set()
#     for item in k_frequent_sets:
#         item_support = get_support(arr_sets, length, item)
#         if item_support >= min_support:
#             k_frequent_sets_pruned.add(item)
#     return k_frequent_sets_pruned

# -------------------------------------------------------------------------------

def main():
    df = load_file()
    columns = list(df.columns)
    arr_sets = process_transactions(df)
    item_sets = join_step(arr_sets)
    print(item_sets)

# -------------------------------------------------------------------------------

if __name__ == '__main__':
    # cProfile.run('main()', sort='calls')
    main()