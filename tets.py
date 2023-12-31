from tkinter import *
from datetime import datetime
from tkinter import messagebox
from tkcalendar import DateEntry 
import mysql.connector

ventana = Tk()

# Creacion de la clase Tarea y sus atributos
class Tarea:
    def __init__(self, titulo, descripcion, fecha_vencimiento):
        self.titulo = titulo
        self.descripcion = descripcion
        self.fecha_vencimiento = fecha_vencimiento
        self.completada = BooleanVar()  # Crear una BooleanVar separada para cada tarea
        self.completada.set(False)  # Inicializar como no completada

# Definicion de variables
lista_tareas = []
checkboxes = []
usuario_id = None

# Traer todos los datos de un usuario
def cargar_tareas_desde_db():
    global usuario_id
    lista_tareas.clear() 
    if usuario_id:
        try:
            iniciobd()
            cursor1.execute("SELECT titulo, descripcion, fecha_venc, completada FROM tareas WHERE user = %s", (usuario_id,))
            tareas = cursor1.fetchall()
            for tarea_data in tareas:
                titulo, descripcion, fecha_vencimiento, completada = tarea_data
                tarea = Tarea(titulo, descripcion, fecha_vencimiento)
                tarea.completada.set(completada)
                lista_tareas.append(tarea)
        except mysql.connector.Error as error:
            messagebox.showerror("Error", f"Error al cargar las tareas desde la base de datos: {error}")
        finally:
            cierrebd()

# Funcion para mostrar el estado de las tareas
def mostrar_estado_tareas():
    # Borrar cualquier widget existente
    for widget in texto.winfo_children():
        widget.destroy()

    # Obtener datos de la base de datos y llenar la lista de tareas
    cargar_tareas_desde_db()

    for i, tarea in enumerate(lista_tareas, start=1):
        tarea_texto = tarea.titulo
        tarea_checkbox = Checkbutton(texto, text=tarea_texto)
        tarea_checkbox.pack(anchor=W)

        tarea_checkbox.var = tarea.completada  # Almacenar la variable BooleanVar en la casilla de verificacion

        # Verificar el valor de completada y establecer el estado del checkbox por consecuencia
        if tarea.completada.get() == 1:
            tarea_checkbox.select()  # Checkbox seleccionado
        else:
            tarea_checkbox.deselect()  # Checkbox no seleccionado

        # Agregar un evento para actualizar el estado de la tarea
        tarea_checkbox.bind("<Button-1>", lambda event, tarea=tarea, checkbox=tarea_checkbox: actualizar_estado_tarea(tarea, checkbox))

    texto.pack()

# Agregar funcion para actualizar el estado de la tarea
def actualizar_estado_tarea(tarea, checkbox):
    tarea.completada.set(not tarea.completada.get())

    try:
        iniciobd()
        sql = "UPDATE tareas SET completada = %s WHERE titulo = %s AND user = %s"
        datos = (tarea.completada.get(), tarea.titulo, usuario_id)
        cursor1.execute(sql, datos)
        conexion1.commit()

        checkbox.var.set(tarea.completada.get())
    except mysql.connector.Error as error:
        messagebox.showerror("Error", f"Error al actualizar el estado de la tarea: {error}")
    finally:
        cierrebd()

# Funcion para mostrar los campos de entrada (boton 1)
def mostrar_campos_de_entrada():
    # Borrar cualquier widget existente
    for widget in texto.winfo_children():
        widget.destroy()

    titulo_label.pack()
    titulo_entry.pack()
    titulo_entry.pack(pady=10)

    descripcion_label.pack()
    descripcion_entry.pack()
    descripcion_entry.pack(pady=10)

    fecha_vencimiento_label.pack()
    fecha_vencimiento_entry.pack()
    fecha_vencimiento_entry.pack(pady=10)

    submit.pack()

def iniciobd():
    global conexion1,cursor1
    conexion1 = mysql.connector.connect(host="localhost", user="root", passwd="", database="lpr")
    cursor1 = conexion1.cursor()

def cierrebd():
    cursor1.close()
    conexion1.close()

# Funcion para agregar tareas a la lista
def agregar_tarea_a_lista():
    global usuario_id
    titulo = titulo_entry.get()
    descripcion = descripcion_entry.get()
    fecha_vencimiento_str = fecha_vencimiento_entry.get_date()  # Obtener la fecha del DateEntry
    fecha_vencimiento = fecha_vencimiento_str.strftime('%Y-%m-%d')  # Convertir la fecha a cadena
    if usuario_id and titulo and descripcion and fecha_vencimiento:
        tarea = Tarea(titulo, descripcion, fecha_vencimiento)
        lista_tareas.append(tarea)

        try:
            iniciobd()
            sql = "INSERT INTO tareas (titulo, descripcion, fecha_venc, user, completada) VALUES (%s, %s, %s, %s, %s)"
            datos = (titulo, descripcion, fecha_vencimiento_str, usuario_id, False)  
            cursor1.execute(sql, datos)
            conexion1.commit()
        except mysql.connector.Error as error:
            messagebox.showerror("Error", f"Error al agregar la tarea: {error}")
        finally:
            cierrebd()

        # Limpiar los entry widgets despues de agregar una tarea
        titulo_entry.delete(0, END)
        descripcion_entry.delete(0, END)
        fecha_vencimiento_entry.set_date(datetime.now())  # Restablecer la fecha al dia actual
        fecha_act = datetime.now()
    else:
        messagebox.showinfo("Campos vacios", "Por favor, complete todos los campos.")

# Funcion para mostrar las tareas (boton 2)
def mostrar_tareas():
    # Borrar cualquier widget previo
    for widget in texto.winfo_children():
        widget.destroy()

    tarea_texto = []  # Usar una lista para almacenar las descripciones de las tareas
    # Crear un Frame para contener el Listbox y la barra de desplazamiento
    frame = Frame(texto)
    frame.pack(padx=10, pady=10, expand=YES, fill=BOTH)

    # Crear un Listbox y asociarlo con la barra de desplazamiento
    tarea_listbox = Listbox(frame, width=70, height=20)
    tarea_listbox.pack(side=LEFT, fill=BOTH, expand=YES)

    # Crear una barra de desplazamiento y asociarla al Listbox
    scrollbar = Scrollbar(frame, orient=VERTICAL, command=tarea_listbox.yview)
    scrollbar.pack(side=RIGHT, fill=Y)
    tarea_listbox.config(yscrollcommand=scrollbar.set)
    iniciobd()
    cursor1.execute(f"SELECT titulo, descripcion, fecha_venc, completada FROM tareas WHERE user = {usuario_id}")
    tareas = cursor1.fetchall()
    cierrebd()

    for i, tarea_data in enumerate(tareas, start=1):
        titulo, descripcion, fecha_vencimiento, completada = tarea_data

        tarea = Tarea(titulo, descripcion, fecha_vencimiento)
        tarea.completada.set(completada)
        tarea_texto = f'Tarea {i}:\n'
        tarea_listbox.insert(END, tarea_texto)
        tarea_texto = f'Título: {tarea.titulo}\n'
        tarea_listbox.insert(END, tarea_texto)
        tarea_texto = f'Descripción: {tarea.descripcion}\n'
        tarea_listbox.insert(END, tarea_texto)
        tarea_texto = f'Fecha de Vencimiento: {tarea.fecha_vencimiento}\n'
        tarea_listbox.insert(END, tarea_texto)
        tarea_texto = f'Estado: {"Completa" if tarea.completada.get() else "Incompleta"}\n\n'
        tarea_listbox.insert(END, tarea_texto)
        tarea_texto = " "
        tarea_listbox.insert(END, tarea_texto)

    tarea_listbox.pack(expand=YES, fill=BOTH)

    # Unir las descripciones de las tareas en una sola cadena
    tarea_texto = "".join(tarea_texto)

    texto.config(text=tarea_texto)
    texto.pack()

# Menu de botones
def botones_opc(opcion):
    texto.config(text="")
    texto.pack_forget()
    titulo_label.pack_forget()
    titulo_entry.pack_forget()
    descripcion_label.pack_forget()
    descripcion_entry.pack_forget()
    fecha_vencimiento_label.pack_forget()
    fecha_vencimiento_entry.pack_forget()
    submit.pack_forget()
    if opcion == 1:
        mostrar_campos_de_entrada()
    elif opcion == 2:
        mostrar_tareas()
    elif opcion == 3:
        mostrar_estado_tareas()

def register():
    a = usuario_register.get()
    b = contrasena_register.get()
    usuario_register.pack_forget()
    contrasena_register.pack_forget()
    iniciobd()
    sql="insert into users(usuario, contra) values (%s,%s)"
    datos=(a,b)
    cursor1.execute(sql, datos)
    conexion1.commit()
    cierrebd()
    principal()

def login():
    global usuario_id
    iniciobd()
    cursor1.execute("SELECT ID FROM users WHERE usuario = %s AND contra = %s", (usuario_login.get(), contrasena_login.get()))
    user_data = cursor1.fetchone()
    if user_data:
        usuario_id = user_data[0]
        cierrebd()
        principal()
    else:
        cierrebd()
        messagebox.showwarning("", "Usuario no encontrado")
            
def principal():
    wasd="800x500"
    ventana.geometry(f"{wasd}")
    # Creacion de los botones de navegacion
    titulo.pack_forget()
    usuario_label1.pack_forget()
    contrasena_label1.pack_forget()
    usuario_login.pack_forget()
    contrasena_login.pack_forget()
    usuario_label.pack_forget()
    contrasena_label.pack_forget()
    boto1.pack_forget()
    boto2.pack_forget()
    boto4.pack_forget()
    enviar.pack_forget()

    global contenedor_botones, titulo_label, titulo_entry, descripcion_entry, descripcion_label, submit, fecha_vencimiento_entry, fecha_vencimiento_label, texto
    texto = Label(ventana, text="", font=("Helvetica", 12))
    contenedor_botones = Frame(ventana)
    contenedor_botones.pack(pady=20)
    boton1 = Button(contenedor_botones, text="Agregar tareas", command=lambda: botones_opc(1))
    boton2 = Button(contenedor_botones, text="Mostrar tareas", command=lambda: botones_opc(2))
    boton3 = Button(contenedor_botones, text="Estado de tareas", command=lambda: botones_opc(3))
    boton4 = Button(contenedor_botones, text="Salir", command=lambda: salida())
    boton1.pack(side=LEFT, padx=10)
    boton2.pack(side=LEFT, padx=10)
    boton3.pack(side=LEFT, padx=10)
    boton4.pack(side=LEFT, padx=10)

    # Creacion de etiquetas y campos de entrada para tareas
    titulo_label = Label(ventana, text="Titulo")
    titulo_label.pack()
    titulo_entry = Entry(ventana)
    titulo_entry.pack()
    titulo_entry.pack(pady=10)

    descripcion_label = Label(ventana, text="Descripcion")
    descripcion_label.pack()
    descripcion_entry = Entry(ventana)
    descripcion_entry.pack()
    descripcion_entry.pack(pady=10)

    # Creacion del calendario
    fecha_vencimiento_label = Label(ventana, text="Fecha de Vencimiento")
    fecha_vencimiento_label.pack()
    fecha_vencimiento_entry = DateEntry(ventana, date_pattern="yyyy-mm-dd")  # Usamos el DateEntry de Tkcalendar
    fecha_vencimiento_entry.pack()
    fecha_vencimiento_entry.pack(pady=10)

    submit = Button(ventana, text="Guardar", command=agregar_tarea_a_lista)
    submit.pack()

titulo = Label(text="")
usuario_label1 = Label(text="Nombre de usuario")
usuario_login = Entry(ventana)
contrasena_label1 = Label(text="Contraseña")
contrasena_login = Entry(ventana)
enviar = Button(text="Enviar", command=login)

usuario_label = Label(text="Nombre de usuario")
usuario_register = Entry(ventana)
contrasena_label = Label(text="Contraseña")
contrasena_register = Entry(ventana)
enviar_register = Button(text="Enviar", command=register)

def log_opc(opcion):
    usuario_label1.pack_forget()
    usuario_login.pack_forget()
    contrasena_label1.pack_forget()
    contrasena_login.pack_forget()
    enviar.pack_forget()
    usuario_label.pack_forget()
    usuario_register.pack_forget()
    contrasena_label.pack_forget()
    contrasena_register.pack_forget()
    enviar_register.pack_forget()
    titulo.pack()

    if opcion == 1:
        titulo.config(text="Iniciar sesion", font=('Helvetica', 15))
        usuario_label1.pack()
        usuario_login.pack(pady=5)
        contrasena_label1.pack()
        contrasena_login.pack()
        enviar.pack()

    elif opcion == 2:
        titulo.config(text="Registrate", font=('Helvetica', 15))
        usuario_label.pack()
        usuario_register.pack(pady=5)
        contrasena_label.pack()
        contrasena_register.pack()
        enviar_register.pack()

def salida():
    check = messagebox.askquestion("Salida", "Estas seguro que quieres salir?")
    if check == "yes":
        ventana.quit()	
# Creacion de la ventana principal
wasd = "400x400"
ventana.title("Michi Notes")                                                   
ventana.geometry(f"{wasd}")

contenedor_botones = Frame(ventana)
contenedor_botones.pack(pady=20)
boto1 = Button(contenedor_botones, text="Iniciar sesion", command=lambda: log_opc(1))
boto2 = Button(contenedor_botones, text="Registrate", command=lambda: log_opc(2))
boto4 = Button(contenedor_botones, text="Salir", command= lambda: salida())
boto1.pack(side=LEFT, padx=10)
boto2.pack(side=LEFT, padx=10)
boto4.pack(side=LEFT, padx=10)

cargar_tareas_desde_db()

# Iniciar la interfaz
ventana.mainloop()

