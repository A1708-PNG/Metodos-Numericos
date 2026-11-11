import sympy as sp

x = sp.symbols("x")


def texto_a_expresion(texto):
    texto = texto.replace("^", "**")
    try:
        expr = sp.sympify(texto, locals={"x": x, "e": sp.E})
    except (sp.SympifyError, SyntaxError, TypeError):
        raise ValueError(f"La función '{texto}' no es válida. Ejemplo: x**3 - x - 2")
    if not isinstance(expr, sp.Expr):
        raise ValueError(f"La función '{texto}' no es válida. Ejemplo: x**3 - x - 2")
    if expr.free_symbols - {x}:
        raise ValueError("Usa solo la variable x")
    return expr


def texto_a_funcion(texto):
    return sp.lambdify(x, texto_a_expresion(texto), "numpy")


def derivar_texto(texto):
    """Devuelve la derivada de f(x) como texto, por ejemplo '3*x**2 - 1'."""
    return str(sp.diff(texto_a_expresion(texto), x))


if __name__ == "__main__":
    f = texto_a_funcion("x^2 - 4")
    print(f(3))
    print(derivar_texto("x**3 - x - 2"))