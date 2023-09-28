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
