import json
import os
from pymongo import MongoClient
import argparse


def parse_course(dir, db):
    with open(dir+"/course.json", "r") as course_file:
        course_json = course_file.read()
    course_dict = json.loads(course_json)
    unique_name = dir.split("/")[-1]
    course_dict["unique_name"] = unique_name
    db.Course.insert_one(course_dict)

def parse_arguments():
    parser = argparse.ArgumentParser(description="Command-line argument parser for adding courses")
    
    # Add the --database-network argument with a default value of "localhost"
    parser.add_argument("--database-host", default="localhost", help="Specify the database network address")
    parser.add_argument("--database-port", default="27017", help="Specify the database network address")

    args = parser.parse_args()
    return args


if __name__ == "__main__":
    args = parse_arguments()
    print("Please give directory of the course folder to add to db:")
    directory = input()
    client = MongoClient(host=args.database_host, port=int(args.database_port))
    db = client["its_db"]
    parse_course(directory, db)
    import parse_tasks
    parse_tasks.parse_all_tasks(directory+"/task_folder", db=db)
