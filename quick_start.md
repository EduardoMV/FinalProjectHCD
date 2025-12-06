# ⚡ Quick Start - Subir a GitHub en 5 Minutos

## 🎯 Objetivo
Subir tu proyecto a GitHub y deployar en Streamlit Cloud lo más rápido posible.

---

## 📝 Comandos Rápidos

### 1️⃣ Preparar Git (Solo primera vez)

```bash
# Configurar tu identidad
git config --global user.name "Tu Nombre"
git config --global user.email "tu-email@ejemplo.com"
```

### 2️⃣ Crear Repositorio en GitHub

1. Ve a https://github.com/new
2. Nombre: `video-games-dashboard`
3. Público
4. NO agregues README ni .gitignore
5. Click "Create repository"
6. **Copia la URL** que aparece

### 3️⃣ Subir el Código

```bash
# En la carpeta de tu proyecto, ejecuta:

# Inicializar Git
git init

# Agregar todos los archivos
git add .

# Hacer commit
git commit -m "Initial commit: Dashboard de videojuegos"

# Conectar con GitHub (reemplaza con TU URL)
git remote add origin https://github.com/TU-USUARIO/video-games-dashboard.git

# Subir
git push -u origin main
```

**Si te pide contraseña:**
- Usuario: Tu username de GitHub
- Contraseña: Crea un [Personal Access Token](https://github.com/settings/tokens)

### 4️⃣ Deployar en Streamlit Cloud

1. Ve a https://share.streamlit.io/
2. Click "New app"
3. Selecciona tu repositorio: `TU-USUARIO/video-games-dashboard`
4. Branch: `main`
5. Main file: `app.py`
6. Click "Deploy!"

**¡Listo!** Tu app estará en línea en 2-3 minutos.

---

## 🔄 Actualizar tu App

Cuando hagas cambios:

```bash
git add .
git commit -m "Descripción del cambio"
git push
```

Streamlit Cloud actualizará automáticamente.

---

## 🆘 Problemas Comunes

### "Permission denied"
→ Usa un Personal Access Token como contraseña

### "ModuleNotFoundError"
→ Verifica que `requirements.txt` tenga todas las dependencias

### "FileNotFoundError" para CSV
→ Asegúrate de que los archivos CSV estén en el repositorio

---

## 📚 Más Ayuda

- Guía completa: [`DEPLOY_GUIDE.md`](DEPLOY_GUIDE.md)
- Documentación Streamlit: https://docs.streamlit.io/
- Soporte: https://discuss.streamlit.io/

---

**¡Éxito! 🎉**
