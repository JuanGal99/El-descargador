import tkinter as tk
import queue
import threading


class InterfazUsuario:
    COLORES = {
        "fondo": "#17191f",
        "panel": "#22252d",
        "entrada": "#2b2f3a",
        "texto": "#f4f5f7",
        "secundario": "#a7adba",
        "acento": "#6c7cff",
        "peligro": "#a83f4b",
    }

    def __init__(self, root):
        self.root = root
        self.root.title("El Descargador")
        self.root.geometry("960x680")
        self.root.minsize(780, 560)
        self.root.configure(bg=self.COLORES["fondo"])
        self.controlador = None
        self.lista_actual = None

        frame = tk.Frame(self.root, bg=self.COLORES["fondo"], padx=24, pady=20)
        frame.grid(row=0, column=0, sticky="nsew")
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        frame.grid_columnconfigure(0, weight=1)
        frame.grid_columnconfigure(1, weight=2)
        frame.grid_rowconfigure(6, weight=1)

        tk.Label(
            frame,
            text="Tu música, en un solo lugar",
            bg=self.COLORES["fondo"],
            fg=self.COLORES["texto"],
            font=("Segoe UI", 19, "bold"),
        ).grid(row=0, column=0, columnspan=3, sticky="w")
        tk.Label(
            frame,
            text="Descarga audio, organiza tu biblioteca y reproduce tus canciones.",
            bg=self.COLORES["fondo"],
            fg=self.COLORES["secundario"],
            font=("Segoe UI", 10),
        ).grid(row=1, column=0, columnspan=3, sticky="w", pady=(2, 18))

        self.entrada_url = tk.Entry(
            frame,
            bg=self.COLORES["entrada"],
            fg=self.COLORES["texto"],
            insertbackground=self.COLORES["texto"],
            relief="flat",
            font=("Segoe UI", 10),
        )
        self.entrada_url.grid(row=2, column=0, columnspan=2, sticky="ew", ipady=9)
        self.entrada_url.insert(0, "Pega aquí un enlace de YouTube")
        self.entrada_url.bind("<FocusIn>", self._limpiar_placeholder_url)

        self.boton_descargar = self._crear_boton(frame, "↓  Descargar audio", self.descargar, primario=True)
        self.boton_descargar.grid(row=2, column=2, padx=(10, 0), sticky="ew")

        tk.Label(
            frame, text="Buscar canción o artista", bg=self.COLORES["fondo"],
            fg=self.COLORES["secundario"], font=("Segoe UI", 9, "bold")
        ).grid(row=3, column=0, columnspan=3, sticky="w", pady=(17, 5))
        self.buscador = tk.Entry(
            frame,
            bg=self.COLORES["entrada"],
            fg=self.COLORES["texto"],
            insertbackground=self.COLORES["texto"],
            relief="flat",
            font=("Segoe UI", 10),
        )
        self.buscador.grid(row=4, column=0, columnspan=3, sticky="ew", ipady=7, pady=(0, 12))
        self.buscador.bind("<KeyRelease>", lambda e: self.filtrar())

        botones_filtro = tk.Frame(frame, bg=self.COLORES["fondo"])
        botones_filtro.grid(row=5, column=0, columnspan=3, sticky="ew", pady=(0, 8))

        self.boton_favoritas = self._crear_boton(botones_filtro, "❤️ Favoritas", self.mostrar_favoritas)
        self.boton_favoritas.pack(side="left", padx=5)

        self.boton_todas = self._crear_boton(botones_filtro, "🔁 Mostrar todas", self.mostrar_todas)
        self.boton_todas.pack(side="left", padx=5)

        self.boton_editar = self._crear_boton(botones_filtro, "✏️ Editar", self.editar)
        self.boton_editar.pack(side="left", padx=5)

        self.boton_ordenar = self._crear_boton(botones_filtro, "↕️ Ordenar", self.ordenar)
        self.boton_ordenar.pack(side="left", padx=5)


        lista_frame = tk.Frame(frame, bg=self.COLORES["panel"], padx=2, pady=2)
        lista_frame.grid(row=6, column=0, columnspan=3, sticky="nsew")
        lista_frame.grid_rowconfigure(0, weight=1)
        lista_frame.grid_columnconfigure(0, weight=1)
        self.lista_canciones = tk.Listbox(
            lista_frame,
            height=10,
            bg=self.COLORES["panel"],
            fg=self.COLORES["texto"],
            selectbackground=self.COLORES["acento"],
            selectforeground="white",
            relief="flat",
            borderwidth=0,
            font=("Segoe UI", 10),
            activestyle="none",
        )
        self.lista_canciones.grid(row=0, column=0, sticky="nsew")
        barra_canciones_y = tk.Scrollbar(
            lista_frame, orient="vertical", command=self.lista_canciones.yview
        )
        barra_canciones_y.grid(row=0, column=1, sticky="ns")
        self.lista_canciones.configure(yscrollcommand=barra_canciones_y.set)
        self.lista_canciones.bind("<<ListboxSelect>>", self.actualizar_texto_boton_fav)

        self.etiqueta_estado = tk.Label(
            frame, text="Biblioteca completa · 0 canciones", bg=self.COLORES["fondo"],
            fg=self.COLORES["secundario"], font=("Segoe UI", 9)
        )
        self.etiqueta_estado.grid(row=7, column=0, columnspan=3, sticky="w", pady=(8, 2))

        controles = tk.Frame(frame, bg=self.COLORES["fondo"])
        controles.grid(row=8, column=0, columnspan=3, pady=(4, 0))

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
        self.boton_fav.grid(row=1, column=0, padx=5, pady=(10, 0))

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
        self._resultados_descarga = queue.Queue()
        self.root.after(100, self._procesar_resultados_descarga)

    def _crear_boton(self, parent, texto, comando, primario=False, peligro=False):
        fondo = self.COLORES["acento"] if primario else self.COLORES["panel"]
        if peligro:
            fondo = self.COLORES["peligro"]
        return tk.Button(
            parent,
            text=texto,
            command=comando,
            bg=fondo,
            fg=self.COLORES["texto"],
            activebackground=self.COLORES["acento"],
            activeforeground="white",
            relief="flat",
            borderwidth=0,
            cursor="hand2",
            padx=12,
            pady=8,
            font=("Segoe UI", 9, "bold"),
        )

    def _limpiar_placeholder_url(self, event=None):
        if self.entrada_url.get() == "Pega aquí un enlace de YouTube":
            self.entrada_url.delete(0, tk.END)

    def _crear_ventana_modal(self, titulo, geometria, redimensionable=False):
        ventana = tk.Toplevel(self.root)
        ventana.title(titulo)
        ventana.configure(bg=self.COLORES["fondo"])
        ventana.transient(self.root)
        ventana.resizable(redimensionable, redimensionable)
        ventana.geometry(geometria)
        ventana.update_idletasks()
        ancho, alto = ventana.winfo_width(), ventana.winfo_height()
        x = self.root.winfo_rootx() + (self.root.winfo_width() - ancho) // 2
        y = self.root.winfo_rooty() + (self.root.winfo_height() - alto) // 2
        ventana.geometry(f"{ancho}x{alto}+{max(x, 0)}+{max(y, 0)}")
        ventana.grab_set()
        ventana.focus_set()
        return ventana

    def _crear_encabezado_dialogo(self, ventana, titulo, descripcion):
        encabezado = tk.Frame(ventana, bg=self.COLORES["fondo"])
        encabezado.pack(fill="x", padx=22, pady=(20, 12))
        tk.Label(
            encabezado, text=titulo, bg=self.COLORES["fondo"],
            fg=self.COLORES["texto"], font=("Segoe UI", 15, "bold")
        ).pack(anchor="w")
        tk.Label(
            encabezado, text=descripcion, bg=self.COLORES["fondo"],
            fg=self.COLORES["secundario"], font=("Segoe UI", 9)
        ).pack(anchor="w", pady=(3, 0))

    def set_controlador(self, controlador):
        self.controlador = controlador
        self.mostrar_todas()

    def descargar(self):
        url = self.entrada_url.get().strip()
        if url and url != "Pega aquí un enlace de YouTube":
            self.boton_descargar.config(state=tk.DISABLED)
            threading.Thread(target=self.controlador.descargar_cancion, args=(url,), daemon=True).start()
        else:
            self.mostrar_mensaje("Pega un enlace de YouTube antes de iniciar la descarga.")

    def finalizar_descarga(self, cancion, mensaje):
        self.boton_descargar.config(state=tk.NORMAL)
        if cancion is not None:
            self.entrada_url.delete(0, tk.END)
            self.mostrar_todas()
        self.mostrar_mensaje(mensaje)

    def encolar_resultado_descarga(self, cancion, error):
        self._resultados_descarga.put((cancion, error))

    def _procesar_resultados_descarga(self):
        try:
            while True:
                cancion, error = self._resultados_descarga.get_nowait()
                if error:
                    self.finalizar_descarga(None, error)
                else:
                    self.controlador.registrar_descarga(cancion)
        except queue.Empty:
            pass
        self.root.after(100, self._procesar_resultados_descarga)

    def actualizar_lista(self):
        self.lista_canciones.delete(0, tk.END)
        for c in self.canciones_mostradas:
            favorito = "❤️" if c.favorito else ""
            self.lista_canciones.insert(tk.END, f"{c.titulo}   —   {c.artista}  {favorito}")
        contexto = self.lista_actual or "Biblioteca completa"
        cantidad = len(self.canciones_mostradas)
        nombre_cantidad = "canción" if cantidad == 1 else "canciones"
        self.etiqueta_estado.config(
            text=f"{contexto}  ·  {cantidad} {nombre_cantidad}"
        )

    def filtrar(self):
        texto = self.buscador.get().lower()
        canciones = self.controlador.filtrar_por_texto(texto)
        self.canciones_mostradas = canciones
        self.lista_actual = "Resultados de búsqueda" if texto else None
        self.actualizar_lista()

    def mostrar_favoritas(self):
        self.canciones_mostradas = self.controlador.obtener_favoritas()
        self.lista_actual = "Favoritas"
        self.actualizar_lista()

    def mostrar_todas(self):
        self.canciones_mostradas = self.controlador.obtener_todas()
        self.lista_actual = None
        self.actualizar_lista()

    def reproducir(self):
        seleccion = self.lista_canciones.curselection()
        if seleccion:
            self.controlador.reproducir_cancion(self.canciones_mostradas[seleccion[0]])
        else:
            self.mostrar_mensaje("⚠️ Selecciona una canción.")

    def pausar(self):
        self.controlador.pausar()

    def detener(self):
        self.controlador.detener()

    def marcar_favorita(self):
        seleccion = self.lista_canciones.curselection()
        if seleccion:
            self.controlador.marcar_favorita(self.canciones_mostradas[seleccion[0]])
            self._actualizar_vista_actual()
            self.actualizar_texto_boton_fav()

    def eliminar(self):
        seleccion = self.lista_canciones.curselection()
        if seleccion:
            index = seleccion[0]
            cancion = self.canciones_mostradas[index]
            if not self._confirmar_accion(
                "Eliminar canción",
                f"Se quitará «{cancion.titulo}» de la biblioteca y se eliminará su archivo de audio. ¿Continuar?"
            ):
                return
            self.controlador.eliminar_cancion_objeto(cancion)
            self._actualizar_vista_actual()
            self.actualizar_texto_boton_fav()

    def _actualizar_vista_actual(self):
        if self.lista_actual == "Favoritas":
            self.canciones_mostradas = self.controlador.obtener_favoritas()
        elif self.lista_actual and self.lista_actual.startswith("Lista: "):
            nombre = self.lista_actual.removeprefix("Lista: ")
            self.canciones_mostradas = list(
                self.controlador.obtener_canciones_de_lista(nombre)
            )
        elif self.lista_actual == "Resultados de búsqueda":
            self.canciones_mostradas = self.controlador.filtrar_por_texto(
                self.buscador.get().lower()
            )
        else:
            self.canciones_mostradas = self.controlador.obtener_todas()
        self.actualizar_lista()

    def editar(self):
        seleccion = self.lista_canciones.curselection()
        if not seleccion:
            self.mostrar_mensaje("⚠️ Selecciona una canción para editar.")
            return

        index = seleccion[0]
        cancion = self.canciones_mostradas[index]

        ventana = self._crear_ventana_modal("Editar canción", "440x260")
        self._crear_encabezado_dialogo(ventana, "Editar canción", "Actualiza el título y el artista.")

        formulario = tk.Frame(ventana, bg=self.COLORES["fondo"])
        formulario.pack(fill="x", padx=22)
        tk.Label(formulario, text="Título", bg=self.COLORES["fondo"], fg=self.COLORES["secundario"]).grid(
            row=0, column=0, sticky="w", pady=6
        )
        entrada_titulo = tk.Entry(
            formulario, bg=self.COLORES["entrada"], fg=self.COLORES["texto"],
            insertbackground=self.COLORES["texto"], relief="flat"
        )
        entrada_titulo.grid(row=0, column=1, sticky="ew", padx=(14, 0), ipady=6)
        entrada_titulo.insert(0, cancion.titulo)

        tk.Label(formulario, text="Artista", bg=self.COLORES["fondo"], fg=self.COLORES["secundario"]).grid(
            row=1, column=0, sticky="w", pady=6
        )
        entrada_artista = tk.Entry(
            formulario, bg=self.COLORES["entrada"], fg=self.COLORES["texto"],
            insertbackground=self.COLORES["texto"], relief="flat"
        )
        entrada_artista.grid(row=1, column=1, sticky="ew", padx=(14, 0), ipady=6)
        entrada_artista.insert(0, cancion.artista)
        formulario.grid_columnconfigure(1, weight=1)

        def guardar():
            nuevo_titulo = entrada_titulo.get().strip()
            nuevo_artista = entrada_artista.get().strip()
            if not nuevo_titulo or not nuevo_artista:
                self.mostrar_mensaje("⚠️ No puedes dejar campos vacíos.")
                return
            self.controlador.editar_cancion(cancion, nuevo_titulo, nuevo_artista)
            self.actualizar_lista()
            ventana.destroy()

        acciones = tk.Frame(ventana, bg=self.COLORES["fondo"])
        acciones.pack(fill="x", padx=22, pady=18)
        self._crear_boton(acciones, "Cancelar", ventana.destroy).pack(side="right")
        self._crear_boton(acciones, "Guardar cambios", guardar, primario=True).pack(side="right", padx=(0, 8))
        entrada_titulo.focus_set()

    def actualizar_texto_boton_fav(self, event=None):
        seleccion = self.lista_canciones.curselection()
        if seleccion:
            index = seleccion[0]
            cancion = self.canciones_mostradas[index]
            self.boton_fav.config(text="💔 Quitar favorita" if cancion.favorito else "⭐ Marcar favorita")
        else:
            self.boton_fav.config(text="⭐ Marcar favorita")

    def mostrar_mensaje(self, texto):
        self.root.after(0, self._mostrar_dialogo_mensaje, texto)

    def _mostrar_dialogo_mensaje(self, texto):
        ventana = self._crear_ventana_modal("Aviso", "420x190")
        self._crear_encabezado_dialogo(ventana, "Aviso", "El Descargador")
        tk.Label(
            ventana,
            text=texto,
            bg=self.COLORES["fondo"],
            fg=self.COLORES["texto"],
            justify="left",
            wraplength=370,
            font=("Segoe UI", 10),
        ).pack(fill="x", padx=22, pady=(0, 14))
        boton = self._crear_boton(ventana, "Entendido", ventana.destroy, primario=True)
        boton.pack(anchor="e", padx=22, pady=(0, 18))
        ventana.bind("<Return>", lambda event: ventana.destroy())
        ventana.bind("<Escape>", lambda event: ventana.destroy())
        boton.focus_set()

    def _confirmar_accion(self, titulo, mensaje):
        ventana = self._crear_ventana_modal(titulo, "440x210")
        self._crear_encabezado_dialogo(ventana, titulo, "Confirma para continuar.")
        tk.Label(
            ventana,
            text=mensaje,
            bg=self.COLORES["fondo"],
            fg=self.COLORES["texto"],
            justify="left",
            wraplength=390,
            font=("Segoe UI", 10),
        ).pack(fill="x", padx=22, pady=(0, 14))
        resultado = {"confirmado": False}

        def cerrar(confirmado):
            resultado["confirmado"] = confirmado
            ventana.destroy()

        acciones = tk.Frame(ventana, bg=self.COLORES["fondo"])
        acciones.pack(fill="x", padx=22, pady=(0, 18))
        self._crear_boton(acciones, "Cancelar", lambda: cerrar(False)).pack(side="right")
        self._crear_boton(
            acciones, "Continuar", lambda: cerrar(True), primario=True
        ).pack(side="right", padx=(0, 8))
        ventana.protocol("WM_DELETE_WINDOW", lambda: cerrar(False))
        ventana.bind("<Escape>", lambda event: cerrar(False))
        ventana.wait_window()
        return resultado["confirmado"]

    def abrir_ventana_crear_lista(self):
        ventana = self._crear_ventana_modal("Crear lista", "420x220")
        self._crear_encabezado_dialogo(
            ventana, "Crear una lista", "Dale un nombre para agrupar tus canciones."
        )
        entrada = tk.Entry(
            ventana,
            bg=self.COLORES["entrada"],
            fg=self.COLORES["texto"],
            insertbackground=self.COLORES["texto"],
            relief="flat",
            font=("Segoe UI", 10),
        )
        entrada.pack(fill="x", padx=22, ipady=7)

        def crear():
            nombre = entrada.get().strip()
            if nombre:
                if self.controlador.crear_lista(nombre):
                    ventana.destroy()
            else:
                self.mostrar_mensaje("⚠️ El nombre no puede estar vacío.")

        acciones = tk.Frame(ventana, bg=self.COLORES["fondo"])
        acciones.pack(fill="x", padx=22, pady=18)
        self._crear_boton(acciones, "Cancelar", ventana.destroy).pack(side="right")
        self._crear_boton(acciones, "Crear lista", crear, primario=True).pack(side="right", padx=(0, 8))
        entrada.focus_set()
        entrada.bind("<Return>", lambda event: crear())

    def abrir_ventana_ver_lista(self):
        listas = self.controlador.obtener_nombres_listas()
        if not listas:
            self.mostrar_mensaje("⚠️ No hay listas disponibles.")
            return

        ventana = self._crear_ventana_modal("Tus listas", "760x470", redimensionable=True)
        ventana.minsize(620, 380)
        self._crear_encabezado_dialogo(
            ventana, "Tus listas", "Selecciona una lista para ver sus canciones."
        )
        contenido = tk.Frame(ventana, bg=self.COLORES["fondo"])
        contenido.pack(fill="both", expand=True, padx=22)
        contenido.grid_rowconfigure(1, weight=1)
        contenido.grid_columnconfigure(1, weight=1)
        tk.Label(
            contenido, text="LISTAS", bg=self.COLORES["fondo"],
            fg=self.COLORES["secundario"], font=("Segoe UI", 8, "bold")
        ).grid(row=0, column=0, sticky="w", pady=(0, 6))
        tk.Label(
            contenido, text="CANCIONES", bg=self.COLORES["fondo"],
            fg=self.COLORES["secundario"], font=("Segoe UI", 8, "bold")
        ).grid(row=0, column=1, sticky="w", padx=(14, 0), pady=(0, 6))
        panel_listas = tk.Frame(contenido, bg=self.COLORES["panel"])
        panel_listas.grid(row=1, column=0, sticky="nsew")
        panel_listas.grid_rowconfigure(0, weight=1)
        panel_listas.grid_columnconfigure(0, weight=1)
        lista_listbox = tk.Listbox(
            panel_listas,
            width=24,
            bg=self.COLORES["panel"],
            fg=self.COLORES["texto"],
            selectbackground=self.COLORES["acento"],
            relief="flat",
            borderwidth=0,
            font=("Segoe UI", 10),
            activestyle="none",
            exportselection=False,
        )
        lista_listbox.grid(row=0, column=0, sticky="nsew")
        barra_listas = tk.Scrollbar(
            panel_listas, orient="vertical", command=lista_listbox.yview
        )
        barra_listas.grid(row=0, column=1, sticky="ns")
        lista_listbox.configure(yscrollcommand=barra_listas.set)
        detalle_frame = tk.Frame(contenido, bg=self.COLORES["panel"])
        detalle_frame.grid(row=1, column=1, sticky="nsew", padx=(14, 0))
        detalle_frame.grid_rowconfigure(0, weight=1)
        detalle_frame.grid_columnconfigure(0, weight=1)
        canciones_listbox = tk.Listbox(
            detalle_frame,
            bg=self.COLORES["panel"],
            fg=self.COLORES["texto"],
            selectbackground=self.COLORES["acento"],
            relief="flat",
            borderwidth=0,
            font=("Segoe UI", 10),
            activestyle="none",
        )
        canciones_listbox.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        barra_canciones = tk.Scrollbar(
            detalle_frame, orient="vertical", command=canciones_listbox.yview
        )
        barra_canciones.grid(row=0, column=1, sticky="ns", pady=10)
        canciones_listbox.configure(yscrollcommand=barra_canciones.set)
        etiqueta_detalle = tk.Label(
            detalle_frame,
            text="Elige una lista para consultar sus canciones.",
            bg=self.COLORES["panel"],
            fg=self.COLORES["secundario"],
            font=("Segoe UI", 9),
        )
        etiqueta_detalle.grid(row=1, column=0, sticky="w", padx=10, pady=(0, 10))

        def ver_lista():
            seleccion = lista_listbox.curselection()
            if seleccion:
                nombre_lista = lista_listbox.get(seleccion[0])
                self.canciones_mostradas = list(
                    self.controlador.obtener_canciones_de_lista(nombre_lista)
                )
                self.lista_actual = f"Lista: {nombre_lista}"
                self.actualizar_lista()
                ventana.destroy()

        def actualizar_detalle(event=None):
            seleccion = lista_listbox.curselection()
            canciones_listbox.delete(0, tk.END)
            if not seleccion:
                etiqueta_detalle.config(text="Elige una lista para consultar sus canciones.")
                return
            nombre = lista_listbox.get(seleccion[0])
            canciones = self.controlador.obtener_canciones_de_lista(nombre)
            etiqueta_detalle.config(
                text=f"{len(canciones)} canciones en «{nombre}»"
                if canciones else "Esta lista todavía no tiene canciones."
            )
            for cancion in canciones:
                canciones_listbox.insert(tk.END, f"{cancion.titulo}   —   {cancion.artista}")

        def eliminar_lista():
            seleccion = lista_listbox.curselection()
            if seleccion:
                nombre = lista_listbox.get(seleccion[0])
                if not self._confirmar_accion(
                    "Eliminar lista", f"Se eliminará la lista «{nombre}». ¿Continuar?"
                ):
                    return
                self.controlador.eliminar_lista(nombre)
                lista_listbox.delete(seleccion[0])
                if self.lista_actual == f"Lista: {nombre}":
                    self.mostrar_todas()
                if lista_listbox.size():
                    lista_listbox.selection_set(min(seleccion[0], lista_listbox.size() - 1))
                actualizar_detalle()
                if not lista_listbox.size():
                    ventana.destroy()

        for nombre in listas:
            lista_listbox.insert(tk.END, nombre)
        lista_listbox.bind("<<ListboxSelect>>", actualizar_detalle)
        lista_listbox.bind("<Double-Button-1>", lambda event: ver_lista())
        lista_listbox.selection_set(0)
        actualizar_detalle()

        acciones = tk.Frame(ventana, bg=self.COLORES["fondo"])
        acciones.pack(fill="x", padx=22, pady=18)
        self._crear_boton(acciones, "Cerrar", ventana.destroy).pack(side="right")
        self._crear_boton(
            acciones, "Eliminar lista", eliminar_lista, peligro=True
        ).pack(side="left")
        self._crear_boton(
            acciones, "Abrir lista", ver_lista, primario=True
        ).pack(side="right", padx=(0, 8))

    def agregar_a_lista(self):
        seleccion = self.lista_canciones.curselection()
        if not seleccion:
            self.mostrar_mensaje("⚠️ Selecciona una canción primero.")
            return

        cancion = self.canciones_mostradas[seleccion[0]]
        listas = self.controlador.obtener_nombres_listas()

        if not listas:
            self.mostrar_mensaje("⚠️ No hay listas creadas.")
            return

        ventana = self._crear_ventana_modal("Agregar a una lista", "430x390")
        self._crear_encabezado_dialogo(
            ventana, "Agregar a una lista", f"Elige dónde guardar «{cancion.titulo}»."
        )
        listbox = tk.Listbox(
            ventana,
            bg=self.COLORES["panel"],
            fg=self.COLORES["texto"],
            selectbackground=self.COLORES["acento"],
            relief="flat",
            borderwidth=0,
            font=("Segoe UI", 10),
            activestyle="none",
            exportselection=False,
        )
        listbox.pack(fill="both", expand=True, padx=22, pady=(0, 12))

        for nombre in listas:
            listbox.insert(tk.END, nombre)

        def confirmar():
            seleccion_lista = listbox.curselection()
            if not seleccion_lista:
                self.mostrar_mensaje("⚠️ Selecciona una lista.")
                return
            nombre_lista = listbox.get(seleccion_lista[0])
            if self.controlador.agregar_cancion_a_lista(cancion, nombre_lista):
                ventana.destroy()

        acciones = tk.Frame(ventana, bg=self.COLORES["fondo"])
        acciones.pack(fill="x", padx=22, pady=(0, 18))
        self._crear_boton(acciones, "Cancelar", ventana.destroy).pack(side="right")
        self._crear_boton(acciones, "Agregar canción", confirmar, primario=True).pack(
            side="right", padx=(0, 8)
        )
        listbox.selection_set(0)
        listbox.focus_set()

    def reproducir_anterior(self):
        seleccion = self.lista_canciones.curselection()
        if seleccion:
            index = seleccion[0] - 1
            if index >= 0:
                self.lista_canciones.select_clear(0, tk.END)
                self.lista_canciones.select_set(index)
                self.lista_canciones.event_generate("<<ListboxSelect>>")
                self.controlador.reproducir_cancion(self.canciones_mostradas[index])

    def reproducir_siguiente(self):
        seleccion = self.lista_canciones.curselection()
        if seleccion:
            index = seleccion[0] + 1
            if index < len(self.canciones_mostradas):
                self.lista_canciones.select_clear(0, tk.END)
                self.lista_canciones.select_set(index)
                self.lista_canciones.event_generate("<<ListboxSelect>>")
                self.controlador.reproducir_cancion(self.canciones_mostradas[index])

    def ordenar(self):
        ventana = self._crear_ventana_modal("Ordenar biblioteca", "380x330")
        self._crear_encabezado_dialogo(
            ventana, "Ordenar biblioteca", "Elige cómo quieres ordenar las canciones."
        )

        def seleccionar(criterio):
            self.controlador.ordenar_por(criterio)
            ventana.destroy()

        opciones = tk.Frame(ventana, bg=self.COLORES["fondo"])
        opciones.pack(fill="x", padx=22)
        for texto, criterio in (("Título", "titulo"), ("Artista", "artista"), ("Duración", "duracion")):
            self._crear_boton(
                opciones,
                texto,
                lambda valor=criterio: seleccionar(valor),
                primario=criterio == "titulo",
            ).pack(fill="x", pady=4)
