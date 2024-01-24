"""Read a folder of tasks from disk to a single .JSON file per task.
"""
import json
import os
import ast
import io
from pymongo import MongoClient
import ast

def process_file(file_path):
    # Process the content of the text file as needed.
    with io.open(file_path, mode="r", encoding="utf-8") as f:
        content = f.readlines()
    content_docstring = "".join(content)
    return(content_docstring)

def get_function_names(file_path):
    with open(file_path, 'r') as file:
        tree = ast.parse(file.read())
    function_names = [node.name for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)]
    return function_names

def extract_argument_names(func_str):
    try:
        tree = ast.parse(func_str)
        # Find the function definition node
        func_def = next(node for node in ast.walk(tree) if isinstance(node, ast.FunctionDef))
        # Extract parameter names
        param_names = [param.arg for param in func_def.args.args]
        return param_names
    except Exception as e:
        raise ValueError(f"Error extracting arguments: {e}")

def task_to_json(dir, task_unique_name, outfile, db=None):
    # Iterate through the files in the folder
    task_dict = {}
    task_dict["unique_name"] = task_unique_name.removeprefix("task_").split(".")[0]
    tests = {}
    #create empty .json file
    if db is None:
        open(file=os.path.join(dir, outfile), mode="w")
    for file_name in os.listdir(os.path.join(dir, task_unique_name)):
        file_path = os.path.join(dir, task_unique_name, file_name)
        content_docstring = process_file(file_path)
        if file_name.startswith("test"):
            #test_name = file_name.split("_", 1)[1]
            test_name = file_name.split(".")[0]
            test_name_alt = get_function_names(file_path)
            assert len(test_name_alt) == 1, "Too many test functions defined in single test file. Define only one!"
            assert test_name == test_name_alt[0], "Name of the test function should be the same as the filename"
            #assert test_number.isnumeric(), "Wrong filename format for tests, should be test_[test_number] but is {0}".format(file_name)
            #Split on stop-symbol for imports
            test = content_docstring.split("#!cut_imports!#")[1]
            #json.dump({"test_{0}".format(test_number): test}, outfile, ensure_ascii=False)
            tests[test_name] = test
        # TODO: find a way to include pictures in the database
        elif file_name.endswith("png"):
            pass
        elif file_name.endswith("md"):
            header = content_docstring.split("\n")[0]
            if not header.startswith("# "):
                raise Exception("task.md should contain the first line '# task_display_name'")
            task_display_name = header.split("#")[1].strip()
            task_dict["display_name"] = task_display_name
            task_dict["task"] = content_docstring
            #json.dump({"task": content_docstring}, outfile, ensure_ascii=False)
        elif file_name == "example_solution.py":
            task_type = content_docstring.split("!#")[0]
            task_type = task_type[2:]
            task_dict["type"] = task_type
            if task_type not in ["function", "print"]:
                raise Exception(f"Invalid task-type use function or print, not {task_type}")
            #json.dump({"example_solution": content_docstring}, outfile, ensure_ascii=False)
            prefix = content_docstring.split("#!prefix!#")[0]
            prefix = prefix.split("!#")[1].lstrip()
            task_dict["prefix"] = prefix.strip()
            #test if there is a required signature, and if so, add it to database.
            task_dict["example_solution"] = content_docstring.split("#!prefix!#\n")[1]
            if task_type == "function":
                task_dict["function_name"] = get_function_names(file_path)[0] #TODO: Secure for example solutions with multiple functions.
                arguments = extract_argument_names(task_dict["prefix"] + "\n" + task_dict["example_solution"])
                task_dict["arguments"] = arguments
        elif file_name == "multiple_choice.py":
            task_dict["type"] = "multiple_choice"
            task_dict["prefix"] = "no_prefix"
            task_dict["example_solution"] = "no_example_solution"

            json_section = content_docstring.split("#!json!#")[1]
            mc_json = json.loads(json_section)

            task_dict["possible_choices"] = mc_json["possible_choices"]
            task_dict["correct_choices"] = mc_json["correct_choices"]
            task_dict["choice_explanations"] = mc_json["choice_explanations"]

    task_dict["tests"] = tests
    if db is None:
        print(task_dict)
        with open(os.path.join(dir, outfile), "w") as f:
            json.dump(task_dict, f, ensure_ascii=False)
    else:
        db.Task.insert_one(task_dict)

def parse_all_tasks(dir, db=None):
    print(os.listdir(dir))
    for task_unique_name in os.listdir(dir):
        if not task_unique_name.endswith(".json"):
            #TODO: Shouldn't task.md be handled in task_to_json?
            task_path = os.path.join(dir, task_unique_name)+"/task.md"
            #with open(task_path, "r") as task_file:
            #    header = task_file.readline()
            #    if not header.startswith("# "):
            #        raise Exception("task.md should contain the first line '# task_display_name'")
            #    task_display_name = header.split("#")[1].strip()
            assert task_unique_name.startswith("task_"), "Wrong format for task folders, use task_[task_unique_name]"
            task_unique_name_postfix = task_unique_name.removeprefix("task_").split(".")[0]
            outfile = "task_{0}.json".format(task_unique_name_postfix)
            if db is None:
                task_to_json(dir, task_unique_name, outfile)
            else:
                task_to_json(dir, task_unique_name, outfile, db)

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
