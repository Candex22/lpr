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

# Definición de variables
lista_tareas = []
checkboxes = []

# Funcion para mostrar el estado de las tareas
def mostrar_estado_tareas():
    # Borrar cualquier widget
    for widget in texto.winfo_children():
        widget.destroy()

    for i, tarea in enumerate(lista_tareas, start=1):
        tarea_texto = f"Tarea {i}: {tarea.titulo}"
        tarea_checkbox = Checkbutton(texto, text=tarea_texto, variable=tarea.completada)
        tarea_checkbox.pack(anchor=W)

        # Agregar un evento de cambio de estado al checkbox
        tarea_checkbox.bind("<Button-1>", lambda event, tarea=tarea: actualizar_estado_tarea(tarea, tarea_checkbox))

    texto.pack()

# Agregar funcion para actualizar el estado de la tarea
def actualizar_estado_tarea(tarea, checkbox):
    tarea.completada.set(['selected'])

# Funcion para mostrar los campos de entrada (boton 1)
def mostrar_campos_de_entrada():
    # Borrar cualquier widget
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
    global conexion1, cursor1
    conexion1 = mysql.connector.connect(host="localhost", user="root", passwd="", database="lpr")
    cursor1 = conexion1.cursor()

def cierrebd():
    cursor1.close()
    conexion1.close()


# Funcion para agregar tareas a la lista
def agregar_tarea_a_lista():
    titulo = titulo_entry.get()
    descripcion = descripcion_entry.get()
    fecha_vencimiento_str = fecha_vencimiento_entry.get_date()  # Obtenemos la fecha del DateEntry
    fecha_vencimiento = fecha_vencimiento_str.strftime('%Y-%m-%d')  # Convertimos la fecha a cadena
    usuario_id = 5  # Reemplaza con el ID del usuario correcto

    if titulo and descripcion and fecha_vencimiento:
        tarea = Tarea(titulo, descripcion, fecha_vencimiento)
        lista_tareas.append(tarea)
        
        # Guardar la tarea en la base de datos
        try:
            iniciobd()
            sql = "INSERT INTO tareas (titulo, descripcion, fecha_venc, user) VALUES (%s, %s, %s, %s)"
            datos = (titulo, descripcion, fecha_vencimiento_str, usuario_id)
            cursor1.execute(sql, datos)
            conexion1.commit()
        except mysql.connector.Error as error:
            messagebox.showerror("Error", f"Error al agregar la tarea: {error}")
        finally:
            cierrebd()

        # Limpiar los entry widgets despues de agregar una tarea
        titulo_entry.delete(0, END)
        descripcion_entry.delete(0, END)
        fecha_vencimiento_entry.set_date(datetime.now())  # Resetear la fecha al día actual
    else:
        messagebox.showwarning("Campos vacios", "Por favor, complete todos los campos.")



# Funcion para mostrar las tareas (boton 2)
def mostrar_tareas():
    # Borrar cualquier widget previo
    for widget in texto.winfo_children():
        widget.destroy()
    
    tarea_texto = ""

    for i, tarea in enumerate(lista_tareas, start=1):
        tarea_texto += f"Tarea {i}:\n"
        tarea_texto += f"Titulo: {tarea.titulo}\n"
        tarea_texto += f"Descripcion: {tarea.descripcion}\n"
        
        if tarea.completada.get() == False:
            tarea_texto += "Estado: Incompleto\n"
        else:
            tarea_texto += "Estado: Completo\n"
        
        tarea_texto += f"Fecha de Vencimiento: {tarea.fecha_vencimiento}\n\n"

    texto.config(text=tarea_texto)
    texto.pack()


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
    iniciobd()
    sql="insert into users(usuario, contra) values (%s,%s)"
    datos=(a,b)
    cursor1.execute(sql, datos)
    conexion1.commit()
    cierrebd()

def login():
    global usuario_actual
    iniciobd()
    cursor1.execute("select usuario, contra FROM users")
    rows = cursor1.fetchall()
    a = usuario_login.get()
    usuario_actual = a
    b = contrasena_login.get()
    check = 0
    for row in rows:
        if a == row[0] and b == row[1]:
            check = 1
            cierrebd()
            principal()
            break
        else:
            check = 2
    if check == 2:
        messagebox.showwarning("","Usuario no encontrado")
            
    

def principal():
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
        boton4 = Button(contenedor_botones, text="Salir", command=lambda: ventana.quit())
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

        #Creacion del calendario
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
enviar = Button(text="enviar", command=login)

usuario_label = Label(text="Nombre de usuario")
usuario_register = Entry(ventana)
contrasena_label = Label(text="Contraseña")
contrasena_register = Entry(ventana)
enviar_register = Button(text="enviar", command=register)

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

# Creacion de la ventana principal
ventana.title("Trabajo programacion")
ventana.geometry("600x800")

contenedor_botones = Frame(ventana)
contenedor_botones.pack(pady=20)
boto1 = Button(contenedor_botones, text="Iniciar sesion", command=lambda: log_opc(1))
boto2 = Button(contenedor_botones, text="Registrate", command=lambda: log_opc(2))
boto4 = Button(contenedor_botones, text="Salir", command=lambda: ventana.quit())
boto1.pack(side=LEFT, padx=10)
boto2.pack(side=LEFT, padx=10)
boto4.pack(side=LEFT, padx=10)

# Iniciar la interfaz
ventana.mainloop()