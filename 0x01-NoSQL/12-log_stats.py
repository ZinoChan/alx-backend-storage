#!/usr/bin/env python3
"""
provides some stats about Nginx logs stored in MongoDB:
"""
from pymongo import MongoClient


def print_stats(mongo_collection):
    """
        print stats abt nginx
    """
    total_logs = mongo_collection.count_documents({})
    methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]
    for method in methods:
        count = mongo_collection.count_documents({"method": method})
        print(f"    method {method}: {count}")

    status_check_count = mongo_collection.count_documents(
        {"method": "GET", "path": "/status"})
    print(f"{status_check_count} status check")


if __name__ == "__main__":
    client = MongoClient()
    db = client.logs
    collection = db.nginx
    print_stats(collection)