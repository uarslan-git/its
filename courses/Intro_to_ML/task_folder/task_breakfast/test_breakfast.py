from example_solution import breakfast as breakfast
#!cut_imports!#
def test_breakfast():
    assert breakfast("eggs, fruit, orange juice")[0] == 5, "It seems that the length of the list was calculated wrong."
    assert breakfast("eggs, fruit, orange juice")[1] == 9, "It seems that the length of the product names is wrong"
    assert breakfast("eggs, fruit, orange juice")[2] == ['coffee', 'eggs', 'fruit'], "It seems that the new breakfast list is collected wrong."
    assert breakfast("eggs, fruit, orange juice")[2][0] == 'coffee', "Coffee should always come first!"
    
