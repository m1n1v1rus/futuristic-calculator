# File: logic/solver.py

import math
from sympy import *
from sympy.parsing.sympy_parser import (
    parse_expr, standard_transformations, implicit_multiplication_application,
    convert_xor, implicit_application
)

# Allowed safe symbols for SymPy
allowed_symbols = {
    'sin': sin, 'cos': cos, 'tan': tan,
    'asin': asin, 'acos': acos, 'atan': atan,
    'log': log, 'ln': log, 'log10': log,
    'sqrt': sqrt, 'abs': Abs,
    'exp': exp, 'factorial': factorial,
    'pi': pi, 'e': E
}

# Python math context (used by eval-based fallback)
math_context = {k: getattr(math, k) for k in dir(math) if not k.startswith("_")}
math_context.update({'pi': math.pi, 'e': math.e})

# Persistent symbol memory
user_namespace = {}

# Enable implicit multiplication like 2x → 2*x, and handle ^ as **
transformations = (
    standard_transformations +
    (implicit_multiplication_application, convert_xor, implicit_application)
)

def evaluate_expression(expr: str, deg_mode: bool = True) -> str:
    """
    Smart evaluator that tries symbolic mode first, then math fallback.
    """
    sympy_result = evaluate_expression_sympy(expr, deg_mode)
    if sympy_result.startswith("✅"):
        return sympy_result
    else:
        math_result = evaluate_expression_math(expr)
        if not math_result.startswith("❌"):
            return f"⚠️ SymPy failed. Math fallback: {math_result}"
        return sympy_result  # Return SymPy's error message if both fail

def evaluate_expression_sympy(expr: str, deg_mode: bool = True) -> str:
    """
    Evaluates a symbolic expression using SymPy with variable assignment and degree-mode support.
    """
    global user_namespace
    try:
        expr = expr.strip().replace("^", "**").replace("÷", "/").replace("\u00d7", "*").replace("\u03c0", "pi")

        # Variable assignment (e.g., x = 2 + 3)
        if '=' in expr:
            var_name, value_expr = map(str.strip, expr.split('=', 1))
            if not var_name.isidentifier():
                return "❌ Invalid variable name."

            parsed_value = parse_expr(value_expr, local_dict={**allowed_symbols, **user_namespace}, transformations=transformations)
            if deg_mode:
                parsed_value = apply_degree_mode(parsed_value)

            user_namespace[var_name] = parsed_value
            return f"✅ Assigned: {var_name} = {parsed_value.evalf()}"

        # Normal expression evaluation
        parsed_expr = parse_expr(expr, local_dict={**allowed_symbols, **user_namespace}, transformations=transformations)
        if deg_mode:
            parsed_expr = apply_degree_mode(parsed_expr)

        result = parsed_expr.evalf()
        return f"✅ Result: {result}"

    except Exception as e:
        return f"❌ Error: {str(e)}"

def evaluate_expression_math(expression: str) -> str:
    """
    Basic math-only evaluator using Python's math module.
    Used as a fallback or for simpler fast calculations.
    """
    try:
        replacements = {
            '^': '**', '×': '*', '÷': '/',
            'π': 'math.pi', 'e': 'math.e', '√': 'math.sqrt',
            'sin': 'math.sin', 'cos': 'math.cos', 'tan': 'math.tan',
            'log': 'math.log10', 'ln': 'math.log', '!': 'math.factorial'
        }

        for word, repl in replacements.items():
            expression = expression.replace(word, repl)

        # Implicit multiplication handler: 2(3) → 2*(3), etc.
        new_expr = ""
        prev = ""
        for ch in expression:
            if ch == '(' and (prev.isdigit() or prev == ')'):
                new_expr += '*' + ch
            elif ch.isalpha() and (prev.isdigit() or prev == ')'):
                new_expr += '*' + ch
            else:
                new_expr += ch
            prev = ch

        result = eval(new_expr, {"__builtins__": {}}, {"math": math})
        return str(result)

    except Exception as e:
        return f"❌ Error: {str(e)}"

def apply_degree_mode(expr):
    """
    Converts radians to degrees for trig functions.
    """
    return expr.replace(
        sin, lambda x: sin(x * pi / 180)
    ).replace(
        cos, lambda x: cos(x * pi / 180)
    ).replace(
        tan, lambda x: tan(x * pi / 180)
    ).replace(
        asin, lambda x: asin(x) * 180 / pi
    ).replace(
        acos, lambda x: acos(x) * 180 / pi
    ).replace(
        atan, lambda x: atan(x) * 180 / pi
    )

