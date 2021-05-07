# CS5228_Assignment1_b_AssociationRules

Two methods of utils module will be used in this file: powerset() and binary_split()

powerset():
Given a set of items, powerset() returns all possible subset of items with a 
specified minimum and maximum length. For example, you can use this method to 
generate all itemsets for a transaction.

binary_split():
Given a set of items, binary_split() return all combinations of how the input 
set can be split into 2 non-empty subsets (where the union of both subsets for 
the input set). It's easy to see that you can use this to get from an itemset
to all possible association rules.
