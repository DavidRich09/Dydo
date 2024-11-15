App Dydo: Guía de Instalación
=======

## Paso 1: Descargar e instalar Python

1. **Ir a la página oficial de Python:**
   - Abre tu navegador web y dirígete a [https://www.python.org/downloads/](https://www.python.org/downloads/).

2. **Seleccionar la versión de Python:**
   - Haz clic en el botón de descarga que muestra la versión recomendada de Python para Windows. Si necesitas una versión específica, puedes encontrarla en la sección de "Releases" de la página.

3. **Ejecutar el instalador de Python:**
   - Una vez descargado el instalador, ejecútalo.
   - **Asegúrate de marcar la casilla** "Add Python to PATH" antes de hacer clic en "Install Now". Esto facilitará el uso de Python desde la línea de comandos.

4. **Verificar la instalación:**
   - Abre la terminal de Windows (CMD) y escribe el siguiente comando para verificar que Pyth

## Paso 2: Instalar PyInstaller

1. **Abrir la terminal de comandos:**
   - Presiona `Win + R`, escribe `cmd` y presiona Enter para abrir la terminal de Windows.

2. **Instalar PyInstaller usando pip:**
   - En la terminal, escribe el siguiente comando para instalar PyInstaller:
     ```bash
     pip install pyinstaller
     ```

3. **Verificar la instalación de PyInstaller:**
   - Una vez que la instalación se haya completado, puedes verificar que PyInstaller se instaló correctamente ejecutando:
     ```bash
     pyinstaller --version
     ```
   - Deberías ver la versión de PyInstaller instalada.

## Paso 3: Crear ejecutable con PyInstaller

1. **Dirígete al directorio de tu proyecto:**
   - En la terminal, navega hasta la carpeta donde tienes el script "main.py" del proyecto.

2. **Crear el ejecutable:**
   - Ejecuta el siguiente comando para generar el ejecutable del script "main.py":
     ```bash
     pyinstaller --onefile main.py
     ```
   - Esto creará una carpeta `dist` en tu directorio, donde encontrarás el archivo ejecutable.
