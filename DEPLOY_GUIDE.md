# 🚀 Guía de Deployment a GitHub y Streamlit Cloud

Esta guía te llevará paso a paso para subir tu proyecto a GitHub y hostearlo en Streamlit Cloud.

---

## 📋 Pre-requisitos

Antes de comenzar, asegúrate de tener:

- ✅ Cuenta de GitHub (https://github.com)
- ✅ Git instalado en tu computadora
- ✅ Cuenta de Streamlit Cloud (https://streamlit.io/cloud) - puedes usar tu cuenta de GitHub

---

## 🔧 Paso 1: Preparar el Proyecto Localmente

### 1.1 Verificar que todo funciona

```bash
# Ejecutar la aplicación localmente
streamlit run app.py
```

Asegúrate de que todo funciona correctamente antes de subir.

### 1.2 Verificar archivos necesarios

Tu proyecto debe tener estos archivos:
- ✅ `app.py` - Aplicación principal
- ✅ `visual_theme.py` - Tema visual
- ✅ `data_loader.py` - Cargador de datos
- ✅ `requirements.txt` - Dependencias
- ✅ `video_games.csv` - Dataset principal
- ✅ `VGSales.csv` - Datos de ventas
- ✅ `WarConsole.csv` - Datos de consolas
- ✅ `GlobalGenres.csv` - Datos de géneros por país
- ✅ `.gitignore` - Archivos a ignorar
- ✅ `README.md` - Documentación

---

## 📦 Paso 2: Crear Repositorio en GitHub

### 2.1 Crear nuevo repositorio

1. Ve a https://github.com
2. Click en el botón **"+"** (arriba derecha) → **"New repository"**
3. Configura tu repositorio:
   - **Repository name**: `video-games-dashboard` (o el nombre que prefieras)
   - **Description**: "Dashboard interactivo de análisis de videojuegos con Streamlit"
   - **Visibility**: Public (necesario para Streamlit Cloud gratis)
   - ❌ **NO** marques "Add a README file" (ya tienes uno)
   - ❌ **NO** agregues .gitignore (ya tienes uno)
4. Click en **"Create repository"**

### 2.2 Copiar la URL del repositorio

GitHub te mostrará una página con comandos. Copia la URL que aparece, algo como:
```
https://github.com/tu-usuario/video-games-dashboard.git
```

---

## 💻 Paso 3: Subir el Proyecto a GitHub

### 3.1 Abrir terminal en tu proyecto

Abre una terminal (CMD, PowerShell, o Git Bash) en la carpeta de tu proyecto.

### 3.2 Inicializar Git (si no está inicializado)

```bash
# Verificar si ya está inicializado
git status

# Si no está inicializado, ejecutar:
git init
```

### 3.3 Configurar Git (primera vez)

Si es tu primera vez usando Git, configura tu identidad:

```bash
git config --global user.name "Tu Nombre"
git config --global user.email "tu-email@ejemplo.com"
```

### 3.4 Agregar archivos al repositorio

```bash
# Agregar todos los archivos
git add .

# Verificar qué archivos se agregarán
git status
```

### 3.5 Hacer el primer commit

```bash
git commit -m "Initial commit: Video Games Dashboard con animaciones"
```

### 3.6 Conectar con GitHub

Reemplaza `TU-URL-AQUI` con la URL que copiaste en el Paso 2.2:

```bash
# Agregar el repositorio remoto
git remote add origin TU-URL-AQUI

# Ejemplo:
# git remote add origin https://github.com/tu-usuario/video-games-dashboard.git
```

### 3.7 Subir el código

```bash
# Subir a GitHub
git push -u origin main
```

Si te pide autenticación:
- **Usuario**: Tu nombre de usuario de GitHub
- **Contraseña**: Usa un **Personal Access Token** (no tu contraseña)
  - Crear token: GitHub → Settings → Developer settings → Personal access tokens → Tokens (classic) → Generate new token
  - Permisos necesarios: `repo` (todos los checkboxes)

### 3.8 Verificar en GitHub

Ve a tu repositorio en GitHub y verifica que todos los archivos estén ahí.

---

## ☁️ Paso 4: Deployar en Streamlit Cloud

### 4.1 Ir a Streamlit Cloud

1. Ve a https://streamlit.io/cloud
2. Click en **"Sign in"** o **"Get started"**
3. Selecciona **"Continue with GitHub"**
4. Autoriza a Streamlit Cloud para acceder a tus repositorios

### 4.2 Crear nueva app

1. Click en **"New app"** (botón azul)
2. Configura tu app:
   - **Repository**: Selecciona `tu-usuario/video-games-dashboard`
   - **Branch**: `main`
   - **Main file path**: `app.py`
   - **App URL**: Elige un nombre único (ej: `mi-dashboard-videojuegos`)
3. Click en **"Deploy!"**

### 4.3 Esperar el deployment

- Streamlit Cloud instalará las dependencias automáticamente
- Verás logs en tiempo real
- El proceso toma 2-5 minutos normalmente
- Cuando termine, verás tu app funcionando 🎉

### 4.4 Obtener la URL

Tu app estará disponible en:
```
https://tu-app-name.streamlit.app
```

---

## 🔄 Paso 5: Actualizar tu App (Futuras Modificaciones)

Cuando hagas cambios en tu código:

```bash
# 1. Agregar cambios
git add .

# 2. Hacer commit con mensaje descriptivo
git commit -m "Descripción de los cambios"

# 3. Subir a GitHub
git push

# 4. Streamlit Cloud detectará los cambios y re-deployará automáticamente
```

---

## 🎨 Paso 6: Personalizar tu Deployment (Opcional)

### 6.1 Configurar recursos

En Streamlit Cloud, puedes ajustar:
- **Settings** → **Resources**: Ajustar memoria y CPU
- **Settings** → **Secrets**: Agregar variables de entorno (si necesitas)

### 6.2 Agregar dominio personalizado

Si tienes un dominio propio:
- **Settings** → **General** → **Custom subdomain**

### 6.3 Configurar analytics

Streamlit Cloud incluye analytics básicos:
- **Analytics** → Ver visitas, usuarios, etc.

---

## 🐛 Solución de Problemas Comunes

### Error: "ModuleNotFoundError"

**Problema**: Falta una dependencia en `requirements.txt`

**Solución**:
```bash
# Agregar la dependencia faltante a requirements.txt
echo "nombre-paquete==version" >> requirements.txt

# Subir cambios
git add requirements.txt
git commit -m "Fix: Agregar dependencia faltante"
git push
```

### Error: "FileNotFoundError" para CSV

**Problema**: Los archivos CSV no se subieron a GitHub

**Solución**:
```bash
# Verificar que los CSV estén en el repositorio
git status

# Si no están, agregarlos
git add *.csv
git commit -m "Add CSV datasets"
git push
```

### Error: "Permission denied" al hacer push

**Problema**: Credenciales incorrectas

**Solución**:
1. Crear un Personal Access Token en GitHub
2. Usar el token como contraseña
3. O configurar SSH keys

### App muy lenta en Streamlit Cloud

**Problema**: Archivos CSV muy grandes

**Solución**:
1. Optimizar CSVs (reducir columnas innecesarias)
2. Usar `@st.cache_data` para cachear datos
3. Considerar plan de pago para más recursos

---

## 📊 Verificación Final

Antes de compartir tu app, verifica:

- ✅ La app carga sin errores
- ✅ Todas las gráficas se muestran correctamente
- ✅ Las animaciones funcionan suavemente
- ✅ El mapa mundial se renderiza
- ✅ Los datos se cargan correctamente
- ✅ La navegación entre tabs funciona
- ✅ El diseño se ve bien en diferentes tamaños de pantalla

---

## 🎉 ¡Listo!

Tu dashboard ya está en línea y accesible para todo el mundo.

### Compartir tu app:

```
🌐 URL de tu app: https://tu-app-name.streamlit.app
📦 Repositorio GitHub: https://github.com/tu-usuario/video-games-dashboard
```

### Próximos pasos:

1. **Compartir**: Envía el link a amigos, colegas, o en redes sociales
2. **Documentar**: Actualiza el README con la URL de tu app
3. **Mejorar**: Agrega nuevas features y actualiza con `git push`
4. **Monitorear**: Revisa analytics en Streamlit Cloud

---

## 📚 Recursos Adicionales

- **Documentación Streamlit Cloud**: https://docs.streamlit.io/streamlit-community-cloud
- **Guía de Git**: https://git-scm.com/doc
- **GitHub Guides**: https://guides.github.com/
- **Streamlit Forum**: https://discuss.streamlit.io/

---

## 💡 Tips Pro

1. **Commits frecuentes**: Haz commits pequeños y descriptivos
2. **Branches**: Usa branches para features nuevas
3. **Issues**: Usa GitHub Issues para trackear bugs y mejoras
4. **README**: Mantén el README actualizado con screenshots
5. **Secrets**: Nunca subas API keys o contraseñas al repositorio

---

**¿Necesitas ayuda?**

- 🐛 Reporta bugs en GitHub Issues
- 💬 Pregunta en Streamlit Forum
- 📧 Contacta al equipo de soporte de Streamlit Cloud

---

**¡Felicidades por tu deployment! 🎊**
