# El Descargador

Aplicación de escritorio para administrar una biblioteca musical local. Permite
descargar el audio de un enlace de YouTube como MP3, reproducirlo, buscar
canciones y artistas, marcar favoritos y organizar canciones en listas.

Descarga únicamente contenido que tengas derecho a descargar y respeta las
condiciones de uso de los servicios correspondientes.

## Funcionalidades

- Descargar audio desde un enlace de YouTube.
- Reproducir, pausar y detener canciones.
- Buscar por título o artista, filtrar favoritas y ordenar la biblioteca.
- Editar canciones y organizarlas en listas de reproducción.
- Guardar la biblioteca y las listas entre ejecuciones.
- Opcionalmente usar la sesión local de Chrome, Edge, Firefox o Brave para
  autenticar solicitudes cuando YouTube pida iniciar sesión.

## Tecnologías y arquitectura

- **Python 3.11**, **Tkinter** y **MVC** para la aplicación de escritorio.
- **yt-dlp** para obtener el audio de los enlaces.
- **FFmpeg** para convertir el audio descargado a MP3.
- **python-vlc** como interfaz Python y **VLC Media Player** como reproductor
  nativo.
- **Cookies del navegador (opcional)** para autenticar solicitudes de YouTube
  con una sesión que el usuario ya tenga abierta.
- **JSON** para persistir la biblioteca.
- **PyInstaller** para crear la distribución de Windows.

El proyecto separa responsabilidades con el patrón **Modelo-Vista-Controlador**:

- `app/model/`: canciones, biblioteca, listas, rutas de datos, descargas y
  reproducción.
- `app/view/InterfazUsuario.py`: interfaz y diálogos de Tkinter.
- `app/controller/ControladorPrincipal.py`: coordina las acciones entre la
  vista y los modelos.
- `main.py`: crea la ventana y conecta la vista con el controlador.

La descarga se ejecuta en segundo plano para mantener la interfaz receptiva.

## Requisitos

### Ejecutar desde el código fuente

- Windows, macOS o Linux.
- Python 3.11 o superior con Tcl/Tk.
- VLC Media Player instalado, de la misma arquitectura que Python.
- FFmpeg instalado y disponible en `PATH`.
- Conexión a Internet para descargar audio.

### Ejecutar la versión empaquetada para Windows

- Windows de 64 bits.
- VLC Media Player de 64 bits instalado. PyInstaller incluye `python-vlc`, pero
  no la biblioteca nativa `libvlc` ni los plugins de VLC.
- FFmpeg instalado y disponible en `PATH`; no se incluye en el paquete.
- Conexión a Internet para descargar audio.

Tkinter y el runtime de Python se incluyen en el paquete de PyInstaller. `yt-dlp`
y `python-vlc` se incorporan al bundle; no hace falta instalar Python ni
dependencias Python para ejecutar la versión empaquetada.

## Ejecutar desde el código fuente

Desde PowerShell, en la carpeta del proyecto:

```powershell
py -m venv venv
.\venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python main.py
```

Si el entorno virtual ya existe, activa `venv` y ejecuta desde la instalación
de dependencias. Si PowerShell bloquea la activación, puedes ejecutar una vez:

```powershell
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
```

O usar `cmd.exe` y `venv\Scripts\activate.bat`. Al terminar, escribe
`deactivate`.

Para macOS o Linux, crea y activa el entorno así:

```bash
python3 -m venv venv
source venv/bin/activate
python -m pip install -r requirements.txt
python main.py
```

## Descargar y ejecutar desde GitHub Releases

1. Abre la sección **Releases** del repositorio y descarga
   `ElDescargador-windows-x64.zip` de la versión deseada.
2. Extrae el ZIP completo en una carpeta normal (no ejecutes el programa desde
   dentro del ZIP).
3. Instala VLC Media Player de 64 bits y FFmpeg, si aún no están instalados.
4. Ejecuta `ElDescargador.exe` dentro de la carpeta extraída.

El ZIP contiene la aplicación y sus dependencias Python; **VLC Media Player y
FFmpeg se instalan por separado**. No hace falta activar un `venv` ni instalar
Python para usar el ejecutable.

## Uso de la aplicación

1. (Opcional) Inicia sesión en YouTube en Chrome, Edge, Firefox o Brave.
2. Pega un enlace de YouTube en el campo superior.
3. Si YouTube rechaza la solicitud sin sesión, selecciona el navegador donde
   iniciaste sesión en **Sesión de YouTube**. Si no hace falta autenticación,
   deja **Sin sesión**. El navegador debe estar instalado y tener un perfil
   normal disponible. Si aparece un error al leer la base de cookies, cierra
   completamente el navegador seleccionado (incluidas las ventanas en segundo
   plano) y vuelve a intentarlo. Windows puede impedir el acceso incluso si el
   navegador parece cerrado; en ese caso, prueba otro navegador o selecciona
   **Sin sesión**. El mensaje de yt-dlp puede decir «Chrome» aunque hayas elegido
   Edge.
4. Pulsa **Descargar audio** y espera el mensaje de finalización. FFmpeg debe
   estar instalado y accesible en `PATH`.
5. Selecciona una canción para reproducirla, pausarla, marcarla como favorita o
   añadirla a una lista.
6. Busca canciones por título o artista; **Mostrar todas** vuelve a la
   biblioteca completa.
7. En **Ver lista**, selecciona una lista para previsualizarla y pulsa
   **Abrir lista** o haz doble clic.

La autenticación opcional lee la sesión del perfil local elegido y usa sus
cookies en solicitudes dirigidas a YouTube. La aplicación no solicita que
copies cookies, no las guarda en su configuración ni las envía a terceros.
Usa esta función solo en una copia de la aplicación en la que confíes y con tu
propia sesión; no compartas los datos del perfil del navegador. La sesión solo
permite acceder a lo que esa cuenta puede ver: no evita restricciones de edad o
región, ni habilita videos privados, DRM o contenido para el que no tengas
permiso de descarga. YouTube aún puede bloquear solicitudes incluso con sesión.

## Datos de la aplicación

- **Desde el código fuente:** la biblioteca y los audios están en
  `biblioteca.json` y `audio/` en la raíz del proyecto.
- **Versión empaquetada:** los datos se guardan en
  `%LOCALAPPDATA%\ElDescargador\` (por ejemplo, bajo el perfil del usuario de
  Windows). No se incluyen la biblioteca ni audios del equipo que construye el
  paquete.
- El registro de diagnóstico `el_descargador.log` se guarda junto a esos datos.

Los archivos de la biblioteca se conservan al reemplazar la carpeta del
ejecutable por una versión nueva, porque se guardan fuera del bundle.

## Crear el paquete en Windows

Para compilar localmente desde la raíz del repositorio:

```powershell
py -m venv venv
.\venv\Scripts\Activate.ps1
python -m pip install -r requirements-build.txt
python -m PyInstaller --noconfirm --clean ElDescargador.spec
```

La carpeta `dist/ElDescargador/` contiene la aplicación. La configuración
`ElDescargador.spec` usa modo **onedir**, incluye los submódulos dinámicos de
`yt-dlp` y no empaqueta `audio/`, `biblioteca.json`, VLC ni FFmpeg.

## Compilación automática y Releases

El flujo `.github/workflows/build-windows.yml` construye la aplicación en
Windows para `push`, `pull_request` y ejecución manual. El ZIP aparece como
artefacto de la ejecución de GitHub Actions.

Al publicar un tag con formato `v*` (por ejemplo, `v1.0.0`), el flujo también
crea una GitHub Release con notas generadas y adjunta
`ElDescargador-windows-x64.zip`. Usa el `GITHUB_TOKEN` proporcionado por GitHub
Actions; no requiere guardar secretos en el repositorio.

El flujo compila el paquete; el artefacto debe probarse en una instalación
Windows limpia con VLC y FFmpeg antes de considerarlo verificado para usuarios.

## Solución de problemas

- **No se encuentra `libvlc.dll`:** instala VLC Media Player de 64 bits, cierra
  y vuelve a abrir la aplicación.
- **Falla la conversión a MP3:** confirma que `ffmpeg` se puede ejecutar desde
  una terminal.
- **Falla la descarga:** comprueba la conexión y que el enlace sea accesible.
  Si YouTube solicita verificación, elige el navegador donde ya iniciaste sesión.
  Si el acceso sigue bloqueado, la restricción de YouTube no se puede resolver
  desde la aplicación.
- **Para probar cambios desde el código fuente:** activa `venv` e inicia con
  `python main.py`.
