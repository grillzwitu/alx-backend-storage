#!/usr/bin/env python3
"""a Python script that provides some stats about Nginx logs stored in MongoDB"""
from pymongo import MongoClient


if __name__ == "__main__":
    '''provides some stats about Nginx logs stored in MongoDB'''
    client = MongoClient('mongodb://127.0.0.1:27017')
    nginx_logs = client.logs.nginx
    print("{} logs".format(nginx_logs.estimated_document_count()))
    print("Methods:")
    for method in ["GET", "POST", "PUT", "PATCH", "DELETE"]:
        count = nginx_logs.count_documents({'method': method})
        print("\tmethod {}: {}".format(method, count))
    status_get = nginx_logs.count_documents({'method': 'GET', 'path': "/status"})
    print("{} status check".format(status_get))
