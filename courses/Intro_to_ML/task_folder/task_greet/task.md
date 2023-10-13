# Welcome!
## This is the very beginning of the Introduction to Python

This is a short introduction to the Python programming language. It focuses on usage and not on theory or underlying concepts. The content is chosen in order to *prepare you for the programming exercises*.

**The course does NOT claim completness and does NOT replace a "proper" (complete) introduction to the Python programming language.**

Additional material:
- [https://www.tutorialspoint.com/python/index.html](https://www.tutorialspoint.com/python/index.html)  
- [https://docs.python.org/3/tutorial/index.html](https://docs.python.org/3/tutorial/index.html)
- [https://cs231n.github.io/python-numpy-tutorial/](https://cs231n.github.io/python-numpy-tutorial/)
- [https://matplotlib.org/users/pyplot_tutorial.html](https://matplotlib.org/users/pyplot_tutorial.html)

You can find more on this tutoring system in "About". 

## This is the very beginning of the Introduction to Python

There are multiple ways of manipulating strings in python. The most easy one is the "+" operator for string concatenation. There is also the option to use a format string via the format method. The most recommended method is to use f-strings, as they are the most readible and require the least boilerplate code. 

```python
name = "Alice"
# Concatenation via +
"Hello" + name
# Format method
"Hello {0}".format(name)
# f-string
f"Hello {name}"
```

## To Do
Write a function named greet that prints "Hello {name}" where name is taken as the function parameter. 
Command **print()** can be used to print out the outputs. You can also add similar arguments directly in the function.
For example: 
```python
print("Who is "+"Marla"+"?")
print( 5 + 5 )
```
```
Who is Marla?
10
```
Use the following signature to say (print) "Hello " to an input name:

```python
def greet(name):
 
```
