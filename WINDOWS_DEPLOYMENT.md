# 🪟 Guía de Deployment para Windows

Comandos específicos para Windows CMD y PowerShell.

---

## 🎯 Opción 1: Usando CMD (Command Prompt)

### Paso 1: Abrir CMD en tu proyecto

1. Abre la carpeta de tu proyecto en el Explorador de Windows
2. En la barra de dirección, escribe `cmd` y presiona Enter
3. Se abrirá CMD en esa carpeta

### Paso 2: Verificar Git

```cmd
git --version
```

Si no está instalado, descarga de: https://git-scm.com/download/win

### Paso 3: Configurar Git (primera vez)

```cmd
git config --global user.name "Tu Nombre"
git config --global user.email "tu-email@ejemplo.com"
```

### Paso 4: Inicializar y subir

```cmd
REM Inicializar Git
git init

REM Agregar todos los archivos
git add .

REM Hacer commit
git commit -m "Initial commit: Dashboard de videojuegos"

REM Conectar con GitHub (reemplaza con TU URL)
git remote add origin https://github.com/TU-USUARIO/video-games-dashboard.git

REM Subir a GitHub
git push -u origin main
```

---

## 🎯 Opción 2: Usando PowerShell

### Paso 1: Abrir PowerShell en tu proyecto

1. Abre la carpeta de tu proyecto en el Explorador de Windows
2. Mantén presionado `Shift` y haz clic derecho en un espacio vacío
3. Selecciona "Abrir ventana de PowerShell aquí"

### Paso 2: Verificar Git

```powershell
git --version
```

### Paso 3: Configurar Git (primera vez)

```powershell
git config --global user.name "Tu Nombre"
git config --global user.email "tu-email@ejemplo.com"
```

### Paso 4: Inicializar y subir

```powershell
# Inicializar Git
git init

# Agregar todos los archivos
git add .

# Hacer commit
git commit -m "Initial commit: Dashboard de videojuegos"

# Conectar con GitHub (reemplaza con TU URL)
git remote add origin https://github.com/TU-USUARIO/video-games-dashboard.git

# Subir a GitHub
git push -u origin main
```

---

## 🎯 Opción 3: Usando Git Bash (Recomendado)

Git Bash viene incluido con Git para Windows y es más compatible con comandos Unix.

### Paso 1: Abrir Git Bash

1. Abre la carpeta de tu proyecto en el Explorador de Windows
2. Haz clic derecho en un espacio vacío
3. Selecciona "Git Bash Here"

### Paso 2: Usar comandos de quick_start.md

Ahora puedes usar los comandos de [`quick_start.md`](quick_start.md) directamente.

---

## 🔐 Autenticación en Windows

### Opción A: GitHub Desktop (Más Fácil)

1. Descarga GitHub Desktop: https://desktop.github.com/
2. Instala y conecta con tu cuenta de GitHub
3. Usa la interfaz gráfica para hacer commits y push

### Opción B: Personal Access Token

1. Ve a GitHub → Settings → Developer settings → Personal access tokens
2. Click "Generate new token (classic)"
3. Selecciona permisos: `repo` (todos los checkboxes)
4. Copia el token generado
5. Cuando Git pida contraseña, usa el token

### Opción C: Git Credential Manager

Git para Windows incluye Credential Manager que guarda tus credenciales:

```cmd
git config --global credential.helper wincred
```

La primera vez que hagas push, te pedirá credenciales y las guardará.

---

## 🐛 Problemas Comunes en Windows

### Error: "git: command not found"

**Solución:**
1. Instala Git: https://git-scm.com/download/win
2. Durante instalación, selecciona "Git from the command line and also from 3rd-party software"
3. Reinicia CMD/PowerShell

### Error: "Permission denied (publickey)"

**Solución:**
Usa HTTPS en lugar de SSH:
```cmd
git remote set-url origin https://github.com/TU-USUARIO/video-games-dashboard.git
```

### Error: "fatal: not a git repository"

**Solución:**
Asegúrate de estar en la carpeta correcta:
```cmd
cd ruta\a\tu\proyecto
git init
```

### Error: "LF will be replaced by CRLF"

**Solución:**
Es solo una advertencia, puedes ignorarla o configurar:
```cmd
git config --global core.autocrlf true
```

### Error: "filename too long"

**Solución:**
```cmd
git config --global core.longpaths true
```

---

## 📝 Script Automatizado para Windows

Crea un archivo `deploy.bat` en tu proyecto:

```batch
@echo off
echo ========================================
echo   Deployment Script - Video Games Dashboard
echo ========================================
echo.

REM Verificar Git
git --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Git no esta instalado
    echo Descarga de: https://git-scm.com/download/win
    pause
    exit /b 1
)

echo [1/5] Inicializando Git...
git init

echo [2/5] Agregando archivos...
git add .

echo [3/5] Haciendo commit...
git commit -m "Initial commit: Dashboard de videojuegos"

echo [4/5] Conectando con GitHub...
set /p REPO_URL="Ingresa la URL de tu repositorio GitHub: "
git remote add origin %REPO_URL%

echo [5/5] Subiendo a GitHub...
git push -u origin main

echo.
echo ========================================
echo   Deployment completado!
echo ========================================
echo.
echo Ahora ve a https://share.streamlit.io/ para deployar
pause
```

Para usar:
1. Guarda como `deploy.bat`
2. Doble click en el archivo
3. Sigue las instrucciones

---

## 🎨 Interfaz Gráfica: GitHub Desktop

Si prefieres no usar comandos:

### Instalación
1. Descarga: https://desktop.github.com/
2. Instala y abre
3. Sign in con tu cuenta de GitHub

### Uso
1. File → Add local repository → Selecciona tu carpeta
2. Escribe mensaje de commit
3. Click "Commit to main"
4. Click "Publish repository"
5. Selecciona público
6. Click "Publish repository"

¡Listo! Ahora ve a Streamlit Cloud para deployar.

---

## 🚀 Verificación Final en Windows

Antes de deployar, ejecuta:

```cmd
REM Verificar que la app funciona
streamlit run app.py

REM Si hay errores, instalar dependencias
pip install -r requirements.txt

REM Verificar Git
git status

REM Ver archivos que se subirán
git ls-files
```

---

## 📱 Atajos de Teclado Útiles

- `Ctrl + C` - Detener Streamlit
- `Ctrl + Shift + C` - Copiar en CMD
- `Ctrl + Shift + V` - Pegar en CMD
- `Tab` - Autocompletar rutas
- `↑` - Comando anterior

---

## 🔧 Configuración Recomendada para Windows

### Git Bash como terminal por defecto en VS Code

Si usas VS Code:

1. `Ctrl + Shift + P`
2. Busca "Terminal: Select Default Profile"
3. Selecciona "Git Bash"

### Configurar Git para Windows

```cmd
REM Configuración recomendada
git config --global core.autocrlf true
git config --global core.longpaths true
git config --global credential.helper wincred
```

---

## 📚 Recursos para Windows

- **Git para Windows**: https://git-scm.com/download/win
- **GitHub Desktop**: https://desktop.github.com/
- **VS Code**: https://code.visualstudio.com/
- **Python para Windows**: https://www.python.org/downloads/windows/

---

## 💡 Tips para Windows

1. **Usa Git Bash** para mejor compatibilidad con comandos Unix
2. **GitHub Desktop** es excelente si no te gustan los comandos
3. **VS Code** tiene integración Git incorporada
4. **Windows Terminal** es mejor que CMD tradicional
5. **Credential Manager** guarda tus credenciales automáticamente

---

## 🆘 Ayuda Adicional

Si tienes problemas:

1. **Revisa la ruta**: Asegúrate de estar en la carpeta correcta
2. **Permisos**: Ejecuta como administrador si es necesario
3. **Antivirus**: Temporalmente desactiva si bloquea Git
4. **Firewall**: Permite conexiones de Git

---

**¡Éxito con tu deployment en Windows! 🪟✨**
