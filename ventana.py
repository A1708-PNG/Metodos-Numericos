import customtkinter as ctk
from interfaz.panel_metodo import PanelMetodo
from metodos.raices import biseccion, falsa_posicion, punto_fijo, newton_raphson, secante, muller_deflacion
from metodos.derivacion import diferencia_adelante, diferencia_atras, diferencia_central
from metodos.integracion import trapecio, simpson_13, simpson_38, cuadratura_adaptativa


EJEMPLO = "x**3 - x - 2"

# El orden de los campos debe ser el mismo que el de los parámetros de cada función.
# "(opcional)" permite dejar el campo vacío. Si f'(x) se deja vacía, se calcula sola.
GRUPOS = {
    "Raíces": {
        "Bisección": {"funcion": biseccion,
                      "campos": {"f(x)": EJEMPLO, "a": "1", "b": "2", "Error": "1e-6",
                                 "Máx. iteraciones": "100"}},
        "Falsa posición": {"funcion": falsa_posicion,
                           "campos": {"f(x)": EJEMPLO, "a": "1", "b": "2", "Error": "1e-6",
                                      "Máx. iteraciones": "100"}},
        "Punto fijo": {"funcion": punto_fijo,
                       "campos": {"g(x)": "(x + 2)**(1/3)", "x0": "1.5", "Error": "1e-6",
                                  "Máx. iteraciones": "100",
                                  "a (opcional)": "1", "b (opcional)": "2"}},
        "Newton-Raphson": {"funcion": newton_raphson,
                           "campos": {"f(x)": EJEMPLO, "f'(x) (vacío = automática)": "",
                                      "x0": "1", "Error": "1e-6", "Máx. iteraciones": "100"}},
        "Secante": {"funcion": secante,
                    "campos": {"f(x)": EJEMPLO, "x0": "1", "x1": "2", "Error": "1e-6",
                               "Máx. iteraciones": "100"}},
        "Müller con deflación": {"funcion": muller_deflacion,
                                 "campos": {"f(x)": "x**3 - 2*x**2 - 5*x + 6",
                                            "x0": "-0.5", "x1": "0", "x2": "0.5",
                                            "Error": "1e-6", "Raíces a buscar": "3",
                                            "Máx. iteraciones": "100"}},
    },
    "Integración": {
        "Regla del trapecio": {"funcion": trapecio,
                               "campos": {"f(x)": "1/(1 + x**2)", "a": "0", "b": "1", "n": "4",
                                          "M₂ = máx |f''(x)| (opcional)": ""}},
        "Simpson 1/3": {"funcion": simpson_13,
                        "campos": {"f(x)": "1/(1 + x**2)", "a": "0", "b": "1", "n (par)": "4",
                                   "M₄ = máx |f⁽⁴⁾(x)| (opcional)": ""}},
        "Simpson 3/8": {"funcion": simpson_38,
                        "campos": {"f(x)": "1/(1 + x**2)", "a": "0", "b": "1",
                                   "n (múltiplo de 3)": "6",
                                   "M₄ = máx |f⁽⁴⁾(x)| (opcional)": ""}},
        "Cuadratura adaptativa": {"funcion": cuadratura_adaptativa, "arbol": True,
                                  "campos": {"f(x)": "exp(3*x)", "a": "2", "b": "7",
                                             "ErrorMax": "1e-6", "Máx. niveles": "30",
                                             "Niveles del árbol a mostrar": "4"}},
    },
    "Derivación": {
        "Diferencia hacia adelante": {"funcion": diferencia_adelante,
                                      "campos": {"f(x)": EJEMPLO,
                                                 "f'(x) exacta (vacío = automática)": "",
                                                 "x": "1", "h": "0.1"}},
        "Diferencia hacia atrás": {"funcion": diferencia_atras,
                                   "campos": {"f(x)": EJEMPLO,
                                              "f'(x) exacta (vacío = automática)": "",
                                              "x": "1", "h": "0.1"}},
        "Diferencia central": {"funcion": diferencia_central,
                               "campos": {"f(x)": EJEMPLO,
                                          "f'(x) exacta (vacío = automática)": "",
                                          "x": "1", "h": "0.1"}},
    },
    "Interpolación": {},
}


class Ventana(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Calculadora de Métodos Numéricos")
        self.geometry("1100x650")

        menu = ctk.CTkTabview(self)
        menu.pack(fill="both", expand=True, padx=10, pady=10)

        for grupo, metodos in GRUPOS.items():
            pestana = menu.add(grupo)
            if metodos:
                PanelMetodo(pestana, metodos).pack(fill="both", expand=True)
            else:
                ctk.CTkLabel(pestana, text="Próximamente").pack(pady=40)