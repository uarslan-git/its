import json
from db import database

async def parse_course(dir):
    with open(dir+"/course.json", "r") as course_file:
        course_json = course_file.read()
    course_dict = json.loads(course_json)
    if len(dir.split("/")) <= 1:
        unique_name = dir.split("\\")[-1]
    else:
        unique_name = dir.split("/")[-1]

    course_dict["unique_name"] = unique_name

    if "course_settings" not in course_dict.keys():
        course_dict["course_settings"] = {}

    if "course_unique_name" not in course_dict.keys():
        course_dict["course_settings"]["course_unique_name"] = course_dict["unique_name"]
    elif course_dict["course_settings"]["course_unique_name"] != course_dict["unique_name"]:
        raise Exception("Course Settings do not seem to have the same course_unique_name as course.")

    if type(course_dict["course_settings"]) != list:

        if "pedagogical_model" not in course_dict.keys():
            course_dict["course_settings"]["pedagogical_model"] = "default"

        if "language_generation_model" not in course_dict.keys():
            course_dict["course_settings"]["language_generation_model"] = "default"


        course_dict["course_settings_list"] = [course_dict["course_settings"]]

        if "sample_settings" not in course_dict.keys():
            course_dict["sample_settings"] = [1]

    else: 
        course_dict["course_settings_list"] = course_dict["course_settings"]

        if "sample_settings" not in course_dict.keys():
            n = len(course_dict["course_settings"])
            course_dict["sample_settings"] = [1/n for i in range(0, n)]
    
    del course_dict["course_settings"]

    await database.create_course(course_dict)

