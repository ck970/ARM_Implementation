from scipy.io.arff import loadarff
import pandas as pd
import numpy as np
import cProfile
from collections import defaultdict
from itertools import combinations

'''
SUMMARY:
This project takes basket.arff file as input and generates association rules 
for grocery store products based upon whether or not the product was present
in a given transaction. 

EVALUATION CRITERIA:
    - MINIMUM SUPPORT: 0.15
    - MINIMUM CONFIDENCE: 0.6
    - MINIMUM LIFT: 1
'''


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
    """
    :param arr_sets: list of sets where each set only contains those columns present in
    transaction row represents
    :param length: length of arr_sets
    :param item: individual product (MaxwellHouseRegularGroundCoffee, BrewRiteConeStyleCoffeeFilters, etc.)
    :return: support of that product
    """
    count = 0
    for row in arr_sets:
        if item <= row:
            count += 1
    return float(count/length)

# -------------------------------------------------------------------------------

def join_step(remaining_frequent_sets, k):
    """
    :param remaining_frequent_sets: list of all frequent itemsets of length k
    :param k: iterable, starts at 1, counts length of itemsets in a given iteration
    :return: new frequent itemsets of length k
    """
    k_frequent_sets = list()
    k_minus_one_frequent_items = remaining_frequent_sets[k - 1]

    # If there are no frequent itemsets of length k-1, then there are no frequent itemsets of length k
    if len(k_minus_one_frequent_items) == 0:
        return k_frequent_sets

    # Iterate through all pairs of frequent itemsets of length k-1,
    # and join them if they are not already in k_frequent_sets
    for i in range(len(k_minus_one_frequent_items)):
        for j in range(i + 1, len(k_minus_one_frequent_items)):
            union_i_j = k_minus_one_frequent_items[i][0].union(k_minus_one_frequent_items[j][0])
            if (union_i_j not in k_frequent_sets and
                    (len(union_i_j) == k)):
                k_frequent_sets.append(union_i_j)
    return k_frequent_sets

# -------------------------------------------------------------------------------

def prune_check(set, k_minus_one_frequent_sets):
    """
    :param set: given frequent itemset of length k from k_frequent_sets
    :param k_minus_one_frequent_sets: list of all frequent itemsets of length k-1
    :return: boolean which is 'True' if the itemset does not need to be pruned, and 'False' otherwise
    """
    valid_candidate = True
    for item in set:
        set_minus_item = set - {item}
        if set_minus_item not in k_minus_one_frequent_sets:
            valid_candidate = False
    return valid_candidate

# -------------------------------------------------------------------------------

def prune_step(remaining_frequent_sets, k_frequent_sets, k):
    """
    :param remaining_frequent_sets: list of all frequent itemsets of length k
    :param k_frequent_sets: list of all frequent itemsets of length k
    :param k: iterable, starts at 1, counts length of itemsets in a given iteration
    :return: pruned list of all frequent itemsets of length k
    """
    counter = 0
    k_frequent_sets_pruned = list()
    if len(k_frequent_sets) == 0:
        return k_frequent_sets_pruned

    k_minus_one_frequent_sets = list()
    for sets, na in remaining_frequent_sets[k - 1]:
        k_minus_one_frequent_sets.append(sets)

    for set in k_frequent_sets:
        if prune_check(set, k_minus_one_frequent_sets):
            k_frequent_sets_pruned.append(set)
    return k_frequent_sets_pruned

# -------------------------------------------------------------------------------

def apriori(min_support):
    """
    :param min_support: minimum support threshold
    :return: number of reamining frequent itemsets of length k, indexed by k
    :return: dictionary of all products and their corresponding index
    """
    df = load_file()
    columns = list(df.columns)
    arr_sets = process_transactions(df)
    arr_sets_dict = dict()

    for index, item in enumerate(columns):
        arr_sets_dict[item] = index + 1

    length = len(arr_sets)
    # Used defaultdict here to avoid key errors, was only solution I could find that actually worked:
    num_remaining_frequent_sets = defaultdict(list)

    for product in columns:
        support = get_support(arr_sets, length, {product})
        if support >= min_support:
            num_remaining_frequent_sets[1].append(({product}, support))

    for k in range(2, len(columns) + 1):
        k_frequent_sets = join_step(num_remaining_frequent_sets, k)
        k_frequent_sets_pruned = prune_step(num_remaining_frequent_sets, k_frequent_sets, k)
        if len(k_frequent_sets_pruned) == 0:
            break

        for set in k_frequent_sets_pruned:
            support = get_support(arr_sets, length, set)
            if support >= min_support:
                num_remaining_frequent_sets[k].append((set, support))
    return num_remaining_frequent_sets, arr_sets_dict

# -------------------------------------------------------------------------------

def generate_all_subsets(set):
    """
    :param set: given set of products
    :return: list of all subsets of the given set
    """
    subsets = []
    possible_combinations = []

    if len(set) > 1:
        for i in range(1, len(set) + 1):
            possible_combinations.append(list(combinations(set, i)))
        for combination in possible_combinations:
            for item in combination:
                subsets.append(item)
    else:
        subsets.append(set)
    return subsets

# -------------------------------------------------------------------------------

def generate_association_rules(remaining_frequent_sets, arr_sets_dict, min_confidence):
    """
    :param remaining_frequent_sets: list of all frequent itemsets with their support, indexed by length k
    :param arr_sets_dict: dictionary of all products and their corresponding index
    :param min_confidence: minimum confidence threshold
    :return: list of all association rules with their antecedent, consequent, confidence, length k, and lift
    """
    temp_list = []
    association_rules = []
    # Store all frequent itemsets with their support:
    rfs_dict = dict()

    item_list = list(arr_sets_dict.keys())
    index_list = list(arr_sets_dict.values())

    for k in remaining_frequent_sets:
        for itemset in remaining_frequent_sets[k]:
            for item in itemset[0]:
                temp_list.append(item)
            rfs_dict[frozenset(temp_list)] = itemset[1]
            temp_list = []

    for item, support in rfs_dict.items():
        length = len(item)
        if length > 1:
                subsets = generate_all_subsets(item)
                for antecedent in subsets:
                    consequent = item.difference(antecedent)
                    consequent = frozenset(consequent)

                    if consequent in rfs_dict:
                        antecedent = frozenset(antecedent)
                        union_antecedent_consequent = antecedent.union(consequent)
                        length_rule = len(union_antecedent_consequent)

                        confidence = rfs_dict[union_antecedent_consequent] / rfs_dict[antecedent]
                        lift = confidence / rfs_dict[consequent]

                        if confidence >= min_confidence and lift >= 1:
                            association_rules.append((antecedent, consequent, confidence, lift, length_rule))
    return association_rules

# -------------------------------------------------------------------------------

def print_rules(association_rules, largest_k, num_best_rules):
    """
    :param association_rules: list of all association rules that meet the minimum confidence and lift threshold
    :param largest_k: largest k for which there are frequent itemsets
    :param num_best_rules: number of rules to print (15)
    :return: None
    """
    num_largest_k_rules = 0
    best_rules = []
    temp_best_rules = []

    print("------------------------------------\n")

    for rule in association_rules:
        if rule[4] == largest_k:
            num_largest_k_rules += 1
    print("Number of association rules for largest K-frequent itemsets: " + str(num_largest_k_rules))
    print("\n")

    print("------------------------------------\n")

    print("Best association rules found based on Confidence: \n")
    for i, entry in enumerate(sorted(association_rules, key=lambda x: x[2], reverse=True)[:15]):
        print("Rule: " + str(list(entry[0])) + " -> " + str(list(entry[1])))
        print("Confidence: " + str(entry[2]))
        print("Lift: " + str(entry[3]) + "\n")
    print("\n")

    print("------------------------------------\n")

    print("Best association rules found based on Lift: \n")
    for i, entry in enumerate(sorted(association_rules, key=lambda x: x[3], reverse=True)[:15]):
        print("Rule: " + str(list(entry[0])) + " -> " + str(list(entry[1])))
        print("Confidence: " + str(entry[2]))
        print("Lift: " + str(entry[3]) + "\n")
    print("\n")

# -------------------------------------------------------------------------------

def main():
    min_support = 0.15
    print("\nMinimum support: " + str(min_support))
    min_confidence = 0.6
    print("Minimum confidence: " + str(min_confidence))
    # Number of rules to print:
    num_best_rules = 15
    print("\n------------------------------------\n")

    remaining_frequent_sets, rfs_dict = apriori(min_support)
    largest_k = max(remaining_frequent_sets.keys())
    for k in remaining_frequent_sets:
        print("K = " + str(k))
        print("Number of frequent itemsets: " + str(len(remaining_frequent_sets[k])))
        print("\n")
    association_rules = generate_association_rules(remaining_frequent_sets, rfs_dict, min_confidence)
    print_rules(association_rules, largest_k, num_best_rules)

# -------------------------------------------------------------------------------

if __name__ == '__main__':
    # cProfile.run('main()', sort='time')
    main()
