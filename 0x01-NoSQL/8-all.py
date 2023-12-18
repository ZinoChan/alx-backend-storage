#!/usr/bin/env python3
"""
list all document in collection from db
"""


def list_all(mongo_collection):
    """
    list all collections
    """
    if not mongo_collection:
        return []
    return list(mongo_collection.find())
