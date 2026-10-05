import math


def f(x):
    """Define aquí la función f(x) a la cual le deseas calcular la raíz."""
    return x**3 - x - 2


def biseccion(f, a, b, tol=1e-5, max_iter=100):
    """Encuentra la raíz de la función f en el intervalo [a, b] mediante bisección.

    Parámetros:
        f        : Función continua f(x)
        a, b     : Extremos del intervalo inicial [a, b]
        tol      : Tolerancia para el error absoluto u objetivo de parada
        max_iter : Número máximo de iteraciones permitidas
    """
    # 1. Validación inicial según el Teorema del Valor Intermedio
    fa, fb = f(a), f(b)

    if fa * fb >= 0:
        print(
            "Error: f(a) y f(b) deben tener signos opuestos. El intervalo no garantiza una raíz."
        )
        return None

    print(
        f"{'Iter':<5} | {'a':<10} | {'b':<10} | {'c (Raíz)':<10} | {'f(c)':<12} | {'Error':<10}"
    )
    print("-" * 68)

    c_old = a

    for i in range(1, max_iter + 1):
        # 2. Cálculo del punto medio
        c = (a + b) / 2.0
        fc = f(c)

        # 3. Cálculo del error aproximado
        error = abs(c - c_old) if i > 1 else abs(b - a)

        # Imprimir fila con los valores de la iteración actual
        print(
            f"{i:<5} | {a:<10.6f} | {b:<10.6f} | {c:<10.6f} | {fc:<12.6e} | {error:<10.6f}"
        )

        # 4. Criterio de parada por tolerancia o coincidencia exacta
        if abs(fc) == 0 or (error < tol and i > 1):
            print("-" * 68)
            print(
                f"\n Raíz aproximada encontrada: x = {c:.6f} en {i} iteraciones."
            )
            return c

        # 5. Selección del nuevo subintervalo
        if fa * fc < 0:
            b = c
            fb = fc
        else:
            a = c
            fa = fc

        c_old = c

    print("-" * 68)
    print(
        "\n Se alcanzó el número máximo de iteraciones sin convergencia completa."
    )
    return c


# Ejemplo de uso
if __name__ == "__main__":
    # Parámetros iniciales
    intervalo_a = 1.0
    intervalo_b = 2.0
    tolerancia = 0.0001

    print(f"Buscando raíz para f(x) en el intervalo [{intervalo_a}, {intervalo_b}]\n")
    raiz = biseccion(f, intervalo_a, intervalo_b, tol=tolerancia)