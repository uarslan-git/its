import json
import os
from pymongo import MongoClient
import parse_tasks

def parse_course(dir, db):
    with open(dir+"/course.json", "r") as course_file:
        course_json = course_file.read()
    course_dict = json.loads(course_json)
    unique_name = dir.split("/")[-1]
    course_dict["unique_name"] = unique_name
    db.Course.insert_one(course_dict)


if __name__ == "__main__":
    print("Please give directory of the course folder to add to db:")
    directory = input()
    client = MongoClient(host="localhost", port=27017)
    db = client["its_db"]
    parse_course(directory, db)
    parse_tasks.parse_all_tasks(directory+"/task_folder", db=db)
