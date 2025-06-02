import tkinter as tk
from tkinter import messagebox

class InterfazUsuario:
    def __init__(self, root):
        self.root = root
        self.root.title("🎵 Reproductor Musical")
        self.root.configure(bg="#1e1e1e")
        self.controlador = None

        # Contenedor principal
        frame = tk.Frame(self.root, bg="#1e1e1e", padx=20, pady=20)
        frame.grid(sticky="nsew")

        # URL y botón descargar
        self.entrada_url = tk.Entry(frame, width=50, bg="#292929", fg="#ffffff", insertbackground="#ffffff", relief="flat")
        self.entrada_url.grid(row=0, column=0, columnspan=2, sticky="ew", pady=(0, 10))

        self.boton_descargar = self._crear_boton(frame, "⬇ Descargar canción", self.descargar)
        self.boton_descargar.grid(row=0, column=2, padx=(10, 0), pady=(0, 10))

        # Buscador
        self.buscador = tk.Entry(frame, width=50, bg="#292929", fg="#ffffff", insertbackground="#ffffff", relief="flat")
        self.buscador.grid(row=1, column=0, columnspan=2, sticky="ew", pady=(0, 10))
        self.buscador.bind("<KeyRelease>", lambda e: self.filtrar())

        # Filtros
        botones_filtro = tk.Frame(frame, bg="#1e1e1e")
        botones_filtro.grid(row=1, column=0, columnspan=3, sticky="w", pady=(0, 10))

        self.boton_favoritas = self._crear_boton(botones_filtro, "❤️ Favoritas", self.mostrar_favoritas)
        self.boton_favoritas.pack(side="left", padx=5)

        self.boton_todas = self._crear_boton(botones_filtro, "🔁 Mostrar todas", self.mostrar_todas)
        self.boton_todas.pack(side="left", padx=5)

        self.boton_editar = self._crear_boton(botones_filtro, "✏️ Editar", self.editar)
        self.boton_editar.pack(side="left", padx=5)

        # Lista de canciones
        self.lista_canciones = tk.Listbox(frame, width=70, height=10, bg="#292929", fg="#ffffff", selectbackground="#444444", relief="flat")
        self.lista_canciones.grid(row=2, column=0, columnspan=3, sticky="nsew", pady=(0, 10))
        self.lista_canciones.bind("<<ListboxSelect>>", self.actualizar_texto_boton_fav)

        # Controles multimedia
        controles = tk.Frame(frame, bg="#1e1e1e")
        controles.grid(row=3, column=0, columnspan=3)

        self.boton_anterior = self._crear_boton(controles, "⏮", self.reproducir_anterior)
        self.boton_anterior.grid(row=0, column=0, padx=2, pady=5)

        self.boton_play = self._crear_boton(controles, "▶", self.reproducir)
        self.boton_play.grid(row=0, column=1, padx=2, pady=5)

        self.boton_pausa = self._crear_boton(controles, "⏸", self.pausar)
        self.boton_pausa.grid(row=0, column=2, padx=2, pady=5)

        self.boton_detener = self._crear_boton(controles, "⏹", self.detener)
        self.boton_detener.grid(row=0, column=3, padx=2, pady=5)

        self.boton_siguiente = self._crear_boton(controles, "⏭", self.reproducir_siguiente)
        self.boton_siguiente.grid(row=0, column=4, padx=2, pady=5)

        self.boton_fav = self._crear_boton(controles, "⭐ Marcar favorita", self.marcar_favorita)
        self.boton_fav.grid(row=1, column=0, padx=5, pady=(10,0))

        self.boton_eliminar = self._crear_boton(controles, "🗑 Eliminar", self.eliminar)
        self.boton_eliminar.grid(row=1, column=1, pady=(10, 0))

        self.boton_agregar_lista = self._crear_boton(controles, "➕ Agregar a lista", self.agregar_a_lista)
        self.boton_agregar_lista.grid(row=1, column=2, pady=(10, 0))


        # Listas de reproducción
        self.boton_crear_lista = self._crear_boton(controles, "📝 Crear Lista", self.abrir_ventana_crear_lista)
        self.boton_crear_lista.grid(row=1, column=3, pady=(10, 0))

        self.boton_ver_lista = self._crear_boton(controles, "📂 Ver Lista", self.abrir_ventana_ver_lista)
        self.boton_ver_lista.grid(row=1, column=4, pady=(10, 0))

        # Variables internas
        self.canciones_mostradas = []

    def _crear_boton(self, parent, texto, comando):
        return tk.Button(parent, text=texto, command=comando, bg="#2d2d2d", fg="white", activebackground="#3e3e3e", relief="flat", width=16)

    def set_controlador(self, controlador):
        self.controlador = controlador
        self.mostrar_todas()

    def descargar(self):
        url = self.entrada_url.get()
        if url:
            self.controlador.descargar_cancion(url)
        else:
            self.mostrar_mensaje("⚠️ Ingresa una URL válida.")

    def agregar_a_lista(self, cancion):
        self.canciones_mostradas.append(cancion)
        self.actualizar_lista()

    def actualizar_lista(self):
        self.lista_canciones.delete(0, tk.END)
        max_titulo = max((len(c.titulo) for c in self.canciones_mostradas), default=10)
        max_artista = max((len(c.artista) for c in self.canciones_mostradas), default=10)

        for c in self.canciones_mostradas:
            titulo = c.titulo.ljust(max_titulo + 5)
            artista = c.artista.ljust(max_artista + 5)
            favorito = "❤️" if c.favorito else ""
            self.lista_canciones.insert(tk.END, f"{titulo} {artista} {favorito}")

    def filtrar(self):
        texto = self.buscador.get().lower()
        canciones = self.controlador.filtrar_por_texto(texto)
        self.canciones_mostradas = canciones
        self.actualizar_lista()

    def mostrar_favoritas(self):
        self.canciones_mostradas = self.controlador.obtener_favoritas()
        self.actualizar_lista()

    def mostrar_todas(self):
        self.canciones_mostradas = self.controlador.obtener_todas()
        self.actualizar_lista()

    def reproducir(self):
        seleccion = self.lista_canciones.curselection()
        if seleccion:
            self.controlador.reproducir_cancion(seleccion[0])
        else:
            self.mostrar_mensaje("⚠️ Selecciona una canción.")

    def pausar(self):
        self.controlador.pausar()

    def detener(self):
        self.controlador.detener()

    def marcar_favorita(self):
        seleccion = self.lista_canciones.curselection()
        if seleccion:
            self.controlador.marcar_favorita(seleccion[0])
            self.actualizar_lista()
            self.actualizar_texto_boton_fav()

    def eliminar(self):
        seleccion = self.lista_canciones.curselection()
        if seleccion:
            index = seleccion[0]
            cancion = self.canciones_mostradas[index]
            self.controlador.eliminar_cancion_objeto(cancion)
            self.mostrar_todas()  # O recargar la lista actual si quieres mantener el filtro o lista
            self.actualizar_texto_boton_fav()

    def editar(self):
        seleccion = self.lista_canciones.curselection()
        if not seleccion:
            self.mostrar_mensaje("⚠️ Selecciona una canción para editar.")
            return

        index = seleccion[0]
        cancion = self.canciones_mostradas[index]

        ventana = tk.Toplevel(self.root)
        ventana.title("Editar Canción")
        ventana.configure(bg="#1e1e1e")

        tk.Label(ventana, text="Título:", bg="#1e1e1e", fg="white").grid(row=0, column=0, padx=10, pady=10)
        entrada_titulo = tk.Entry(ventana, bg="#292929", fg="white", insertbackground="white")
        entrada_titulo.grid(row=0, column=1, padx=10, pady=10)
        entrada_titulo.insert(0, cancion.titulo)

        tk.Label(ventana, text="Artista:", bg="#1e1e1e", fg="white").grid(row=1, column=0, padx=10, pady=10)
        entrada_artista = tk.Entry(ventana, bg="#292929", fg="white", insertbackground="white")
        entrada_artista.grid(row=1, column=1, padx=10, pady=10)
        entrada_artista.insert(0, cancion.artista)

        def guardar():
            nuevo_titulo = entrada_titulo.get().strip()
            nuevo_artista = entrada_artista.get().strip()
            if not nuevo_titulo or not nuevo_artista:
                self.mostrar_mensaje("⚠️ No puedes dejar campos vacíos.")
                return
            self.controlador.editar_cancion(index, nuevo_titulo, nuevo_artista)
            self.actualizar_lista()
            ventana.destroy()

        tk.Button(ventana, text="Guardar", command=guardar, bg="#2d2d2d", fg="white").grid(row=2, column=0, columnspan=2, pady=10)

    def actualizar_texto_boton_fav(self, event=None):
        seleccion = self.lista_canciones.curselection()
        if seleccion:
            index = seleccion[0]
            cancion = self.canciones_mostradas[index]
            self.boton_fav.config(text="💔 Quitar favorita" if cancion.favorito else "⭐ Marcar favorita")
        else:
            self.boton_fav.config(text="⭐ Marcar favorita")

    def mostrar_mensaje(self, texto):
        messagebox.showinfo("Información", texto)

    def abrir_ventana_crear_lista(self):
        ventana = tk.Toplevel(self.root)
        ventana.title("Crear Lista de Reproducción")
        ventana.configure(bg="#1e1e1e")

        tk.Label(ventana, text="Nombre:", bg="#1e1e1e", fg="white").pack(pady=5)
        entrada = tk.Entry(ventana, bg="#292929", fg="white")
        entrada.pack(pady=5)

        def crear():
            nombre = entrada.get().strip()
            if nombre:
                self.controlador.crear_lista(nombre)
                ventana.destroy()
            else:
                self.mostrar_mensaje("⚠️ El nombre no puede estar vacío.")

        tk.Button(ventana, text="Crear", command=crear, bg="#2d2d2d", fg="white").pack(pady=10)

    def abrir_ventana_ver_lista(self):
        listas = self.controlador.obtener_nombres_listas()
        if not listas:
            self.mostrar_mensaje("⚠️ No hay listas disponibles.")
            return

        ventana = tk.Toplevel(self.root)
        ventana.title("Listas de Reproducción")
        ventana.configure(bg="#1e1e1e")

        lista_listbox = tk.Listbox(ventana, bg="#292929", fg="white")
        lista_listbox.pack(padx=10, pady=10)

        for nombre in listas:
            lista_listbox.insert(tk.END, nombre)

        def ver_lista():
            seleccion = lista_listbox.curselection()
            if seleccion:
                nombre_lista = lista_listbox.get(seleccion[0])
                canciones = self.controlador.obtener_canciones_de_lista(nombre_lista)
                self.canciones_mostradas = canciones
                self.lista_actual = nombre_lista  
                self.actualizar_lista()
                ventana.destroy()

        def eliminar_lista():
            seleccion = lista_listbox.curselection()
            if seleccion:
                nombre = lista_listbox.get(seleccion[0])
                self.controlador.eliminar_lista(nombre)
                ventana.destroy()

        tk.Button(ventana, text="Ver canciones", command=ver_lista, bg="#2d2d2d", fg="white").pack(pady=5)
        tk.Button(ventana, text="🗑 Eliminar lista", command=eliminar_lista, bg="#882222", fg="white").pack(pady=5)
        
    def agregar_a_lista(self):
        seleccion = self.lista_canciones.curselection()
        if not seleccion:
            self.mostrar_mensaje("⚠️ Selecciona una canción primero.")
            return

        index_cancion = seleccion[0]
        listas = self.controlador.obtener_nombres_listas()

        if not listas:
            self.mostrar_mensaje("⚠️ No hay listas creadas.")
            return

        ventana = tk.Toplevel(self.root)
        ventana.title("Seleccionar Lista")
        ventana.configure(bg="#1e1e1e")

        tk.Label(ventana, text="Selecciona una lista:", bg="#1e1e1e", fg="white").pack(pady=5)
        listbox = tk.Listbox(ventana, bg="#292929", fg="white")
        listbox.pack(padx=10, pady=10)

        for nombre in listas:
            listbox.insert(tk.END, nombre)

        def confirmar():
            seleccion_lista = listbox.curselection()
            if not seleccion_lista:
                self.mostrar_mensaje("⚠️ Selecciona una lista.")
                return
            nombre_lista = listbox.get(seleccion_lista[0])
            self.controlador.agregar_cancion_a_lista(index_cancion, nombre_lista)
            self.mostrar_mensaje(f"✅ Canción agregada a '{nombre_lista}'.")
            ventana.destroy()

        tk.Button(ventana, text="Agregar", command=confirmar, bg="#2d2d2d", fg="white").pack(pady=10)

    def reproducir_anterior(self):
        seleccion = self.lista_canciones.curselection()
        if seleccion:
            index = seleccion[0] - 1
            if index >= 0:
                self.lista_canciones.select_clear(0, tk.END)
                self.lista_canciones.select_set(index)
                self.lista_canciones.event_generate("<<ListboxSelect>>")
                self.controlador.reproducir_cancion(index)

    def reproducir_siguiente(self):
        seleccion = self.lista_canciones.curselection()
        if seleccion:
            index = seleccion[0] + 1
            if index < len(self.canciones_mostradas):
                self.lista_canciones.select_clear(0, tk.END)
                self.lista_canciones.select_set(index)
                self.lista_canciones.event_generate("<<ListboxSelect>>")
                self.controlador.reproducir_cancion(index)
