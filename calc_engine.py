# calc_engine.py
from sympy import sympify, symbols, sin, cos, tan, asin, acos, atan, sqrt, exp, log, pi, E
from sympy import lambdify
import math

X = symbols('x')  # not required for base calc, handy if you later add graphing
SAFE = {
    "sin": sin, "cos": cos, "tan": tan,
    "asin": asin, "acos": acos, "atan": atan,
    "sqrt": sqrt, "exp": exp, "log": log, "ln": log, "log10": lambda v: log(v, 10),
    "pi": pi, "e": E
}

def evaluate_expr(expr: str, mode: str = "radians") -> float:
    if not expr or len(expr) > 120:
        raise ValueError("Invalid expression length")
    # Convert degree-based trig inputs if needed: wrap numeric angles to radians
    # A simple trick: replace sin( with sind( and predefine sind that converts.
    from sympy import deg
    local = {**SAFE}
    if mode == "degrees":
        # deg(x) converts degrees to radians in SymPy
        local.update({
            "sin": lambda v: sin(deg(v)),
            "cos": lambda v: cos(deg(v)),
            "tan": lambda v: tan(deg(v)),
            "asin": lambda v: asin(v)*(180/math.pi),
            "acos": lambda v: acos(v)*(180/math.pi),
            "atan": lambda v: atan(v)*(180/math.pi),
        })
    sym = sympify(expr, locals=local)  # no builtins, no eval
    val = float(sym.evalf())
    if math.isfinite(val) is False:
        raise ValueError("Non-finite result")
    return val
