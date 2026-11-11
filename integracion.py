import numpy as np


def _validar(a, b, n, multiplo=1, nombre=""):
    if a == b:
        raise ValueError("Los límites a y b deben ser distintos")
    if n != int(n) or n < 1:
        raise ValueError("n debe ser un entero positivo")
    n = int(n)
    if n % multiplo != 0:
        raise ValueError(f"En {nombre}, n debe ser múltiplo de {multiplo} (n = {n})")
    return n


def _valor(f, x):
    """Evalúa f(x) y avisa claramente si no está definida (división entre 0, raíz negativa...)."""
    try:
        y = float(f(x))
    except (ZeroDivisionError, ValueError, OverflowError):
        y = float("nan")
    if not np.isfinite(y):
        raise ValueError(f"f(x) no está definida en x = {x:.6g}, dentro del intervalo [a, b]")
    return y


def _evaluar(f, a, b, n):
    h = (b - a) / n
    xs = [a + i * h for i in range(n + 1)]
    ys = [_valor(f, x) for x in xs]
    return h, xs, ys


def _suma_pesada(f, a, b, n, pesos_de, factor_de):
    """Aplica una regla compuesta con n subintervalos. Sirve para estimar el error con 2n."""
    h, xs, ys = _evaluar(f, a, b, n)
    pesos = pesos_de(n)
    return factor_de(h) * sum(w * y for w, y in zip(pesos, ys))


def _resultado(f, a, b, n, h, xs, ys, pesos, factor, texto_factor,
               cota, piezas, estimar, divisor):
    suma = sum(w * y for w, y in zip(pesos, ys))
    integral = factor * suma
    filas = [[i, x, y, w, w * y, factor * w * y]
             for i, (x, y, w) in enumerate(zip(xs, ys, pesos))]

    extra = [f"h = (b − a)/n = {h:.8g}",
             f"Suma de pesos·f(xi) = {suma:.10g}",
             f"Integral = {texto_factor} · suma = {integral:.10g}"]
    if cota is not None:
        error = cota
        extra.append(f"Cota de error (con la M dada): {cota:.3e}")
    else:
        integral_2n = estimar(2 * n)
        error = abs(integral_2n - integral) / divisor
        extra.append(f"Error estimado comparando con 2n: |I(2n) − I(n)|/{divisor} = {error:.3e}")
        extra.append("(Da un valor de M para obtener la cota clásica del manual)")

    return {
        "resultado": integral,
        "error": error,
        "columnas": ["i", "xi", "f(xi)", "Peso", "Peso·f(xi)", "Contribución"],
        "tabla": filas,
        "extra": extra,
        "tipo": "integral",
        "piezas": piezas,
    }


def _pesos_trapecio(n):
    return [1] + [2] * (n - 1) + [1]


def _pesos_simpson13(n):
    return [1] + [4 if i % 2 else 2 for i in range(1, n)] + [1]


def _pesos_simpson38(n):
    return [1] + [2 if i % 3 == 0 else 3 for i in range(1, n)] + [1]


def _curva(xs_grupo, ys_grupo):
    """Polinomio que pasa por los puntos del grupo (recta, parábola o cúbica), para la gráfica."""
    grado = len(xs_grupo) - 1
    coef = np.polyfit(xs_grupo, ys_grupo, grado)
    px = np.linspace(xs_grupo[0], xs_grupo[-1], 40)
    return px, np.polyval(coef, px)


def trapecio(f, a, b, n, M2=None):
    n = _validar(a, b, n)
    h, xs, ys = _evaluar(f, a, b, n)
    pesos = _pesos_trapecio(n)
    cota = None if M2 is None else (b - a) ** 3 / (12 * n ** 2) * M2
    piezas = [([xs[i], xs[i + 1]], [ys[i], ys[i + 1]]) for i in range(n)]
    return _resultado(f, a, b, n, h, xs, ys, pesos, h / 2, "(h/2)", cota, piezas,
                      lambda m: _suma_pesada(f, a, b, m, _pesos_trapecio, lambda h: h / 2), 3)


def simpson_13(f, a, b, n, M4=None):
    n = _validar(a, b, n, 2, "Simpson 1/3")
    h, xs, ys = _evaluar(f, a, b, n)
    pesos = _pesos_simpson13(n)
    cota = None if M4 is None else (b - a) ** 5 / (180 * n ** 4) * M4
    piezas = [_curva(xs[i:i + 3], ys[i:i + 3]) for i in range(0, n, 2)]
    return _resultado(f, a, b, n, h, xs, ys, pesos, h / 3, "(h/3)", cota, piezas,
                      lambda m: _suma_pesada(f, a, b, m, _pesos_simpson13, lambda h: h / 3), 15)


def simpson_38(f, a, b, n, M4=None):
    n = _validar(a, b, n, 3, "Simpson 3/8")
    h, xs, ys = _evaluar(f, a, b, n)
    pesos = _pesos_simpson38(n)
    cota = None if M4 is None else (b - a) ** 5 / (80 * n ** 4) * M4
    piezas = [_curva(xs[i:i + 4], ys[i:i + 4]) for i in range(0, n, 3)]
    return _resultado(f, a, b, n, h, xs, ys, pesos, 3 * h / 8, "(3h/8)", cota, piezas,
                      lambda m: _suma_pesada(f, a, b, m, _pesos_simpson38, lambda h: 3 * h / 8), 15)


def cuadratura_adaptativa(f, a, b, error_max=1e-6, max_nivel=30, niveles_arbol=4):
    """Mismo procedimiento recursivo que Cuad_Adap(a, b, ErrorMax) de la clase."""
    if a == b:
        raise ValueError("Los límites a y b deben ser distintos")
    if error_max <= 0:
        raise ValueError("ErrorMax debe ser mayor que 0")
    max_nivel = int(max_nivel)
    niveles_arbol = max(1, int(niveles_arbol))

    def simp(a, b, k):
        """Simpson 1/3 compuesto con n = 2k subintervalos (como Simps1_3 de la clase)."""
        h = (b - a) / (2 * k)
        suma_pares = sum(_valor(f, a + h * 2 * i) for i in range(1, k))
        suma_impares = sum(_valor(f, a + h * (2 * i - 1)) for i in range(1, k + 1))
        return (h / 3) * (_valor(f, a) + 2 * suma_pares + 4 * suma_impares + _valor(f, b))

    nodos, piezas, filas = [], [], []

    def cuad_adap(a, b, error_max, nivel, padre):
        I_1 = simp(a, b, 2)
        I_2 = simp(a, b, 1)
        aprox_error = abs(I_1 - I_2)
        acepta = aprox_error <= 15 * error_max
        nodo = {"id": len(nodos), "padre": padre, "nivel": nivel, "a": a, "b": b,
                "I1": I_1, "I2": I_2, "dif": aprox_error, "emax": error_max,
                "acepta": acepta}
        nodos.append(nodo)
        filas.append([nivel, a, b, error_max, I_1, I_2, aprox_error, 15 * error_max,
                      "sí" if acepta else "no, se divide"])

        if acepta or nivel >= max_nivel:
            m = (a + b) / 2
            for x0, x2 in ((a, m), (m, b)):
                x1 = (x0 + x2) / 2
                piezas.append(_curva([x0, x1, x2], [_valor(f, x0), _valor(f, x1), _valor(f, x2)]))
            return I_1

        m = (a + b) / 2
        return (cuad_adap(a, m, error_max / 2, nivel + 1, nodo["id"]) +
                cuad_adap(m, b, error_max / 2, nivel + 1, nodo["id"]))

    integral = cuad_adap(a, b, error_max, 1, None)
    hojas = sum(1 for n in nodos if n["acepta"])
    sin_converger = sum(1 for n in nodos if not n["acepta"] and n["nivel"] >= max_nivel)
    profundidad = max(n["nivel"] for n in nodos)

    extra = ["I1 = Simp(a, b, 2)  (n = 4)     I2 = Simp(a, b, 1)  (n = 2)",
             "Si |I1 − I2| ≤ 15·ErrorMax se acepta I1; si no, se divide a la mitad",
             "y cada mitad se calcula con ErrorMax/2.",
             f"Subintervalos calculados: {len(nodos)}   ·   aceptados: {hojas}"
             f"   ·   niveles: {profundidad}"]
    if sin_converger:
        extra.append(f"Atención: {sin_converger} subintervalo(s) llegaron al nivel máximo "
                     "sin cumplir el error")

    return {
        "resultado": integral,
        "error": error_max,
        "columnas": ["Nivel", "a", "b", "ErrorMax", "I1 = Simp(a,b,2)", "I2 = Simp(a,b,1)",
                     "|I1 − I2|", "15·ErrorMax", "¿Se acepta?"],
        "tabla": filas,
        "extra": extra,
        "tipo": "integral",
        "piezas": piezas,
        "nodos": nodos,
        "niveles_arbol": niveles_arbol,
    }