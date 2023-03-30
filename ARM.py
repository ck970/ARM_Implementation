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

def main():
    df = load_file()
    arr_hash = transform_df_arr_hash(df)
    arr_sets = transform_ah_to_arr_sets(arr_hash)
    arr_sets = sorted(arr_sets)
    length = len(arr_sets)
    min_support = 0.3
    count = 0
    frequent_items = []
    for i in range(len(df.columns)):
        support = get_support(arr_sets, length, {df.columns[i]})
        if support >= min_support:
            frequent_items.append(df.columns[i])
            # print(str(df.columns[i]) + ": " + str(support))
            count += 1
            # print("\n")
    print("Number of frequent itemsets: " + str(count))
    print("\n\n")
    count = 0
    frequent_pairs = []
    for i in range(len(frequent_items)):
        for j in range(i+1, len(frequent_items)):
            support = get_support(arr_sets, length, {frequent_items[i], frequent_items[j]})
            if support >= min_support:
                if {frequent_items[i], frequent_items[j]} not in frequent_pairs and \
                        {frequent_items[j], frequent_items[i]} not in frequent_pairs:
                    frequent_pairs.append({frequent_items[i], frequent_items[j]})
                    # print(str(frequent_items[i]) + ", " + str(frequent_items[j]) + ": " + str(support))
                    count+=1
                    # print("\n")
    print("Number of frequent itemsets: " + str(count))
    print("\n\n")
    count = 0
    frequent_triples = []
    index = 0
    for i in range(len(frequent_pairs)):
        for item in frequent_items:
            if item not in frequent_pairs[i]:
                support = get_support(arr_sets, length, frequent_pairs[i].union({item}))
                if support >= min_support:
                    if frequent_pairs[i].union({item}) not in frequent_triples:
                        frequent_triples.append(frequent_pairs[i].union({item}))
                        # print(str(frequent_triples[index]) + ": " + str(support))
                        # print("Here")
                        # print("\n")
                        count+=1
                        index+=1
    # print(frequent_items)
    # print("\n")
    # print(frequent_pairs)
    # print("\n")
    # print(frequent_triples)
    # print("\n")
    print("Number of frequent itemsets: " + str(count))
    print("\n\n")



# -------------------------------------------------------------------------------

if __name__ == '__main__':
    main()
