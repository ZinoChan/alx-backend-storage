#!/usr/bin/env python3
"""
the list of school having a specific topic
"""


def schools_by_topic(mongo_collection, topic):
    """
    find specific topic
    """
    return mongo_collection.find({"topics": topic})
