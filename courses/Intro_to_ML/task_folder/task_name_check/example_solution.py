#!function!#
#!prefix!#
def name_check(n):
    my_name = tuple(n)
    a = "x" in my_name
    b = my_name[1:] 
    return a,b