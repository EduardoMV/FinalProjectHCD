# 📁 Estructura del Proyecto

## Archivos Principales

### 🎮 Aplicación
- `app.py` - Dashboard principal de Streamlit (2034 líneas)
- `visual_theme.py` - Tema visual y estilos
- `data_loader.py` - Carga y procesamiento de datos

### 📊 Datasets
- `video_games.csv` - Dataset principal CORGIS
- `VGSales.csv` - Ventas por género (2006-2024)
- `WarConsole.csv` - Ventas por consola (2006-2025)

### 📄 Documentación
- `README.md` - Guía completa del proyecto
- `CAMBIOS_FINALES_GRAFICAS.md` - Detalles técnicos de las mejoras
- `requirements.txt` - Dependencias de Python

### 🧪 Testing
- `test_chart_completeness.py` - Tests de gráficas
- `test_spanish_compliance.py` - Tests de idioma
- `test_visual_theme.py` - Tests de tema
- `test_sales_analysis.py` - Tests de ventas
- `test_temporal_analysis.py` - Tests temporales
- `test_correlation_analysis.py` - Tests de correlación
- `test_quality_popularity.py` - Tests de calidad
- `test_introduction.py` - Tests de introducción
- `test_navigation_layout.py` - Tests de navegación
- `test_data_loader.py` - Tests de carga de datos

## 🚀 Comandos Rápidos

```bash
# Instalar dependencias
pip install -r requirements.txt

# Ejecutar aplicación
streamlit run app.py

# Ejecutar tests
pytest
```

## 📊 Gráficas Animadas

Las dos gráficas animadas están en el tab **"⏳ Evolución Temporal"**:

1. **Ventas por Género** (VGSales.csv)
   - Período: 2006-2024
   - 15 géneros
   - Animación fluida

2. **Guerra de Consolas** (WarConsole.csv)
   - Período: 2006-2025
   - Top 5 consolas
   - Race bars horizontales

---

**Versión:** 2.0 Final  
**Estado:** ✅ Producción
