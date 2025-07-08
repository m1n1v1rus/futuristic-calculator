from sympy import *
from sympy.parsing.sympy_parser import parse_expr

def evaluate_expression(expr):
    try:
        parsed = parse_expr(expr, evaluate=True)
        result = str(parsed.doit() if hasattr(parsed, 'doit') else parsed)
        return f"Result: {result}"
    except Exception as e:
        return f"Error: {str(e)}"
