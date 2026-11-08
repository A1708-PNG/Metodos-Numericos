import math


def f(x):
    """Define aquí la función f(x) a la cual le deseas calcular la raíz."""
    return x**3 - 2 * x - 5


def secante(f, x0, x1, tol=1e-5, max_iter=100):
    """Encuentra la raíz de la función f(x) mediante el Método de la Secante.

    Parámetros:
        f        : Función continua f(x)
        x0, x1   : Aproximaciones iniciales
        tol      : Tolerancia para el error absoluto u objetivo de parada
        max_iter : Número máximo de iteraciones permitidas
    """
    f0 = f(x0)
    f1 = f(x1)

    print(
        f"{'Iter':<5} | {'x0':<12} | {'x1':<12} | {'x2 (Raíz)':<12} | {'f(x2)':<12} | {'Error':<10}"
    )
    print("-" * 75)

    for i in range(1, max_iter + 1):
        denominador = f1 - f0

        if abs(denominador) < 1e-14:
            print("Error: División por cero o denominador extremadamente pequeño.")
            return None

        # Fórmula de la secante
        x2 = x1 - (f1 * (x1 - x0)) / denominador
        f2 = f(x2)

        error = abs(x2 - x1)

        print(
            f"{i:<5} | {x0:<12.6f} | {x1:<12.6f} | {x2:<12.6f} | {f2:<12.6e} | {error:<10.6e}"
        )

        if abs(f2) == 0 or error < tol:
            print("-" * 75)
            print(
                f"\n Raíz aproximada encontrada: x = {x2:.6f} en {i} iteraciones."
            )
            return x2

        # Actualización de valores para la siguiente iteración
        x0, f0 = x1, f1
        x1, f1 = x2, f2

    print("-" * 75)
    print("\n Se alcanzó el número máximo de iteraciones.")
    return x2


if __name__ == "__main__":
    val_x0 = 2.0
    val_x1 = 3.0
    tolerancia = 1e-5

    print(f"Buscando raíz para f(x) con valores iniciales x0 = {val_x0} y x1 = {val_x1}\n")
    raiz = secante(f, val_x0, val_x1, tol=tolerancia)