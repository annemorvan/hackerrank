#!/bin/python3

import math
import os
import random
import re
import sys

#
# Complete the 'bigSorting' function below.
#
# The function is expected to return a STRING_ARRAY.
# The function accepts STRING_ARRAY unsorted as parameter.
#

def bigSorting(unsorted):
    # Write your code here
    
    # Solution 1 - Tests 3-4-5-6 failed
    #sorted_list = [int(x) for x in unsorted]
    #sorted_list.sort()
    #return [str(x) for x in sorted_list]
    
    # Solution 2 - Tests 3-4-5-6 failed
    #int_list = []
    #for x in unsorted:
    #    int_list.append(int(x))
    #int_list.sort()
    #sorted_list = []
    #for x in int_list:
    #    sorted_list.append(str(x))
    #return sorted_list
    
    # Solution 3 - Tests 3-4-5-6 failed
    #unsorted.sort(key=lambda x: int(x))
    #return unsorted
    
    # Solution 4 - Dichotomy - Tests 2-3-4-5-6-7 failed
    #a = [unsorted[0]]
    #unsorted.pop(0)
    #
    #for x in unsorted:
    #    
    #    start = 0
    #    end = len(a)
    #    while start < end:
    #        
    #        mid = (start + end)//2
    #        
    #        if int(x) < int(a[mid]):
    #            end = mid
    #        else:
    #            start = mid+1
    #            
    #    print(a, start, x)
    #    a.insert(start, x)
    #return a
    
    # Solution 5 - Leverage the length of the string to avoid int
    return sorted(unsorted,key=lambda x: (len(x), x))

if __name__ == '__main__':
    fptr = open(os.environ['OUTPUT_PATH'], 'w')

    n = int(input().strip())

    unsorted = []

    for _ in range(n):
        unsorted_item = input()
        unsorted.append(unsorted_item)

    result = bigSorting(unsorted)

    fptr.write('\n'.join(result))
    fptr.write('\n')

    fptr.close()
