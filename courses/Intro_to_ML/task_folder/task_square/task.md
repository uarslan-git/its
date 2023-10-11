# Defining own functions
## def - 

In the previous exercise, you have already used the "print" function and defined your own function with *def*. 

```python
# A very simple function
def myFunction():
    print("Hello from inside myFunction!")
myFunction()
```
```
Hello from inside myFunction!
```
Youe function can be either called on itself (as in the example above), or it can have some arguments: 

```python
# A simple function with argument(s)
def anotherFunction(a):   # Multiple arguments are possible: def anotherFunction(a, b, c, ...)
    print(a)
 anotherFunction(89)   
```
```
89
```
Additionally, a function can return a specific value: that is, you can write a value into a variable. 

```python
# Function with a return value
def functionWithRetVal(x):
    return x + 1
r = functionWithRetVal(5)
print(r)

```
```
6
```
## To Do 
Define a function, that returns the square of a real input number.
Use the folowing signature:

```python
def square(x):
    ...
```