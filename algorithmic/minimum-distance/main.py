"""
Exercice 1 - Minimum Absolute Distance

Given an array of integers, write a function min_distance to calculate the minimum absolute
distance between two elements then return all pairs having that absolute difference.

Note: Make sure to print the pairs in ascending order.

Example:

Input:
v = [3, 12, 126, 44, 52, 57, 144, 61, 68, 72, 122]

Output:
def min_distance(v) ->
min = 4
[(57, 61), (68, 72), (22, 126)]
"""

def distance(a, b):
    """
    :param a:
    :param b:
    :return:
    """
    return abs(a-b)

def min_distance_approach_one(v):
    """
    :param v:
    :return:

    Bruteforce approach where we cannot save anything. It requires twice for nested loops.
    1. We determine the min distance first by computing n * (n - 1) / 2 distances between pairs
    (no need to compute pairs twice).
    2. Once we do have the min distance, we cross the pairs a second time to list all of them with that distance.
    3. We sort the pairs.
    Complexity in time: O(n**2) where n in the length of the list
    """

    min_distance_value = None
    length_list = len(v)

    count = 0
    for i in range(length_list):
        for j in range(i+1, length_list):
            distance_value = distance(v[i], v[j])
            count += 1
            if (not min_distance_value) or distance_value < min_distance_value:
                min_distance_value = distance_value
    assert count == length_list * (length_list-1) / 2
    print(min_distance_value)

    list_to_return = []
    for i in range(length_list):
        for j in range(i+1, length_list):
            a, b = v[i], v[j]
            distance_value = distance(a, b)
            if distance_value == min_distance_value:
                left = a if a <= b else b
                right = b if a <= b else a
                list_to_return.append((left, right))

    # sort in ascending order
    list_to_return.sort()
    print(list_to_return)

def min_distance_approach_two(v):
    """
    :param v:
    :return:

    We can save each distance
    1. We determine all the pairwise distances by computing n * (n - 1) / 2 distances between pairs
    (no need to compute pairs twice).
    2. We save all pair distances into a dictionary indexed by distance
    3. We sort keys to obtain the minimum distance and return the sorted list of element of the dictionary
    for that key
    """

    pair_distances_recorder = {}
    length_list = len(v)
    min_distance_value = None

    for i in range(length_list):
        for j in range(i+1, length_list):
            a, b = v[i], v[j]
            distance_value = distance(a, b)
            if (not min_distance_value) or distance_value < min_distance_value:
                min_distance_value = distance_value
            left = a if a <= b else b
            right = b if a <= b else a
            pair_distances_recorder.setdefault(distance_value, []).append((left,right))

#    min_distance_value = min(pair_distances_recorder.keys())
    print(min_distance_value)
    list_to_return = pair_distances_recorder[min_distance_value]
    list_to_return.sort()
    print(list_to_return)

def min_distance_approach_three(v):
    """
    :param v:
    :return:

    1. We sort the array
    2. Compute the distance between elements of the array + store it
    3. Access the pairs from the minimum distance

    """
    min_distance_value = None
    pair_distances_recorder = {}
    length_list = len(v)
    v.sort()
    for i in range(1, length_list):
        a, b = v[i-1], v[i]
        distance_value = distance(a, b)
        if (not min_distance_value) or distance_value < min_distance_value:
            min_distance_value = distance_value
        pair_distances_recorder.setdefault(distance_value, []).append((a, b))
    print(min_distance_value)
    list_to_return = pair_distances_recorder[min_distance_value]
    list_to_return.sort()
    print(list_to_return)

def min_distance_approach_four(v):
    """
    :param v:
    :return:

    1. We sort the array
    2. Compute the distance between elements of the array to get the minimum distance but we don't store it
    3. Linear search to get the pairs with the minimum distance

    """
    min_distance_value = None
    list_to_return = []
    length_list = len(v)

    v.sort()
    for i in range(1, length_list):
        a, b = v[i-1], v[i]
        distance_value = distance(a, b)
        if (not min_distance_value) or distance_value < min_distance_value:
            min_distance_value = distance_value

    print(min_distance_value)
    for i in range(1, length_list):
        a, b = v[i-1], v[i]
        distance_value = distance(a, b)
        if distance_value == min_distance_value:
            list_to_return.append((a, b))

    print(list_to_return)

if __name__ == '__main__':
    res = distance(57, 61)
    print(res)

    v = [3, 12, 126, 44, 52, 57, 144, 61, 68, 72, 122]

    print("Approche 1 - bruteforce with 2 nested for loops")
    min_distance_approach_one(v)

    print("Approche 2 - with storage")
    min_distance_approach_two(v)

    print("Approche 3 - sorting the array + storage")
    min_distance_approach_three(v)

    print("Approche 4 - sorting the array but no storage")
    min_distance_approach_four(v)

