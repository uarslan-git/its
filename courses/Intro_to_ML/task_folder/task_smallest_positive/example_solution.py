#!function!#
#Define requred imports here, be carefull abput allowing certain modules
#!prefix!#
def find_smallest_positive_above_threshold(numbers, threshold):
    smallest_positive = None

    for num in numbers:
        if num > threshold:
            if smallest_positive is None or num < smallest_positive:
                smallest_positive = num

    return smallest_positive