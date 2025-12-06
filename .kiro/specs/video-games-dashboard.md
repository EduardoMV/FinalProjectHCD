# Video Games Dashboard - Especificación Completa

## 📋 Resumen del Proyecto

Dashboard interactivo de análisis de datos de videojuegos construido con Streamlit, que permite explorar ventas, calidad, evolución temporal, experiencia del jugador y correlaciones en la industria de los videojuegos.

**Estado:** ✅ Completado y Funcional  
**Versión:** 1.0  
**Fecha:** Diciembre 2024  
**Idioma:** Español

---

## 🎯 Objetivos del Proyecto

### Objetivo Principal
Crear una aplicación web interactiva que permita a analistas, investigadores y entusiastas explorar datos de la industria de videojuegos a través de visualizaciones dinámicas y análisis estadísticos.

### Objetivos Específicos
1. **Análisis de Mercado:** Visualizar ventas por género, plataforma y región
2. **Calidad vs Popularidad:** Explorar la relación entre crítica y éxito comercial
3. **Evolución Temporal:** Mostrar tendencias históricas con animaciones fluidas
4. **Experiencia del Jugador:** Analizar tiempos de completado por género
5. **Correlaciones:** Descubrir relaciones ocultas entre variables

---

## 👥 Usuarios Objetivo

- **Analistas de Datos:** Profesionales que necesitan insights del mercado de videojuegos
- **Investigadores:** Académicos estudiando la industria del entretenimiento
- **Desarrolladores de Juegos:** Equipos buscando entender tendencias del mercado
- **Entusiastas:** Jugadores interesados en estadísticas de la industria

---

## 📊 Fuentes de Datos

### 1. video_games.csv (CORGIS Dataset)
**Propósito:** Dataset principal con información detallada de juegos  
**Columnas Clave:**
- `Title`: Nombre del juego
- `Metadata_Genres`: Género del juego
- `Release_Console`: Plataforma de lanzamiento
- `Release_Year`: Año de publicación
- `Metrics_Sales`: Ventas globales (millones)
- `Metrics_Review_Score`: Puntuación de crítica (0-100)
- `Length_Main_Story_Average`: Tiempo para completar historia principal (horas)
- `Features_Max_Players`: Número máximo de jugadores

### 2. VGSales.csv
**Propósito:** Datos de ventas por género y año para animaciones temporales  
**Columnas:**
- `Year`: Año (2006-2024)
- `Genre`: Género del juego
- `Global_Sales_Millions`: Ventas globales en millones
- `North_America_Sales`, `Europe_Sales`, `Asia_Pacific_Sales`, `Rest_of_World_Sales`: Ventas regionales
- `YoY_Growth_Percent`: Crecimiento año a año
- `Market_Share_Percent`: Participación de mercado
- `Platform_Primary`: Plataforma principal

**Géneros incluidos:** Action, Shooter, Role-Playing, Sports, Adventure, Racing, Strategy, Puzzle_Casual, Fighting, Simulation, Battle_Royale, MMORPG, Platformer, Horror, Music_Rhythm

### 3. WarConsole.csv
**Propósito:** Datos históricos de ventas acumuladas por consola para race bars  
**Columnas:**
- `Year`: Año (2006-2025)
- Columnas de consolas (20 total): PlayStation_2, PlayStation_3, PlayStation_4, PlayStation_5, Xbox, Xbox_360, Xbox_One, Xbox_Series_XS, GameCube, Nintendo_Wii, Nintendo_Wii_U, Nintendo_Switch, Nintendo_Switch_2, Nintendo_DS, Nintendo_3DS, Game_Boy_Advance, PSP, PS_Vita, Sega_Dreamcast, Steam_Deck

**Valores:** Ventas acumuladas en millones de unidades

### 4. GlobalGenres.csv
**Propósito:** Género más jugado por país para mapa geográfico  
**Columnas:**
- `Country`: Nombre del país (195 países)
- `Most_Played_Genre`: Género más popular (Action, Shooter, Sports, Role-Playing, Strategy, MOBA)

---

## 🏗️ Arquitectura del Sistema

### Estructura de Archivos
```
proyecto/
├── app.py                          # Aplicación principal (2117 líneas)
├── visual_theme.py                 # Tema visual y estilos
├── data_loader.py                  # Carga y procesamiento de datos
├── video_games.csv                 # Dataset principal CORGIS
├── VGSales.csv                     # Ventas por género/año
├── WarConsole.csv                  # Ventas por consola/año
├── GlobalGenres.csv                # Géneros por país
├── requirements.txt                # Dependencias Python
├── README.md                       # Documentación principal
├── CAMBIOS_FINALES_GRAFICAS.md    # Detalles técnicos de gráficas
├── ESTRUCTURA_PROYECTO.md         # Estructura del proyecto
└── test_*.py                       # 10 archivos de pruebas
```

### Stack Tecnológico

**Framework Principal:**
- Streamlit 1.x - Framework web para dashboards interactivos

**Librerías de Datos:**
- pandas - Manipulación y análisis de datos
- numpy - Operaciones numéricas

**Librerías de Visualización:**
- matplotlib - Gráficas estáticas
- seaborn - Visualizaciones estadísticas
- plotly.express - Gráficas interactivas
- plotly.graph_objects - Gráficas personalizadas avanzadas

**Análisis Estadístico:**
- scipy.stats - Correlaciones y análisis estadístico

**Python:** 3.x (compatible con 3.8+)

---

## 🎨 Sistema de Diseño Visual

### Tema Visual (visual_theme.py)

**Paleta de Colores:**
```python
PRIMARY_COLORS = ['#8B5CF6', '#3B82F6', '#10B981', '#F59E0B', '#EF4444']
ACCENT_COLORS = ['#EC4899', '#06B6D4', '#FBBF24', '#60A5FA', '#34D399']
TEXT_PRIMARY = '#F1F5F9'
TEXT_SECONDARY = '#94A3B8'
CARD_BACKGROUND = '#1E293B'
```

**Características:**
- Modo oscuro por defecto
- Gradientes suaves en tarjetas métricas
- Colores consistentes por categoría
- Alta legibilidad con contraste optimizado

### Componentes Visuales

1. **Tarjetas Métricas:** Gradientes con bordes redondeados
2. **Gráficas:** Tema oscuro consistente con Plotly
3. **Contenedores:** Fondos con sombras y bordes redondeados
4. **Texto:** Jerarquía clara con colores primarios y secundarios

---

## 📑 Estructura de la Aplicación

### Configuración Inicial
```python
st.set_page_config(
    page_title="Video Games Dashboard (CORGIS)",
    layout="wide"
)
```

### Sistema de Pestañas (6 tabs)

#### 1. 📘 Introducción
**Propósito:** Bienvenida y vista general del dataset

**Componentes:**
- Título con emoji y descripción
- 3 tarjetas métricas: Juegos Totales, Rango de Años, Plataformas
- Narrativa introductoria
- Vista previa de datos (primeras 10 filas)
- Información de columnas disponibles

**Métricas Calculadas:**
- Total de juegos en dataset
- Rango de años (filtrado 1980-2025)
- Número de plataformas únicas

#### 2. 💰 El Mercado
**Propósito:** Análisis de ventas por género y plataforma

**Visualizaciones:**

1. **Ventas por Género (Barras Horizontales)**
   - Tipo: `go.Bar` horizontal
   - Datos: Suma de ventas por género
   - Colores: Asignados por categoría
   - Texto: Valores formateados (ej: "25.0M")
   - Orden: Descendente por ventas

2. **Distribución de Juegos por Género (Donut Chart)**
   - Tipo: `go.Pie` con hole=0.3
   - Datos: Conteo de juegos por género
   - Información: Label + porcentaje
   - Leyenda: Vertical a la derecha

3. **Ventas por Plataforma (Top 15)**
   - Tipo: `go.Bar` horizontal
   - Datos: Top 15 plataformas por ventas
   - Destacado: Top 3 con colores accent
   - Anotaciones: "Top 1", "Top 2", "Top 3"

4. **Ventas por Plataforma y Género (Barras Apiladas)**
   - Tipo: `go.Bar` con barmode='stack'
   - Datos: Top 10 plataformas, Top 8 géneros
   - Colores: Por género
   - Orientación: Horizontal

5. **Mapa Mundial de Géneros Más Jugados**
   - Tipo: `go.Choropleth`
   - Datos: GlobalGenres.csv
   - Colores: Por género (países con mismo género = mismo color)
   - Mapeo: 195 países con códigos ISO-3
   - Leyenda: 6 géneros con conteo de países
   - Proyección: Natural Earth

**Mapeo de Colores por Género:**
- Action: #8B5CF6 (Púrpura)
- Shooter: #3B82F6 (Azul)
- Sports: #10B981 (Verde)
- Role-Playing: #F59E0B (Ámbar)
- Strategy: #EF4444 (Rojo)
- MOBA: #EC4899 (Rosa)

#### 3. ⭐ Calidad vs Popularidad
**Propósito:** Explorar relación entre crítica y ventas

**Visualizaciones:**

1. **Scatter Plot: Puntuación vs Ventas**
   - Tipo: `go.Scatter` con puntos por género
   - Línea de tendencia: Regresión lineal con scipy.stats
   - Colores: Por género
   - Estadística: Coeficiente de correlación (r)
   - Interpretación: Fuerza y dirección de correlación

2. **Violin Plot: Distribución de Puntuaciones por Género**
   - Tipo: `go.Violin`
   - Datos: Puntuaciones por género
   - Orden: Descendente por mediana
   - Características: Box visible, meanline visible
   - Opacidad: 0.6

**Análisis Estadístico:**
- Correlación de Pearson
- Interpretación automática de fuerza (fuerte/moderada/débil)
- Narrativa contextual basada en resultados

#### 4. ⏳ Evolución Temporal
**Propósito:** Mostrar tendencias históricas con animaciones

**Visualizaciones:**

1. **Lanzamientos por Año (Area Chart)**
   - Tipo: `go.Scatter` con fill='tozeroy'
   - Datos: Conteo de juegos por año
   - Anotación: Año pico con número de lanzamientos

2. **Tendencias de Ventas (Dual Y-Axis)**
   - Tipo: Dos `go.Scatter` (ventas totales y promedio)
   - Eje Y1: Ventas totales
   - Eje Y2: Ventas promedio
   - Anotación: Año con ventas máximas

3. **Vista Combinada: Lanzamientos vs Ventas**
   - Tipo: `go.Bar` + `go.Scatter`
   - Barras: Lanzamientos
   - Línea: Ventas totales
   - Análisis: Correlación entre cantidad y ventas

4. **Evolución de Ventas por Género (Animada)**
   - Fuente: VGSales.csv
   - Tipo: `px.bar` con animation_frame
   - Período: 2006-2024
   - Géneros: 15 géneros
   - Animación: 
     - Frame duration: 1000ms
     - Transition duration: 800ms
     - Easing: cubic-in-out
   - Texto: Valores formateados en barras
   - Colores: Consistentes por género
   - Controles: Botones play/pause estándar de Plotly

5. **Race Bars: Guerra de Consolas (Animada)**
   - Fuente: WarConsole.csv
   - Tipo: `go.Figure` con frames manuales
   - Período: 2006-2025
   - Consolas: Top 5 por año
   - Orientación: Horizontal
   - Características:
     - Reordenamiento dinámico (líder siempre arriba)
     - Ejes fijos (no se mueve el contenedor)
     - Frame duration: 1200ms
     - Transition duration: 800ms
     - Easing: cubic-in-out
   - Controles:
     - Botones: ▶ (play) y ⏸ (pause) en parte inferior
     - Slider: Navegación por años
   - Colores: Únicos por consola
   - Texto: Valores formateados (ej: "154.0M")
   - Rango X: Fijo en [0, max_sales * 1.15]

**Implementación Técnica de Race Bars:**
```python
# Crear frames manualmente para control total
for year in years:
    year_data = df_race[df_race['Year'] == year]
    year_data = year_data.sort_values('Sales', ascending=True).tail(5)
    
    frame = go.Frame(
        data=[go.Bar(...)],
        name=str(year),
        layout=go.Layout(
            xaxis=dict(range=[0, max_sales * 1.15])  # Rango fijo
        )
    )
```

**Estadísticas Mostradas:**
- Número de consolas en competencia
- Líder actual
- Período analizado

#### 5. 🎮 Experiencia del Jugador
**Propósito:** Analizar tiempos de completado

**Visualizaciones:**

1. **Histograma con KDE: Distribución de Tiempos**
   - Tipo: `go.Histogram` + `go.Scatter` (KDE)
   - Bins: 30
   - Overlay: Curva de densidad (KDE) en eje Y secundario
   - Líneas verticales: Media y mediana
   - Posicionamiento inteligente de anotaciones

2. **Box Plot: Tiempos por Género**
   - Tipo: `go.Box`
   - Filtro: Géneros con ≥5 juegos
   - Orden: Descendente por mediana
   - Características: boxmean='sd' (muestra media y desviación)

3. **Tabla de Estadísticas por Género**
   - Columnas: Promedio, Mediana, Mínimo, Máximo, Juegos
   - Orden: Por mediana descendente
   - Formato: 1 decimal

**Análisis Estadístico:**
- Media y mediana de tiempos
- Distribución por género
- Identificación de géneros más largos/cortos

#### 6. 🔗 Correlaciones
**Propósito:** Descubrir relaciones ocultas entre variables

**Visualizaciones:**

1. **Mapa de Calor de Correlaciones**
   - Tipo: `go.Heatmap`
   - Colorscale: 'RdYlBu_r' (Rojo-Amarillo-Azul)
   - Rango: -1 a +1, centrado en 0
   - Anotaciones: Valores en cada celda
   - Destacado: Correlaciones fuertes (|r| > 0.7) en negrita

**Variables Analizadas:**
- Ventas (millones)
- Puntuación de Crítica
- Precio Usado ($)
- Año de Lanzamiento
- Tiempo Historia Principal (hrs)
- Tiempo Todos los Estilos (hrs)
- Tiempo Completionistas (hrs)
- Jugadores Máximos

2. **Tabla de Correlaciones Fuertes**
   - Filtro: |r| > 0.7
   - Columnas: Variable 1, Variable 2, Correlación, Tipo
   - Orden: Por fuerza descendente

**Interpretación Automática:**
- Clasificación de fuerza (fuerte/moderada/débil)
- Dirección (positiva/negativa)
- Narrativa contextual
- Guía de interpretación de valores

---

## 🔧 Funcionalidades Técnicas

### Carga de Datos (data_loader.py)

**Función `load_data(filename)`:**
- Carga CSV con manejo de errores
- Normaliza nombres de columnas (reemplaza `.` y espacios con `_`)
- Retorna DataFrame de pandas

**Función `find_column(df, options)`:**
- Búsqueda flexible de columnas
- Acepta lista de nombres alternativos
- Retorna primer match encontrado
- Manejo de case-insensitive

### Sistema de Colores Dinámico

**Función `get_color_for_category(category, all_categories)`:**
- Asigna colores consistentes por categoría
- Usa hash para determinismo
- Cicla entre PRIMARY_COLORS y ACCENT_COLORS
- Garantiza mismo color para misma categoría

### Aplicación de Tema

**Función `apply_plotly_theme(fig)`:**
- Aplica colores de fondo consistentes
- Configura colores de texto
- Ajusta colores de ejes y grids
- Retorna figura modificada

**Función `inject_custom_css()`:**
- Inyecta CSS personalizado en Streamlit
- Modifica estilos de botones y controles
- Mejora apariencia de sliders

### Manejo de Datos Faltantes

**Estrategias:**
1. **Filtrado:** Eliminar filas con valores nulos en columnas críticas
2. **Validación:** Verificar rangos válidos (ej: años 1980-2025)
3. **Valores positivos:** Filtrar valores ≤ 0 en tiempos de juego
4. **Mensajes informativos:** Warnings cuando no hay datos suficientes

---

## 📐 Especificaciones de Animaciones

### Animación de Ventas por Género

**Configuración:**
```python
fig.layout.updatemenus[0].buttons[0].args[1] = {
    'frame': {'duration': 1000, 'redraw': True},
    'transition': {'duration': 800, 'easing': 'cubic-in-out'}
}
```

**Características:**
- Transiciones suaves entre años
- Colores consistentes por género
- Valores formateados en barras
- Rango Y fijo para evitar saltos

### Animación de Race Bars

**Configuración:**
```python
updatemenus=[{
    'type': 'buttons',
    'y': 0,  # Botones en parte inferior
    'buttons': [
        {'label': '▶', 'args': [None, {
            'frame': {'duration': 1200},
            'transition': {'duration': 800, 'easing': 'cubic-in-out'}
        }]},
        {'label': '⏸', 'args': [[None], {'frame': {'duration': 0}}]}
    ]
}]
```

**Características Clave:**
- Reordenamiento dinámico en cada frame
- Ejes X fijos (range=[0, max * 1.15])
- Solo barras se mueven, contenedor estático
- Botones estilo Plotly estándar
- Slider sincronizado con frames

---

## 🧪 Testing

### Archivos de Prueba (10 archivos)

1. `test_chart_completeness.py` - Verifica que todas las gráficas se generen
2. `test_correlation_analysis.py` - Prueba análisis de correlaciones
3. `test_data_loader.py` - Valida carga de datos
4. `test_introduction.py` - Verifica tab de introducción
5. `test_navigation_layout.py` - Prueba navegación y layout
6. `test_quality_popularity.py` - Valida análisis calidad vs popularidad
7. `test_sales_analysis.py` - Prueba análisis de ventas
8. `test_spanish_compliance.py` - Verifica texto en español
9. `test_temporal_analysis.py` - Valida análisis temporal
10. `test_visual_theme.py` - Prueba tema visual

**Framework:** pytest con hypothesis para property-based testing

---

## 📝 Convenciones de Código

### Estilo
- **Idioma:** Español para UI, comentarios y variables de usuario
- **Formato:** PEP 8 con algunas excepciones para legibilidad
- **Nombres:** snake_case para variables, PascalCase para clases

### Estructura de Código
```python
# 1. Imports
# 2. Configuración de página
# 3. Aplicación de tema
# 4. Header
# 5. Carga de datos
# 6. Detección de columnas
# 7. Tabs (6 secciones)
```

### Patrones de Visualización
```python
# Patrón estándar para gráficas
st.markdown("""<div>Título y descripción</div>""", unsafe_allow_html=True)
# Crear figura
fig = go.Figure(...)
# Aplicar tema
fig = VisualTheme.apply_plotly_theme(fig)
# Mostrar
st.plotly_chart(fig, use_container_width=True)
# Explicación de variables
st.markdown("""<div>Explicación</div>""", unsafe_allow_html=True)
# Insight narrativo
st.markdown(f"""<div>Insight: {resultado}</div>""", unsafe_allow_html=True)
```

---

## 🚀 Comandos de Ejecución

### Instalación
```bash
pip install -r requirements.txt
```

### Ejecución
```bash
streamlit run app.py
```

### Testing
```bash
pytest
pytest test_specific.py
pytest -v  # Verbose
```

---

## 📦 Dependencias (requirements.txt)

```
streamlit>=1.28.0
pandas>=2.0.0
numpy>=1.24.0
matplotlib>=3.7.0
seaborn>=0.12.0
plotly>=5.17.0
scipy>=1.11.0
pytest>=7.4.0
hypothesis>=6.88.0
```

---

## 🎯 Criterios de Aceptación

### Funcionalidad
- [x] Carga correcta de 4 datasets (video_games.csv, VGSales.csv, WarConsole.csv, GlobalGenres.csv)
- [x] 6 tabs funcionales con contenido completo
- [x] 20+ visualizaciones interactivas
- [x] Animaciones fluidas (género y consolas)
- [x] Mapa geográfico con 195 países
- [x] Análisis estadístico (correlaciones, regresiones)

### Rendimiento
- [x] Carga inicial < 5 segundos
- [x] Transiciones de animación suaves (800ms)
- [x] Responsive en diferentes tamaños de pantalla

### Usabilidad
- [x] Interfaz en español
- [x] Narrativas contextuales en cada gráfica
- [x] Explicaciones de variables
- [x] Insights automáticos basados en datos
- [x] Controles intuitivos (play/pause, sliders)

### Calidad de Código
- [x] Código modularizado (app.py, visual_theme.py, data_loader.py)
- [x] Manejo de errores robusto
- [x] Comentarios en español
- [x] 10 archivos de pruebas

---

## 🐛 Problemas Conocidos y Soluciones

### Problema 1: Race Bars con Plotly Express
**Síntoma:** Consolas no se reordenan dinámicamente  
**Causa:** px.bar no soporta reordenamiento en frames  
**Solución:** Usar go.Frame manual con sort en cada frame

### Problema 2: Ejes móviles en animaciones
**Síntoma:** Gráfica completa se mueve, no solo barras  
**Causa:** Rango de ejes no fijo  
**Solución:** Establecer range=[0, max*1.15] en cada frame

### Problema 3: Atributos de VisualTheme
**Síntoma:** AttributeError: 'BG_SECONDARY' no existe  
**Causa:** Nombres de atributos incorrectos  
**Solución:** Usar CARD_BACKGROUND en lugar de BG_SECONDARY/BG_PRIMARY

### Problema 4: Sintaxis de Plotly titlefont
**Síntoma:** Invalid property 'titlefont'  
**Causa:** Sintaxis antigua de Plotly  
**Solución:** Usar title.font en lugar de titlefont

---

## 🔮 Mejoras Futuras (Backlog)

### Funcionalidades
- [ ] Filtros interactivos por año, género, plataforma
- [ ] Exportación de gráficas a PNG/SVG
- [ ] Comparación lado a lado de géneros/plataformas
- [ ] Predicciones con machine learning
- [ ] Dashboard personalizable (drag & drop)

### Datos
- [ ] Integración con APIs en tiempo real
- [ ] Datos de streaming (Twitch, YouTube Gaming)
- [ ] Información de desarrolladores y publishers
- [ ] Datos de DLC y microtransacciones

### Visualizaciones
- [ ] Gráficas 3D interactivas
- [ ] Network graphs de géneros relacionados
- [ ] Sankey diagrams de flujo de jugadores
- [ ] Heatmaps temporales

### Técnicas
- [ ] Caché de datos con @st.cache_data
- [ ] Lazy loading de gráficas pesadas
- [ ] Modo claro/oscuro toggle
- [ ] Internacionalización (i18n) para inglés

---

## 📚 Referencias y Recursos

### Datasets
- **CORGIS:** https://corgis-edu.github.io/corgis/csv/video_games/
- **VGSales:** Dataset personalizado de ventas por género
- **WarConsole:** Dataset personalizado de ventas por consola
- **GlobalGenres:** Dataset personalizado de preferencias por país

### Documentación
- **Streamlit:** https://docs.streamlit.io/
- **Plotly:** https://plotly.com/python/
- **Pandas:** https://pandas.pydata.org/docs/
- **Seaborn:** https://seaborn.pydata.org/

### Inspiración
- Dashboards de análisis de videojuegos
- Visualizaciones de datos temporales
- Race bar charts animados

---

## 👨‍💻 Información de Desarrollo

### Historial de Cambios Principales

**Versión 1.0 (Diciembre 2024)**
- ✅ Migración de ventas por género a VGSales.csv
- ✅ Implementación de race bars con WarConsole.csv
- ✅ Corrección de errores de VisualTheme
- ✅ Optimización de animaciones (800ms cubic-in-out)
- ✅ Mapa mundial con GlobalGenres.csv
- ✅ Limpieza de archivos redundantes
- ✅ Documentación completa

### Lecciones Aprendidas

1. **Animaciones Fluidas:** Usar transiciones cubic-in-out con duración 800ms para mejor UX
2. **Race Bars:** Frames manuales necesarios para reordenamiento dinámico
3. **Ejes Fijos:** Crucial para evitar que contenedor se mueva en animaciones
4. **Colores Consistentes:** Hash-based color assignment garantiza consistencia
5. **Narrativas:** Insights automáticos mejoran comprensión de datos

---

## 📄 Licencia y Uso

**Tipo:** Proyecto educativo/analítico  
**Uso:** Libre para análisis, investigación y educación  
**Datos:** CORGIS dataset (dominio público), datasets personalizados

---

## 🤝 Contribuciones

Para contribuir al proyecto:

1. Mantener idioma español en UI
2. Seguir convenciones de código existentes
3. Agregar pruebas para nuevas funcionalidades
4. Documentar cambios en esta especificación
5. Asegurar que animaciones sean fluidas (800ms transitions)

---

## 📞 Soporte

Para preguntas o problemas:
- Revisar esta especificación completa
- Consultar archivos de documentación (README.md, CAMBIOS_FINALES_GRAFICAS.md)
- Ejecutar pruebas con pytest
- Verificar logs de Streamlit

---

**Última actualización:** Diciembre 6, 2024  
**Estado del proyecto:** ✅ Completado y Funcional  
**Próxima revisión:** Según necesidades de mejoras futuras
