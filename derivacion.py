import math

FORMULAS = {
    "adelante": ("[f(x + h) − f(x)] / h", "O(h)",
                 lambda f, x, h: (f(x + h) - f(x)) / h),
    "atrás": ("[f(x) − f(x − h)] / h", "O(h)",
              lambda f, x, h: (f(x) - f(x - h)) / h),
    "central": ("[f(x + h) − f(x − h)] / (2h)", "O(h²)",
                lambda f, x, h: (f(x + h) - f(x - h)) / (2 * h)),
}


def _validar_h(h):
    if h == 0:
        raise ValueError("El paso h debe ser distinto de 0")


def _armar(f, df, x, h, tipo, aprox, puntos):
    if not math.isfinite(aprox):
        raise ValueError("f(x) no está definida en alguno de los puntos usados (x, x + h o x − h)")
    exacta = float(df(x))
    error = abs(aprox - exacta)

    filas = []
    for nombre, (formula, orden, calcular) in FORMULAS.items():
        valor = calcular(f, x, h)
        marca = "  ← elegida" if nombre == tipo else ""
        filas.append([nombre + marca, formula, valor, abs(valor - exacta), orden])

    formula, orden, _ = FORMULAS[tipo]
    extra = [f"Tipo: diferencia {tipo}   ·   h = {h:g}",
             f"Fórmula: f'(x) ≈ {formula}",
             "Valores evaluados:"]
    extra += [f"   f({p:.6g}) = {float(f(p)):.10g}" for p in sorted(set([x] + puntos))]
    extra += [f"Derivada exacta f'({x:g}) = {exacta:.10g}",
              f"Orden del error de truncamiento: {orden}"]

    return {
        "resultado": aprox,
        "error": error,
        "columnas": ["Variante", "Fórmula", "Aproximación", "Error real", "Orden"],
        "tabla": filas,
        "extra": extra,
        "tipo": "derivada",
        "x0": x,
        "puntos": puntos,
        "exacta": exacta,
    }


def diferencia_adelante(f, df, x, h):
    _validar_h(h)
    aprox = (f(x + h) - f(x)) / h
    return _armar(f, df, x, h, "adelante", aprox, [x, x + h])


def diferencia_atras(f, df, x, h):
    _validar_h(h)
    aprox = (f(x) - f(x - h)) / h
    return _armar(f, df, x, h, "atrás", aprox, [x - h, x])


def diferencia_central(f, df, x, h):
    _validar_h(h)
    aprox = (f(x + h) - f(x - h)) / (2 * h)
    return _armar(f, df, x, h, "central", aprox, [x - h, x + h])