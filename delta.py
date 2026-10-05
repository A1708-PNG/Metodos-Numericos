import math


def g(x):
    """Función de punto fijo g(x) tal que x = g(x).

    Para x^3 - x - 2 = 0, despejando x obtenemos x = (x + 2)^(1/3)
    """
    return math.pow(x + 2, 1 / 3)


def aitken(g, x0, tol=1e-6, max_iter=50):
    """Aplica la aceleración del método delta^2 de Aitken a la iteración de punto fijo g(x).

    Parámetros:
        g        : Función de punto fijo g(x)
        x0       : Valor inicial
        tol      : Tolerancia para el error relativo/absoluto
        max_iter : Número máximo de iteraciones permitidas
    """
    print(
        f"{'Iter':<5} | {'x_k':<12} | {'x_{k+1}':<12} | {'x_{k+2}':<12} | {'x_Aitken (^x)':<14} | {'Error':<10}"
    )
    print("-" * 75)

    x_curr = x0

    for i in range(1, max_iter + 1):
        # 1. Generar los tres puntos consecutivos mediante x_{n+1} = g(x_n)
        x1 = g(x_curr)
        x2 = g(x1)

        # 2. Denominador de la fórmula de Aitken (segunda diferencia finita Delta^2 x_k)
        denom = x2 - 2 * x1 + x_curr

        if abs(denom) < 1e-12:
            print("El denominador está demasiado cercano a cero.")
            return x2

        # 3. Aplicar la fórmula de aceleración de Aitken
        x_aitken = x_curr - ((x1 - x_curr) ** 2) / denom

        # 4. Cálculo del error
        error = abs(x_aitken - x_curr)

        print(
            f"{i:<5} | {x_curr:<12.6f} | {x1:<12.6f} | {x2:<12.6f} | {x_aitken:<14.6f} | {error:<10.6e}"
        )

        # 5. Criterio de parada
        if error < tol:
            print("-" * 75)
            print(
                f"\n Raíz acelerada encontrada: x = {x_aitken:.6f} en {i} iteraciones."
            )
            return x_aitken

        # Preparar el siguiente ciclo reutilizando el valor acelerado
        x_curr = x_aitken

    print("-" * 75)
    print("\n Se alcanzó el número máximo de iteraciones.")
    return x_aitken


if __name__ == "__main__":
    valor_inicial = 1.0
    tolerancia = 1e-6

    print(
        f"Acelerando punto fijo para g(x) comenzando en x0 = {valor_inicial}\n"
    )
    raiz = aitken(g, valor_inicial, tol=tolerancia)