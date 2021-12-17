#!/usr/bin/env python3
""" a Python function  that inserts a new document in a collection """
import pymongo


def insert_school(mongo_collection, **kwargs):
    ''' Returns the new _id '''
    if len(kwargs) == 0:
        return None
    return mongo_collection.insert(kwargs)
