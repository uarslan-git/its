#!function!#
#!prefix!#
def name_check(my_name):
    my_name_tuple = tuple(my_name)
    a = "x" in my_name_tuple
    b = my_name_tuple[1:] 
    return a,b