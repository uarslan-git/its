#!function!#
import math #Define requred imports here, be carefull abput allowing certain modules
#!prefix!#
def largest_perfect_square(numbers):
    largest_square = None

    for num in numbers:
        if num > 0 and math.isqrt(num) ** 2 == num:
            if largest_square is None or num > largest_square:
                largest_square = num

    return largest_square