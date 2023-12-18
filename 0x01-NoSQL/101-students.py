#!/usr/bin/env python3
"""
top students
"""


def top_students(mongo_collection):
    """ students top score """
    return mongo_collection.aggregate([
        {
            "$project":
                {
                    "name": "$name",
                    "avgScore": {"$avg": "$topics.score"}
                }
        },
        {
            "$sort":
                {
                    "avgScore": -1
                }
        }
    ])
