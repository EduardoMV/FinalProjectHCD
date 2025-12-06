# 📸 Screenshots Sugeridos para el README

Para hacer tu README más atractivo, toma screenshots de estas secciones y agrégalas al README.md

## 🎯 Screenshots Recomendados

### 1. Hero Image (Principal)
**Ubicación:** Justo después del título en README.md  
**Captura:** Vista completa del dashboard en la tab "Introducción"  
**Incluye:** Título, métricas principales, y vista previa de datos

```markdown
![Dashboard Principal](screenshots/hero.png)
```

### 2. Animación de Ventas por Género
**Ubicación:** Sección "Características Principales"  
**Captura:** GIF o imagen de la gráfica animada de ventas por género  
**Incluye:** Barras de colores con valores, controles de reproducción

```markdown
![Ventas por Género Animadas](screenshots/genre-animation.gif)
```

### 3. Race Bars de Consolas
**Ubicación:** Sección "Características Principales"  
**Captura:** GIF de las race bars en acción  
**Incluye:** Top 5 consolas moviéndose, slider temporal

```markdown
![Guerra de Consolas](screenshots/console-race.gif)
```

### 4. Mapa Mundial
**Ubicación:** Sección "Análisis Incluidos"  
**Captura:** Mapa mundial con leyenda de géneros al lado derecho  
**Incluye:** Países coloreados, leyenda visible

```markdown
![Mapa de Géneros por País](screenshots/world-map.png)
```

### 5. Análisis de Correlaciones
**Ubicación:** Sección "Análisis Incluidos"  
**Captura:** Heatmap de correlaciones  
**Incluye:** Matriz completa con valores

```markdown
![Análisis de Correlaciones](screenshots/correlations.png)
```

### 6. Scatter Plot Calidad vs Popularidad
**Ubicación:** Sección "Análisis Incluidos"  
**Captura:** Gráfica de dispersión con línea de tendencia  
**Incluye:** Puntos de colores, línea de regresión

```markdown
![Calidad vs Popularidad](screenshots/quality-vs-sales.png)
```

---

## 📁 Estructura de Carpeta Sugerida

```
screenshots/
├── hero.png                    # Vista principal
├── genre-animation.gif         # Animación de géneros
├── console-race.gif           # Race bars de consolas
├── world-map.png              # Mapa mundial
├── correlations.png           # Heatmap
└── quality-vs-sales.png       # Scatter plot
```

---

## 🎬 Cómo Crear GIFs

### Opción 1: ScreenToGif (Windows)
1. Descarga: https://www.screentogif.com/
2. Graba la animación
3. Edita y exporta como GIF

### Opción 2: LICEcap (Mac/Windows)
1. Descarga: https://www.cockos.com/licecap/
2. Selecciona área
3. Graba y guarda

### Opción 3: Kap (Mac)
1. Descarga: https://getkap.co/
2. Graba pantalla
3. Exporta como GIF

---

## 📝 Ejemplo de README con Screenshots

```markdown
# 🎮 Dashboard de Análisis de Videojuegos

![Dashboard Principal](screenshots/hero.png)

## ✨ Características Principales

### 🎬 Animaciones Fluidas

<div align="center">
  <img src="screenshots/genre-animation.gif" width="45%" />
  <img src="screenshots/console-race.gif" width="45%" />
</div>

### 🌍 Análisis Geográfico

![Mapa Mundial](screenshots/world-map.png)

### 📊 Análisis Estadísticos

<div align="center">
  <img src="screenshots/correlations.png" width="45%" />
  <img src="screenshots/quality-vs-sales.png" width="45%" />
</div>
```

---

## 💡 Tips para Buenos Screenshots

1. **Resolución**: Usa al menos 1920x1080
2. **Zoom**: Asegúrate de que el texto sea legible
3. **Tema**: Captura con el tema oscuro (se ve mejor)
4. **Datos**: Muestra datos interesantes, no el estado inicial vacío
5. **GIFs**: Mantén duración entre 5-10 segundos
6. **Tamaño**: Optimiza GIFs para que sean < 5MB

---

## 🔧 Optimizar Imágenes

### Para PNG
```bash
# Usando TinyPNG (online)
https://tinypng.com/

# O con ImageMagick
convert input.png -quality 85 output.png
```

### Para GIF
```bash
# Usando gifsicle
gifsicle -O3 --colors 256 input.gif -o output.gif
```

---

## 📤 Subir Screenshots a GitHub

```bash
# Crear carpeta
mkdir screenshots

# Agregar imágenes
git add screenshots/
git commit -m "Add screenshots"
git push
```

---

**¡Tus screenshots harán que tu README sea mucho más atractivo! 📸✨**
