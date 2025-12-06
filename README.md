# 🎮 Dashboard de Análisis de Videojuegos

Dashboard interactivo construido con Streamlit para análisis exploratorio de datos de la industria de videojuegos.

[![Python](https://img.shields.io/badge/Python-3.x-blue)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.x-red)](https://streamlit.io/)
[![Plotly](https://img.shields.io/badge/Plotly-5.x-purple)](https://plotly.com/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

## 🌐 Demo en Vivo

**[🚀 Ver Dashboard en Vivo](https://tu-app-aqui.streamlit.app)** ← *Actualiza este link después del deployment*

## 📋 Descripción

Aplicación web interactiva que permite explorar y visualizar datos de la industria de videojuegos, incluyendo:
- 📊 Análisis de ventas por género y plataforma
- 🏆 Evolución temporal de consolas (Race Bars animadas)
- 🎨 Visualizaciones interactivas con Plotly
- 📈 Métricas y estadísticas del mercado
- 🌍 Distribución geográfica de ventas

## ✨ Características Principales

### 🎬 Gráficas Animadas
- **Ventas por Género**: Animación fluida mostrando la evolución de ventas por género (2006-2024)
- **Guerra de Consolas**: Race bars horizontales con las Top 5 consolas compitiendo en tiempo real (2006-2025)

### 🎨 Tema Visual
- Diseño oscuro moderno con gradientes púrpura/azul
- Colores consistentes en todas las visualizaciones
- Interfaz intuitiva y profesional

### 📊 Análisis Incluidos
1. **Introducción**: Vista general del dataset
2. **El Mercado**: Análisis de ventas por género y plataforma
3. **Calidad vs Popularidad**: Relación entre puntuaciones y ventas
4. **Evolución Temporal**: Tendencias a lo largo del tiempo
5. **Experiencia del Jugador**: Métricas de tiempo de juego
6. **Correlaciones**: Relaciones entre variables

## 🚀 Instalación y Uso

### Opción 1: Usar la App en Línea (Recomendado)

Simplemente visita el [Dashboard en Vivo](https://tu-app-aqui.streamlit.app) - ¡No requiere instalación!

### Opción 2: Ejecutar Localmente

#### Requisitos Previos
- Python 3.8 o superior
- pip

#### Pasos de Instalación

1. **Clonar el repositorio**
```bash
git clone https://github.com/tu-usuario/video-games-dashboard.git
cd video-games-dashboard
```

2. **Instalar dependencias**
```bash
pip install -r requirements.txt
```

3. **Ejecutar la aplicación**
```bash
streamlit run app.py
```

4. **Abrir en el navegador**
La aplicación se abrirá automáticamente en `http://localhost:8501`

### Opción 3: Deployar tu Propia Versión

Sigue la guía completa en [`DEPLOY_GUIDE.md`](DEPLOY_GUIDE.md) para subir a GitHub y Streamlit Cloud.

## 📁 Estructura del Proyecto

```
.
├── app.py                          # Aplicación principal de Streamlit
├── visual_theme.py                 # Tema visual y estilos
├── data_loader.py                  # Carga y procesamiento de datos
├── video_games.csv                 # Dataset principal (CORGIS)
├── VGSales.csv                     # Datos de ventas por género
├── WarConsole.csv                  # Datos de ventas por consola
├── requirements.txt                # Dependencias del proyecto
├── README.md                       # Este archivo
├── CAMBIOS_FINALES_GRAFICAS.md    # Documentación de cambios
└── test_*.py                       # Tests de calidad
```

## 📊 Datasets

### 1. video_games.csv (CORGIS)
Dataset principal con información detallada de videojuegos:
- Títulos, géneros, plataformas
- Ventas globales y regionales
- Puntuaciones de crítica y usuarios
- Métricas de tiempo de juego

### 2. VGSales.csv
Datos agregados de ventas por género:
- Ventas globales por año (2006-2024)
- Desglose por región (NA, Europa, Asia-Pacífico)
- Crecimiento año a año
- Participación de mercado

### 3. WarConsole.csv
Ventas acumuladas por consola:
- 20 consolas diferentes
- Datos históricos (2006-2025)
- Ventas en millones de unidades

## 🎯 Uso

### Navegación
1. **Tabs superiores**: Navega entre diferentes análisis
2. **Gráficas interactivas**: Hover para ver detalles
3. **Animaciones**: Usa los botones ▶️ Reproducir y ⏸️ Pausar
4. **Slider temporal**: Navega año por año en las animaciones

### Características Interactivas
- 🖱️ **Hover**: Información detallada al pasar el mouse
- 🎚️ **Zoom**: Acerca/aleja en las gráficas
- 📥 **Exportar**: Descarga gráficas como imágenes
- 🎬 **Animaciones**: Controles de reproducción fluidos

## 🛠️ Tecnologías

- **Streamlit**: Framework web para aplicaciones de datos
- **Pandas**: Manipulación y análisis de datos
- **Plotly**: Visualizaciones interactivas
- **Matplotlib/Seaborn**: Gráficas estáticas
- **NumPy**: Operaciones numéricas
- **SciPy**: Análisis estadístico

## 🎨 Tema Visual

### Paleta de Colores
- **Primario**: Púrpura (#8B5CF6)
- **Secundario**: Azul (#3B82F6)
- **Acento**: Verde (#10B981), Ámbar (#F59E0B)
- **Fondo**: Slate oscuro (#0F172A, #1E293B)
- **Texto**: Gris claro (#F1F5F9)

### Características de Diseño
- Gradientes suaves
- Bordes redondeados
- Sombras sutiles
- Animaciones fluidas (800-1200ms)
- Transiciones cubic-in-out

## 📈 Características Técnicas

### Animaciones
- **Duración de frame**: 1000-1200ms
- **Transición**: 800ms con easing cubic-in-out
- **Redraw**: Completo en cada frame
- **Ordenamiento**: Dinámico en race bars

### Optimizaciones
- Carga eficiente de datos
- Detección automática de columnas
- Manejo de errores robusto
- Código modular y mantenible

## 🧪 Testing

El proyecto incluye tests completos:

```bash
# Ejecutar todos los tests
pytest

# Tests específicos
pytest test_chart_completeness.py
pytest test_spanish_compliance.py
pytest test_visual_theme.py
```

## 📝 Documentación Adicional

- `CAMBIOS_FINALES_GRAFICAS.md`: Detalles de las mejoras implementadas
- `CAMBIOS_*.md`: Historial de cambios específicos
- Comentarios en código para funciones complejas

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Por favor:
1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📄 Licencia

Este proyecto está bajo la licencia MIT. Ver archivo `LICENSE` para más detalles.

## 👥 Autores

- Dashboard desarrollado con Kiro AI
- Dataset CORGIS: https://corgis-edu.github.io/corgis/

## 🙏 Agradecimientos

- Dataset CORGIS por los datos de videojuegos
- Comunidad de Streamlit por el framework
- Plotly por las visualizaciones interactivas

## 📞 Soporte

Para preguntas o problemas:
- Abre un issue en GitHub
- Consulta la documentación en los archivos MD

---

**Última actualización:** Diciembre 6, 2025
**Versión:** 2.0 - Gráficas Animadas Optimizadas
**Estado:** ✅ Producción
