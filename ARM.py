from scipy.io.arff import loadarff
import pandas as pd
import numpy as np
import cProfile


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
        if item<=row:
            count += 1
    return count/length

# -------------------------------------------------------------------------------

def apriori_join(arr_sets, length, k, min_support):
    # Join frequent itemsets of size k-1 to create candidate itemsets of size k.
    # Returns a list of candidate itemsets of size k.
    for i in arr_sets:
        if len(i) != k-1:
            raise ValueError('Invalid itemset size.')
    candidate_itemsets = []
    for i in range(length):
        for j in range(i+1, length):
            itemset1 = arr_sets[i]
            itemset2 = arr_sets[j]
            if list(itemset1)[:k-2] == list(itemset2)[:k-2]:
                candidate_itemset = itemset1.union(itemset2)
                if candidate_itemset not in candidate_itemsets:
                    candidate_itemsets.append(candidate_itemset)
    return candidate_itemsets

# -------------------------------------------------------------------------------
def apriori_prune(arr_sets, length, k, min_support):
    # Prunes candidate itemsets that contain subsets of size k-1 that are not frequent.
    candidate_itemsets = []
    for i in range(length):
        for j in range(i+1, length):
            itemset1 = arr_sets[i]
            itemset2 = arr_sets[j]
            if list(itemset1)[:k-2] == list(itemset2)[:k-2]:
                candidate_itemset = itemset1.union(itemset2)
                if candidate_itemset not in candidate_itemsets:
                    candidate_itemsets.append(candidate_itemset)
    return candidate_itemsets\

# -------------------------------------------------------------------------------

def apriori(arr_sets, min_support):
    # Returns a list of all frequent itemsets.
    frequent_itemsets = []
    length = len(arr_sets)
    k = 1
    while True:
        candidate_itemsets = apriori_join(arr_sets, length, k, min_support)
        if not candidate_itemsets:
            break
        for candidate_itemset in candidate_itemsets:
            support = get_support(arr_sets, length, candidate_itemset)
            if support >= min_support:
                frequent_itemsets.append(candidate_itemset)
        k += 1
    return frequent_itemsets

# -------------------------------------------------------------------------------

def main():
    df = load_file()
    arr_sets = process_transactions(df)
    frequent_itemsets = apriori(arr_sets, 0.1)
    print(frequent_itemsets)

# -------------------------------------------------------------------------------

if __name__ == '__main__':
    # cProfile.run('main()', sort='calls')
    main()