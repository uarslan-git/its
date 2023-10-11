#!function!#
#!prefix!#
def breakfast(sentence):
    breakfast = sentence.split(", ")
    breakfast.append("coffee")
    breakfast.extend(["pizza", "noodles"])
    a = len(breakfast)
    new_list = breakfast[:2] 
    overall = 0
    for item in new_list:
        a = len(item)
        overall += a
    new_list.insert(0, "coffee")
    return a,overall, new_list 