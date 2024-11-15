import customtkinter as ctk
import json
import os
from tkinter import ttk, messagebox
from datetime import datetime

# Configuración inicial del JSON
data = {
    "clientes": [],
    "facturas": []
}

# Función para cargar datos desde el archivo JSON
def cargar_datos():
    documents_folder = os.path.join(os.environ['USERPROFILE'], 'Documents')
    dydo_folder = os.path.join(documents_folder, 'Dydo')
    file_path = os.path.join(dydo_folder, 'data.json')
    
    os.makedirs(dydo_folder, exist_ok=True)
    initial_data = {
        "clientes": [],
        "facturas": []
    }
    if not os.path.isfile(file_path):
        with open(file_path, 'w') as file:
            json.dump(initial_data, file, indent=4)
    
    with open(file_path, 'r') as file:
        return json.load(file)

    


# Función para guardar datos en el archivo JSON
def guardar_datos():
    documents_folder = os.path.join(os.environ['USERPROFILE'], 'Documents')
    dydo_folder = os.path.join(documents_folder, 'Dydo')
    file_path = os.path.join(dydo_folder, 'data.json')
    with open(file_path, "w") as file:
        json.dump(data, file, indent=4)

# Cargar datos iniciales desde el archivo
data = cargar_datos()

# Configurar CustomTkinter
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

# Crear la ventana principal
app = ctk.CTk()
app.geometry("800x600")
app.title("Dydo")

# Hacer que la ventana principal sea redimensionable
app.grid_columnconfigure(1, weight=1)
app.grid_rowconfigure(0, weight=1)

# Variable para almacenar el índice del cliente seleccionado
cliente_seleccionado = None

# Función de validación para permitir solo números positivos
def solo_numeros(valor):
    if isinstance(valor, str) and not valor:
        return True
    return valor.isdigit()  # Solo permite dígitos (números positivos)

# Registro de la validación para usar en los Entry
validacion_numerica = app.register(solo_numeros)

# Función para agregar un cliente
def agregar_cliente():
    nombre = entry_nombre.get()
    cedula = entry_cedula.get()

    if nombre and cedula:
        for cliente in data["clientes"]:
            if cliente["nombre"] == nombre and cliente["cedula"] == cedula:
                messagebox.showinfo("Advertencia", "Ya existe un cliente con ese nombre y cédula")
                return
        nuevo_cliente = {"nombre": nombre, "cedula": cedula}
        data["clientes"].append(nuevo_cliente)
        guardar_datos()
        actualizar_tabla_clientes()
        actualizar_clientes_dropdown()
        entry_nombre.delete(0, "end")
        entry_cedula.delete(0, "end")
    else:
        messagebox.showinfo("Advertencia", "Por favor, complete ambos campos")

# Función para seleccionar un cliente en la tabla
def seleccionar_cliente(event):
    global cliente_seleccionado
    seleccion = tabla_clientes.selection()
    if seleccion:
        cliente_seleccionado = tabla_clientes.item(seleccion)["values"]
    else:
        cliente_seleccionado = None

# Función para borrar el cliente seleccionado
def borrar_cliente():
    global cliente_seleccionado
    cliente_global = cliente_seleccionado

    if cliente_seleccionado:
        for cliente in data["clientes"]:
            if cliente["nombre"] == cliente_global[0] and cliente["cedula"] == str(cliente_global[1]):
                data["clientes"].remove(cliente)
                guardar_datos()
                actualizar_tabla_clientes()
                actualizar_clientes_dropdown()
                cliente_seleccionado = None
                messagebox.showinfo("Eliminado", "Cliente eliminado con éxito.")
                return
    else:
        messagebox.showwarning("Advertencia", "Seleccione un cliente para borrar.")

# Función para actualizar la tabla de clientes
def actualizar_tabla_clientes():
    for row in tabla_clientes.get_children():
        tabla_clientes.delete(row)
    for cliente in data["clientes"]:
        tabla_clientes.insert("", "end", values=(cliente["nombre"], cliente["cedula"]))

# Función para actualizar el dropdown de clientes
def actualizar_clientes_dropdown():
    clientes = [cliente["nombre"] for cliente in data["clientes"]]
    dropdown_cliente.configure(values=clientes)

def obtener_cliente(nombre):
    clientes = data["clientes"]
    for cliente in clientes:
        if cliente["nombre"] == nombre:
            return cliente
    return None

# Función para agregar una factura
def agregar_factura():
    nombre_cliente = dropdown_cliente.get()
    cliente = obtener_cliente(nombre_cliente)
    numero_factura = entry_numero_factura.get()
    fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    saldo_total = entry_saldo_total.get()
    saldo_restante = saldo_total  # Saldo restante igual al saldo total inicialmente

    if cliente == None:
        messagebox.showwarning("Advertencia", "El cliente no existe.")
        return

    if nombre_cliente and numero_factura and saldo_total:
        for factura in data["facturas"]:
            if int(factura["numero_factura"]) == int(numero_factura):
                messagebox.showinfo("Advertencia", "Ya existe una factura con este número")
                return
        nueva_factura = {
            "nombre_cliente": nombre_cliente,
            "cedula_cliente": cliente["cedula"],
            "numero_factura": str(int(numero_factura)),
            "fecha": fecha,
            "saldo_total": saldo_total,
            "saldo_restante": saldo_restante
        }
        data["facturas"].append(nueva_factura)
        guardar_datos()
        actualizar_tabla_facturas()
        entry_numero_factura.delete(0, "end")
        entry_saldo_total.delete(0, "end")
    else:
        messagebox.showwarning("Advertencia", "Complete todos los campos para agregar una factura.")

# Función para actualizar la tabla de facturas
def actualizar_tabla_facturas():
    for row in tabla_facturas.get_children():
        tabla_facturas.delete(row)
    for factura in data["facturas"]:
        tabla_facturas.insert("", "end", values=(
            factura["nombre_cliente"],
            factura["cedula_cliente"],
            factura["numero_factura"],
            factura["fecha"],
            factura["saldo_total"],
            factura["saldo_restante"]
        ))

# Función para actualizar el dropdown de clientes
def actualizar_clientes_dropdown():
    clientes = [cliente["nombre"] for cliente in data["clientes"]]
    dropdown_cliente.configure(values=clientes)
    dropdown_cliente_abono.configure(values=clientes)

# Función para buscar facturas del cliente en el frame de abono
def buscar_facturas():
    cliente_nombre = dropdown_cliente_abono.get()
    cliente = obtener_cliente(cliente_nombre)
    if cliente:
        facturas_cliente = [factura for factura in data["facturas"] if factura["nombre_cliente"] == cliente_nombre]
        actualizar_tabla_abonos(facturas_cliente)
        btn_abonar.configure(state="normal")  # Habilitar el botón de abonar
    else:
        messagebox.showwarning("Advertencia", "Seleccione un cliente válido.")

# Función para actualizar la tabla en el frame de abono
def actualizar_tabla_abonos(facturas):
    for row in tabla_abonos.get_children():
        tabla_abonos.delete(row)
    for factura in facturas:
        tabla_abonos.insert("", "end", values=(
            factura["numero_factura"],
            factura["fecha"],
            factura["saldo_total"],
            factura["saldo_restante"]
        ))

# Función para calcular el saldo total pendiente de todas las facturas de un cliente
def obtener_saldo_total(cliente_nombre):
    return sum(float(factura["saldo_restante"]) for factura in data["facturas"] if factura["nombre_cliente"] == cliente_nombre)

# Función para abonar monto a las facturas del cliente seleccionado
def abonar_monto():
    cliente_nombre = dropdown_cliente_abono.get()
    monto_abonar = float(entry_monto_abonar.get())
    saldo_total = obtener_saldo_total(cliente_nombre)

    if monto_abonar > saldo_total:
        messagebox.showwarning("Advertencia", "El monto a abonar supera el saldo pendiente total.")
        return

    # Obtener las facturas pendientes en orden de antigüedad
    facturas_cliente = sorted(
        [factura for factura in data["facturas"] if factura["nombre_cliente"] == cliente_nombre],
        key=lambda x: x["fecha"]
    )

    for factura in facturas_cliente:
        saldo_restante = float(factura["saldo_restante"])
        if monto_abonar <= saldo_restante:
            factura["saldo_restante"] = saldo_restante - monto_abonar
            break
        else:
            factura["saldo_restante"] = 0.0
            monto_abonar -= saldo_restante

    guardar_datos()
    buscar_facturas()  # Actualizar la tabla después del abono
    entry_monto_abonar.delete(0, "end")

# Función para cambiar el contenido de la ventana según el apartado seleccionado
def mostrar_frame(frame):
    actualizar_tabla_clientes()
    actualizar_tabla_facturas()
    frame.tkraise()

#Función para verificar existencia de clientes para dropdown de facturas que retorne la lista de clientes:

def verificar_existencia_clientes():
    if not data["clientes"]: 
        return ["No Hay Clientes"]   
    return [cliente["nombre"] for cliente in data["clientes"]]



# Crear el sidebar (barra lateral)
sidebar = ctk.CTkFrame(app, width=200, fg_color="#ADD8E6")
sidebar.grid(row=0, column=0, sticky="ns")
sidebar.grid_propagate(False)

# Botón para clientes
btn_clientes = ctk.CTkButton(sidebar, text="Clientes", command=lambda: mostrar_frame(contenido_clientes))
btn_clientes.pack(pady=20, padx=10)

# Botón para factura
btn_factura = ctk.CTkButton(sidebar, text="Factura", command=lambda: mostrar_frame(contenido_factura))
btn_factura.pack(pady=20, padx=10)

# Botón para mostrar el frame de Abonar
btn_abono = ctk.CTkButton(sidebar, text="Abonar", command=lambda: mostrar_frame(contenido_abono))
btn_abono.pack(pady=20, padx=10)

# Crear el frame de contenido para clientes
contenido_clientes = ctk.CTkFrame(app, fg_color="white")
contenido_clientes.grid(row=0, column=1, sticky="nsew")
contenido_clientes.grid_columnconfigure(1, weight=1)
contenido_clientes.grid_rowconfigure(3, weight=1)

# Elementos dentro del frame de clientes
label_nombre = ctk.CTkLabel(contenido_clientes, text="Nombre:")
label_nombre.grid(row=0, column=0, padx=10, pady=5, sticky="e")

entry_nombre = ctk.CTkEntry(contenido_clientes)
entry_nombre.grid(row=0, column=1, padx=10, pady=5, sticky="ew")

label_cedula = ctk.CTkLabel(contenido_clientes, text="Cédula:")
label_cedula.grid(row=1, column=0, padx=10, pady=5, sticky="e")

# Campo de cédula solo numérico
entry_cedula = ctk.CTkEntry(contenido_clientes, validate="key", validatecommand=(validacion_numerica, "%P"))
entry_cedula.grid(row=1, column=1, padx=10, pady=5, sticky="ew")

btn_agregar = ctk.CTkButton(contenido_clientes, text="Agregar Cliente", command=agregar_cliente)
btn_agregar.grid(row=2, column=0, pady=10, padx=10)

btn_borrar = ctk.CTkButton(contenido_clientes, text="Borrar Cliente", command=borrar_cliente)
btn_borrar.grid(row=2, column=1, pady=10, padx=10)

tabla_clientes = ttk.Treeview(contenido_clientes, columns=("Nombre", "Cédula"), show="headings")
tabla_clientes.heading("Nombre", text="Nombre")
tabla_clientes.heading("Cédula", text="Cédula")
tabla_clientes.grid(row=3, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")

tabla_clientes.bind("<<TreeviewSelect>>", seleccionar_cliente)

# Crear el frame de contenido para factura
contenido_factura = ctk.CTkFrame(app, fg_color="white")
contenido_factura.grid(row=0, column=1, sticky="nsew")
contenido_factura.grid_columnconfigure(1, weight=1)
contenido_factura.grid_rowconfigure(5, weight=1)

# Elementos dentro del frame de facturas
label_cliente = ctk.CTkLabel(contenido_factura, text="Cliente:")
label_cliente.grid(row=0, column=0, padx=10, pady=5, sticky="e")

dropdown_cliente = ctk.CTkComboBox(contenido_factura, values=verificar_existencia_clientes())
dropdown_cliente.grid(row=0, column=1, padx=10, pady=5, sticky="ew")

label_numero_factura = ctk.CTkLabel(contenido_factura, text="Número de Factura:")
label_numero_factura.grid(row=2, column=0, padx=10, pady=5, sticky="e")

entry_numero_factura = ctk.CTkEntry(contenido_factura, validate="key", validatecommand=(validacion_numerica, "%P"))
entry_numero_factura.grid(row=2, column=1, padx=10, pady=5, sticky="ew")

label_saldo_total = ctk.CTkLabel(contenido_factura, text="Saldo Total:")
label_saldo_total.grid(row=3, column=0, padx=10, pady=5, sticky="e")

# Campo de saldo total solo numérico
entry_saldo_total = ctk.CTkEntry(contenido_factura, validate="key", validatecommand=(validacion_numerica, "%P"))
entry_saldo_total.grid(row=3, column=1, padx=10, pady=5, sticky="ew")

btn_agregar_factura = ctk.CTkButton(contenido_factura, text="Agregar Factura", command=agregar_factura)
btn_agregar_factura.grid(row=4, column=0, columnspan=2, pady=10, padx=10)

# Creación de la tabla
tabla_facturas = ttk.Treeview(contenido_factura, columns=("Cliente", "Cédula", "N° Factura", "Fecha", "Saldo Total", "Saldo Restante"), show="headings")

# Configuración de encabezados y ajuste de ancho para cada columna
columnas = {
    "Cliente": 100,
    "Cédula": 50,
    "N° Factura": 50,
    "Fecha": 100,
    "Saldo Total": 50,
    "Saldo Restante": 50
}

for col, ancho in columnas.items():
    tabla_facturas.heading(col, text=col)
    tabla_facturas.column(col, width=ancho)

# Posicionamiento de la tabla
tabla_facturas.grid(row=5, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")

# Frame de Abono
contenido_abono = ctk.CTkFrame(app, fg_color="white")
contenido_abono.grid(row=0, column=1, sticky="nsew")
contenido_abono.grid_columnconfigure(1, weight=1)
contenido_abono.grid_rowconfigure(4, weight=1)

# Elementos dentro del frame de abono
label_cliente_abono = ctk.CTkLabel(contenido_abono, text="Cliente:")
label_cliente_abono.grid(row=0, column=0, padx=10, pady=5, sticky="e")

dropdown_cliente_abono = ctk.CTkComboBox(contenido_abono, values=[cliente["nombre"] for cliente in data["clientes"]])
dropdown_cliente_abono.grid(row=0, column=1, padx=10, pady=5, sticky="ew")

label_monto_abonar = ctk.CTkLabel(contenido_abono, text="Monto a Abonar:")
label_monto_abonar.grid(row=1, column=0, padx=10, pady=5, sticky="e")

entry_monto_abonar = ctk.CTkEntry(contenido_abono, validate="key", validatecommand=(validacion_numerica, "%P"))
entry_monto_abonar.grid(row=1, column=1, padx=10, pady=5, sticky="ew")

btn_buscar = ctk.CTkButton(contenido_abono, text="Buscar", command=buscar_facturas)
btn_buscar.grid(row=2, column=0, pady=10, padx=10)

btn_abonar = ctk.CTkButton(contenido_abono, text="Abonar", command=abonar_monto, state="disabled")
btn_abonar.grid(row=2, column=1, pady=10, padx=10)

# Tabla para mostrar las facturas en el frame de abono
tabla_abonos = ttk.Treeview(contenido_abono, columns=("N° Factura", "Fecha", "Saldo Total", "Saldo Restante"), show="headings")
for col in ("N° Factura", "Fecha", "Saldo Total", "Saldo Restante"):
    tabla_abonos.heading(col, text=col)
    tabla_abonos.column(col, width=100)
tabla_abonos.grid(row=3, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")

# Cargar los datos iniciales en la tabla de clientes y facturas
actualizar_tabla_clientes()
actualizar_tabla_facturas()

# Mostrar el frame de clientes al iniciar la aplicación
mostrar_frame(contenido_clientes)

# Ejecutar la aplicación
app.mainloop()
