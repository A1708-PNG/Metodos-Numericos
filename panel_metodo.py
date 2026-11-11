import inspect
import customtkinter as ctk
from utilidades.parser import texto_a_funcion, derivar_texto
from interfaz.widgets import Tabla, Grafica, VisorCodigo, Arbol, formato


class PanelMetodo(ctk.CTkFrame):
    def __init__(self, master, metodos):
        super().__init__(master, fg_color="transparent")
        self.metodos = metodos
        self.entradas = {}

        izquierda = ctk.CTkFrame(self, width=280)
        izquierda.pack(side="left", fill="y", padx=10, pady=10)

        ctk.CTkLabel(izquierda, text="Método").pack(anchor="w", padx=10, pady=(10, 0))
        self.selector = ctk.CTkOptionMenu(izquierda, values=list(metodos),
                                          command=self.cambiar_metodo)
        self.selector.pack(fill="x", padx=10, pady=5)

        self.zona_campos = ctk.CTkFrame(izquierda, fg_color="transparent")
        self.zona_campos.pack(fill="x")

        ctk.CTkButton(izquierda, text="Calcular", command=self.calcular).pack(
            fill="x", padx=10, pady=(15, 5))
        ctk.CTkButton(izquierda, text="Limpiar", fg_color="gray",
                      command=self.limpiar).pack(fill="x", padx=10, pady=5)

        self.mensaje = ctk.CTkLabel(izquierda, text="", text_color="#e05555",
                                    wraplength=240, justify="left")
        self.mensaje.pack(fill="x", padx=10, pady=10)

        self.resultados = ctk.CTkTabview(self)
        self.resultados.pack(side="right", fill="both", expand=True, padx=10, pady=10)
        for nombre in ["Tabla", "Gráfica", "Resultado", "Código"]:
            self.resultados.add(nombre)

        self.tabla = Tabla(self.resultados.tab("Tabla"))
        self.tabla.pack(fill="both", expand=True)
        self.grafica = Grafica(self.resultados.tab("Gráfica"))
        self.grafica.pack(fill="both", expand=True)
        self.texto_resultado = ctk.CTkLabel(self.resultados.tab("Resultado"), text="",
                                            font=("", 18), justify="left")
        self.texto_resultado.pack(pady=30)
        self.codigo = VisorCodigo(self.resultados.tab("Código"))
        self.codigo.pack(fill="both", expand=True)
        self.arbol = None   # la pestaña Árbol solo aparece en los métodos que la usan

        self.cambiar_metodo(self.selector.get())

    def _pestana_arbol(self, mostrar):
        if mostrar and self.arbol is None:
            self.resultados.add("Árbol")
            self.arbol = Arbol(self.resultados.tab("Árbol"))
            self.arbol.pack(fill="both", expand=True)
        elif not mostrar and self.arbol is not None:
            self.resultados.delete("Árbol")
            self.arbol = None

    def cambiar_metodo(self, nombre):
        self._pestana_arbol(self.metodos[nombre].get("arbol", False))
        for w in self.zona_campos.winfo_children():
            w.destroy()
        self.entradas = {}
        for campo, ejemplo in self.metodos[nombre]["campos"].items():
            ctk.CTkLabel(self.zona_campos, text=campo).pack(anchor="w", padx=10, pady=(8, 0))
            entrada = ctk.CTkEntry(self.zona_campos)
            entrada.insert(0, ejemplo)
            entrada.pack(fill="x", padx=10)
            self.entradas[campo] = entrada
        self.limpiar()

    def leer_valores(self):
        # La llave de cada valor es la primera palabra del campo: "f'(x) (opcional)" -> "f'(x)"
        valores = {}
        for campo, entrada in self.entradas.items():
            clave = campo.split()[0]
            texto = entrada.get().strip()

            if clave == "f'(x)" and texto == "":
                # Derivada automática: se calcula con SymPy y se muestra en el campo
                texto = derivar_texto(self.entradas["f(x)"].get().strip())
                entrada.insert(0, texto)

            if texto == "":
                if "opcional" in campo:
                    valores[clave] = None
                    continue
                raise ValueError(f"Falta llenar el campo '{campo}'")

            if clave.endswith("(x)"):
                valores[clave] = texto_a_funcion(texto)
            else:
                try:
                    valores[clave] = float(texto)
                except ValueError:
                    raise ValueError(f"El campo '{campo}' debe ser un número")
        return valores

    def calcular(self):
        self.limpiar()
        nombre = self.selector.get()
        info = self.metodos[nombre]
        try:
            valores = self.leer_valores()
            res = info["funcion"](*valores.values())
        except ValueError as e:
            self.mensaje.configure(text=str(e))
            return
        except Exception as e:
            self.mensaje.configure(text=f"Error: {e}")
            return

        self.tabla.mostrar(res["columnas"], res["tabla"],
                           res.get("signo", []), res.get("resaltar", []))

        r = res["resultado"]
        if isinstance(r, list):
            lineas = ["Raíces:"] + [f"   x{i + 1} = {formato(z)}" for i, z in enumerate(r)]
        else:
            lineas = [f"Resultado: {formato(r)}"]
        lineas.append(f"Error: {res['error']:.3e}")
        if "iteraciones" in res:
            lineas.append(f"Iteraciones: {res['iteraciones']}")
        if "estado" in res:
            lineas.append(f"Estado: {res['estado']}")
        if res.get("extra"):
            lineas += [""] + res["extra"]
        self.texto_resultado.configure(text="\n".join(lineas))

        self.codigo.mostrar(inspect.getsource(info["funcion"]))

        try:
            self.graficar(valores, res, nombre)
        except Exception:
            pass  # si la gráfica falla, los demás resultados se siguen viendo

        if self.arbol is not None and "nodos" in res:
            self.arbol.dibujar(res["nodos"], res["niveles_arbol"], nombre)

    def graficar(self, valores, res, nombre):
        r = res["resultado"]
        if res.get("tipo") == "derivada":
            self.grafica.graficar_derivada(valores["f(x)"], res["x0"], res["puntos"],
                                           r, res["exacta"], nombre)
        elif res.get("tipo") == "integral":
            self.grafica.graficar_integral(valores["f(x)"], res["piezas"], nombre)
        elif "f(x)" in valores:
            lista = r if isinstance(r, list) else [r]
            marcas = [complex(z).real for z in lista if abs(complex(z).imag) < 1e-9]
            if "rango" in res:
                a, b = res["rango"]
            elif valores.get("a") is not None and valores.get("b") is not None:
                a, b = valores["a"], valores["b"]
            elif marcas:
                a, b = min(marcas) - 2, max(marcas) + 2
            else:
                a, b = -5, 5
            self.grafica.graficar_funcion(valores["f(x)"], a, b, marcas, nombre,
                                          res.get("lineas"), res.get("intervalo"))
        elif "g(x)" in valores:
            self.grafica.graficar_punto_fijo(valores["g(x)"], r, nombre,
                                             res.get("rango"), res.get("lineas"))

    def limpiar(self):
        self.tabla.limpiar()
        self.grafica.limpiar()
        self.texto_resultado.configure(text="")
        self.codigo.mostrar("")
        self.mensaje.configure(text="")
        if self.arbol is not None:
            self.arbol.limpiar()