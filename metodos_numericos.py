import tkinter as tk
from tkinter import ttk, messagebox
import sympy as sp

def preparar_funcion(texto):
    x = sp.Symbol("x")

    try:
        expr = sp.sympify(texto)
        funcion = sp.lambdify(x, expr, "math")
        return x, expr, funcion

    except Exception as e:
        raise ValueError(f"Función no válida: {e}")


def validar(error, iteraciones):
    if error <= 0:
        raise ValueError("El error máximo debe ser mayor que cero.")

    if iteraciones <= 0:
        raise ValueError("Las iteraciones deben ser mayores que cero.")


def biseccion_algoritmo(a, b, err_max, max_iter, funcion_str):

    _, _, f = preparar_funcion(funcion_str)

    fa = f(a)
    fb = f(b)

    if fa == 0:
        return [], f"La raíz exacta es a = {a}"

    if fb == 0:
        return [], f"La raíz exacta es b = {b}"

    if fa * fb > 0:
        raise ValueError(
            "f(a) y f(b) tienen el mismo signo. "
            "Ingresa un intervalo con cambio de signo."
        )

    filas = []

    for i in range(1, max_iter + 1):

        c = (a + b) / 2
        fc = f(c)

        error = abs(b - a) / 2

        filas.append((
            i,
            f"{a:.6f}",
            f"{b:.6f}",
            f"{c:.6f}",
            f"{fa:.6f}",
            f"{fc:.6f}",
            f"{fb:.6f}",
            f"{error:.6g}"
        ))

        if fc == 0 or error <= err_max:
            break

        if fa * fc < 0:
            b = c
            fb = fc

        else:
            a = c
            fa = fc

    return filas, (
        f"Aproximación de la raíz: {c:.10f} "
        f"| f(c) = {fc:.3e}"
    )


def newton_raphson_algoritmo(x0, err_max, max_iter, funcion_str):

    x, expr, f = preparar_funcion(funcion_str)

    derivada = sp.diff(expr, x)
    df = sp.lambdify(x, derivada, "math")

    actual = x0
    filas = []

    for i in range(1, max_iter + 1):

        fx = f(actual)
        dfx = df(actual)

        if abs(dfx) < 1e-14:
            raise ValueError(
                f"La derivada es cero o muy cercana a cero "
                f"en x = {actual}."
            )

        siguiente = actual - fx / dfx

        error = abs(siguiente - actual)

        filas.append((
            i,
            f"{actual:.8f}",
            f"{fx:.8f}",
            f"{dfx:.8f}",
            f"{siguiente:.8f}",
            f"{error:.6g}"
        ))

        actual = siguiente

        if error <= err_max:
            break

    return filas, (
        f"Aproximación de la raíz: {actual:.10f} "
        f"| f(x) = {f(actual):.3e}"
    )



def steffensen_algoritmo(x0, err_max, max_iter, funcion_str):

    _, _, f = preparar_funcion(funcion_str)

    actual = x0
    filas = []

    for i in range(1, max_iter + 1):

        fx = f(actual)

        denominador = f(actual + fx) - fx

        if abs(denominador) < 1e-14:
            raise ValueError(
                "Denominador cero o muy cercano a cero. "
                "Prueba otro valor inicial."
            )

        siguiente = actual - (fx ** 2) / denominador

        error = abs(siguiente - actual)

        filas.append((
            i,
            f"{actual:.8f}",
            f"{fx:.8f}",
            f"{denominador:.8f}",
            f"{siguiente:.8f}",
            f"{error:.6g}"
        ))

        actual = siguiente

        if error <= err_max:
            break

    return filas, (
        f"Aproximación de la raíz: {actual:.10f} "
        f"| f(x) = {f(actual):.3e}"
    )



class AppMetodosNumericos(tk.Tk):

    def __init__(self):

        super().__init__()

        self.title("Métodos Numéricos")
        self.geometry("1000x680")
        self.minsize(850, 580)

        # Menú principal

        barra_menu = tk.Menu(self)
        self.config(menu=barra_menu)

        menu_principal = tk.Menu(barra_menu, tearoff=0)

        barra_menu.add_cascade(
            label="Métodos Numéricos",
            menu=menu_principal
        )

        # Submenú de ecuaciones de una variable

        menu_solucion = tk.Menu(menu_principal, tearoff=0)

        menu_principal.add_cascade(
            label="Solución de Ecuaciones 1 Variable",
            menu=menu_solucion
        )

        menu_solucion.add_command(
            label="Método de Bisección",
            command=self.mostrar_biseccion
        )

        menu_solucion.add_command(
            label="Método de Newton-Raphson",
            command=self.mostrar_newton
        )

        menu_solucion.add_command(
            label="Método de Steffensen",
            command=self.mostrar_steffensen
        )

        menu_principal.add_separator()

        menu_principal.add_command(
            label="Inicio",
            command=self.mostrar_inicio
        )

        menu_principal.add_command(
            label="Salir",
            command=self.destroy
        )

        # Botones superiores

        barra_botones = tk.Frame(self, bd=1, relief="raised")
        barra_botones.pack(fill="x")

        tk.Button(
            barra_botones,
            text="Inicio",
            command=self.mostrar_inicio
        ).pack(side="left", padx=5, pady=5)

        tk.Button(
            barra_botones,
            text="Bisección",
            command=self.mostrar_biseccion
        ).pack(side="left", padx=5, pady=5)

        tk.Button(
            barra_botones,
            text="Newton-Raphson",
            command=self.mostrar_newton
        ).pack(side="left", padx=5, pady=5)

        tk.Button(
            barra_botones,
            text="Steffensen",
            command=self.mostrar_steffensen
        ).pack(side="left", padx=5, pady=5)

        # Contenedor dinámico principal

        self.contenedor = tk.Frame(self)

        self.contenedor.pack(
            fill="both",
            expand=True,
            padx=18,
            pady=15
        )

        self.mostrar_inicio()


    def limpiar_contenedor(self):

        for widget in self.contenedor.winfo_children():
            widget.destroy()

    def mostrar_inicio(self):

        self.limpiar_contenedor()

        tk.Label(
            self.contenedor,
            text="Métodos Numéricos",
            font=("Arial", 22, "bold")
        ).pack(pady=25)

        tk.Label(
            self.contenedor,
            text="Seleccione un método para resolver ecuaciones de una variable.",
            font=("Arial", 12)
        ).pack(pady=8)

        frame_botones = tk.Frame(self.contenedor)
        frame_botones.pack(pady=25)

        tk.Button(
            frame_botones,
            text="Método de Bisección",
            width=22,
            height=2,
            command=self.mostrar_biseccion
        ).grid(row=0, column=0, padx=8)

        tk.Button(
            frame_botones,
            text="Método de Newton-Raphson",
            width=22,
            height=2,
            command=self.mostrar_newton
        ).grid(row=0, column=1, padx=8)

        tk.Button(
            frame_botones,
            text="Método de Steffensen",
            width=22,
            height=2,
            command=self.mostrar_steffensen
        ).grid(row=0, column=2, padx=8)

    def crear_vista(self, titulo, campos, columnas, funcion_calculo):

        self.limpiar_contenedor()

        # Título

        tk.Label(
            self.contenedor,
            text=titulo,
            font=("Arial", 17, "bold")
        ).pack(pady=10)

        # Formulario de entrada

        frame_inputs = tk.LabelFrame(
            self.contenedor,
            text="Datos de entrada",
            padx=10,
            pady=8
        )

        frame_inputs.pack(fill="x", pady=8)

        entradas = {}

        for i, (nombre, valor) in enumerate(campos):

            tk.Label(
                frame_inputs,
                text=nombre
            ).grid(row=i, column=0, sticky="e", padx=6, pady=4)

            entrada = tk.Entry(frame_inputs, width=28)

            entrada.insert(0, valor)

            entrada.grid(row=i, column=1, sticky="w", padx=6, pady=4)

            entradas[nombre] = entrada

        # Botones de acciones

        frame_acciones = tk.Frame(self.contenedor)
        frame_acciones.pack(pady=5)

        # Tabla de resultados

        tabla_frame = tk.Frame(self.contenedor)
        tabla_frame.pack(fill="both", expand=True, pady=8)

        tabla = ttk.Treeview(
            tabla_frame,
            columns=columnas,
            show="headings",
            height=10
        )

        scroll_y = ttk.Scrollbar(
            tabla_frame,
            orient="vertical",
            command=tabla.yview
        )

        scroll_x = ttk.Scrollbar(
            tabla_frame,
            orient="horizontal",
            command=tabla.xview
        )

        tabla.configure(
            yscrollcommand=scroll_y.set,
            xscrollcommand=scroll_x.set
        )

        tabla.grid(row=0, column=0, sticky="nsew")
        scroll_y.grid(row=0, column=1, sticky="ns")
        scroll_x.grid(row=1, column=0, sticky="ew")

        tabla_frame.grid_rowconfigure(0, weight=1)
        tabla_frame.grid_columnconfigure(0, weight=1)

        for col in columnas:

            tabla.heading(col, text=col)

            tabla.column(
                col,
                width=105,
                anchor="center"
            )

        # Resultado final

        lbl_resultado = tk.Label(
            self.contenedor,
            text="",
            font=("Arial", 11, "bold")
        )

        lbl_resultado.pack(pady=4)

        # Evento del botón Calcular

        def ejecutar_calculo():

            for item in tabla.get_children():
                tabla.delete(item)

            lbl_resultado.config(text="")

            try:

                datos = {
                    k: v.get().strip()
                    for k, v in entradas.items()
                }

                filas, mensaje = funcion_calculo(datos)

                for fila in filas:
                    tabla.insert("", tk.END, values=fila)

                lbl_resultado.config(text=mensaje)

            except Exception as e:

                messagebox.showerror("Error", str(e))

        # Botón Calcular

        tk.Button(
            frame_acciones,
            text="Calcular",
            width=14,
            bg="#d9ead3",
            command=ejecutar_calculo
        ).pack(side="left", padx=6)

        # Botón Limpiar

        tk.Button(
            frame_acciones,
            text="Limpiar tabla",
            width=14,
            command=lambda: tabla.delete(*tabla.get_children())
        ).pack(side="left", padx=6)

        # Botón Volver

        tk.Button(
            frame_acciones,
            text="Volver al inicio",
            width=14,
            command=self.mostrar_inicio
        ).pack(side="left", padx=6)


    def mostrar_biseccion(self):

        def ejecutar(datos):

            a = float(datos["a"])
            b = float(datos["b"])

            error = float(datos["Error máximo"])
            iteraciones = int(datos["Iteraciones máximas"])

            validar(error, iteraciones)

            return biseccion_algoritmo(
                a, b, error, iteraciones, datos["f(x)"]
            )

        self.crear_vista(
            "Método de Bisección",

            [
                ("f(x)", "x**3 - x - 2"),
                ("a", "1"),
                ("b", "2"),
                ("Error máximo", "0.001"),
                ("Iteraciones máximas", "20")
            ],

            ("i", "a", "b", "c", "f(a)", "f(c)", "f(b)", "Error"),

            ejecutar
        )


    def mostrar_newton(self):

        def ejecutar(datos):

            x0 = float(datos["x inicial"])

            error = float(datos["Error máximo"])
            iteraciones = int(datos["Iteraciones máximas"])

            validar(error, iteraciones)

            return newton_raphson_algoritmo(
                x0, error, iteraciones, datos["f(x)"]
            )

        self.crear_vista(
            "Método de Newton-Raphson",

            [
                ("f(x)", "x**3 - x - 2"),
                ("x inicial", "1.5"),
                ("Error máximo", "0.001"),
                ("Iteraciones máximas", "20")
            ],

            ("i", "x actual", "f(x)", "f'(x)", "x siguiente", "Error"),

            ejecutar
        )


    def mostrar_steffensen(self):

        def ejecutar(datos):

            x0 = float(datos["x inicial"])

            error = float(datos["Error máximo"])
            iteraciones = int(datos["Iteraciones máximas"])

            validar(error, iteraciones)

            return steffensen_algoritmo(
                x0, error, iteraciones, datos["f(x)"]
            )

        self.crear_vista(
            "Método de Steffensen",

            [
                ("f(x)", "x**2 - 2"),
                ("x inicial", "1.5"),
                ("Error máximo", "0.001"),
                ("Iteraciones máximas", "20")
            ],

            ("i", "x actual", "f(x)", "Denominador", "x siguiente", "Error"),

            ejecutar
        )



if __name__ == "__main__":

    app = AppMetodosNumericos()

    app.mainloop()