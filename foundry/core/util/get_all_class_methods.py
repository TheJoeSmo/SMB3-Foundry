

from inspect import getmembers, ismethod


def get_all_class_methods(func):
    """
    Retrieves every method of a class
    :return: the methods objects of the class
    """
    return [member[1] for member in getmembers(func, predicate=ismethod)]
