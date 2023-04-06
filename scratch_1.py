# Import required libraries
from collections import defaultdict
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


# Function to generate frequent itemsets of size 1
def generate_candidates_1(itemsets, min_support):
    candidate_counts = defaultdict(int)
    for itemset in itemsets:
        for item in itemset:
            candidate_counts[item] += 1

    frequent_items = []
    for item, count in candidate_counts.items():
        if count >= min_support:
            frequent_items.append(frozenset([item]))

    return frequent_items


# Function to join two sets of frequent itemsets
def join_sets(itemsets):
    new_itemsets = []
    for i, itemset1 in enumerate(itemsets):
        for itemset2 in itemsets[i + 1:]:
            new_itemset = itemset1.union(itemset2)
            new_itemsets.append(new_itemset)
    return new_itemsets


# Function to prune infrequent itemsets
def prune_sets(itemsets, frequent_sets):
    pruned_itemsets = []
    for itemset in itemsets:
        for subset in itemset:
            if frozenset([subset]) not in frequent_sets:
                break
        else:
            pruned_itemsets.append(itemset)
    return pruned_itemsets


# Function to generate frequent itemsets of size k from frequent itemsets of size k-1
def generate_candidates_k(frequent_sets, k):
    joined_sets = join_sets(frequent_sets)
    return prune_sets(joined_sets, frequent_sets)


# Function to generate all frequent itemsets using the Apriori algorithm
def apriori(itemsets, min_support):
    frequent_sets = []
    candidates = generate_candidates_1(itemsets, min_support)
    k = 2
    while candidates:
        frequent_itemsets = []
        candidate_counts = defaultdict(int)
        for itemset in itemsets:
            for candidate in candidates:
                if candidate.issubset(itemset):
                    candidate_counts[candidate] += 1
        for candidate, count in candidate_counts.items():
            if count >= min_support:
                frequent_itemsets.append(candidate)
        if frequent_itemsets:
            frequent_sets.append(frequent_itemsets)
            candidates = generate_candidates_k(frequent_sets[-1], k)
            k += 1
        else:
            break
    return frequent_sets


# df = loadfile()
# itemsets = process_transactions(df)
# frequent_itemsets = apriori(itemsets, 0.15)
#
# # Print the frequent itemsets
# for i, itemsets in enumerate(frequent_itemsets):
#     print(f"Frequent itemsets of size {i+1}:")
#     for itemset in itemsets:
#         print(list(itemset))


# -------------------------------------------------------------------------------

def main():
    df = load_file()
    itemsets = process_transactions(df)
    frequent_itemsets = apriori(itemsets, 0.15)

    # Print the frequent itemsets
    for i, itemsets in enumerate(frequent_itemsets):
        print(f"Frequent itemsets of size {i + 1}:")
        for itemset in itemsets:
            print(list(itemset))


# -------------------------------------------------------------------------------

if __name__ == '__main__':
    # cProfile.run('main()', sort='calls')
    main()