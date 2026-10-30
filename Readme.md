# El Descargador

Aplicación de escritorio para administrar una biblioteca musical local. Permite
descargar audio a partir de un enlace de YouTube, reproducir archivos MP3,
buscar canciones y artistas, marcar favoritos y organizar canciones en listas.

## Funcionalidades

- Pegar un enlace de YouTube y descargar su audio como MP3.
- Ver las canciones de la biblioteca y reproducirlas, pausarlas o detenerlas.
- Buscar por título o artista, y filtrar las canciones favoritas.
- Editar la información de una canción, ordenarla y quitarla de la biblioteca.
- Crear listas de reproducción, consultar su contenido y añadir canciones.
- Guardar la biblioteca y las listas entre ejecuciones.

La aplicación recibe el enlace que se pega en el campo superior y usa `yt-dlp`
para obtener el audio. Las descargas se convierten a MP3 y se guardan en
`audio/`. Descarga únicamente contenido que tengas derecho a descargar.

## Tecnologías

- **Python 3.11 o superior** para la aplicación.
- **Tkinter** para la interfaz gráfica.
- **yt-dlp** para procesar enlaces y descargar audio.
- **FFmpeg** para convertir el audio descargado a MP3.
- **python-vlc** y **VLC Media Player** para reproducir los archivos.
- **JSON** para guardar la biblioteca y las listas en `biblioteca.json`.

## Arquitectura

El proyecto sigue el patrón **Modelo-Vista-Controlador (MVC)**:

- `app/model/`: canciones, biblioteca, listas, descargas y reproducción.
- `app/view/InterfazUsuario.py`: ventanas, controles y presentación.
- `app/controller/ControladorPrincipal.py`: conecta la interfaz con los modelos
  y coordina las acciones del usuario.
- `main.py`: inicia Tkinter y conecta la vista con el controlador.

La descarga se ejecuta en segundo plano para mantener la interfaz receptiva; el
resultado se devuelve a la interfaz mediante una cola.

## Requisitos del sistema

- Python 3.11 o superior.
- VLC Media Player instalado. `python-vlc` por sí solo no incluye la biblioteca
  nativa de VLC (`libvlc`).
- FFmpeg instalado y disponible en `PATH`.
- Conexión a Internet para descargar audio.

## Instalación y ejecución en Windows

Abre PowerShell en la carpeta del proyecto y ejecuta:

```powershell
py -m venv venv
.\venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python main.py
```

Si ya creaste el entorno virtual, no necesitas repetir el primer comando.
Si PowerShell bloquea la activación del entorno, ejecuta una vez:

```powershell
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
```

También puedes activar el entorno desde `cmd.exe` con:

```cmd
venv\Scripts\activate.bat
```

También puedes omitir la activación y usar directamente el Python del entorno:

```powershell
.\venv\Scripts\python.exe main.py
```

Al terminar, cierra la aplicación y, si activaste el entorno, escribe:

```powershell
deactivate
```

## macOS y Linux

Instala previamente VLC Media Player y FFmpeg con el gestor de paquetes de tu
sistema. Después, desde la carpeta del proyecto:

```bash
python3 -m venv venv
source venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python main.py
```

Al terminar, escribe `deactivate`.

## Uso

1. Inicia la aplicación y pega un enlace de YouTube en el campo superior.
2. Pulsa **Descargar audio** y espera el aviso de finalización. Necesitas
   conexión a Internet y FFmpeg; la ventana sigue respondiendo durante la
   descarga.
3. Selecciona una canción para reproducirla, pausarla, marcarla como favorita
   o añadirla a una lista.
4. Usa la búsqueda para encontrar canciones por título o artista. **Mostrar
   todas** vuelve a la biblioteca completa.
5. En **Ver lista** puedes seleccionar una lista para previsualizar su
   contenido; pulsa **Abrir lista** o haz doble clic sobre ella.

La biblioteca se conserva en `biblioteca.json` y los audios descargados en
`audio/`. El proyecto incluye algunos archivos MP3 de muestra para probar la
reproducción sin descargar una canción.

## Solución de problemas

- **No se encuentra `libvlc.dll`:** instala VLC Media Player (misma arquitectura
  de Python, normalmente 64 bits), cierra y vuelve a abrir PowerShell e inicia
  otra vez la aplicación.
- **No se puede convertir a MP3 o falla una descarga:** comprueba que FFmpeg esté
  instalado y que `ffmpeg` se pueda ejecutar desde una terminal.
- **Falla la instalación de paquetes:** confirma que el entorno `venv` está
  activado y vuelve a ejecutar `python -m pip install -r requirements.txt`.
