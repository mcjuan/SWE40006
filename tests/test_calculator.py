# test_calculator.py
import pytest
import math
from calculator import OPERATIONS

class TestBasicOperations:
    def test_add(self):
        assert OPERATIONS["add"](5, 3) == 8
        assert OPERATIONS["add"](-5, 3) == -2
        assert OPERATIONS["add"](0, 0) == 0
    
    def test_sub(self):
        assert OPERATIONS["sub"](10, 3) == 7
        assert OPERATIONS["sub"](3, 10) == -7
        assert OPERATIONS["sub"](0, 0) == 0
    
    def test_mul(self):
        assert OPERATIONS["mul"](5, 3) == 15
        assert OPERATIONS["mul"](-5, 3) == -15
        assert OPERATIONS["mul"](0, 100) == 0
    
    def test_div(self):
        assert OPERATIONS["div"](10, 2) == 5
        assert OPERATIONS["div"](7, 2) == 3.5
        with pytest.raises(ZeroDivisionError):
            OPERATIONS["div"](10, 0)
    
    def test_mod(self):
        assert OPERATIONS["mod"](10, 3) == 1
        assert OPERATIONS["mod"](15, 5) == 0
        with pytest.raises(ZeroDivisionError):
            OPERATIONS["mod"](10, 0)
    
    def test_pow(self):
        assert OPERATIONS["pow"](2, 3) == 8
        assert OPERATIONS["pow"](5, 0) == 1
        assert OPERATIONS["pow"](4, 0.5) == 2

class TestScientificOperations:
    def test_sqrt(self):
        assert OPERATIONS["sqrt"](16, None) == 4
        assert OPERATIONS["sqrt"](25, None) == 5
        assert abs(OPERATIONS["sqrt"](2, None) - 1.414213) < 0.001
    
    def test_sin(self):
        assert abs(OPERATIONS["sin"](0, None)) < 0.001
        assert abs(OPERATIONS["sin"](math.pi/2, None) - 1) < 0.001
        assert abs(OPERATIONS["sin"](math.pi, None)) < 0.001
    
    def test_cos(self):
        assert abs(OPERATIONS["cos"](0, None) - 1) < 0.001
        assert abs(OPERATIONS["cos"](math.pi/2, None)) < 0.001
        assert abs(OPERATIONS["cos"](math.pi, None) + 1) < 0.001
    
    def test_tan(self):
        assert abs(OPERATIONS["tan"](0, None)) < 0.001
        assert abs(OPERATIONS["tan"](math.pi/4, None) - 1) < 0.001
    
    def test_log(self):
        assert OPERATIONS["log"](10, None) == 1
        assert OPERATIONS["log"](100, None) == 2
        assert OPERATIONS["log"](1, None) == 0
    
    def test_ln(self):
        assert abs(OPERATIONS["ln"](math.e, None) - 1) < 0.001
        assert OPERATIONS["ln"](1, None) == 0
    
    def test_exp(self):
        assert abs(OPERATIONS["exp"](0, None) - 1) < 0.001
        assert abs(OPERATIONS["exp"](1, None) - math.e) < 0.001
    
    def test_degree_functions(self):
        assert abs(OPERATIONS["sind"](0, None)) < 0.001
        assert abs(OPERATIONS["sind"](90, None) - 1) < 0.001
        assert abs(OPERATIONS["cosd"](0, None) - 1) < 0.001
        assert abs(OPERATIONS["cosd"](90, None)) < 0.001
        assert abs(OPERATIONS["tand"](45, None) - 1) < 0.001

class TestIntegration:
    def test_all_operations_exist(self):
        expected_ops = ["add", "sub", "mul", "div", "mod", "pow", 
                       "sqrt", "sin", "cos", "tan", "log", "ln", "exp",
                       "sind", "cosd", "tand", "asin", "acos", "atan"]
        for op in expected_ops:
            assert op in OPERATIONS, f"Operation {op} missing"
    
    def test_chained_operations(self):
        # Test: (5 + 3) * 2 = 16
        result = OPERATIONS["add"](5, 3)
        result = OPERATIONS["mul"](result, 2)
        assert result == 16
        
        # Test: sqrt(16) + 2 = 6
        result = OPERATIONS["sqrt"](16, None)
        result = OPERATIONS["add"](result, 2)
        assert result == 6

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
