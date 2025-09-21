# tests/test_calculator.py
import math
import pytest
import calculator as c

def test_add():       assert c.add(2, 3) == 5
def test_sub():       assert c.sub(2, 3) == -1
def test_mul():       assert c.mul(2, 3) == 6
def test_div():       assert c.div(6, 3) == 2
def test_div_zero():  with pytest.raises(ZeroDivisionError): c.div(1, 0)
def test_mod():       assert c.mod(7, 4) == 3
def test_mod_zero():  with pytest.raises(ZeroDivisionError): c.mod(1, 0)
def test_pow():       assert c.pow_(2, 3) == 8
def test_pow_float(): assert math.isclose(c.pow_(9, 0.5), 3.0)
