"""Read a folder of tasks from disk to a single .JSON file per task.
"""
import json
import os
import ast
import io
from pymongo import MongoClient
from fastapi.encoders import jsonable_encoder

def process_file(file_path):
    # Process the content of the text file as needed.
    # For this example, let's assume each text file contains a single line of text.
    # with open(file_path, 'r') as file:
    #     content = file.readlines()
    with io.open(file_path, mode="r", encoding="utf-8") as f:
        content = f.readlines()
    content_docstring = "".join(content)
    return(content_docstring)

def get_function_names(file_path):
    with open(file_path, 'r') as file:
        tree = ast.parse(file.read())
    function_names = [node.name for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)]
    return function_names

def task_to_json(dir, task_name, task_number, outfile, db=None):
    # Iterate through the files in the folder
    task_dict = {}
    task_dict["task_id"] = task_number
    tests = {}
    #create empty .json file
    if db is None:
        open(file=os.path.join(dir, outfile), mode="w")
    for file_name in os.listdir(os.path.join(dir, task_name)):
        file_path = os.path.join(dir, task_name, file_name)
        content_docstring = process_file(file_path)
        if file_name.startswith("test"):
            #test_name = file_name.split("_", 1)[1]
            test_name = file_name.split(".")[0]
            test_name_alt = get_function_names(file_path)
            assert len(test_name_alt) == 1, "Too many test functions defined in single test file. Define only one!"
            assert test_name == test_name_alt[0], "Name of the test function should be the same as the filename"
            #assert test_number.isnumeric(), "Wrong filename format for tests, should be test_[test_number] but is {0}".format(file_name)
            #Split on stop-symbol for imports
            test = content_docstring.split("#!--!#")[1]
            #json.dump({"test_{0}".format(test_number): test}, outfile, ensure_ascii=False)
            tests[test_name] = test
        elif file_name.endswith("md"):
            task_dict["task"] = content_docstring
            #json.dump({"task": content_docstring}, outfile, ensure_ascii=False)
        elif file_name == "example_solution.py":
            #json.dump({"example_solution": content_docstring}, outfile, ensure_ascii=False)
            task_dict["example_solution"] = content_docstring
    task_dict["tests"] = tests
    if db is None:
        print(task_dict)
        with open(os.path.join(dir, outfile), "w") as f:
            json.dump(task_dict, f, ensure_ascii=False)
    else:
        db.tasks.insert_one(task_dict)

def parse_all_tasks(dir, db=None):
    print(os.listdir(dir))
    for task_name in os.listdir(dir):
        if not task_name.endswith(".json"):
            assert task_name.startswith("task_"), "Wrong format for task folders, use task_[task_number]"
            task_number = task_name.split("_")[1].split(".")[0]
            assert task_number.isnumeric(), "Wrong task folder format, use task_[task_number]"
            outfile = "task_{0}.json".format(task_number)
            if db is None:
                task_to_json(dir, task_name, task_number, outfile)
            else:
                task_to_json(dir, task_name, task_number, outfile, db)

if __name__ == "__main__":
    print("Database import? (Y/N)")
    db_import = input()
    print("Please give directory of the task folder to convert:")
    directory = input()
    if db_import == "Y":
        client = MongoClient(host="localhost", port=27017)
        db = client["its_db"]
        parse_all_tasks(directory, db)
    elif db_import == "N":
        parse_all_tasks(directory)
