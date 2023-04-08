import pandas as pd
import numpy as np
from itertools import combinations
from scipy.io.arff import loadarff
from collections import defaultdict
import cProfile

data, meta = loadarff('basket.arff')
df = pd.DataFrame(data)
i = 0
for dtype in df.dtypes:
    df[df.columns[i]] = df[df.columns[i]].str.decode("utf-8")
    i += 1

item_list = list(df.columns)
item_dict = dict()
for i, item in enumerate(item_list):
    item_dict[item] = i + 1

transactions = list()

for i, row in df.iterrows():
    transaction = set()
    for item in item_dict:
        if row[item] == '1':
            transaction.add(item_dict[item])
    transactions.append(transaction)

def get_support(transactions, item_set):
    match_count = 0
    # print(item_set)
    for transaction in transactions:
        # print(transaction)
        if item_set.issubset(transaction):
            match_count += 1

    return float(match_count / len(transactions))


def self_join(frequent_item_sets_per_level, level):
    current_level_candidates = list()
    last_level_items = frequent_item_sets_per_level[level - 1]
    # print(type(last_level_items))

    if len(last_level_items) == 0:
        return current_level_candidates

    for i in range(len(last_level_items)):
        for j in range(i + 1, len(last_level_items)):
            itemset_i = last_level_items[i][0]
            itemset_j = last_level_items[j][0]
            union_set = itemset_i.union(itemset_j)

            if union_set not in current_level_candidates and len(union_set) == level:
                current_level_candidates.append(union_set)

    return current_level_candidates


def get_single_drop_subsets(item_set):
    single_drop_subsets = list()
    for item in item_set:
        temp = item_set.copy()
        temp.remove(item)
        single_drop_subsets.append(temp)

    return single_drop_subsets


def is_valid_set(item_set, prev_level_sets):
    single_drop_subsets = get_single_drop_subsets(item_set)

    for single_drop_set in single_drop_subsets:
        if single_drop_set not in prev_level_sets:
            return False
    return True


def pruning(frequent_item_sets_per_level, level, candidate_set):
    post_pruning_set = list()
    if len(candidate_set) == 0:
        return post_pruning_set

    prev_level_sets = list()
    for item_set, _ in frequent_item_sets_per_level[level - 1]:
        prev_level_sets.append(item_set)

    for item_set in candidate_set:
        if is_valid_set(item_set, prev_level_sets):
            post_pruning_set.append(item_set)

    return post_pruning_set


def apriori(min_support):
    frequent_item_sets_per_level = defaultdict(list)
    # print(type(frequent_item_sets_per_level))
    print("level : 1", end=" ")

    for item in range(1, len(item_list) + 1):
        # print(type({item}))
        support = get_support(transactions, {item})
        if support >= min_support:
            frequent_item_sets_per_level[1].append(({item}, support))
    # print(frequent_item_sets_per_level)

    for level in range(2, len(item_list) + 1):
        print(level, end=" ")
        current_level_candidates = self_join(frequent_item_sets_per_level, level)

        post_pruning_candidates = pruning(frequent_item_sets_per_level, level, current_level_candidates)
        if len(post_pruning_candidates) == 0:

            break

        for item_set in post_pruning_candidates:
            support = get_support(transactions, item_set)
            if support >= min_support:
                frequent_item_sets_per_level[level].append((item_set, support))

    return frequent_item_sets_per_level

def main():

    min_support = 0.15
    frequent_item_sets_per_level = apriori(min_support)
    print("\n")
    for level in frequent_item_sets_per_level:
        print(len(frequent_item_sets_per_level[level]))
        # print(frequent_item_sets_per_level[level])
    print("\n\n")

if __name__ == '__main__':
    cProfile.run('main()', sort='time')

# item_support_dict = dict()
# item_list = list()
#
# key_list = list(item_dict.keys())
# val_list = list(item_dict.values())
#
# for level in frequent_item_sets_per_level:
#     for set_support_pair in frequent_item_sets_per_level[level]:
#         for i in set_support_pair[0]:
#             item_list.append(key_list[val_list.index(i)])
#         item_support_dict[frozenset(item_list)] = set_support_pair[1]
#         item_list = list()
#
# def find_subset(item, item_length):
#     combs = []
#     for i in range(1, item_length + 1):
#         combs.append(list(combinations(item, i)))
#
#     subsets = []
#     for comb in combs:
#         for elt in comb:
#             subsets.append(elt)
#
#     return subsets
#
#
# def association_rules(min_confidence, support_dict):
#     rules = list()
#     for item, support in support_dict.items():
#         item_length = len(item)
#
#         if item_length > 1:
#             subsets = find_subset(item, item_length)
#
#             for A in subsets:
#                 B = item.difference(A)
#
#                 if B:
#                     A = frozenset(A)
#
#                     AB = A | B
#
#                     confidence = support_dict[AB] / support_dict[A]
#                     if confidence >= min_confidence:
#                         rules.append((A, B, confidence))
#
#     return rules
#
# association_rules = association_rules(min_confidence = 0.5, support_dict = item_support_dict)
#
# print("Number of rules: ", len(association_rules), "\n")
#
# for rule in association_rules:
#     print('{0} -> {1} <confidence: {2}>'.format(set(rule[0]), set(rule[1]), rule[2]))
