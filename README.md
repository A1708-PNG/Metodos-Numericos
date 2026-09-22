# Métodos Numéricos

Aplicación desarrollada en Python para resolver ecuaciones de una variable mediante métodos numéricos clásicos, con interfaz gráfica amigable para facilitar la práctica y la visualización de cada iteración.

## Descripción

Este proyecto implementa una interfaz en Tkinter para calcular raíces de funciones mediante tres técnicas fundamentales:

- Método de Bisección
- Método de Newton-Raphson
- Método de Steffensen

La aplicación permite ingresar la función, definir el intervalo o valor inicial, establecer el error máximo y el número de iteraciones, y observar la tabla de resultados generada en cada paso del proceso.

## Objetivo

Proporcionar una herramienta didáctica para comprender y aplicar métodos numéricos en la solución aproximada de ecuaciones, reforzando tanto la teoría como la implementación computacional.

## Tecnologías utilizadas

- Python 3
- Tkinter
- SymPy

## Requisitos

- Python 3.10 o superior
- pip actualizado
- Biblioteca `sympy`

## Instalación

1. Clona el repositorio:

```bash
git clone https://github.com/A1708-PNG/Metodos-Numericos.git
```

2. Ingresa al directorio del proyecto:

```bash
cd Metodos-Numericos
```

3. Instala la dependencia requerida:

```bash
pip install sympy
```

## Ejecución

Ejecuta la aplicación con:

```bash
python metodos_numericos.py
```

## Uso

La interfaz permite:

- seleccionar el método a utilizar,
- ingresar la ecuación en formato Python,
- establecer el intervalo o valor inicial,
- definir el error máximo deseado,
- elegir la cantidad máxima de iteraciones,
- revisar la tabla de cálculo y la aproximación final de la raíz.

### Ejemplos de ecuaciones

- `x**3 - x - 2`
- `x**2 - 2`
- `sin(x) - 0.5`

## Estructura del proyecto

```text
Metodos-Numericos/
├── metodos_numericos.py
├── README.md
└── .gitignore
```

## Métodos implementados

### Bisección
Es un método robusto que trabaja con un intervalo `[a, b]` donde la función cambia de signo. Repite la división del intervalo hasta obtener una aproximación con la precisión requerida.

### Newton-Raphson
Usa la derivada de la función para construir una sucesión iterativa que converge a la raíz, siempre que la estimación inicial sea adecuada.

### Steffensen
Es un método acelerado para resolver ecuaciones de punto fijo, útil para mejorar la convergencia en ciertos casos donde el método tradicional resulta más lento.

## Autor

A1708-PNG

## Licencia

Este proyecto es de uso académico y educativo.
