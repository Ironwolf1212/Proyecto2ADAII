import tkinter as tk
import subprocess
import datetime
from tkinter import ttk, filedialog
from minizinc import Instance, Model, Solver

#Crear la ventana principal
root = tk.Tk()
root.geometry("1200x700")
root.title("PUICA - ADA II")

#Establecer el estilo de la ventana
style = ttk.Style()
style.theme_use("clam")

#Dividir la ventana en dos secciones
frame_input = ttk.Frame(root, padding=10)
frame_input.grid(row=0, column=0, sticky="nsew")
frame_output = ttk.Frame(root, padding=10)
frame_output.grid(row=0, column=1, sticky="nsew")

#Seleccionar un archivo de entrada
def open_file():
    path = filedialog.askopenfilename()
    if path:
        select_file(path)

#Leer el archivo de entrada y crear un archivo auxiliar
def select_file(path):
    with open(path, 'r') as file:
        lines = file.read().splitlines()

    clients = int(lines[0])
    places = int(lines[1])
    costs = lines[2]
    capacities = lines[3]
    demands = lines[4]
    benefits = []
    for i in range(5, len(lines)):
        benefits.append(lines[i])

    #Mostrar la información en la interfaz
    text_input.config(state="normal")
    text_input.delete("1.0", tk.END)
    text_input.insert(tk.END, f"Data:\n\n")
    text_input.insert(tk.END, f"Clientes: {clients}\n\n")
    text_input.insert(tk.END, f"Centros: {places}\n\n")
    text_input.insert(tk.END, f"Costos: {costs}\n\n")
    text_input.insert(tk.END, f"Capacidades: {capacities}\n\n")
    text_input.insert(tk.END, f"Demandas: {demands}\n\n")
    text_input.insert(tk.END, f"Tabla de beneficios:\n\n")
    for benefit in benefits:
        text_input.insert(tk.END, f"{benefit}\n")
        
    text_input.config(state="disabled")

    #Crear un archivo que MiniZinc pueda leer
    create_file(clients, places, costs, capacities, demands, benefits)


#Crear un archivo que MiniZinc pueda leer, a partir de los datos de entrada
def create_file(clients, places, costs, capacities, demands, benefits):
    with open("PUICAData.dzn", "w") as file:
        file.write(f"N = {clients};\n")
        file.write(f"M = {places};\n")
        file.write(f"F = [{costs}];\n")
        file.write(f"C = [{capacities}];\n")
        file.write(f"D = [{demands}];\n")
        file.write("B = [|\n")
        for row in benefits:
            file.write(f"{row}")
            file.write("|")
            if row == benefits[-1]:
                file.write("];\n")
            else:
                file.write("\n")


#Ejecutar el modelo de MiniZinc
def execute_model():
    text_output.config(state="normal")
    text_output.delete("1.0", tk.END)

    try:
        model = Model("PUICA.mzn")
        model.add_file("PUICAData.dzn")
        solver = Solver.lookup("cbc")
        instance = Instance(solver, model)
        start = datetime.datetime.now()
        result = instance.solve(timeout=datetime.timedelta(seconds=180))
        end = datetime.datetime.now()

        if result:
            profit = result.objective
            cal_products = result["R"]
            text_output.insert(tk.END, f"Solución encontrada en {end-start} segundos\n\n")
            text_output.insert(tk.END, f"Beneficio total: {profit}\n\n")
            text_output.insert(tk.END, f"Productos a enviar:\n\n")
            for i in range(len(cal_products)):
                text_output.insert(tk.END, f"Cliente {i+1}: {cal_products[i]}\n")
            text_output.insert(tk.END, f"\n")
        elif end - start < datetime.timedelta(seconds=180):
            text_output.insert(tk.END, f"No se encontró solución\n\n")
            text_output.insert(tk.END, f"El problema es INSATISFACTIBLE\n\n")
        else:
            text_output.insert(tk.END, f"No se encontró solución\n\n")
            text_output.insert(tk.END, f"Se agotó el tiempo de ejecución\n\n")
        
        text_output.insert(tk.END, f"Tiempo de ejecución: {end-start} \n\n")
        text_output.config(state="disabled")
    except subprocess.CalledProcessError as e:
        error_message = e.output.decode()
        text_output.delete("1.0", tk.END)
        text_output.insert(tk.END, f"Error en la ejecución del modelo:\n{error_message}")

#Botón para seleccionar un archivo de entrada
button_open = ttk.Button(
    frame_input, text="Seleccionar archivo", style="Custom.TButton", command=open_file, cursor="hand2")
button_open.pack(pady=10)

#Botón para ejecutar el modelo
button_run = ttk.Button(
    frame_input, text="Resolver", style="Custom.TButton", cursor="hand2", command=execute_model)
button_run.pack(pady=10)

#Establecer el estilo del botón de ejecución del modelo
style.configure(
    "Custom.TButton", foreground="black", background="green",
    font=("Montserrat", 12, "bold"),
    relief="raised",
    borderwidth=4,
    padding=10,
    width=20,
)

#Crear el panel de entrada
label_input = ttk.Label(frame_input, text="Entrada")
label_input.pack()

#Scroll vertical
scroll_input = ttk.Scrollbar(frame_input)
scroll_input.pack(side="right", fill="y")

#Scroll Horizontal
scroll_input_x = ttk.Scrollbar(frame_input, orient="horizontal")
scroll_input_x.pack(side="bottom", fill="x")

#Crear cuadro de texto para la entrada
text_input = tk.Text(
    frame_input, height=45, width=70, yscrollcommand=scroll_input.set, xscrollcommand=scroll_input_x.set, state="disabled", wrap="none")
text_input.pack()

scroll_input.config(command=text_input.yview)
scroll_input_x.config(command=text_input.xview)

#Crear el panel de salida
label_output = ttk.Label(frame_output, text="Salida")
label_output.pack()

#Crea el scroll de y para la salida
scroll_output = ttk.Scrollbar(frame_output)
scroll_output.pack(side="right", fill="y")

#Crea el scroll de x para la salida
scroll_output_x = ttk.Scrollbar(frame_output, orient="horizontal")
scroll_output_x.pack(side="bottom", fill="x")

#Crear cuadro de texto para la salida
text_output = tk.Text(
    frame_output, height=45, width=70, yscrollcommand=scroll_output.set, xscrollcommand=scroll_output_x.set, state="disabled", wrap="none")
text_output.pack()
scroll_output.config(command=text_output.yview)
scroll_output_x.config(command=text_output.xview)

#Expandir los paneles para que ocupen toda la ventana
root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)

#Ejecutar la interfaz
root.mainloop()
