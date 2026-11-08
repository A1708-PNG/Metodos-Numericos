def deflacion_polinomial(coeficientes, raiz):
    """Reduce el grado de un polinomio P(x) dividiéndolo entre (x - raiz).

    Parámetros:
        coeficientes : Lista con los coeficientes del polinomio de mayor a menor grado.
                       Ejemplo: P(x) = x^3 - 6x^2 + 11x - 6  -> [1, -6, 11, -6]
        raiz         : Raíz conocida 'r' para dividir entre (x - r).

    Retorna:
        nuevos_coef  : Coeficientes del polinomio resultantes de grado n-1.
        residuo      : El residuo de la división P(r).
    """
    n = len(coeficientes)
    nuevos_coef = [0.0] * (n - 1)

    print(f"Ejecutando deflación para el polinomio de grado {n - 1} en r = {raiz}...")
    print("-" * 55)

    nuevos_coef[0] = coeficientes[0]
    print(f"c_0 = {nuevos_coef[0]:.6f}")

    for i in range(1, n - 1):
        nuevos_coef[i] = coeficientes[i] + nuevos_coef[i - 1] * raiz
        print(f"c_{i} = {coeficientes[i]:.6f} + ({nuevos_coef[i-1]:.6f} * {raiz}) = {nuevos_coef[i]:.6f}")

    residuo = coeficientes[-1] + nuevos_coef[-1] * raiz
    print(f"Residuo = {coeficientes[-1]:.6f} + ({nuevos_coef[-1]:.6f} * {raiz}) = {residuo:.6e}")
    print("-" * 55)

    return nuevos_coef, residuo


if __name__ == "__main__":
    # Polinomio P(x) = x^3 - 6x^2 + 11x - 6  (cuyas raíces son 1, 2 y 3)
    polinomio = [1.0, -6.0, 11.0, -6.0]
    r = 1.0  # Raíz conocida

    print(f"Polinomio original: {polinomio}")
    nuevos_coef, residuo = deflacion_polinomial(polinomio, r)

    print(f"\nPolinomio deflactado (grado {len(nuevos_coef)-1}): {nuevos_coef}")
    print(f"Residuo obtenido: {residuo:.6e}")