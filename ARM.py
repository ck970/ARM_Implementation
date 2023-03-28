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

# -----------------------------

def transform_df_arr_hash(df):
    arr_hash = df.to_dict('records')
    return arr_hash

# -----------------------------

def transform_dict_to_set(dict_vals_0_1):
    return set(key for key, val in dict_vals_0_1.items() if val == '1')

# -----------------------------

def transform_ah_to_arr_sets(arr_hash):
    return [transform_dict_to_set(dict_0_1) for dict_0_1 in arr_hash]

# -----------------------------

def get_support(arr_sets, item):
    count = 0
    for row in arr_sets:
        if item.issubset(row):
            count += 1
    return count

# -----------------------------

def get_confidence(arr_sets, item_a, item_b):
    count = 0
    for row in arr_sets:
        if item_a.issubset(row) and item_b.issubset(row):
            count += 1
    return count / get_support(arr_sets, item_a)

# -----------------------------

def get_lift(arr_sets, item_a, item_b):
    return get_confidence(arr_sets, item_a, item_b) / get_support(arr_sets, item_b)

# -----------------------------

def get_candidates(items, k):
    candidates = set()
    for item_a in items:
        for item_b in items:
            if len(item_a.union(item_b)) == k:
                candidates.add(item_a.union(item_b))
    return candidates

# -----------------------------

def apriori(arr_sets, min_support):
    items = set()
    for row in arr_sets:
        for item in row:
            items.add(frozenset([item]))
    k = 2
    while len(items) > 0:
        items = get_candidates(items, k)
        items = set([item for item in items if get_support(arr_sets, item) >= min_support])
        k += 1
    return items

# -----------------------------

def get_association_rules(arr_sets, min_confidence, min_lift, min_support):
    items = apriori(arr_sets, min_support)
    rules = []
    for item in items:
        for i in range(1, len(item)):
            for subset in itertools.combinations(item, i):
                subset = frozenset(subset)
                if get_confidence(arr_sets, subset, item - subset) >= min_confidence and \
                        get_lift(arr_sets, subset, item - subset) >= min_lift and \
                        get_support(arr_sets, subset) >= min_support:
                    rules.append((subset, item - subset))
    return rules
# -----------------------------

def main():
    df = load_file()
    arr_hash = transform_df_arr_hash(df)
    arr_sets = transform_ah_to_arr_sets(arr_hash)
    rules = get_association_rules(arr_sets, 0.5, 1, 10)
    print(rules)

# -----------------------------

if __name__ == '__main__':
    main()
