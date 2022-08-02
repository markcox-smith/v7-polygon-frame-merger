import numpy as np


def _Array_AND(arr1,arr2):
    """
    A function that takes two multidimensional arrays (with the same dimensions) and returns an array where each component has undergone AND logic
    """
    arr1 = np.array(arr1)
    arr2 = np.array(arr2)

    flat_1 = __Flatten(arr1)
    flat_2 = __Flatten(arr2)

    return np.logical_and(flat_1,flat_2)

def __Flatten(arr):
    """
    Returns a flattened array
    """
    return arr.flatten()

def Overlap_Bool(arr1,arr2):
    """
    Determines whether there is any overlap between two numpy arrays
    """
    And_Array = _Array_AND(arr1,arr2)
    return np.any(And_Array)

