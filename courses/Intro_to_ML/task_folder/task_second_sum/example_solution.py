#!function!#
#!prefix!#
def second_sum(input_list):
    result = sum(input_list[1::2])  # Slices the list starting from the second element, taking every second element
    return result

