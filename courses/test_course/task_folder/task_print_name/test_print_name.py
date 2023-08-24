from example_solution import greet as greet
#!--!#
import sys
from io import StringIO

def test_print_name():
    captured_output = StringIO()
    sys.stdout = captured_output
    greet("AI Overlord")
    greet("Bob")
    greet("Alice")
    sys.stdout = sys.__stdout__
    captured_output =  captured_output.getvalue().strip()
    assert captured_output == "Hello AI Overlord\nHello Bob\nHello Alice"
