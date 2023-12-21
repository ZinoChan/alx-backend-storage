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
    print(f"{total_logs} logs")
    methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]
    print("Methods:")
    for method in methods:
        count = mongo_collection.count_documents({"method": method})
        print(f"    method {method}: {count}")

    status_check_count = mongo_collection.count_documents(
        {"path": "/status"})
    print(f"{status_check_count} status check")

    print("IPs:")

    pipeline = [
        {"$group": {"_id": "$ip", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}},
        {"$limit": 10},
        {"$project": {"_id": 0, "ip": "$_id", "count": 1}}
    ]

    top_ips = collection.aggregate(pipeline)

    for top_ip in top_ips:
        count = top_ip.get("count")
        ip_address = top_ip.get("ip")
        print(f"\t{ip_address}: {count}")


if __name__ == "__main__":
    client = MongoClient('mongodb://127.0.0.1:27017')
    db = client.logs
    collection = db.nginx
    print_stats(collection)
