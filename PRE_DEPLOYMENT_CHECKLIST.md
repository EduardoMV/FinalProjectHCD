# ✅ Checklist Pre-Deployment

Usa esta lista para verificar que todo está listo antes de subir a GitHub y deployar en Streamlit Cloud.

---

## 📋 Archivos Esenciales

- [ ] `app.py` - Aplicación principal existe y funciona
- [ ] `visual_theme.py` - Módulo de tema visual
- [ ] `data_loader.py` - Módulo de carga de datos
- [ ] `requirements.txt` - Todas las dependencias listadas
- [ ] `README.md` - Documentación completa
- [ ] `.gitignore` - Archivos a ignorar configurados
- [ ] `.streamlit/config.toml` - Configuración de Streamlit

## 📊 Datasets

- [ ] `video_games.csv` - Dataset principal CORGIS
- [ ] `VGSales.csv` - Datos de ventas por género
- [ ] `WarConsole.csv` - Datos de ventas por consola
- [ ] `GlobalGenres.csv` - Géneros por país
- [ ] Todos los CSV están en la raíz del proyecto
- [ ] Los CSV no están en `.gitignore`

## 🧪 Testing Local

- [ ] La app corre sin errores: `streamlit run app.py`
- [ ] Todas las 6 tabs cargan correctamente
- [ ] Las animaciones funcionan suavemente
- [ ] El mapa mundial se renderiza con leyenda a la derecha
- [ ] Las race bars se reordenan correctamente
- [ ] No hay errores en la consola
- [ ] Los datos se cargan correctamente

## 🎨 Visualizaciones

- [ ] Gráfica de ventas por género (barras horizontales)
- [ ] Gráfica de distribución por género (donut)
- [ ] Gráfica de ventas por plataforma (top 15)
- [ ] Gráfica de ventas apiladas (plataforma + género)
- [ ] Mapa mundial con leyenda a la derecha ✨ NUEVO
- [ ] Scatter plot (calidad vs popularidad)
- [ ] Violin plot (puntuaciones por género)
- [ ] Area chart (lanzamientos por año)
- [ ] Dual axis (ventas totales y promedio)
- [ ] Animación de ventas por género (2006-2024)
- [ ] Race bars de consolas (2006-2025) con Top 5
- [ ] Histograma con KDE (tiempos de juego)
- [ ] Box plot (tiempos por género)
- [ ] Heatmap de correlaciones

## 🎬 Animaciones

- [ ] Animación de géneros tiene transiciones suaves (800ms)
- [ ] Race bars se reordenan dinámicamente
- [ ] Botones ▶️ y ⏸️ funcionan correctamente
- [ ] Slider temporal funciona
- [ ] Ejes permanecen fijos (no se mueve el contenedor)
- [ ] Colores son consistentes en todos los frames

## 📝 Documentación

- [ ] README.md tiene descripción clara
- [ ] README.md incluye instrucciones de instalación
- [ ] README.md lista todas las características
- [ ] DEPLOY_GUIDE.md está completo
- [ ] quick_start.md está disponible
- [ ] Comentarios en código están en español
- [ ] Variables tienen nombres descriptivos

## 🔧 Configuración

- [ ] `requirements.txt` incluye todas las dependencias:
  - [ ] streamlit>=1.28.0
  - [ ] pandas>=2.0.0
  - [ ] numpy>=1.24.0
  - [ ] matplotlib>=3.7.0
  - [ ] seaborn>=0.12.0
  - [ ] plotly>=5.17.0
  - [ ] scipy>=1.11.0
- [ ] `.gitignore` excluye archivos innecesarios
- [ ] `.streamlit/config.toml` tiene tema configurado

## 🌐 Preparación para GitHub

- [ ] Git está instalado: `git --version`
- [ ] Git está configurado:
  - [ ] `git config user.name` retorna tu nombre
  - [ ] `git config user.email` retorna tu email
- [ ] Tienes cuenta de GitHub
- [ ] Has creado un Personal Access Token (si es necesario)

## ☁️ Preparación para Streamlit Cloud

- [ ] Tienes cuenta en Streamlit Cloud
- [ ] Has autorizado Streamlit Cloud con GitHub
- [ ] El repositorio será público (requerido para plan gratis)
- [ ] Conoces el nombre que usarás para tu app

## 🎯 Optimizaciones

- [ ] Los CSV no son excesivamente grandes (< 50MB cada uno)
- [ ] No hay archivos innecesarios en el proyecto
- [ ] El código está limpio y comentado
- [ ] No hay prints de debug en el código
- [ ] No hay credenciales hardcodeadas

## 🔒 Seguridad

- [ ] No hay API keys en el código
- [ ] No hay contraseñas en el código
- [ ] `.gitignore` incluye archivos sensibles
- [ ] No hay datos personales en los datasets

## 📸 Extras (Opcional pero Recomendado)

- [ ] Has tomado screenshots del dashboard
- [ ] Has creado GIFs de las animaciones
- [ ] Has actualizado README con imágenes
- [ ] Has preparado una descripción para compartir

---

## 🚀 Listo para Deployar

Si marcaste todas las casillas esenciales (las primeras 5 secciones), ¡estás listo!

### Próximos Pasos:

1. **Subir a GitHub**: Sigue [`quick_start.md`](quick_start.md)
2. **Deployar**: Sigue [`DEPLOY_GUIDE.md`](DEPLOY_GUIDE.md)
3. **Compartir**: ¡Comparte tu app con el mundo!

---

## 🐛 Si Algo Falla

### Durante Testing Local
- Revisa errores en la terminal
- Verifica que todos los CSV existan
- Asegúrate de que requirements.txt esté completo

### Durante Git Push
- Verifica credenciales de GitHub
- Usa Personal Access Token si es necesario
- Revisa que el repositorio remoto esté configurado

### Durante Deployment en Streamlit
- Revisa logs en Streamlit Cloud
- Verifica que requirements.txt sea correcto
- Asegúrate de que todos los archivos estén en GitHub

---

## 📞 Ayuda

- **Git**: https://git-scm.com/doc
- **GitHub**: https://docs.github.com/
- **Streamlit Cloud**: https://docs.streamlit.io/streamlit-community-cloud
- **Forum**: https://discuss.streamlit.io/

---

**¡Buena suerte con tu deployment! 🎉**

---

## 📝 Notas

Fecha de revisión: _______________

Problemas encontrados:
- 
- 
- 

Soluciones aplicadas:
- 
- 
- 

---

**Última actualización:** Diciembre 6, 2024
