length = len(arr_sets)
    min_support = 0.15
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

# -------------------------------------------------------------------------------