
from tkinter import ttk  # Importar ttk para usar Treeview

# Resto del código...

def mostrar_tareas():
    # Borrar cualquier widget previo
    for widget in texto.winfo_children():
        widget.destroy()

    # Obtener datos de la base de datos y llenar la lista de tareas
    cargar_tareas_desde_db()

    # Crear Treeview para mostrar las tareas en una vista similar a un explorador de archivos
    tarea_treeview = ttk.Treeview(texto, columns=("Título", "Descripción", "Fecha de Vencimiento", "Estado"), show="headings")
    tarea_treeview.heading("Título", text="Título")
    tarea_treeview.heading("Descripción", text="Descripción")
    tarea_treeview.heading("Fecha de Vencimiento", text="Fecha de Vencimiento")
    tarea_treeview.heading("Estado", text="Estado")

    for i, tarea in enumerate(lista_tareas, start=1):
        estado = "Completa" if tarea.completada.get() else "Incompleta"
        tarea_treeview.insert("", "end", values=(tarea.titulo, tarea.descripcion, tarea.fecha_vencimiento, estado))

    # Ajustar el ancho de las columnas
    for col in ("Título", "Descripción", "Fecha de Vencimiento", "Estado"):
        tarea_treeview.column(col, width=150, anchor="center")
        tarea_treeview.heading(col, text=col)

    tarea_treeview.pack(expand=YES, fill=BOTH)

# Resto del código...

# Iniciar la interfaz
ventana.mainloop()
