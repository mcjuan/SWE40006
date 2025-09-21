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

OPERATIONS = {
    "add": add,
    "sub": sub,
    "mul": mul,
    "div": div,
    "mod": mod,
    "pow": pow_,
}
