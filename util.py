"""This module is for generic utility functions. (zero application logic)"""

def split_at(index, seq):
    """Split a sequence into two at a given index and return the two parts"""
    return seq[:index], seq[index:]