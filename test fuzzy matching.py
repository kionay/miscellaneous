# most of this is a clone of
# https://github.com/saimadhu-polamuri/DataAspirant_codes/tree/master/Similarity_measures

from math import *
from decimal import Decimal
import difflib
from difflib import SequenceMatcher

def strings_to_vectors(string1,string2):
    uniqueset = set(string1+string2)
    string1_vector = []
    string2_vector = []
    for x in uniqueset:
        string1_vector.append(string1.count(x))
        string2_vector.append(string2.count(x))
    return string1_vector,string2_vector

def euclidean_distance(x,y):
    return sqrt(sum(pow(a-b,2) for a, b in zip(x, y)))

def manhattan_distance(x,y):
    return sum(abs(a-b) for a,b in zip(x,y))

def minkowski_distance(x,y,p_value):
    return nth_root(sum(pow(abs(a-b),p_value) for a,b in zip(x, y)),p_value)

def nth_root(value, n_root):
    root_value  = 1/float(n_root)
    return round (Decimal(value) ** Decimal(root_value),3)

def cosine_similarity(x,y):
    numerator = sum(a*b for a,b in zip(x,y))
    denominator = square_rooted(x)*square_rooted(y)
    return round(numerator/float(denominator),3)

def square_rooted(x):
    return round(sqrt(sum([a*a for a in x])),3)

def jaccard_similarity(x,y):
    intersection_cardinality = len(set.intersection(*[set(x), set(y)]))
    union_cardinality = len(set.union(*[set(x), set(y)]))
    return intersection_cardinality/float(union_cardinality)

def sequence_similarity(x,y):
    return SequenceMatcher(None,x,y).ratio()

def get_score(stringone,stringtwo):
    onelist,twolist = strings_to_vectors(stringone,stringtwo)
    print("euclidean distance\t\t\t" + str(euclidean_distance(onelist,twolist)))
    print("manhattan distance\t\t\t" + str(manhattan_distance(onelist,twolist)))
    print("minkowski distance\t\t\t" + str(minkowski_distance(onelist,twolist,3)))
    print("cosine similarity\t\t\t"  + str(cosine_similarity(onelist,twolist)))
    print("jaccard similarity\t\t\t" + str(jaccard_similarity(onelist,twolist)))
    print("sequence similarity\t\t\t"+ str(sequence_similarity(onelist,twolist)))
