from audioextractor import addition
from audioextractor import subtraction

def func(x):
    return x + 1

def test_answer():
    assert addition(1, 2) == 3

def test_subtraction():
    assert subtraction(3, 1) == 2
