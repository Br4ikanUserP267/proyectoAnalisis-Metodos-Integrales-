import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from scipy import integrate

#tiempos = [450, 465, 480, 495, 525, 555]  # Tiempos en minutos
#tasas_autos = [18, 24, 14, 24, 21, 9]  # Tasas de autos por cada intervalo de 4 minutos
class CalculadoraIntegral(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Calculadora de Integrales")
        
        # ...

        self.label_tiempos = tk.Label(self, text="Tiempos minutos (separados por coma):")
        self.label_tiempos.pack()

       
        self.entry_tiempos = tk.Entry(self)
        self.entry_tiempos.pack()

        self.label_tasas = tk.Label(self, text="Tasas de autos  (separados por coma):")
        self.label_tasas.pack()


        self.entry_tasas = tk.Entry(self)
        self.entry_tasas.pack()
        self.calcular_btn = tk.Button(self, text="Calcular", command=self.calcular_integral)
        self.calcular_btn.pack()


        self.table_trapecio = ttk.Treeview(self)
        self.table_trapecio["columns"] = ("f_x0", "f_xn", "I", "Etrunc", "Et")
        self.table_trapecio.heading("f_x0", text="f(x0)")
        self.table_trapecio.heading("f_xn", text="f(xn)")
        self.table_trapecio.heading("I", text="I")
        self.table_trapecio.heading("Etrunc", text="Etrunc")
        self.table_trapecio.heading("Et", text="Et")
        self.table_trapecio.pack()

        self.table_simpson_13 = ttk.Treeview(self)
        self.table_simpson_13["columns"] = ("f_x0", "f_xi", "f_xn", "I", "Etrunc", "Et")
        self.table_simpson_13.heading("f_x0", text="f(x0)")
        self.table_simpson_13.heading("f_xi", text="f(xi)")
        self.table_simpson_13.heading("f_xn", text="f(xn)")
        self.table_simpson_13.heading("I", text="I")
        self.table_simpson_13.heading("Etrunc", text="Etrunc")
        self.table_simpson_13.heading("Et", text="Et")
        self.table_simpson_13.pack()

        self.table_simpson_38 = ttk.Treeview(self)
        self.table_simpson_38["columns"] = ("f_x0", "f_xi", "f_xi2", "f_xn", "I", "Etrunc", "Et")
        self.table_simpson_38.heading("f_x0", text="f(x0)")
        self.table_simpson_38.heading("f_xi", text="f(xi)")
        self.table_simpson_38.heading("f_xi2", text="f(xi+1)")
        self.table_simpson_38.heading("f_xn", text="f(xn)")
        self.table_simpson_38.heading("I", text="I")
        self.table_simpson_38.heading("Etrunc", text="Etrunc")
        self.table_simpson_38.heading("Et", text="Et")
        self.table_simpson_38.pack()


        
    def calcular_integral(self):
        tiempos = [float(x) for x in self.entry_tiempos.get().split(",")]
        tasas_autos = [float(x) for x in self.entry_tasas.get().split(",")]
        
        funcion = lambda t: sum(tasas_autos[i] for i in range(len(tiempos)) if tiempos[i] <= t)
        
        resultado, error = integrate.quad(funcion, min(tiempos), max(tiempos))
        
        integral_trapecio = integrate.trapz([funcion(t) for t in tiempos], tiempos)
        integral_simpson_13 = integrate.simps([funcion(t) for t in tiempos], tiempos)
        integral_simpson_38 = integrate.simps([funcion(t) for t in tiempos], tiempos)
        
        error_truncamiento_trapecio = abs(resultado - integral_trapecio)
        error_relativo_trapecio = (error_truncamiento_trapecio / resultado) * 100
        
        error_truncamiento_simpson_13 = abs(resultado - integral_simpson_13)
        error_relativo_simpson_13 = (error_truncamiento_simpson_13 / resultado) * 100
        
        error_truncamiento_simpson_38 = abs(resultado - integral_simpson_38)
        error_relativo_simpson_38 = (error_truncamiento_simpson_38 / resultado) * 100
       

        table_data_trapecio = [
            (funcion(min(tiempos)), funcion(max(tiempos)), integral_trapecio, error_truncamiento_trapecio, error_relativo_trapecio)
        ]
        table_data_simpson_13 = [
            (funcion(min(tiempos)), funcion(tiempos[1]), funcion(tiempos[2]), funcion(tiempos[3]), funcion(max(tiempos)), integral_simpson_13, error_truncamiento_simpson_13, error_relativo_simpson_13)
        ]
        table_data_simpson_38 = [
            (funcion(min(tiempos)), funcion(tiempos[1]), funcion(tiempos[2]), funcion(tiempos[3]), funcion(tiempos[4]), funcion(max(tiempos)), integral_simpson_38, error_truncamiento_simpson_38, error_relativo_simpson_38)
        ]

        self.table_trapecio.delete(*self.table_trapecio.get_children())
        for row in table_data_trapecio:
            self.table_trapecio.insert("", tk.END, values=row)

        self.table_simpson_13.delete(*self.table_simpson_13.get_children())
        for row in table_data_simpson_13:
            self.table_simpson_13.insert("", tk.END, values=row)

        self.table_simpson_38.delete(*self.table_simpson_38.get_children())
        for row in table_data_simpson_38:
            self.table_simpson_38.insert("", tk.END, values=row)
        
            errores = [error_truncamiento_trapecio, error_truncamiento_simpson_13, error_truncamiento_simpson_38]

        colores = ['red', 'green', 'blue']

        fig, ax = plt.subplots()


        for i, error in enumerate(errores):
            ax.scatter([], error, color=colores[i], label=['Trapecio', 'Simpson 1/3', 'Simpson 3/8'][i])

        ax.set_title('Errores de integración numérica')
        ax.set_xlabel('Puntos de la integral')
        ax.set_ylabel('Error')
        ax.legend()

        plt.show()

          



    





# Inicializar la aplicación
app = CalculadoraIntegral()
app.mainloop()
