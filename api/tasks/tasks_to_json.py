"""Read a folder of tasks from disk to a single .JSON file per task.
"""
import json
import os

def process_file(file_path):
    # Process the content of the text file as needed.
    # For this example, let's assume each text file contains a single line of text.
    with open(file_path, 'r') as file:
        content = file.readlines()
    content_docstring = "".join(content)
    return(content_docstring)

def task_to_json(dir, task_name, outfile):
    # Iterate through the files in the folder
    task_dict = {}
    tests = {}
    #create empty .json file
    open(file=os.path.join(dir, outfile), mode="w")
    for file_name in os.listdir(os.path.join(dir, task_name)):
        file_path = os.path.join(dir, task_name, file_name)
        content_docstring = process_file(file_path)
        if file_name.startswith("test"):
            test_number = file_name.split("_")[1]
            test_number = test_number.split(".")[0]
            assert test_number.isnumeric(), "Wrong filename format for tests, should be test_[test_number] but is {0}".format(file_name)
            #Split on stop-symbol for imports
            test = content_docstring.split("#!--!#")[1]
            #json.dump({"test_{0}".format(test_number): test}, outfile, ensure_ascii=False)
            tests[test_number] = test
        elif file_name.endswith("md"):
            task_dict["task"] = content_docstring
            #json.dump({"task": content_docstring}, outfile, ensure_ascii=False)
        elif file_name == "example_solution.py":
            #json.dump({"example_solution": content_docstring}, outfile, ensure_ascii=False)
            task_dict["example_solution"] = content_docstring
    task_dict["tests"] = tests
    print(task_dict)
    with open(os.path.join(dir, outfile), "w") as f:
        json.dump(task_dict, f, ensure_ascii=False)

def parse_all_tasks(dir):
    for task_name in os.listdir(dir):
        if not task_name.endswith(".json"):
            assert task_name.startswith("task_"), "Wrong format for task folders, use task_[task_number]"
            task_number = task_name.split("_")[1].split(".")[0]
            assert task_number.isnumeric(), "Wrong task folder format, use task_[task_number]"
            outfile = "task_{0}.json".format(task_number)
            task_to_json(dir, task_name, outfile)

if __name__ == "__main__":
    print("Please give directory of the task folder to convert:")
    directory = input()
    parse_all_tasks(directory)
