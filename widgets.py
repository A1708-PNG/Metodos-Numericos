import tkinter as tk
import customtkinter as ctk
import numpy as np
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk


def formato(v):
    if v is None:
        return "—"
    if isinstance(v, (bool, np.bool_)):
        return str(v)
    if isinstance(v, (int, np.integer)):
        return str(v)
    if isinstance(v, complex):
        if abs(v.imag) < 1e-12:
            return f"{v.real:.8g}"
        return f"{v.real:.6g} {'+' if v.imag >= 0 else '-'} {abs(v.imag):.6g}i"
    try:
        return f"{float(v):.8g}"
    except (TypeError, ValueError):
        return str(v)


# Colores de la tabla
LINEA = "#7a7a7a"          # cuadrícula
ENCABEZADO = "#1f6aa5"     # fondo de los títulos (azul de CustomTkinter)
FILA_PAR = "#ffffff"
FILA_IMPAR = "#eef3f8"
NEGATIVO = "#c62828"       # texto rojo
POSITIVO = "#1550a8"       # texto azul
FONDO_MENOS = "#fbd5d5"    # celda "−"
FONDO_MAS = "#d4ecd4"      # celda "+"
FONDO_RESALTE = "#fff1b8"  # otras celdas resaltadas


class Tabla(ctk.CTkFrame):
    FUENTE = ("Segoe UI", 15)
    FUENTE_TITULO = ("Segoe UI", 15, "bold")
    MAX_FILAS = 300   # más filas harían lenta la ventana

    def __init__(self, master):
        super().__init__(master, fg_color="white")
        self.lienzo = tk.Canvas(self, bg="white", highlightthickness=0,
                                xscrollincrement=20, yscrollincrement=20)
        barra_y = ctk.CTkScrollbar(self, orientation="vertical", command=self.lienzo.yview)
        barra_x = ctk.CTkScrollbar(self, orientation="horizontal", command=self.lienzo.xview)
        self.lienzo.configure(yscrollcommand=barra_y.set, xscrollcommand=barra_x.set)
        self.lienzo.grid(row=0, column=0, sticky="nsew")
        barra_y.grid(row=0, column=1, sticky="ns")
        barra_x.grid(row=1, column=0, sticky="ew")
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # La cuadrícula: un marco gris con celdas blancas separadas por 1 píxel
        self.rejilla = tk.Frame(self.lienzo, bg=LINEA, padx=1, pady=1)
        self.lienzo.create_window((0, 0), window=self.rejilla, anchor="nw")
        self.rejilla.bind("<Configure>", lambda e: self.lienzo.configure(
            scrollregion=self.lienzo.bbox("all")))
        self._rueda(self.lienzo)

    def _rueda(self, widget):
        widget.bind("<MouseWheel>", lambda e: self.lienzo.yview_scroll(
            -3 if e.delta > 0 else 3, "units"))
        widget.bind("<Shift-MouseWheel>", lambda e: self.lienzo.xview_scroll(
            -3 if e.delta > 0 else 3, "units"))

    def _celda(self, fila, columna, texto, fondo, color="#1a1a1a", fuente=None):
        celda = tk.Label(self.rejilla, text=texto, bg=fondo, fg=color,
                         font=fuente or self.FUENTE, padx=16, pady=7)
        celda.grid(row=fila, column=columna, sticky="nsew", padx=(0, 1), pady=(0, 1))
        self._rueda(celda)

    def mostrar(self, columnas, filas, signo=(), resaltar=()):
        self.limpiar()
        for j, c in enumerate(columnas):
            self._celda(0, j, c, ENCABEZADO, "white", self.FUENTE_TITULO)

        if len(filas) > self.MAX_FILAS:
            ocultas = len(filas) - self.MAX_FILAS
            filas = filas[:self.MAX_FILAS] + [[f"… y {ocultas} filas más (se muestran las primeras {self.MAX_FILAS})"]
                                              + [""] * (len(columnas) - 1)]
        for i, fila in enumerate(filas, start=1):
            fondo_fila = FILA_PAR if i % 2 else FILA_IMPAR
            for j, valor in enumerate(fila):
                texto = formato(valor)
                fondo, color = fondo_fila, "#1a1a1a"
                nombre = columnas[j]
                if nombre in signo and isinstance(valor, (int, float, np.number)):
                    if valor < 0:
                        color = NEGATIVO
                    elif valor > 0:
                        color = POSITIVO
                if nombre in resaltar:
                    if texto == "−":
                        fondo, color = FONDO_MENOS, NEGATIVO
                    elif texto == "+":
                        fondo, color = FONDO_MAS, "#1b5e20"
                    else:
                        fondo = FONDO_RESALTE
                self._celda(i, j, texto, fondo, color)

    def limpiar(self):
        for w in self.rejilla.winfo_children():
            w.destroy()
        self.lienzo.xview_moveto(0)
        self.lienzo.yview_moveto(0)


class Grafica(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.figura = Figure(figsize=(5, 4), dpi=100)
        self.ejes = self.figura.add_subplot(111)
        self.lienzo = FigureCanvasTkAgg(self.figura, master=self)
        self.lienzo.get_tk_widget().pack(fill="both", expand=True)

    def _terminar(self, titulo):
        self.ejes.set_title(titulo)
        self.ejes.grid(True, alpha=0.3)
        self.ejes.legend()
        self.lienzo.draw()

    def _dibujar_lineas(self, lineas):
        if not lineas:
            return
        for i, (x1, y1, x2, y2) in enumerate(lineas["segmentos"]):
            self.ejes.plot([x1, x2], [y1, y2], color="orange", linewidth=0.9, alpha=0.7,
                           label=lineas["nombre"] if i == 0 else None)

    def graficar_funcion(self, f, a, b, marcas=(), titulo="", lineas=None, intervalo=None):
        self.ejes.clear()
        margen = abs(b - a) * 0.2 or 1
        xs = np.linspace(min(a, b) - margen, max(a, b) + margen, 400)
        ys = f(xs) * np.ones_like(xs)
        self.ejes.plot(xs, ys, label="f(x)")
        self.ejes.axhline(0, color="gray", linewidth=0.8)
        if intervalo:
            self.ejes.axvspan(*intervalo, color="green", alpha=0.08, label="intervalo [a, b]")
        self._dibujar_lineas(lineas)
        for xm in marcas:
            self.ejes.plot(xm, f(xm), "ro", label=f"raíz ≈ {xm:.6g}")
        self._terminar(titulo)

    def graficar_punto_fijo(self, g, x_marca, titulo="", rango=None, lineas=None):
        self.ejes.clear()
        a, b = rango if rango else (x_marca - 2, x_marca + 2)
        margen = abs(b - a) * 0.2 or 1
        xs = np.linspace(min(a, b) - margen, max(a, b) + margen, 400)
        self.ejes.plot(xs, g(xs) * np.ones_like(xs), label="g(x)")
        self.ejes.plot(xs, xs, "--", color="gray", label="y = x")
        self._dibujar_lineas(lineas)
        self.ejes.plot(x_marca, x_marca, "ro", label=f"punto fijo ≈ {x_marca:.6g}")
        self._terminar(titulo)

    def graficar_derivada(self, f, x0, puntos, pendiente, exacta, titulo=""):
        self.ejes.clear()
        ancho = max(1.0, 4 * abs(puntos[-1] - puntos[0]))
        xs = np.linspace(x0 - ancho, x0 + ancho, 400)
        self.ejes.plot(xs, f(xs) * np.ones_like(xs), label="f(x)")
        p = puntos[0]
        self.ejes.plot(xs, f(p) + pendiente * (xs - p), "--", color="orange",
                       label=f"pendiente aproximada = {pendiente:.6g}")
        self.ejes.plot(xs, f(x0) + exacta * (xs - x0), ":", color="green",
                       label=f"tangente exacta = {exacta:.6g}")
        for q in puntos:
            self.ejes.plot(q, f(q), "o", color="orange")
        self.ejes.plot(x0, f(x0), "ro", label=f"x = {x0:g}")
        self._terminar(titulo)

    def graficar_integral(self, f, piezas, titulo=""):
        self.ejes.clear()
        a = min(px[0] for px, _ in piezas)
        b = max(px[-1] for px, _ in piezas)
        margen = (b - a) * 0.05
        xs = np.linspace(a - margen, b + margen, 400)
        with np.errstate(all="ignore"):
            ys = f(xs) * np.ones_like(xs)
        self.ejes.plot(xs, ys, linewidth=2, label="f(x)")
        if len(piezas) > 150:
            # Demasiados subintervalos para dibujarlos uno por uno: se sombrea toda el área
            # y se marcan las divisiones con líneas verticales.
            dentro = (xs >= a) & (xs <= b)
            self.ejes.fill_between(xs[dentro], 0, ys[dentro], color="orange", alpha=0.3,
                                   label="área aproximada")
            bordes = sorted({px[0] for px, _ in piezas} | {b})
            self.ejes.vlines(bordes, 0, f(np.array(bordes)) * np.ones(len(bordes)),
                             color="darkorange", linewidth=0.3)
            self.ejes.axhline(0, color="gray", linewidth=0.8)
            self._terminar(titulo)
            return
        for i, (px, py) in enumerate(piezas):
            self.ejes.fill_between(px, 0, py, color="orange", alpha=0.3,
                                   label="área aproximada" if i == 0 else None)
            self.ejes.plot(px, py, color="darkorange", linewidth=1)
            self.ejes.vlines([px[0], px[-1]], 0, [py[0], py[-1]], color="darkorange", linewidth=0.8)
        self.ejes.axhline(0, color="gray", linewidth=0.8)
        self._terminar(titulo)

    def limpiar(self):
        self.ejes.clear()
        self.lienzo.draw()


class Arbol(ctk.CTkFrame):
    """Dibuja el árbol de subintervalos de la cuadratura adaptativa."""

    def __init__(self, master):
        super().__init__(master)
        self.figura = Figure(figsize=(8, 5), dpi=100)
        self.ejes = self.figura.add_subplot(111)
        self.lienzo = FigureCanvasTkAgg(self.figura, master=self)
        barra = NavigationToolbar2Tk(self.lienzo, self, pack_toolbar=False)  # lupa para hacer zoom
        barra.update()
        barra.pack(side="bottom", fill="x")
        self.lienzo.get_tk_widget().pack(fill="both", expand=True)

    def dibujar(self, nodos, niveles, titulo=""):
        ax = self.ejes
        ax.clear()
        ax.axis("off")
        visibles = [n for n in nodos if n["nivel"] <= niveles]
        a0, b0 = nodos[0]["a"], nodos[0]["b"]

        # Cada caja va en el centro de su subintervalo (x) y en la fila de su nivel (y)
        pos = {n["id"]: (((n["a"] + n["b"]) / 2 - a0) / (b0 - a0), -(n["nivel"] - 1))
               for n in visibles}

        for n in visibles:
            if n["padre"] in pos:
                (x1, y1), (x2, y2) = pos[n["padre"]], pos[n["id"]]
                ax.plot([x1, x2], [y1, y2], color="gray", linewidth=1, zorder=1)

        fuente = max(6, 11 - niveles)
        for n in visibles:
            x, y = pos[n["id"]]
            texto = (f"a = {n['a']:.6g}    b = {n['b']:.6g}\n"
                     f"I1 = {n['I1']:.10g}\n"
                     f"|I1 − I2| = {n['dif']:.6g}\n"
                     f"ErrorMax = {n['emax']:.3g}")
            fondo = "#d4ecd4" if n["acepta"] else "#fff1b8"
            ax.text(x, y, texto, ha="center", va="center", fontsize=fuente, zorder=2,
                    bbox=dict(boxstyle="round,pad=0.4", facecolor=fondo, edgecolor="#555"))
            if not n["acepta"] and n["nivel"] == niveles:
                ax.text(x, y - 0.42, "⋮", ha="center", va="top", fontsize=14, color="gray")

        ax.set_xlim(-0.1, 1.1)
        ax.set_ylim(-(niveles - 1) - 0.7, 0.6)
        total = max(n["nivel"] for n in nodos)
        ax.set_title(f"{titulo}   ·   verde = se acepta, amarillo = se divide   ·   "
                     f"se muestran {min(niveles, total)} de {total} niveles", fontsize=10)
        self.figura.tight_layout()
        self.lienzo.draw()

    def limpiar(self):
        self.ejes.clear()
        self.ejes.axis("off")
        self.lienzo.draw()


class VisorCodigo(ctk.CTkTextbox):
    def __init__(self, master):
        super().__init__(master, font=("Consolas", 13), wrap="none")

    def mostrar(self, texto):
        self.configure(state="normal")
        self.delete("1.0", "end")
        self.insert("1.0", texto)
        self.configure(state="disabled")