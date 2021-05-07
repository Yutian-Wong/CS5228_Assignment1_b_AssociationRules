# -*- coding: utf-8 -*-
"""
Created on Fri May  7 15:24:44 2021

@author: Wang Yutian

Association Rules and Apriori Algorithm
"""

import numpy as np
import pandas as pd
from datetime import datetime


from efficient_apriori import apriori

from utils import powerset, binary_split

#Two methods of utils module will be used in this file: powerset() and binary_split()
"""
powerset():
Given a set of items, powerset() returns all possible subset of items with a 
specified minimum and maximum length. For example, you can use this method to 
generate all itemsets for a transaction.
"""

for subset in powerset(('c', 'b', 'a'), min_len=1, max_len=3):
    print(subset)

"""
binary_split():
Given a set of items, binary_split() return all combinations of how the input 
set can be split into 2 non-empty subsets (where the union of both subsets for 
the input set). It's easy to see that you can use this to get from an itemset
to all possible association rules.
"""

for X, Y in binary_split(('b','c','a')):
    print('{} => {}'.format(X, Y))


#Sample Dataset
transactions_demo = [
    ('bread', 'yogurt'),
    ('bread', 'milk', 'cereal', 'eggs'),
    ('yogurt', 'milk', 'cereal', 'cheese'),
    ('bread', 'yogurt', 'milk', 'cereal'),
    ('bread', 'yogurt', 'milk', 'cheese')
]


"""
Frequent Itemset Generation

Implement the brute force approach for Frequent Itemset Generation -- 
i.e., generate all possible itemsets for each transaction and calculate the 
overall support -- using the template for method find_frequent_itemsets() below. 
The expected format of the output is given in the comments below. 
The auxiliary method powerset() should help for this task.
"""
def find_frequent_itemsets(transactions, minsup):
    
    num_transactions = len(transactions)
    
    #########################################################################################
    # Step 1: Count the number of occurences of all possible itemset
    #########################################################################################

    # Create a dictionary to keep track of the support counts for each itemset
    # e.g., support_counts = {(a,): 4, (b,): 20, (c,): 5, (a, c): 2, ...}
    support_counts = {}
    
    for transaction in transactions:
        for subset in powerset(transaction, min_len=1, max_len=len(transaction)):
            support_counts[subset] = support_counts[subset] + 1 if subset in support_counts else 1
                    
                
    #########################################################################################
    # Step 2: Filter all itemset with a support >= minsup ==> frequent item sets
    #########################################################################################
    
    # In the end, frequent_itemsets as dictionary (key = itemset, value = support)
    # e.g., frequent_itemsets = {(a,): 0.8, (b,): 0.6, (c,): 0.8, (a, c): 0.4, ...}
    frequent_itemsets = {}

    for item in support_counts:
        if (support_counts[item] / num_transactions) >= minsup:
            frequent_itemsets[item] = support_counts[item] / num_transactions
        pass

    # Return frequent itemsets (incl. their support)
    return frequent_itemsets

frequent_itemsets = find_frequent_itemsets(transactions_demo, 0.6)

for itemset, support_count in frequent_itemsets.items():
    print(itemset, support_count)
    
for i in frequent_itemsets.keys():
    print(i)

for item in binary_split(frequent_itemsets.keys()):
    print(item)
    

"""
Find Association Rules

Complete method find_association_rules() to find all association rules with 
sufficient support and confidence for a given set of transactions. 
This method uses find_frequent_itemsets to first compute all frequent itemsets. 
Again, the expected format of the output is given in the comments below. 
The auxiliary method binary_split() should help for this task.
"""
def find_association_rules(transactions, minsup=0.0, minconf=0.0):

    # Perform Step 1: Frequent Itemset Generation
    frequent_itemsets = find_frequent_itemsets(transactions, minsup)
    
    # In the end, rules is a dictionary (key = (X, Y), value = (support, confidence, lift))
    # e.g., {(('cereal',), ('milk,')): (0.6, 1.0, 1.25), ...}
    rules = {}
    
    for frequent_itemset in frequent_itemsets.keys():
            if (len(frequent_itemset) >= 2):
                for X,Y in binary_split(frequent_itemset):
                    if (frequent_itemsets[frequent_itemset] / frequent_itemsets[X] >= minconf):
                        rules[X,Y] = (frequent_itemsets[frequent_itemset], frequent_itemsets[frequent_itemset] / frequent_itemsets[X],
                                    frequent_itemsets[frequent_itemset] / (frequent_itemsets[X] * frequent_itemsets[Y] )) 
                    pass   
            pass
                
    return rules

#Test implementation of find_association_rules()
rules = find_association_rules(transactions_demo, minsup=0.6, minconf=1.0)
    
for (X, Y), (sup, conf, lift) in rules.items():
    print('Rule [{} => {}] (support: {}, confidence: {}, lift: {})'.format(X, Y, sup, conf, lift))
    
#Comparison with efficient-apriori package
_, rules = apriori(transactions_demo, min_support=0.6, min_confidence=1.0, max_length=4)

for r in rules:
    print('Rule [{} => {}] (support: {}, confidence: {}, lift: {})'.format(r.lhs, r.rhs, r.support, r.confidence, r.lift))
    

"""
Apriori Algorithm

Different min_support and min_confidence lead to different lift values and wall 
time. There would be several pairs of min_support and min_confidence for comparison,
all the formats are the same.
"""
df_retail = pd.read_csv('data/online-retail.csv')

df_retail.head()

num_entries, num_attributes = df_retail.shape
print('There are {} entries, each with {} attributes.'.format(num_entries, num_attributes))

code2desc = { row['StockCode']:row['Description'] for  idx, row in df_retail.iterrows() }
stock_code = '85048'
print('The item (description) for {} is: {}'.format(stock_code, code2desc[stock_code]))

transactions_retail = df_retail.groupby(['Invoice']).agg({'StockCode': tuple})['StockCode'].to_list()

#
# Output format
#
# transactions_retail = [
#     (22554, 82494L, 21975),    
#     (21175, 84991, 85099F, 85099B),
#     (85099B, 21930),
#     ...
#]
print(transactions_retail[0:5])

#Formats to implement apriori of efficient-apriori package
itemsets, rules = apriori(transactions_retail, min_support=0.005, min_confidence=0.2, max_length=4)
lift = 0

for rule in rules:
    if rule.lift > lift:
        lift = rule.lift
        lhs = rule.lhs
        rhs = rule.rhs

print('Rule [{} => {}] (lift: {})'.format(lhs, rhs, lift))

r1 = (('22521', '22522'), ('22520', '22523'))

r1_lift = 155.62820777433782


