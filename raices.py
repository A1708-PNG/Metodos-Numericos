import math
import cmath
import numpy as np

CONVERGIO = "Convergió: el error es menor que la tolerancia"
EXACTA = "Raíz exacta encontrada"
MAXIMO = "Se alcanzó el máximo de iteraciones sin cumplir la tolerancia"


def _validar(tol, max_iter):
    if tol <= 0:
        raise ValueError("La tolerancia debe ser mayor que 0")
    max_iter = int(max_iter)
    if max_iter < 1:
        raise ValueError("El máximo de iteraciones debe ser al menos 1")
    return max_iter


def _resultado(raiz, error, n, columnas, filas, estado, **extras):
    res = {
        "resultado": raiz,
        "error": error,
        "iteraciones": n,
        "columnas": columnas,
        "tabla": filas,
        "estado": estado,
    }
    res.update(extras)
    return res


def _signo(v):
    if v > 0:
        return "+"
    if v < 0:
        return "−"
    return "0"


def _nuevo_intervalo(fa, fxr):
    """Regla del manual: si f(a) y f(xr) tienen signos opuestos, la raíz está en [a, xr];
    si no, el cambio de signo está entre f(xr) y f(b), y se conserva [xr, b]."""
    if fa * fxr < 0:
        return "[a, xr]  →  b = xr"
    if fa * fxr > 0:
        return "[xr, b]  →  a = xr"
    return "raíz exacta"


# Columnas que se pintan: "+" en verde, "−" en rojo, el resto en amarillo
RESALTAR = ["f(a)", "f(xr)", "f(b)"]


def biseccion(f, a, b, tol=1e-6, max_iter=100):
    max_iter = _validar(tol, max_iter)
    if a > b:
        a, b = b, a
    columnas = ["n", "a", "b", "xr", "f(a)", "f(xr)", "f(b)",  "error"]
    fa, fb = f(a), f(b)
    if fa == 0:
        return _resultado(a, 0.0, 0, columnas, [], EXACTA + " en el extremo a")
    if fb == 0:
        return _resultado(b, 0.0, 0, columnas, [], EXACTA + " en el extremo b")
    if fa * fb > 0:
        raise ValueError("f(a) y f(b) deben tener signos opuestos (no hay cambio de signo en [a, b])")

    a0, b0 = a, b
    n_teorico = max(0, math.ceil(math.log2((b0 - a0) / tol)))
    filas = []
    estado = MAXIMO
    for n in range(1, max_iter + 1):
        xr = (a + b) / 2
        fxr = f(xr)
        error = (b - a) / 2
        filas.append([n, a, b, xr, _signo(fa), _signo(fxr), _signo(fb),
                      error])
        if fxr == 0:
            estado = EXACTA
            break
        if error < tol:
            estado = CONVERGIO
            break
        if fa * fxr < 0:
            b, fb = xr, fxr
        else:
            a, fa = xr, fxr
    return _resultado(xr, error, n, columnas, filas, estado,
                      extra=[f"Iteraciones teóricas: n ≥ log2((b − a)/ε) = {n_teorico}"],
                      intervalo=(a0, b0), resaltar=RESALTAR)


def falsa_posicion(f, a, b, tol=1e-6, max_iter=100):
    max_iter = _validar(tol, max_iter)
    if a > b:
        a, b = b, a
    columnas = ["n", "a", "b", "xr", "f(a)", "f(xr)", "f(b)",  "Ea"]
    fa, fb = f(a), f(b)
    if fa == 0:
        return _resultado(a, 0.0, 0, columnas, [], EXACTA + " en el extremo a")
    if fb == 0:
        return _resultado(b, 0.0, 0, columnas, [], EXACTA + " en el extremo b")
    if fa * fb > 0:
        raise ValueError("f(a) y f(b) deben tener signos opuestos (no hay cambio de signo en [a, b])")

    a0, b0 = a, b
    filas, secantes = [], []
    xr_anterior = None
    error = abs(b - a)
    estado = MAXIMO
    for n in range(1, max_iter + 1):
        if fa - fb == 0:
            raise ValueError("f(a) − f(b) = 0: el denominador se anula")
        xr = b - fb * (a - b) / (fa - fb)
        fxr = f(xr)
        ea = abs(xr - xr_anterior) if xr_anterior is not None else None
        filas.append([n, a, b, xr, _signo(fa), _signo(fxr), _signo(fb),
                       error])
        secantes.append((a, fa, b, fb))
        if ea is not None:
            error = ea
        if fxr == 0:
            estado = EXACTA
            break
        if ea is not None and ea < tol:
            estado = CONVERGIO
            break
        if fa * fxr < 0:
            b, fb = xr, fxr
        else:
            a, fa = xr, fxr
        xr_anterior = xr
    return _resultado(xr, error, n, columnas, filas, estado,
                      intervalo=(a0, b0), resaltar=RESALTAR,
                      lineas={"nombre": "secantes", "segmentos": secantes})

def _verificar_punto_fijo(g, a, b):
    if a > b:
        a, b = b, a
    xs = np.linspace(a, b, 1001)
    gx = g(xs) * np.ones_like(xs)
    h = 1e-6
    dg = (g(xs + h) - g(xs - h)) / (2 * h) * np.ones_like(xs)
    k = float(np.max(np.abs(dg)))
    se_mapea = bool(np.all((gx >= a - 1e-12) & (gx <= b + 1e-12)))
    lineas = [
        f"g([a, b]) ⊆ [a, b]: {'sí' if se_mapea else 'no'}",
        f"k = máx |g'(x)| en [a, b] ≈ {k:.6g}",
    ]
    if se_mapea and k < 1:
        lineas.append("Convergencia garantizada en [a, b]")
    else:
        lineas.append("No se garantiza la convergencia (la condición es suficiente, no necesaria)")
    return k if se_mapea and k < 1 else None, lineas


def punto_fijo(g, x0, tol=1e-6, max_iter=100, a=None, b=None):
    max_iter = _validar(tol, max_iter)
    columnas = ["n", "xn", "g(xn)", "|xn+1 − xn|"]
    extra, k = [], None
    if a is not None and b is not None:
        k, extra = _verificar_punto_fijo(g, a, b)

    filas, telarana, visitados = [], [], [x0]
    x = x0
    estado = MAXIMO
    for n in range(1, max_iter + 1):
        x_nuevo = float(g(x))
        error = abs(x_nuevo - x)
        filas.append([n, x, x_nuevo, error])
        telarana += [(x, x, x, x_nuevo), (x, x_nuevo, x_nuevo, x_nuevo)]
        x = x_nuevo
        visitados.append(x)
        if abs(x) > 1e12 or x != x:
            raise ValueError("El método diverge; prueba otra g(x) con |g'(x)| < 1 cerca de la raíz")
        if error < tol:
            estado = CONVERGIO
            break
    if k is not None:
        extra.append(f"Cota a posteriori: |xn − r| ≤ k/(1−k)·|xn − xn-1| = {k / (1 - k) * error:.3e}")
    return _resultado(x, error, n, columnas, filas, estado, extra=extra,
                      rango=(min(visitados), max(visitados)),
                      lineas={"nombre": "iteraciones", "segmentos": telarana})

def newton_raphson(f, df, x0, tol=1e-6, max_iter=100):
    max_iter = _validar(tol, max_iter)
    columnas = ["n", "xn", "f(xn)", "f'(xn)", "xn+1", "Ea"]
    x = x0
    if f(x) == 0:
        return _resultado(x, 0.0, 0, columnas, [], EXACTA + " en x0")
    filas, tangentes, visitados = [], [], [x]
    estado = MAXIMO
    for n in range(1, max_iter + 1):
        fx, dfx = f(x), df(x)
        if abs(dfx) < 1e-14:
            raise ValueError(f"f'(x) ≈ 0 en x = {x:.6g}; elige otro x0")
        x_nuevo = x - fx / dfx
        error = abs(x_nuevo - x)
        filas.append([n, x, fx, dfx, x_nuevo, error])
        tangentes.append((x, fx, x_nuevo, 0.0))
        x = x_nuevo
        visitados.append(x)
        if abs(x) > 1e12 or x != x:
            raise ValueError("El método diverge; prueba con otro x0")
        if f(x) == 0:
            estado = EXACTA
            break
        if error < tol:
            estado = CONVERGIO
            break
    return _resultado(x, error, n, columnas, filas, estado,
                      rango=(min(visitados), max(visitados)),
                      lineas={"nombre": "tangentes", "segmentos": tangentes})


def secante(f, x0, x1, tol=1e-6, max_iter=100):
    max_iter = _validar(tol, max_iter)
    if x0 == x1:
        raise ValueError("x0 y x1 deben ser distintos")
    columnas = ["n", "xn-1", "xn", "f(xn-1)", "f(xn)", "xn+1", "Ea"]
    filas, secantes, visitados = [], [], [x0, x1]
    estado = MAXIMO
    for n in range(1, max_iter + 1):
        f0, f1 = f(x0), f(x1)
        if abs(f1 - f0) < 1e-14:
            raise ValueError("f(xn) − f(xn-1) ≈ 0: el denominador se anula; elige otros valores")
        x2 = x1 - f1 * (x1 - x0) / (f1 - f0)
        error = abs(x2 - x1)
        filas.append([n, x0, x1, f0, f1, x2, error])
        secantes.append((x0, f0, x2, 0.0))
        x0, x1 = x1, x2
        visitados.append(x2)
        if abs(x2) > 1e12 or x2 != x2:
            raise ValueError("El método diverge; prueba con otros valores iniciales")
        if f(x2) == 0:
            estado = EXACTA
            break
        if error < tol:
            estado = CONVERGIO
            break
    return _resultado(x2, error, n, columnas, filas, estado,
                      rango=(min(visitados), max(visitados)),
                      lineas={"nombre": "secantes", "segmentos": secantes})

def _muller(f, x0, x1, x2, tol, max_iter, num_raiz, filas):
    for n in range(1, max_iter + 1):
        f0, f1, f2 = f(x0), f(x1), f(x2)
        h1, h2 = x1 - x0, x2 - x1
        if h1 == 0 or h2 == 0:
            raise ValueError("x0, x1 y x2 deben ser distintos")
        d1, d2 = (f1 - f0) / h1, (f2 - f1) / h2
        a = (d2 - d1) / (h2 + h1)
        b = a * h2 + d2
        c = f2
        raiz_disc = cmath.sqrt(b * b - 4 * a * c)
        den = b + raiz_disc if abs(b + raiz_disc) > abs(b - raiz_disc) else b - raiz_disc
        if den == 0:
            raise ValueError("Denominador cero en Müller; elige otros valores iniciales")
        x3 = x2 - 2 * c / den
        error = abs(x3 - x2)
        filas.append([num_raiz, n, x0, x1, x2, x3, error])
        x0, x1, x2 = x1, x2, x3
        if error < tol:
            return x3, error
    raise ValueError(f"Müller no convergió para la raíz {num_raiz} en {max_iter} iteraciones")


def muller_deflacion(f, x0, x1, x2, tol=1e-6, num_raices=1, max_iter=100):
    max_iter = _validar(tol, max_iter)
    num_raices = int(num_raices)
    if num_raices < 1:
        raise ValueError("El número de raíces debe ser al menos 1")
    raices, filas = [], []
    error = 0.0
    for k in range(1, num_raices + 1):
        encontradas = tuple(raices)

        def f_deflactada(x, encontradas=encontradas):
            valor = f(x)
            for r in encontradas:
                valor = valor / (x - r)
            return valor

        r, error = _muller(f_deflactada, complex(x0), complex(x1), complex(x2),
                           tol, max_iter, k, filas)
        if abs(r.imag) < 1e-9:
            r = r.real
        raices.append(r)
    return _resultado(raices, error, len(filas),
                      ["raíz", "n", "x0", "x1", "x2", "x3", "error"], filas, CONVERGIO,
                      extra=["Deflación: cada raíz nueva se busca en f(x) / Π(x − r) de las ya encontradas"])