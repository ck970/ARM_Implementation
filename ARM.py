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
        if item in str(row):
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

def generate_frequent_itemsets_size_two_join(products, arr_sets, min_support):
    frequent_sets_size_two = set()
    item_set = set()
    num_remaining_frequent_items = len(products)
    current_index = 0
    for item in products:
        for i in range(num_remaining_frequent_items - current_index):
            item_set = arr_sets[current_index].union(products[current_index+i])
            item_set_support = get_support(arr_sets, length, item_set)
            if item_set_support >= min_support:
                frequent_sets_size_two.add(item_set)
        current_index += 1
        num_remaining_frequent_items -= 1
    return frequent_sets_size_two

# -------------------------------------------------------------------------------

def main():
    df = load_file()
    columns = list(df.columns)
    arr_sets = process_transactions(df)
    item_sets = generate_frequent_itemsets_size_one(columns, arr_sets, min_support)
    item_sets = generate_frequent_itemsets_size_two_join(item_sets, arr_sets, min_support)
    print(item_sets)

# -------------------------------------------------------------------------------

if __name__ == '__main__':
    # cProfile.run('main()', sort='calls')
    main()