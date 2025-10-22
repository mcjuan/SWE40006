# calculator.py
def add(a, b): return a + b
def sub(a, b): return a - b
def mul(a, b): return a * b

def div(a, b):
    if b == 0:
        raise ZeroDivisionError("division by zero")
    return a / b

def mod(a, b):
    if b == 0:
        raise ZeroDivisionError("modulo by zero")
    return a % b

def pow_(a, b): return a ** b
import math

# Basic operations
def add(a, b): return a + b
def sub(a, b): return a - b
def mul(a, b): return a * b

def div(a, b):
    if b == 0:
        raise ZeroDivisionError("division by zero")
    return a / b

def mod(a, b):
    if b == 0:
        raise ZeroDivisionError("modulo by zero")
    return a % b

def pow_(a, b): return a ** b

# Scientific functions (single operand)
def sqrt_(a, b=None): return math.sqrt(a)
def sin_(a, b=None): return math.sin(a)
def cos_(a, b=None): return math.cos(a)
def tan_(a, b=None): return math.tan(a)
def log_(a, b=None): return math.log10(a)
def ln_(a, b=None): return math.log(a)
def exp_(a, b=None): return math.exp(a)
def asin_(a, b=None): return math.asin(a)
def acos_(a, b=None): return math.acos(a)
def atan_(a, b=None): return math.atan(a)

# Degree versions
def sind_(a, b=None): return math.sin(math.radians(a))
def cosd_(a, b=None): return math.cos(math.radians(a))
def tand_(a, b=None): return math.tan(math.radians(a))

OPERATIONS = {
    # Basic operations
    "add": add,
    "sub": sub,
    "mul": mul,
    "div": div,
    "mod": mod,
    "pow": pow_,
    
    # Scientific functions (radians)
    "sqrt": sqrt_,
    "sin": sin_,
    "cos": cos_,
    "tan": tan_,
    "log": log_,
    "ln": ln_,
    "exp": exp_,
    "asin": asin_,
    "acos": acos_,
    "atan": atan_,
    
    # Degree versions
    "sind": sind_,
    "cosd": cosd_,
    "tand": tand_,
}
# OPERATIONS = {
#     "add": add,
#     "sub": sub,
#     "mul": mul,
#     "div": div,
#     "mod": mod,
#     "pow": pow_,
# }
