import math


def g(x):
    """Función de punto fijo g(x) tal que x = g(x).

    Ejemplo para x^3 - x - 2 = 0 despejando x: x = (x + 2)^(1/3)
    """
    return math.pow(x + 2, 1 / 3)


def punto_fijo(g, x0, tol=1e-5, max_iter=100):
    """Calcula el punto fijo x = g(x) mediante iteración directa.

    Parámetros:
        g        : Función g(x)
        x0       : Valor inicial
        tol      : Tolerancia para el error
        max_iter : Número máximo de iteraciones
    """
    print(
        f"{'Iter':<5} | {'x_k':<12} | {'g(x_k)':<12} | {'Error':<10}"
    )
    print("-" * 48)

    x_actual = x0

    for i in range(1, max_iter + 1):
        x_siguiente = g(x_actual)
        error = abs(x_siguiente - x_actual)

        print(
            f"{i:<5} | {x_actual:<12.6f} | {x_siguiente:<12.6f} | {error:<10.6e}"
        )

        if error < tol:
            print("-" * 48)
            print(
                f"\n Punto fijo encontrado: x = {x_siguiente:.6f} en {i} iteraciones."
            )
            return x_siguiente

        x_actual = x_siguiente

    print("-" * 48)
    print("\n Se alcanzó el número máximo de iteraciones.")
    return x_actual


if __name__ == "__main__":
    valor_inicial = 1.0
    tolerancia = 1e-5

    print(f"Buscando punto fijo para g(x) con x0 = {valor_inicial}\n")
    raiz = punto_fijo(g, valor_inicial, tol=tolerancia)