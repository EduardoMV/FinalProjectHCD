import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from scipy import stats

from visual_theme import VisualTheme
from data_loader import load_data, find_column

st.set_page_config(
    page_title="Video Games Dashboard (CORGIS)",
    layout="wide",
)

# Apply visual theme
VisualTheme.inject_custom_css()
VisualTheme.apply_matplotlib_theme()

# ---------------------------------------------------------
# HEADER
# ---------------------------------------------------------
st.title("🎮 Video Games — Dashboard de Datos (CORGIS)")

# ---------------------------------------------------------
# AUTOMATIC DATA LOADING
# ---------------------------------------------------------
try:
    df = load_data("video_games.csv")
    
except FileNotFoundError as e:
    st.error(str(e))
    st.info("**Sugerencia**: Coloca el archivo `video_games.csv` en el directorio raíz del proyecto.")
    st.stop()
    
except Exception as e:
    st.error(str(e))
    st.stop()

# Detect possible columns using the helper function
def find_col(options):
    return find_column(df, options)

title_col = find_col(["Title", "title", "Name"])
genre_col = find_col(["Genre", "genre"])
platform_col = find_col(["Platform", "platform"])
sales_col = find_col(["Global_Sales", "global_sales", "sales"])
score_col = find_col(["Score", "meta_score", "rating"])

# ---------------------------------------------------------
# TABS
# ---------------------------------------------------------
tab_intro, tab_mercado, tab_calidad, tab_temporal, tab_experiencia, tab_corr = st.tabs(
    ["📘 Introducción", "💰 El Mercado", "⭐ Calidad vs Popularidad", "⏳ Evolución Temporal", "🎮 Experiencia del Jugador", "🔗 Correlaciones"]
)

# ---------------------------------------------------------
# TAB 1 – Intro
# ---------------------------------------------------------
with tab_intro:
    # Welcome header with emoji and engaging title
    st.markdown("""
    <h1 style='text-align: center; color: #8B5CF6; font-size: 3rem; margin-bottom: 1rem;'>
        🎮 Bienvenido al Mundo de los Videojuegos
    </h1>
    <p style='text-align: center; font-size: 1.2rem; color: #94A3B8; margin-bottom: 2rem;'>
        Descubre las historias ocultas detrás de miles de juegos a través de datos y visualizaciones
    </p>
    """, unsafe_allow_html=True)
    
    # Calculate key statistics
    total_games = len(df)
    
    # Year range calculation
    year_col = find_col(["Release_Year", "Year", "year", "release_year"])
    if year_col:
        valid_years = df[year_col].dropna()
        valid_years = valid_years[(valid_years >= 1980) & (valid_years <= 2025)]
        if len(valid_years) > 0:
            year_min = int(valid_years.min())
            year_max = int(valid_years.max())
            year_range = f"{year_min} - {year_max}"
        else:
            year_range = "N/A"
    else:
        year_range = "N/A"
    
    # Platform count
    platform_col = find_col(["Release_Console", "Platform", "platform", "console"])
    if platform_col:
        platform_count = df[platform_col].nunique()
    else:
        platform_count = "N/A"
    
    # Display metric cards with gradient backgrounds
    st.markdown("<div style='margin: 2rem 0;'>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(
            VisualTheme.create_metric_card_html(f"{total_games:,}", "Juegos Totales"),
            unsafe_allow_html=True
        )
    
    with col2:
        st.markdown(
            VisualTheme.create_metric_card_html(year_range, "Rango de Años"),
            unsafe_allow_html=True
        )
    
    with col3:
        st.markdown(
            VisualTheme.create_metric_card_html(str(platform_count), "Plataformas"),
            unsafe_allow_html=True
        )
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Narrative introduction
    st.markdown("""
    <div style='background: #1E293B; border-radius: 12px; padding: 2rem; margin: 2rem 0; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);'>
        <h3 style='color: #8B5CF6; margin-top: 0;'>Una Historia de Datos</h3>
        <p style='color: #F1F5F9; font-size: 1.1rem; line-height: 1.8;'>
            Este dashboard te lleva en un viaje a través de la industria de los videojuegos. 
            Desde los clásicos que definieron generaciones hasta los títulos modernos que rompen récords, 
            cada dato cuenta una historia. Exploraremos patrones de ventas, la relación entre calidad y 
            popularidad, tendencias temporales, y las conexiones ocultas que revelan los secretos del éxito 
            en esta industria multimillonaria.
        </p>
        <p style='color: #94A3B8; font-size: 1rem; margin-top: 1rem;'>
            <strong>Navega por las pestañas</strong> para descubrir diferentes aspectos de esta fascinante historia de datos.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Sample data preview in styled container
    st.markdown("""
    <div style='margin-top: 2rem;'>
        <h3 style='color: #F1F5F9;'>Vista Previa de los Datos</h3>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div style='background: #1E293B; border-radius: 12px; padding: 1.5rem; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);'>
    """, unsafe_allow_html=True)
    
    st.dataframe(
        df.head(10), 
        use_container_width=True,
        height=400
    )
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Additional context
    st.markdown(f"""
    <div style='margin-top: 1.5rem; padding: 1rem; background: rgba(139, 92, 246, 0.1); border-left: 4px solid #8B5CF6; border-radius: 4px;'>
        <p style='color: #F1F5F9; margin: 0;'>
            <strong>Columnas disponibles:</strong> {len(df.columns)} variables que incluyen información sobre 
            ventas, puntuaciones, características de juego, y métricas de tiempo de juego.
        </p>
    </div>
    """, unsafe_allow_html=True)

# ---------------------------------------------------------
# TAB 2 – El Mercado (Sales Analysis)
# ---------------------------------------------------------
with tab_mercado:
    st.markdown("""
    <h2 style='color: #8B5CF6; text-align: center; margin-bottom: 1rem;'>
        El Mercado: Análisis de Ventas
    </h2>
    <p style='text-align: center; font-size: 1.1rem; color: #94A3B8; margin-bottom: 2rem;'>
        Descubre qué géneros y plataformas dominan la industria de los videojuegos
    </p>
    """, unsafe_allow_html=True)
    
    # Find required columns
    sales_col = find_col(["Metrics_Sales", "Global_Sales", "sales", "Sales"])
    genre_col = find_col(["Metadata_Genres", "Genre", "genre", "Genres"])
    platform_col = find_col(["Release_Console", "Platform", "platform", "console"])
    
    if sales_col and genre_col:
        # --- Sales by Genre ---
        st.markdown("""
        <div style='background: #1E293B; border-radius: 12px; padding: 2rem; margin: 2rem 0; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);'>
            <h3 style='color: #8B5CF6; margin-top: 0;'>Ventas por Género</h3>
            <p style='color: #F1F5F9; font-size: 1rem; line-height: 1.6;'>
                ¿Qué géneros generan más ingresos? Esta visualización revela los gigantes del mercado.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Calculate sales by genre
        sales_by_genre = df.groupby(genre_col)[sales_col].sum().sort_values(ascending=False)
        
        # Get all genres for consistent coloring
        all_genres = sales_by_genre.index.tolist()
        
        # Create horizontal bar chart with gradient colors
        fig_genre = go.Figure()
        
        # Add bars with colors from theme
        colors = [VisualTheme.get_color_for_category(genre, all_genres) for genre in all_genres]
        
        fig_genre.add_trace(go.Bar(
            y=sales_by_genre.index,
            x=sales_by_genre.values,
            orientation='h',
            marker=dict(
                color=colors,
                line=dict(color='rgba(255, 255, 255, 0.2)', width=1)
            ),
            text=[f'{val:.1f}M' for val in sales_by_genre.values],
            textposition='outside',
            hovertemplate='<b>%{y}</b><br>Ventas: %{x:.2f}M<extra></extra>'
        ))
        
        fig_genre.update_layout(
            title=dict(
                text='Ventas Totales por Género (en millones)',
                font=dict(size=20, color=VisualTheme.TEXT_PRIMARY)
            ),
            xaxis_title='Ventas Totales (millones)',
            yaxis_title='Género',
            height=max(400, len(sales_by_genre) * 30),
            showlegend=False,
            yaxis=dict(autorange='reversed')  # Top genre at top
        )
        
        # Apply theme
        fig_genre = VisualTheme.apply_plotly_theme(fig_genre)
        st.plotly_chart(fig_genre, use_container_width=True)
        
        # Variable explanation
        st.markdown("""
        <div style='background: rgba(59, 130, 246, 0.1); border-left: 4px solid #3B82F6; border-radius: 4px; padding: 1rem; margin: 1rem 0;'>
            <p style='color: #F1F5F9; margin: 0; font-size: 0.95rem;'>
                <strong>Variables:</strong><br>
                • <strong>Género:</strong> Categoría del juego (Acción, Deportes, RPG, etc.)<br>
                • <strong>Ventas Totales:</strong> Suma de todas las ventas globales en millones de unidades
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Narrative text
        top_genre = sales_by_genre.index[0]
        top_sales = sales_by_genre.values[0]
        st.markdown(f"""
        <div style='background: rgba(139, 92, 246, 0.1); border-left: 4px solid #8B5CF6; border-radius: 4px; padding: 1rem; margin: 1rem 0;'>
            <p style='color: #F1F5F9; margin: 0; font-size: 1rem;'>
                <strong>Insight:</strong> <strong>{top_genre}</strong> lidera el mercado con 
                <strong>{top_sales:.1f} millones</strong> en ventas totales, estableciéndose como el 
                género más lucrativo de la industria.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # --- PIE CHART: Distribution of Games by Genre ---
        st.markdown("""
        <div style='background: #1E293B; border-radius: 12px; padding: 2rem; margin: 2rem 0; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);'>
            <h3 style='color: #8B5CF6; margin-top: 0;'>Distribución de Juegos por Género</h3>
            <p style='color: #F1F5F9; font-size: 1rem; line-height: 1.6;'>
                ¿Cómo se distribuyen los juegos entre los diferentes géneros? Esta gráfica de pastel muestra la proporción.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Count games by genre
        games_by_genre = df[genre_col].value_counts()
        
        # Create pie chart using Plotly
        fig_pie = go.Figure(data=[go.Pie(
            labels=games_by_genre.index,
            values=games_by_genre.values,
            hole=0.3,  # Donut chart
            marker=dict(
                colors=[VisualTheme.get_color_for_category(genre, games_by_genre.index.tolist()) 
                        for genre in games_by_genre.index]
            ),
            textinfo='label+percent',
            textposition='outside',
            hovertemplate='<b>%{label}</b><br>Juegos: %{value}<br>Porcentaje: %{percent}<extra></extra>'
        )])
        
        fig_pie.update_layout(
            title=dict(
                text='Proporción de Juegos por Género',
                font=dict(size=20, color=VisualTheme.TEXT_PRIMARY)
            ),
            height=600,
            showlegend=True,
            legend=dict(
                orientation='v',
                yanchor='middle',
                y=0.5,
                xanchor='left',
                x=1.02
            )
        )
        
        fig_pie = VisualTheme.apply_plotly_theme(fig_pie)
        st.plotly_chart(fig_pie, use_container_width=True)
        
        # Variable explanation
        st.markdown("""
        <div style='background: rgba(59, 130, 246, 0.1); border-left: 4px solid #3B82F6; border-radius: 4px; padding: 1rem; margin: 1rem 0;'>
            <p style='color: #F1F5F9; margin: 0; font-size: 0.95rem;'>
                <strong>Variables:</strong><br>
                • <strong>Género:</strong> Categoría del juego<br>
                • <strong>Cantidad:</strong> Número total de juegos en cada género<br>
                • <strong>Porcentaje:</strong> Proporción que representa cada género del total
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Insight
        top_genre_count = games_by_genre.index[0]
        top_count = games_by_genre.values[0]
        total_games = games_by_genre.sum()
        percentage = (top_count / total_games) * 100
        
        st.markdown(f"""
        <div style='background: rgba(139, 92, 246, 0.1); border-left: 4px solid #8B5CF6; border-radius: 4px; padding: 1rem; margin: 1rem 0;'>
            <p style='color: #F1F5F9; margin: 0; font-size: 1rem;'>
                <strong>Insight:</strong> <strong>{top_genre_count}</strong> es el género más común con 
                <strong>{top_count}</strong> juegos, representando el <strong>{percentage:.1f}%</strong> del catálogo total.
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    if sales_col and platform_col:
        # --- Sales by Platform ---
        st.markdown("""
        <div style='background: #1E293B; border-radius: 12px; padding: 2rem; margin: 2rem 0; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);'>
            <h3 style='color: #8B5CF6; margin-top: 0;'>Comparación de Plataformas</h3>
            <p style='color: #F1F5F9; font-size: 1rem; line-height: 1.6;'>
                Las plataformas compiten por dominar el mercado. Veamos quién gana.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Calculate sales by platform
        sales_by_platform = df.groupby(platform_col)[sales_col].sum().sort_values(ascending=False)
        
        # Limit to top 15 platforms for readability
        top_platforms = sales_by_platform.head(15)
        all_platforms = top_platforms.index.tolist()
        
        # Create horizontal bar chart
        fig_platform = go.Figure()
        
        # Highlight top 3 performers
        colors_platform = []
        for i, platform in enumerate(all_platforms):
            if i < 3:
                # Top 3 get accent colors
                colors_platform.append(VisualTheme.ACCENT_COLORS[i % len(VisualTheme.ACCENT_COLORS)])
            else:
                colors_platform.append(VisualTheme.get_color_for_category(platform, all_platforms))
        
        fig_platform.add_trace(go.Bar(
            y=top_platforms.index,
            x=top_platforms.values,
            orientation='h',
            marker=dict(
                color=colors_platform,
                line=dict(color='rgba(255, 255, 255, 0.2)', width=1)
            ),
            text=[f'{val:.1f}M' for val in top_platforms.values],
            textposition='outside',
            hovertemplate='<b>%{y}</b><br>Ventas: %{x:.2f}M<extra></extra>'
        ))
        
        # Add annotations for top 3
        annotations = []
        for i in range(min(3, len(top_platforms))):
            annotations.append(dict(
                x=top_platforms.values[i],
                y=i,
                text=f'Top {i+1}',
                xanchor='left',
                xshift=10,
                showarrow=False,
                font=dict(size=12, color=VisualTheme.ACCENT_COLORS[i])
            ))
        
        fig_platform.update_layout(
            title=dict(
                text='Top 15 Plataformas por Ventas Totales',
                font=dict(size=20, color=VisualTheme.TEXT_PRIMARY)
            ),
            xaxis_title='Ventas Totales (millones)',
            yaxis_title='Plataforma',
            height=500,
            showlegend=False,
            yaxis=dict(autorange='reversed'),
            annotations=annotations
        )
        
        # Apply theme
        fig_platform = VisualTheme.apply_plotly_theme(fig_platform)
        st.plotly_chart(fig_platform, use_container_width=True)
        
        # Variable explanation
        st.markdown("""
        <div style='background: rgba(59, 130, 246, 0.1); border-left: 4px solid #3B82F6; border-radius: 4px; padding: 1rem; margin: 1rem 0;'>
            <p style='color: #F1F5F9; margin: 0; font-size: 0.95rem;'>
                <strong>Variables:</strong><br>
                • <strong>Plataforma:</strong> Consola o sistema donde se lanzó el juego (PS4, Xbox, PC, etc.)<br>
                • <strong>Ventas Totales:</strong> Suma de ventas globales por plataforma en millones de unidades
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Narrative text
        top_platform = top_platforms.index[0]
        top_platform_sales = top_platforms.values[0]
        second_platform = top_platforms.index[1] if len(top_platforms) > 1 else "N/A"
        
        st.markdown(f"""
        <div style='background: rgba(139, 92, 246, 0.1); border-left: 4px solid #8B5CF6; border-radius: 4px; padding: 1rem; margin: 1rem 0;'>
            <p style='color: #F1F5F9; margin: 0; font-size: 1rem;'>
                <strong>Insight:</strong> <strong>{top_platform}</strong> domina el mercado de plataformas 
                con <strong>{top_platform_sales:.1f} millones</strong> en ventas, superando a <strong>{second_platform}</strong> 
                y consolidándose como la plataforma preferida por los jugadores.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # --- STACKED BAR CHART: Sales by Platform and Genre ---
        if genre_col:
            st.markdown("""
            <div style='background: #1E293B; border-radius: 12px; padding: 2rem; margin: 2rem 0; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);'>
                <h3 style='color: #8B5CF6; margin-top: 0;'>Ventas por Plataforma y Género (Barras Apiladas)</h3>
                <p style='color: #F1F5F9; font-size: 1rem; line-height: 1.6;'>
                    ¿Cómo se distribuyen las ventas de cada género en las diferentes plataformas? 
                    Esta gráfica de barras apiladas muestra la composición detallada.
                </p>
            </div>
            """, unsafe_allow_html=True)
            
            # Create pivot table for stacked bar chart
            # Get top 10 platforms and top 8 genres for readability
            top_10_platforms = sales_by_platform.head(10).index.tolist()
            top_genres = df.groupby(genre_col)[sales_col].sum().sort_values(ascending=False).head(8).index.tolist()
            
            # Filter data
            df_filtered = df[df[platform_col].isin(top_10_platforms) & df[genre_col].isin(top_genres)]
            
            # Create pivot table
            pivot_data = df_filtered.pivot_table(
                values=sales_col,
                index=platform_col,
                columns=genre_col,
                aggfunc='sum',
                fill_value=0
            )
            
            # Sort by total sales
            pivot_data['Total'] = pivot_data.sum(axis=1)
            pivot_data = pivot_data.sort_values('Total', ascending=True)
            pivot_data = pivot_data.drop('Total', axis=1)
            
            # Create stacked bar chart
            fig_stacked = go.Figure()
            
            for i, genre in enumerate(pivot_data.columns):
                fig_stacked.add_trace(go.Bar(
                    name=genre,
                    y=pivot_data.index,
                    x=pivot_data[genre],
                    orientation='h',
                    marker=dict(
                        color=VisualTheme.get_color_for_category(genre, top_genres)
                    ),
                    hovertemplate='<b>%{y}</b><br>' + genre + ': %{x:.2f}M<extra></extra>'
                ))
            
            fig_stacked.update_layout(
                title=dict(
                    text='Composición de Ventas por Plataforma y Género (Top 10 Plataformas)',
                    font=dict(size=20, color=VisualTheme.TEXT_PRIMARY)
                ),
                xaxis_title='Ventas Totales (millones)',
                yaxis_title='Plataforma',
                barmode='stack',
                height=600,
                showlegend=True,
                legend=dict(
                    orientation='v',
                    yanchor='top',
                    y=1,
                    xanchor='left',
                    x=1.02
                )
            )
            
            fig_stacked = VisualTheme.apply_plotly_theme(fig_stacked)
            st.plotly_chart(fig_stacked, use_container_width=True)
            
            # Variable explanation
            st.markdown("""
            <div style='background: rgba(59, 130, 246, 0.1); border-left: 4px solid #3B82F6; border-radius: 4px; padding: 1rem; margin: 1rem 0;'>
                <p style='color: #F1F5F9; margin: 0; font-size: 0.95rem;'>
                    <strong>Variables:</strong><br>
                    • <strong>Plataforma:</strong> Sistema de juego (eje Y)<br>
                    • <strong>Ventas por Género:</strong> Cada color representa un género diferente<br>
                    • <strong>Ventas Totales:</strong> La longitud total de la barra (eje X)<br>
                    • <strong>Composición:</strong> Los segmentos muestran qué porción de ventas corresponde a cada género
                </p>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("""
            <div style='background: rgba(139, 92, 246, 0.1); border-left: 4px solid #8B5CF6; border-radius: 4px; padding: 1rem; margin: 1rem 0;'>
                <p style='color: #F1F5F9; margin: 0; font-size: 1rem;'>
                    <strong>Insight:</strong> Esta visualización revela que diferentes plataformas tienen 
                    preferencias distintas de género. Algunas plataformas se especializan en ciertos géneros, 
                    mientras que otras tienen una distribución más equilibrada.
                </p>
            </div>
            """, unsafe_allow_html=True)
        
        # Summary section
        st.markdown("""
        <div style='background: #1E293B; border-radius: 12px; padding: 2rem; margin: 2rem 0; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);'>
            <h3 style='color: #8B5CF6; margin-top: 0;'>Conclusiones del Mercado</h3>
            <p style='color: #F1F5F9; font-size: 1rem; line-height: 1.8;'>
                El análisis de ventas revela patrones claros en las preferencias del mercado. Los géneros 
                más populares y las plataformas dominantes no solo reflejan las tendencias actuales, sino 
                que también guían las decisiones estratégicas de desarrolladores y publishers. Entender 
                estos patrones es clave para el éxito en la industria.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # --- GEOGRAPHIC MAP: Sales Distribution by Region ---
        st.markdown("""
        <div style='background: #1E293B; border-radius: 12px; padding: 2rem; margin: 2rem 0; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);'>
            <h3 style='color: #8B5CF6; margin-top: 0;'>🌍 Géneros Más Jugados por País</h3>
            <p style='color: #F1F5F9; font-size: 1rem; line-height: 1.6;'>
                Mapa interactivo que muestra el género de videojuegos más popular en cada país.
                Los países con el mismo género favorito comparten el mismo color.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Cargar datos de GlobalGenres.csv
        try:
            df_global_genres = pd.read_csv('GlobalGenres.csv')
            
            # Mapeo de nombres de países a códigos ISO-3
            country_to_iso = {
                'Afghanistan': 'AFG', 'Albania': 'ALB', 'Algeria': 'DZA', 'Andorra': 'AND', 'Angola': 'AGO',
                'Antigua and Barbuda': 'ATG', 'Argentina': 'ARG', 'Armenia': 'ARM', 'Australia': 'AUS', 'Austria': 'AUT',
                'Azerbaijan': 'AZE', 'Bahamas': 'BHS', 'Bahrain': 'BHR', 'Bangladesh': 'BGD', 'Barbados': 'BRB',
                'Belarus': 'BLR', 'Belgium': 'BEL', 'Belize': 'BLZ', 'Benin': 'BEN', 'Bhutan': 'BTN',
                'Bolivia': 'BOL', 'Bosnia and Herzegovina': 'BIH', 'Botswana': 'BWA', 'Brazil': 'BRA', 'Brunei': 'BRN',
                'Bulgaria': 'BGR', 'Burkina Faso': 'BFA', 'Burundi': 'BDI', 'Cabo Verde': 'CPV', 'Cambodia': 'KHM',
                'Cameroon': 'CMR', 'Canada': 'CAN', 'Central African Republic': 'CAF', 'Chad': 'TCD', 'Chile': 'CHL',
                'China': 'CHN', 'Colombia': 'COL', 'Comoros': 'COM', 'Congo (Congo-Brazzaville)': 'COG', 'Costa Rica': 'CRI',
                'Croatia': 'HRV', 'Cuba': 'CUB', 'Cyprus': 'CYP', 'Czechia (Czech Republic)': 'CZE',
                'Democratic Republic of the Congo': 'COD', 'Denmark': 'DNK', 'Djibouti': 'DJI', 'Dominica': 'DMA',
                'Dominican Republic': 'DOM', 'Ecuador': 'ECU', 'Egypt': 'EGY', 'El Salvador': 'SLV',
                'Equatorial Guinea': 'GNQ', 'Eritrea': 'ERI', 'Estonia': 'EST', 'Eswatini': 'SWZ', 'Ethiopia': 'ETH',
                'Fiji': 'FJI', 'Finland': 'FIN', 'France': 'FRA', 'Gabon': 'GAB', 'Gambia': 'GMB',
                'Georgia': 'GEO', 'Germany': 'DEU', 'Ghana': 'GHA', 'Greece': 'GRC', 'Grenada': 'GRD',
                'Guatemala': 'GTM', 'Guinea': 'GIN', 'Guinea-Bissau': 'GNB', 'Guyana': 'GUY', 'Haiti': 'HTI',
                'Honduras': 'HND', 'Hungary': 'HUN', 'Iceland': 'ISL', 'India': 'IND', 'Indonesia': 'IDN',
                'Iran': 'IRN', 'Iraq': 'IRQ', 'Ireland': 'IRL', 'Israel': 'ISR', 'Italy': 'ITA',
                'Jamaica': 'JAM', 'Japan': 'JPN', 'Jordan': 'JOR', 'Kazakhstan': 'KAZ', 'Kenya': 'KEN',
                'Kiribati': 'KIR', 'Kuwait': 'KWT', 'Kyrgyzstan': 'KGZ', 'Laos': 'LAO', 'Latvia': 'LVA',
                'Lebanon': 'LBN', 'Lesotho': 'LSO', 'Liberia': 'LBR', 'Libya': 'LBY', 'Liechtenstein': 'LIE',
                'Lithuania': 'LTU', 'Luxembourg': 'LUX', 'Madagascar': 'MDG', 'Malawi': 'MWI', 'Malaysia': 'MYS',
                'Maldives': 'MDV', 'Mali': 'MLI', 'Malta': 'MLT', 'Marshall Islands': 'MHL', 'Mauritania': 'MRT',
                'Mauritius': 'MUS', 'Mexico': 'MEX', 'Micronesia': 'FSM', 'Moldova': 'MDA', 'Monaco': 'MCO',
                'Mongolia': 'MNG', 'Montenegro': 'MNE', 'Morocco': 'MAR', 'Mozambique': 'MOZ',
                'Myanmar (formerly Burma)': 'MMR', 'Namibia': 'NAM', 'Nauru': 'NRU', 'Nepal': 'NPL',
                'Netherlands': 'NLD', 'New Zealand': 'NZL', 'Nicaragua': 'NIC', 'Niger': 'NER', 'Nigeria': 'NGA',
                'North Korea': 'PRK', 'North Macedonia': 'MKD', 'Norway': 'NOR', 'Oman': 'OMN', 'Pakistan': 'PAK',
                'Palau': 'PLW', 'Palestine State': 'PSE', 'Panama': 'PAN', 'Papua New Guinea': 'PNG', 'Paraguay': 'PRY',
                'Peru': 'PER', 'Philippines': 'PHL', 'Poland': 'POL', 'Portugal': 'PRT', 'Qatar': 'QAT',
                'Romania': 'ROU', 'Russia': 'RUS', 'Rwanda': 'RWA', 'Saint Kitts and Nevis': 'KNA',
                'Saint Lucia': 'LCA', 'Saint Vincent and the Grenadines': 'VCT', 'Samoa': 'WSM', 'San Marino': 'SMR',
                'Sao Tome and Principe': 'STP', 'Saudi Arabia': 'SAU', 'Senegal': 'SEN', 'Serbia': 'SRB',
                'Seychelles': 'SYC', 'Sierra Leone': 'SLE', 'Singapore': 'SGP', 'Slovakia': 'SVK', 'Slovenia': 'SVN',
                'Solomon Islands': 'SLB', 'Somalia': 'SOM', 'South Africa': 'ZAF', 'South Korea': 'KOR',
                'South Sudan': 'SSD', 'Spain': 'ESP', 'Sri Lanka': 'LKA', 'Sudan': 'SDN', 'Suriname': 'SUR',
                'Sweden': 'SWE', 'Switzerland': 'CHE', 'Syria': 'SYR', 'Tajikistan': 'TJK', 'Tanzania': 'TZA',
                'Thailand': 'THA', 'Timor-Leste': 'TLS', 'Togo': 'TGO', 'Tonga': 'TON', 'Trinidad and Tobago': 'TTO',
                'Tunisia': 'TUN', 'Turkey': 'TUR', 'Turkmenistan': 'TKM', 'Tuvalu': 'TUV', 'Uganda': 'UGA',
                'Ukraine': 'UKR', 'United Arab Emirates': 'ARE', 'United Kingdom': 'GBR', 'United States': 'USA',
                'Uruguay': 'URY', 'Uzbekistan': 'UZB', 'Vanuatu': 'VUT', 'Venezuela': 'VEN', 'Vietnam': 'VNM',
                'Yemen': 'YEM', 'Zambia': 'ZMB', 'Zimbabwe': 'ZWE'
            }
            
            # Agregar códigos ISO
            df_global_genres['Country_Code'] = df_global_genres['Country'].map(country_to_iso)
            
            # Obtener géneros únicos y asignar colores
            unique_genres = sorted(df_global_genres['Most_Played_Genre'].unique())
            genre_colors_map = {
                'Action': '#8B5CF6',      # Púrpura
                'Shooter': '#3B82F6',     # Azul
                'Sports': '#10B981',      # Verde
                'Role-Playing': '#F59E0B', # Ámbar
                'Strategy': '#EF4444',    # Rojo
                'MOBA': '#EC4899',        # Rosa
                'Adventure': '#06B6D4',   # Cyan
                'Racing': '#A78BFA',      # Lila
                'Fighting': '#60A5FA',    # Azul claro
                'Simulation': '#34D399',  # Verde claro
                'Puzzle': '#FBBF24'       # Amarillo
            }
            
            # Asignar colores a cada país según su género
            df_global_genres['Color'] = df_global_genres['Most_Played_Genre'].map(
                lambda x: genre_colors_map.get(x, '#94A3B8')
            )
            
            # Crear valores numéricos para el mapa (para que funcione el hover)
            genre_to_num = {genre: i+1 for i, genre in enumerate(unique_genres)}
            df_global_genres['Genre_Num'] = df_global_genres['Most_Played_Genre'].map(genre_to_num)
            
            # Crear mapa
            fig_map = go.Figure(data=go.Choropleth(
                locations=df_global_genres['Country_Code'],
                z=df_global_genres['Genre_Num'],
                text=df_global_genres['Most_Played_Genre'],
                locationmode='ISO-3',
                colorscale=[[i/(len(unique_genres)-1), genre_colors_map.get(genre, '#94A3B8')] 
                           for i, genre in enumerate(unique_genres)],
                showscale=False,
                marker_line_color='#475569',
                marker_line_width=0.5,
                hovertemplate='<b>%{location}</b><br>Género más jugado: %{text}<extra></extra>'
            ))
            
            fig_map.update_layout(
                title=dict(
                    text='🌍 Géneros Más Jugados por País',
                    font=dict(size=20, color=VisualTheme.TEXT_PRIMARY),
                    x=0.5,
                    xanchor='center'
                ),
                geo=dict(
                    showframe=True,
                    showcoastlines=True,
                    projection_type='natural earth',
                    bgcolor='#0F172A',
                    landcolor='#1E293B',
                    coastlinecolor='#475569',
                    framecolor='#8B5CF6',
                    framewidth=2,
                    showland=True,
                    showcountries=True,
                    countrycolor='#334155',
                    countrywidth=0.5,
                    oceancolor='#0F172A',
                    showocean=True
                ),
                height=650,
                paper_bgcolor='rgba(15, 23, 42, 0.95)',
                plot_bgcolor='rgba(15, 23, 42, 0.95)',
                font=dict(color=VisualTheme.TEXT_PRIMARY),
                margin=dict(l=0, r=0, t=60, b=0)
            )
            
            # Crear layout con mapa a la izquierda y leyenda a la derecha
            col_map, col_legend = st.columns([3, 1])
            
            with col_map:
                st.plotly_chart(fig_map, use_container_width=True)
            
            with col_legend:
                # Leyenda de géneros
                st.markdown("""
                <div style='background: #1E293B; border-radius: 12px; padding: 1.5rem; margin: 1rem 0; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);'>
                    <h4 style='color: #8B5CF6; margin-top: 0; text-align: center;'>Leyenda de Géneros</h4>
                </div>
                """, unsafe_allow_html=True)
                
                # Crear leyenda vertical
                for genre in unique_genres:
                    color = genre_colors_map.get(genre, '#94A3B8')
                    count = len(df_global_genres[df_global_genres['Most_Played_Genre'] == genre])
                    st.markdown(f"""
                    <div style='background: {color}; border-radius: 8px; padding: 0.75rem; margin: 0.5rem 0; text-align: center;'>
                        <div style='color: white; font-weight: bold; font-size: 0.9rem;'>{genre}</div>
                        <div style='color: rgba(255,255,255,0.9); font-size: 0.8rem;'>{count} países</div>
                    </div>
                    """, unsafe_allow_html=True)
            
        except FileNotFoundError:
            st.error("❌ No se encontró el archivo GlobalGenres.csv")
        except Exception as e:
            st.error(f"❌ Error al cargar el mapa: {str(e)}")
    
    else:
        st.warning("⚠️ No se encontraron las columnas necesarias para el análisis de ventas.")

# ---------------------------------------------------------
# TAB 3 – Calidad vs Popularidad (Review Scores Analysis)
# ---------------------------------------------------------
with tab_calidad:
    st.markdown("""
    <h2 style='color: #8B5CF6; text-align: center; margin-bottom: 1rem;'>Calidad vs Popularidad: El Dilema del Éxito
    </h2>
    <p style='text-align: center; font-size: 1.1rem; color: #94A3B8; margin-bottom: 2rem;'>
        ¿Los mejores juegos son los más vendidos? Exploremos la relación entre crítica y comercio
    </p>
    """, unsafe_allow_html=True)
    
    # Find required columns
    score_col = find_col(["Metrics_Review_Score", "Score", "meta_score", "rating", "score"])
    sales_col = find_col(["Metrics_Sales", "Global_Sales", "sales", "Sales"])
    genre_col = find_col(["Metadata_Genres", "Genre", "genre", "Genres"])
    
    if score_col and sales_col:
        # Filter out missing score data gracefully
        df_with_scores = df[df[score_col].notna()].copy()
        
        if len(df_with_scores) > 0:
            # --- Scatter Plot: Review Scores vs Sales ---
            st.markdown("""
            <div style='background: #1E293B; border-radius: 12px; padding: 2rem; margin: 2rem 0; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);'>
                <h3 style='color: #8B5CF6; margin-top: 0;'>Puntuación vs Ventas</h3>
                <p style='color: #F1F5F9; font-size: 1rem; line-height: 1.6;'>
                    ¿Existe una correlación entre la calidad crítica y el éxito comercial?
                </p>
            </div>
            """, unsafe_allow_html=True)
            
            # Create scatter plot with trend line
            if genre_col:
                # Get all genres for consistent coloring
                all_genres = df_with_scores[genre_col].unique().tolist()
                
                # Create scatter plot colored by genre
                fig_scatter = go.Figure()
                
                # Add scatter points for each genre
                for genre in all_genres:
                    genre_data = df_with_scores[df_with_scores[genre_col] == genre]
                    
                    fig_scatter.add_trace(go.Scatter(
                        x=genre_data[score_col],
                        y=genre_data[sales_col],
                        mode='markers',
                        name=genre,
                        marker=dict(
                            color=VisualTheme.get_color_for_category(genre, all_genres),
                            size=8,
                            opacity=0.6,
                            line=dict(color='rgba(255, 255, 255, 0.2)', width=1)
                        ),
                        hovertemplate='<b>%{text}</b><br>Puntuación: %{x:.1f}<br>Ventas: %{y:.2f}M<extra></extra>',
                        text=genre_data[find_col(["Title", "title", "Name"])] if find_col(["Title", "title", "Name"]) else [genre] * len(genre_data)
                    ))
                
                # Add trend line
                from scipy import stats
                slope, intercept, r_value, p_value, std_err = stats.linregress(
                    df_with_scores[score_col], 
                    df_with_scores[sales_col]
                )
                
                x_trend = np.array([df_with_scores[score_col].min(), df_with_scores[score_col].max()])
                y_trend = slope * x_trend + intercept
                
                fig_scatter.add_trace(go.Scatter(
                    x=x_trend,
                    y=y_trend,
                    mode='lines',
                    name=f'Tendencia (r={r_value:.3f})',
                    line=dict(color='#FBBF24', width=3, dash='dash'),
                    hovertemplate='Línea de tendencia<extra></extra>'
                ))
                
                fig_scatter.update_layout(
                    title=dict(
                        text='Relación entre Puntuación de Crítica y Ventas',
                        font=dict(size=20, color=VisualTheme.TEXT_PRIMARY)
                    ),
                    xaxis_title='Puntuación de Crítica',
                    yaxis_title='Ventas (millones)',
                    height=600,
                    legend=dict(
                        orientation='v',
                        yanchor='top',
                        y=1,
                        xanchor='left',
                        x=1.02
                    )
                )
                
                # Apply theme
                fig_scatter = VisualTheme.apply_plotly_theme(fig_scatter)
                st.plotly_chart(fig_scatter, use_container_width=True)
                
                # Variable explanation
                st.markdown("""
                <div style='background: rgba(59, 130, 246, 0.1); border-left: 4px solid #3B82F6; border-radius: 4px; padding: 1rem; margin: 1rem 0;'>
                    <p style='color: #F1F5F9; margin: 0; font-size: 0.95rem;'>
                        <strong>Variables:</strong><br>
                        • <strong>Puntuación de Crítica:</strong> Calificación promedio otorgada por críticos profesionales (escala 0-100)<br>
                        • <strong>Ventas:</strong> Unidades vendidas globalmente en millones<br>
                        • <strong>Género:</strong> Categoría del juego (representada por colores)<br>
                        • <strong>Línea de Tendencia:</strong> Muestra la relación general entre puntuación y ventas
                    </p>
                </div>
                """, unsafe_allow_html=True)
                
                # Narrative interpretation
                correlation_strength = "fuerte" if abs(r_value) > 0.7 else "moderada" if abs(r_value) > 0.4 else "débil"
                correlation_direction = "positiva" if r_value > 0 else "negativa"
                
                st.markdown(f"""
                <div style='background: rgba(139, 92, 246, 0.1); border-left: 4px solid #8B5CF6; border-radius: 4px; padding: 1rem; margin: 1rem 0;'>
                    <p style='color: #F1F5F9; margin: 0; font-size: 1rem;'>
                        <strong>Insight:</strong> La correlación entre puntuación y ventas es 
                        <strong>{correlation_strength} y {correlation_direction}</strong> (r={r_value:.3f}). 
                        {'Esto sugiere que las mejores críticas tienden a traducirse en mayores ventas.' if r_value > 0.4 else 'Esto indica que el éxito comercial no siempre depende de la crítica positiva.'}
                    </p>
                </div>
                """, unsafe_allow_html=True)
            
            else:
                # Simple scatter without genre coloring
                fig_scatter = go.Figure()
                
                fig_scatter.add_trace(go.Scatter(
                    x=df_with_scores[score_col],
                    y=df_with_scores[sales_col],
                    mode='markers',
                    marker=dict(
                        color=VisualTheme.PRIMARY_COLORS[0],
                        size=8,
                        opacity=0.6
                    )
                ))
                
                fig_scatter.update_layout(
                    title='Relación entre Puntuación y Ventas',
                    xaxis_title='Puntuación',
                    yaxis_title='Ventas (millones)',
                    height=600
                )
                
                fig_scatter = VisualTheme.apply_plotly_theme(fig_scatter)
                st.plotly_chart(fig_scatter, use_container_width=True)
            
            # --- Violin Plot: Score Distributions by Genre ---
            if genre_col:
                st.markdown("""
                <div style='background: #1E293B; border-radius: 12px; padding: 2rem; margin: 2rem 0; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);'>
                    <h3 style='color: #8B5CF6; margin-top: 0;'>Distribución de Puntuaciones por Género</h3>
                    <p style='color: #F1F5F9; font-size: 1rem; line-height: 1.6;'>
                        ¿Qué géneros reciben las mejores críticas? Exploremos la distribución de calidad.
                    </p>
                </div>
                """, unsafe_allow_html=True)
                
                # Calculate average scores by genre for sorting
                avg_scores_by_genre = df_with_scores.groupby(genre_col)[score_col].mean().sort_values(ascending=False)
                sorted_genres = avg_scores_by_genre.index.tolist()
                
                # Create violin plot
                fig_violin = go.Figure()
                
                for genre in sorted_genres:
                    genre_data = df_with_scores[df_with_scores[genre_col] == genre]
                    
                    fig_violin.add_trace(go.Violin(
                        y=genre_data[score_col],
                        name=genre,
                        box_visible=True,
                        meanline_visible=True,
                        fillcolor=VisualTheme.get_color_for_category(genre, sorted_genres),
                        opacity=0.6,
                        line_color=VisualTheme.get_color_for_category(genre, sorted_genres),
                        hovertemplate='<b>%{fullData.name}</b><br>Puntuación: %{y:.1f}<extra></extra>'
                    ))
                
                fig_violin.update_layout(
                    title=dict(
                        text='Distribución de Puntuaciones de Crítica por Género',
                        font=dict(size=20, color=VisualTheme.TEXT_PRIMARY)
                    ),
                    yaxis_title='Puntuación de Crítica',
                    xaxis_title='Género',
                    height=600,
                    showlegend=False,
                    xaxis=dict(tickangle=-45)
                )
                
                # Apply theme
                fig_violin = VisualTheme.apply_plotly_theme(fig_violin)
                st.plotly_chart(fig_violin, use_container_width=True)
                
                # Narrative text
                top_genre = sorted_genres[0]
                top_avg_score = avg_scores_by_genre.iloc[0]
                
                st.markdown(f"""
                <div style='background: rgba(139, 92, 246, 0.1); border-left: 4px solid #8B5CF6; border-radius: 4px; padding: 1rem; margin: 1rem 0;'>
                    <p style='color: #F1F5F9; margin: 0; font-size: 1rem;'>
                        <strong>Insight:</strong> <strong>{top_genre}</strong> lidera en calidad crítica 
                        con una puntuación promedio de <strong>{top_avg_score:.1f}</strong>. La distribución 
                        de puntuaciones revela que algunos géneros mantienen consistentemente alta calidad, 
                        mientras otros muestran mayor variabilidad.
                    </p>
                </div>
                """, unsafe_allow_html=True)
            
            # Summary section
            st.markdown("""
            <div style='background: #1E293B; border-radius: 12px; padding: 2rem; margin: 2rem 0; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);'>
                <h3 style='color: #8B5CF6; margin-top: 0;'>El Veredicto: Calidad vs Popularidad</h3>
                <p style='color: #F1F5F9; font-size: 1rem; line-height: 1.8;'>
                    La relación entre crítica y comercio es compleja. Mientras que las buenas puntuaciones 
                    pueden impulsar las ventas, factores como el marketing, la franquicia, y el momento de 
                    lanzamiento también juegan roles cruciales. Los datos revelan que el éxito verdadero 
                    requiere un equilibrio: calidad que satisfaga a los críticos y atractivo que capture 
                    al público masivo.
                </p>
            </div>
            """, unsafe_allow_html=True)
        
        else:
            st.warning("⚠️ No hay datos de puntuaciones disponibles para el análisis.")
    
    else:
        st.warning("⚠️ No se encontraron las columnas necesarias para el análisis de calidad vs popularidad.")

# ---------------------------------------------------------
# TAB 4 – Evolución Temporal (Time Series Analysis)
# ---------------------------------------------------------
with tab_temporal:
    st.markdown("""
    <h2 style='color: #8B5CF6; text-align: center; margin-bottom: 1rem;'>Evolución Temporal: La Historia de la Industria
    </h2>
    <p style='text-align: center; font-size: 1.1rem; color: #94A3B8; margin-bottom: 2rem;'>
        Viaja a través del tiempo y descubre cómo ha evolucionado la industria de los videojuegos
    </p>
    """, unsafe_allow_html=True)
    
    # Find required columns
    year_col = find_col(["Release_Year", "Year", "year", "release_year"])
    sales_col = find_col(["Metrics_Sales", "Global_Sales", "sales", "Sales"])
    
    if year_col:
        # Filter out invalid year data (outside 1980-2025 range)
        df_temporal = df[df[year_col].notna()].copy()
        df_temporal = df_temporal[(df_temporal[year_col] >= 1980) & (df_temporal[year_col] <= 2025)]
        
        if len(df_temporal) > 0:
            # --- Game Releases Over Time (Area Chart) ---
            st.markdown("""
            <div style='background: #1E293B; border-radius: 12px; padding: 2rem; margin: 2rem 0; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);'>
                <h3 style='color: #8B5CF6; margin-top: 0;'>Lanzamientos de Juegos por Año</h3>
                <p style='color: #F1F5F9; font-size: 1rem; line-height: 1.6;'>
                    ¿Cuándo fue la edad de oro de los videojuegos? Veamos la evolución de lanzamientos.
                </p>
            </div>
            """, unsafe_allow_html=True)
            
            # Count releases by year
            releases_by_year = df_temporal.groupby(year_col).size().reset_index(name='releases')
            
            # Create area chart
            fig_releases = go.Figure()
            
            fig_releases.add_trace(go.Scatter(
                x=releases_by_year[year_col],
                y=releases_by_year['releases'],
                mode='lines',
                fill='tozeroy',
                line=dict(color=VisualTheme.PRIMARY_COLORS[0], width=3),
                fillcolor=f'rgba({int(VisualTheme.PRIMARY_COLORS[0][1:3], 16)}, {int(VisualTheme.PRIMARY_COLORS[0][3:5], 16)}, {int(VisualTheme.PRIMARY_COLORS[0][5:7], 16)}, 0.3)',
                hovertemplate='<b>Año %{x}</b><br>Lanzamientos: %{y}<extra></extra>'
            ))
            
            # Add annotations for significant periods
            # Find peak year
            peak_year = releases_by_year.loc[releases_by_year['releases'].idxmax()]
            
            fig_releases.add_annotation(
                x=peak_year[year_col],
                y=peak_year['releases'],
                text=f"Pico: {int(peak_year['releases'])} juegos",
                showarrow=True,
                arrowhead=2,
                arrowcolor=VisualTheme.ACCENT_COLORS[0],
                ax=0,
                ay=-40,
                font=dict(size=12, color=VisualTheme.ACCENT_COLORS[0])
            )
            
            fig_releases.update_layout(
                title=dict(
                    text='Número de Juegos Lanzados por Año',
                    font=dict(size=20, color=VisualTheme.TEXT_PRIMARY)
                ),
                xaxis_title='Año',
                yaxis_title='Número de Lanzamientos',
                height=500,
                showlegend=False
            )
            
            # Apply theme
            fig_releases = VisualTheme.apply_plotly_theme(fig_releases)
            st.plotly_chart(fig_releases, use_container_width=True)
            
            # Narrative text
            peak_year_value = int(peak_year[year_col])
            peak_releases = int(peak_year['releases'])
            
            st.markdown(f"""
            <div style='background: rgba(139, 92, 246, 0.1); border-left: 4px solid #8B5CF6; border-radius: 4px; padding: 1rem; margin: 1rem 0;'>
                <p style='color: #F1F5F9; margin: 0; font-size: 1rem;'>
                    <strong>Insight:</strong> El año <strong>{peak_year_value}</strong> marcó el pico de 
                    lanzamientos con <strong>{peak_releases} juegos</strong>, reflejando un momento de 
                    intensa actividad en la industria.
                </p>
            </div>
            """, unsafe_allow_html=True)
            
            # --- Sales Trends Over Time (Line Chart) ---
            if sales_col:
                st.markdown("""
                <div style='background: #1E293B; border-radius: 12px; padding: 2rem; margin: 2rem 0; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);'>
                    <h3 style='color: #8B5CF6; margin-top: 0;'>Tendencias de Ventas a lo Largo del Tiempo</h3>
                    <p style='color: #F1F5F9; font-size: 1rem; line-height: 1.6;'>
                        ¿Cómo han cambiado las ventas con el paso de los años? Exploremos el éxito comercial temporal.
                    </p>
                </div>
                """, unsafe_allow_html=True)
                
                # Calculate total sales and average sales by year
                sales_by_year = df_temporal.groupby(year_col)[sales_col].agg(['sum', 'mean']).reset_index()
                sales_by_year.columns = [year_col, 'total_sales', 'avg_sales']
                
                # Create figure with dual y-axes
                fig_sales = go.Figure()
                
                # Total sales line
                fig_sales.add_trace(go.Scatter(
                    x=sales_by_year[year_col],
                    y=sales_by_year['total_sales'],
                    mode='lines+markers',
                    name='Ventas Totales',
                    line=dict(color=VisualTheme.PRIMARY_COLORS[1], width=3),
                    marker=dict(size=6),
                    hovertemplate='<b>Año %{x}</b><br>Ventas Totales: %{y:.2f}M<extra></extra>'
                ))
                
                # Average sales line
                fig_sales.add_trace(go.Scatter(
                    x=sales_by_year[year_col],
                    y=sales_by_year['avg_sales'],
                    mode='lines+markers',
                    name='Ventas Promedio',
                    line=dict(color=VisualTheme.PRIMARY_COLORS[3], width=3, dash='dash'),
                    marker=dict(size=6),
                    yaxis='y2',
                    hovertemplate='<b>Año %{x}</b><br>Ventas Promedio: %{y:.2f}M<extra></extra>'
                ))
                
                # Find peak sales year
                peak_sales_year = sales_by_year.loc[sales_by_year['total_sales'].idxmax()]
                
                # Add annotation for peak sales
                fig_sales.add_annotation(
                    x=peak_sales_year[year_col],
                    y=peak_sales_year['total_sales'],
                    text=f"Máximo: {peak_sales_year['total_sales']:.1f}M",
                    showarrow=True,
                    arrowhead=2,
                    arrowcolor=VisualTheme.ACCENT_COLORS[1],
                    ax=0,
                    ay=-40,
                    font=dict(size=12, color=VisualTheme.ACCENT_COLORS[1])
                )
                
                fig_sales.update_layout(
                    title=dict(
                        text='Evolución de Ventas por Año',
                        font=dict(size=20, color=VisualTheme.TEXT_PRIMARY)
                    ),
                    xaxis_title='Año',
                    yaxis_title='Ventas Totales (millones)',
                    yaxis2=dict(
                        title='Ventas Promedio (millones)',
                        overlaying='y',
                        side='right',
                        gridcolor='rgba(51, 65, 85, 0.3)'
                    ),
                    height=500,
                    legend=dict(
                        orientation='h',
                        yanchor='bottom',
                        y=1.02,
                        xanchor='center',
                        x=0.5
                    )
                )
                
                # Apply theme
                fig_sales = VisualTheme.apply_plotly_theme(fig_sales)
                st.plotly_chart(fig_sales, use_container_width=True)
                
                # Narrative text
                peak_sales_year_value = int(peak_sales_year[year_col])
                peak_sales_value = peak_sales_year['total_sales']
                
                # Calculate trend
                first_half = sales_by_year.iloc[:len(sales_by_year)//2]['total_sales'].mean()
                second_half = sales_by_year.iloc[len(sales_by_year)//2:]['total_sales'].mean()
                trend = "crecimiento" if second_half > first_half else "declive"
                
                st.markdown(f"""
                <div style='background: rgba(139, 92, 246, 0.1); border-left: 4px solid #8B5CF6; border-radius: 4px; padding: 1rem; margin: 1rem 0;'>
                    <p style='color: #F1F5F9; margin: 0; font-size: 1rem;'>
                        <strong>Insight:</strong> Las ventas alcanzaron su punto máximo en 
                        <strong>{peak_sales_year_value}</strong> con <strong>{peak_sales_value:.1f} millones</strong>. 
                        La industria muestra una tendencia general de <strong>{trend}</strong> en la segunda mitad 
                        del período analizado.
                    </p>
                </div>
                """, unsafe_allow_html=True)
            
            # --- Combined View: Releases and Sales ---
            if sales_col:
                st.markdown("""
                <div style='background: #1E293B; border-radius: 12px; padding: 2rem; margin: 2rem 0; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);'>
                    <h3 style='color: #8B5CF6; margin-top: 0;'>Vista Combinada: Lanzamientos y Ventas</h3>
                    <p style='color: #F1F5F9; font-size: 1rem; line-height: 1.6;'>
                        ¿Más juegos significa más ventas? Veamos la relación entre cantidad y éxito comercial.
                    </p>
                </div>
                """, unsafe_allow_html=True)
                
                # Merge releases and sales data
                combined_data = releases_by_year.merge(sales_by_year, on=year_col)
                
                # Create dual-axis chart
                fig_combined = go.Figure()
                
                # Releases as bars
                fig_combined.add_trace(go.Bar(
                    x=combined_data[year_col],
                    y=combined_data['releases'],
                    name='Lanzamientos',
                    marker=dict(color=VisualTheme.PRIMARY_COLORS[2], opacity=0.6),
                    hovertemplate='<b>Año %{x}</b><br>Lanzamientos: %{y}<extra></extra>'
                ))
                
                # Total sales as line
                fig_combined.add_trace(go.Scatter(
                    x=combined_data[year_col],
                    y=combined_data['total_sales'],
                    mode='lines+markers',
                    name='Ventas Totales',
                    line=dict(color=VisualTheme.ACCENT_COLORS[0], width=3),
                    marker=dict(size=8),
                    yaxis='y2',
                    hovertemplate='<b>Año %{x}</b><br>Ventas: %{y:.2f}M<extra></extra>'
                ))
                
                fig_combined.update_layout(
                    title=dict(
                        text='Lanzamientos vs Ventas por Año',
                        font=dict(size=20, color=VisualTheme.TEXT_PRIMARY)
                    ),
                    xaxis_title='Año',
                    yaxis_title='Número de Lanzamientos',
                    yaxis2=dict(
                        title='Ventas Totales (millones)',
                        overlaying='y',
                        side='right',
                        gridcolor='rgba(51, 65, 85, 0.3)'
                    ),
                    height=500,
                    legend=dict(
                        orientation='h',
                        yanchor='bottom',
                        y=1.02,
                        xanchor='center',
                        x=0.5
                    ),
                    barmode='overlay'
                )
                
                # Apply theme
                fig_combined = VisualTheme.apply_plotly_theme(fig_combined)
                st.plotly_chart(fig_combined, use_container_width=True)
                
                # Calculate correlation
                from scipy import stats
                corr, p_value = stats.pearsonr(combined_data['releases'], combined_data['total_sales'])
                corr_strength = "fuerte" if abs(corr) > 0.7 else "moderada" if abs(corr) > 0.4 else "débil"
                
                st.markdown(f"""
                <div style='background: rgba(139, 92, 246, 0.1); border-left: 4px solid #8B5CF6; border-radius: 4px; padding: 1rem; margin: 1rem 0;'>
                    <p style='color: #F1F5F9; margin: 0; font-size: 1rem;'>
                        <strong>Insight:</strong> La correlación entre lanzamientos y ventas es 
                        <strong>{corr_strength}</strong> (r={corr:.3f}). 
                        {'Esto sugiere que más lanzamientos tienden a generar mayores ventas totales.' if corr > 0.4 else 'Esto indica que la cantidad de lanzamientos no siempre se traduce en mayores ventas.'}
                    </p>
                </div>
                """, unsafe_allow_html=True)
            
            # --- NUEVA GRÁFICA: Evolución de Ventas por Género ---
            st.markdown("""
            <div style='background: #1E293B; border-radius: 12px; padding: 2rem; margin: 2rem 0; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);'>
                <h3 style='color: #8B5CF6; margin-top: 0;'>Evolución de Ventas por Género (2006-2024)</h3>
                <p style='color: #F1F5F9; font-size: 1rem; line-height: 1.6;'>
                    Gráfica animada mostrando las ventas de cada género año por año con transiciones fluidas.
                </p>
            </div>
            """, unsafe_allow_html=True)
            
            # Cargar datos de VGSales.csv
            try:
                df_vgsales = pd.read_csv('VGSales.csv')
                
                if len(df_vgsales) > 0:
                    # Asignar colores a cada género
                    all_genres = sorted(df_vgsales['Genre'].unique())
                    genre_colors = {genre: VisualTheme.get_color_for_category(genre, all_genres) 
                                   for genre in all_genres}
                    df_vgsales['Color'] = df_vgsales['Genre'].map(genre_colors)
                    
                    # Crear gráfica animada con transiciones fluidas
                    fig_genres = px.bar(
                        df_vgsales,
                        x='Genre',
                        y='Global_Sales_Millions',
                        animation_frame='Year',
                        range_y=[0, df_vgsales['Global_Sales_Millions'].max() * 1.1],
                        title='Ventas Globales por Género (2006-2024)',
                        labels={'Global_Sales_Millions': 'Ventas Globales (millones)', 'Genre': 'Género'},
                        text='Global_Sales_Millions'
                    )
                    
                    # Aplicar colores manualmente a cada barra
                    for frame in fig_genres.frames:
                        frame_data = df_vgsales[df_vgsales['Year'] == int(frame.name)]
                        frame.data[0].marker.color = frame_data['Color'].tolist()
                        # Formatear texto de las barras
                        frame.data[0].text = [f'{val:.1f}M' for val in frame_data['Global_Sales_Millions']]
                        frame.data[0].textposition = 'outside'
                    
                    # Aplicar colores al frame inicial también
                    initial_year = df_vgsales['Year'].min()
                    initial_data = df_vgsales[df_vgsales['Year'] == initial_year]
                    fig_genres.data[0].marker.color = initial_data['Color'].tolist()
                    fig_genres.data[0].text = [f'{val:.1f}M' for val in initial_data['Global_Sales_Millions']]
                    fig_genres.data[0].textposition = 'outside'
                    
                    # Configurar animación fluida
                    fig_genres.update_layout(
                        height=600,
                        showlegend=False,
                        xaxis_title='Género',
                        yaxis_title='Ventas Globales (millones)',
                        transition={
                            'duration': 800,  # Duración de transición en ms
                            'easing': 'cubic-in-out'  # Tipo de easing para transición suave
                        }
                    )
                    
                    # Configurar controles de animación para hacerla más fluida
                    fig_genres.layout.updatemenus[0].buttons[0].args[1]['frame']['duration'] = 1000
                    fig_genres.layout.updatemenus[0].buttons[0].args[1]['transition']['duration'] = 800
                    
                    fig_genres = VisualTheme.apply_plotly_theme(fig_genres)
                    st.plotly_chart(fig_genres, use_container_width=True)
                    
                    st.info(f"📊 Mostrando {df_vgsales['Genre'].nunique()} géneros desde {df_vgsales['Year'].min()} hasta {df_vgsales['Year'].max()}")
                else:
                    st.warning("⚠️ No hay datos en VGSales.csv")
                    
            except FileNotFoundError:
                st.error("❌ No se encontró el archivo VGSales.csv")
            except Exception as e:
                st.error(f"❌ Error al cargar VGSales.csv: {str(e)}")
            
            # --- RACE BARS: La Guerra de las Consolas ---
            st.markdown("""
            <div style='background: #1E293B; border-radius: 12px; padding: 2rem; margin: 2rem 0; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);'>
                <h3 style='color: #8B5CF6; margin-top: 0;'>🏆 La Guerra de las Consolas (2006-2025)</h3>
                <p style='color: #F1F5F9; font-size: 1rem; line-height: 1.6;'>
                    Race bars animadas mostrando la batalla épica entre consolas. Observa cómo las líderes 
                    cambian de posición año tras año en esta competencia por dominar el mercado.
                </p>
            </div>
            """, unsafe_allow_html=True)
            
            # Cargar datos de WarConsole.csv
            try:
                df_war = pd.read_csv('WarConsole.csv')
                
                if len(df_war) > 0:
                    # Transformar a formato largo para race bars
                    console_cols = [col for col in df_war.columns if col != 'Year']
                    df_race = df_war.melt(
                        id_vars=['Year'],
                        value_vars=console_cols,
                        var_name='Console',
                        value_name='Sales'
                    )
                    
                    # Limpiar nombres de consolas
                    df_race['Console'] = df_race['Console'].str.replace('_', ' ')
                    
                    # Filtrar consolas con ventas > 0
                    df_race = df_race[df_race['Sales'] > 0].copy()
                    
                    # Asignar colores únicos a cada consola
                    all_consoles = sorted(df_race['Console'].unique())
                    console_colors = {console: VisualTheme.get_color_for_category(console, all_consoles) 
                                     for console in all_consoles}
                    
                    # Crear frames manualmente para race bars horizontales
                    years = sorted(df_race['Year'].unique())
                    frames = []
                    
                    # Configurar número de consolas a mostrar (top 5)
                    top_n = 5
                    
                    # Calcular el máximo de ventas para fijar el eje X
                    max_sales = df_race['Sales'].max()
                    
                    for year in years:
                        # Obtener datos del año y ordenar por ventas (descendente)
                        year_data = df_race[df_race['Year'] == year].copy()
                        year_data = year_data.sort_values('Sales', ascending=True)  # Ascendente para que el top esté arriba
                        
                        # Tomar solo las top N consolas
                        year_data = year_data.tail(top_n)
                        
                        # Crear frame
                        frame = go.Frame(
                            data=[go.Bar(
                                y=year_data['Console'],
                                x=year_data['Sales'],
                                orientation='h',
                                marker=dict(
                                    color=[console_colors[console] for console in year_data['Console']],
                                    line=dict(color='rgba(255, 255, 255, 0.3)', width=1.5)
                                ),
                                text=[f'{val:.1f}M' for val in year_data['Sales']],
                                textposition='outside',
                                textfont=dict(size=12, color=VisualTheme.TEXT_PRIMARY),
                                hovertemplate='<b>%{y}</b><br>Ventas: %{x:.2f}M<extra></extra>'
                            )],
                            name=str(year),
                            layout=go.Layout(
                                xaxis=dict(range=[0, max_sales * 1.15]),  # Rango fijo en cada frame
                                title=dict(
                                    text=f'🎮 Guerra de Consolas - Año {year}',
                                    font=dict(size=24, color=VisualTheme.TEXT_PRIMARY)
                                )
                            )
                        )
                        frames.append(frame)
                    
                    # Crear figura inicial con el primer año
                    initial_data = df_race[df_race['Year'] == years[0]].copy()
                    initial_data = initial_data.sort_values('Sales', ascending=True).tail(top_n)
                    
                    fig_race = go.Figure(
                        data=[go.Bar(
                            y=initial_data['Console'],
                            x=initial_data['Sales'],
                            orientation='h',
                            marker=dict(
                                color=[console_colors[console] for console in initial_data['Console']],
                                line=dict(color='rgba(255, 255, 255, 0.3)', width=1.5)
                            ),
                            text=[f'{val:.1f}M' for val in initial_data['Sales']],
                            textposition='outside',
                            textfont=dict(size=12, color=VisualTheme.TEXT_PRIMARY),
                            hovertemplate='<b>%{y}</b><br>Ventas: %{x:.2f}M<extra></extra>'
                        )],
                        frames=frames
                    )
                    
                    # Configurar layout con animación fluida y ejes fijos
                    fig_race.update_layout(
                        title=dict(
                            text=f'🎮 Guerra de Consolas - Año {years[0]}',
                            font=dict(size=24, color=VisualTheme.TEXT_PRIMARY)
                        ),
                        xaxis=dict(
                            title=dict(
                                text='Ventas Acumuladas (millones)',
                                font=dict(size=14, color=VisualTheme.TEXT_PRIMARY)
                            ),
                            range=[0, max_sales * 1.15],  # Rango fijo
                            tickfont=dict(size=12, color=VisualTheme.TEXT_SECONDARY)
                        ),
                        yaxis=dict(
                            title=dict(
                                text='',
                                font=dict(size=14, color=VisualTheme.TEXT_PRIMARY)
                            ),
                            tickfont=dict(size=12, color=VisualTheme.TEXT_PRIMARY)
                        ),
                        height=600,
                        showlegend=False,
                        plot_bgcolor=VisualTheme.CARD_BACKGROUND,
                        paper_bgcolor=VisualTheme.CARD_BACKGROUND,
                        transition={
                            'duration': 800,
                            'easing': 'cubic-in-out'
                        },
                        # Botones abajo (como la gráfica de géneros)
                        updatemenus=[{
                            'type': 'buttons',
                            'showactive': False,
                            'y': 0,
                            'yanchor': 'top',
                            'xanchor': 'left',
                            'buttons': [
                                {
                                    'label': '▶',
                                    'method': 'animate',
                                    'args': [None, {
                                        'frame': {'duration': 1200, 'redraw': True},
                                        'fromcurrent': True,
                                        'transition': {'duration': 800, 'easing': 'cubic-in-out'}
                                    }]
                                },
                                {
                                    'label': '⏸',
                                    'method': 'animate',
                                    'args': [[None], {
                                        'frame': {'duration': 0, 'redraw': False},
                                        'mode': 'immediate',
                                        'transition': {'duration': 0}
                                    }]
                                }
                            ]
                        }],
                        sliders=[{
                            'active': 0,
                            'steps': [
                                {
                                    'args': [[f.name], {
                                        'frame': {'duration': 800, 'redraw': True},
                                        'mode': 'immediate',
                                        'transition': {'duration': 800, 'easing': 'cubic-in-out'}
                                    }],
                                    'label': str(year),
                                    'method': 'animate'
                                }
                                for year, f in zip(years, frames)
                            ],
                            'currentvalue': {
                                'prefix': 'Año: ',
                                'visible': True,
                                'xanchor': 'right'
                            }
                        }]
                    )
                    
                    # Aplicar tema
                    fig_race = VisualTheme.apply_plotly_theme(fig_race)
                    
                    st.plotly_chart(fig_race, use_container_width=True)
                    
                    # Estadísticas
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.markdown(
                            VisualTheme.create_metric_card_html(
                                f"{len(all_consoles)}", 
                                "Consolas en Competencia"
                            ),
                            unsafe_allow_html=True
                        )
                    with col2:
                        leader = df_race[df_race['Year'] == years[-1]].nlargest(1, 'Sales')['Console'].values[0]
                        st.markdown(
                            VisualTheme.create_metric_card_html(
                                leader, 
                                "Líder Actual"
                            ),
                            unsafe_allow_html=True
                        )
                    with col3:
                        st.markdown(
                            VisualTheme.create_metric_card_html(
                                f"{years[0]} - {years[-1]}", 
                                "Período"
                            ),
                            unsafe_allow_html=True
                        )
                    
                    st.markdown("""
                    <div style='background: rgba(139, 92, 246, 0.1); border-left: 4px solid #8B5CF6; border-radius: 4px; padding: 1rem; margin: 1.5rem 0;'>
                        <p style='color: #F1F5F9; margin: 0; font-size: 1rem;'>
                            <strong>💡 Tip:</strong> Presiona <strong>▶️ Reproducir</strong> para ver la animación completa o usa el slider 
                            para navegar entre años específicos. Observa cómo las consolas compiten por el primer lugar en tiempo real.
                        </p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                else:
                    st.warning("⚠️ No hay datos en WarConsole.csv")
                    
            except FileNotFoundError:
                st.error("❌ No se encontró el archivo WarConsole.csv")
            except Exception as e:
                st.error(f"❌ Error al cargar WarConsole.csv: {str(e)}")
                import traceback
                st.code(traceback.format_exc())
            
            # Summary section
            st.markdown("""
            <div style='background: #1E293B; border-radius: 12px; padding: 2rem; margin: 2rem 0; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);'>
                <h3 style='color: #8B5CF6; margin-top: 0;'>La Evolución de una Industria</h3>
                <p style='color: #F1F5F9; font-size: 1rem; line-height: 1.8;'>
                    La industria de los videojuegos ha experimentado una transformación dramática a lo largo 
                    de las décadas. Desde los primeros días de los arcades hasta la era moderna de los juegos 
                    digitales, cada período ha dejado su marca. Los datos revelan ciclos de expansión y 
                    consolidación, reflejando cambios tecnológicos, crisis económicas, y la evolución de las 
                    preferencias de los jugadores. Entender estos patrones temporales es esencial para 
                    anticipar el futuro de la industria.
                </p>
            </div>
            """, unsafe_allow_html=True)
        
        else:
            st.warning("⚠️ No hay datos temporales válidos (años entre 1980-2025) para el análisis.")
    
    else:
        st.warning("⚠️ No se encontró la columna de año necesaria para el análisis temporal.")

# ---------------------------------------------------------
# TAB 5 – Experiencia del Jugador (Game Length Analysis)
# ---------------------------------------------------------
with tab_experiencia:
    st.markdown("""
    <h2 style='color: #8B5CF6; text-align: center; margin-bottom: 1rem;'>Experiencia del Jugador: Tiempo de Juego
    </h2>
    <p style='text-align: center; font-size: 1.1rem; color: #94A3B8; margin-bottom: 2rem;'>
        ¿Cuánto tiempo dedican los jugadores a completar sus juegos favoritos?
    </p>
    """, unsafe_allow_html=True)
    
    # Find required columns for game length
    main_story_col = find_col(["Length_Main_Story_Average", "Main_Story_Average", "main_story", "Length.Main Story.Average"])
    genre_col = find_col(["Metadata_Genres", "Genre", "genre", "Genres"])
    
    if main_story_col:
        # Handle zero and missing length data appropriately
        df_length = df[df[main_story_col].notna()].copy()
        df_length = df_length[df_length[main_story_col] > 0]  # Filter out zero values
        
        if len(df_length) > 0:
            # --- Histogram with KDE overlay for main story completion times ---
            st.markdown("""
            <div style='background: #1E293B; border-radius: 12px; padding: 2rem; margin: 2rem 0; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);'>
                <h3 style='color: #8B5CF6; margin-top: 0;'>Distribución de Tiempos de Completado</h3>
                <p style='color: #F1F5F9; font-size: 1rem; line-height: 1.6;'>
                    ¿Cuántas horas necesitas para terminar la historia principal? Exploremos la distribución.
                </p>
            </div>
            """, unsafe_allow_html=True)
            
            # Create histogram with KDE overlay using Plotly
            fig_hist = go.Figure()
            
            # Add histogram
            fig_hist.add_trace(go.Histogram(
                x=df_length[main_story_col],
                nbinsx=30,
                name='Frecuencia',
                marker=dict(
                    color=VisualTheme.PRIMARY_COLORS[0],
                    line=dict(color='rgba(255, 255, 255, 0.2)', width=1)
                ),
                opacity=0.7,
                hovertemplate='Tiempo: %{x:.1f} horas<br>Frecuencia: %{y}<extra></extra>'
            ))
            
            # Calculate KDE for overlay
            from scipy import stats as scipy_stats
            kde = scipy_stats.gaussian_kde(df_length[main_story_col])
            x_range = np.linspace(df_length[main_story_col].min(), df_length[main_story_col].max(), 200)
            kde_values = kde(x_range)
            
            # Add KDE overlay on secondary y-axis to avoid overlap
            fig_hist.add_trace(go.Scatter(
                x=x_range,
                y=kde_values,
                mode='lines',
                name='Densidad (KDE)',
                line=dict(color=VisualTheme.ACCENT_COLORS[0], width=3),
                yaxis='y2',
                hovertemplate='Tiempo: %{x:.1f} horas<br>Densidad: %{y:.4f}<extra></extra>'
            ))
            
            # Calculate statistics
            mean_time = df_length[main_story_col].mean()
            median_time = df_length[main_story_col].median()
            
            # Add vertical lines for mean and median with smart positioning
            # Si están muy cerca, poner una arriba y otra abajo
            if abs(mean_time - median_time) < (df_length[main_story_col].max() * 0.1):
                # Están cerca - poner en posiciones diferentes
                fig_hist.add_vline(
                    x=mean_time,
                    line_dash="dash",
                    line_color=VisualTheme.ACCENT_COLORS[1],
                    annotation_text=f"Media: {mean_time:.1f}h",
                    annotation_position="top left"
                )
                
                fig_hist.add_vline(
                    x=median_time,
                    line_dash="dot",
                    line_color=VisualTheme.ACCENT_COLORS[2],
                    annotation_text=f"Mediana: {median_time:.1f}h",
                    annotation_position="bottom right"
                )
            else:
                # Están separadas - ambas arriba está bien
                fig_hist.add_vline(
                    x=mean_time,
                    line_dash="dash",
                    line_color=VisualTheme.ACCENT_COLORS[1],
                    annotation_text=f"Media: {mean_time:.1f}h",
                    annotation_position="top"
                )
                
                fig_hist.add_vline(
                    x=median_time,
                    line_dash="dot",
                    line_color=VisualTheme.ACCENT_COLORS[2],
                    annotation_text=f"Mediana: {median_time:.1f}h",
                    annotation_position="top"
                )
            
            fig_hist.update_layout(
                title=dict(
                    text='Distribución de Tiempos de Completado de Historia Principal',
                    font=dict(size=20, color=VisualTheme.TEXT_PRIMARY)
                ),
                xaxis_title='Tiempo de Completado (horas)',
                yaxis_title='Frecuencia',
                yaxis2=dict(
                    title='Densidad',
                    overlaying='y',
                    side='right',
                    showgrid=False
                ),
                height=500,
                showlegend=True,
                legend=dict(
                    orientation='h',
                    yanchor='bottom',
                    y=1.02,
                    xanchor='center',
                    x=0.5
                )
            )
            
            # Apply theme
            fig_hist = VisualTheme.apply_plotly_theme(fig_hist)
            st.plotly_chart(fig_hist, use_container_width=True)
            
            # Narrative text
            st.markdown(f"""
            <div style='background: rgba(139, 92, 246, 0.1); border-left: 4px solid #8B5CF6; border-radius: 4px; padding: 1rem; margin: 1rem 0;'>
                <p style='color: #F1F5F9; margin: 0; font-size: 1rem;'>
                    <strong>Insight:</strong> El tiempo promedio para completar la historia principal es 
                    <strong>{mean_time:.1f} horas</strong>, con una mediana de <strong>{median_time:.1f} horas</strong>. 
                    La distribución revela que la mayoría de los juegos ofrecen experiencias de duración moderada, 
                    aunque existen títulos épicos que requieren inversiones significativas de tiempo.
                </p>
            </div>
            """, unsafe_allow_html=True)
            
            # --- Box plot comparing completion times across genres ---
            if genre_col:
                st.markdown("""
                <div style='background: #1E293B; border-radius: 12px; padding: 2rem; margin: 2rem 0; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);'>
                    <h3 style='color: #8B5CF6; margin-top: 0;'>Comparación de Tiempos por Género</h3>
                    <p style='color: #F1F5F9; font-size: 1rem; line-height: 1.6;'>
                        ¿Qué géneros ofrecen las experiencias más largas? Comparemos los tiempos de completado.
                    </p>
                </div>
                """, unsafe_allow_html=True)
                
                # Calculate median completion time by genre for sorting
                median_by_genre = df_length.groupby(genre_col)[main_story_col].median().sort_values(ascending=False)
                sorted_genres = median_by_genre.index.tolist()
                
                # Limit to top genres with sufficient data
                genre_counts = df_length[genre_col].value_counts()
                top_genres = genre_counts[genre_counts >= 5].index.tolist()  # At least 5 games per genre
                
                # Filter to top genres
                df_length_filtered = df_length[df_length[genre_col].isin(top_genres)]
                
                # Sort genres by median completion time
                sorted_genres = [g for g in sorted_genres if g in top_genres]
                
                # Create box plot
                fig_box = go.Figure()
                
                for genre in sorted_genres:
                    genre_data = df_length_filtered[df_length_filtered[genre_col] == genre]
                    
                    fig_box.add_trace(go.Box(
                        y=genre_data[main_story_col],
                        name=genre,
                        marker=dict(
                            color=VisualTheme.get_color_for_category(genre, sorted_genres),
                            line=dict(color='rgba(255, 255, 255, 0.3)', width=1)
                        ),
                        boxmean='sd',  # Show mean and standard deviation
                        hovertemplate='<b>%{fullData.name}</b><br>Tiempo: %{y:.1f} horas<extra></extra>'
                    ))
                
                fig_box.update_layout(
                    title=dict(
                        text='Distribución de Tiempos de Completado por Género',
                        font=dict(size=20, color=VisualTheme.TEXT_PRIMARY)
                    ),
                    yaxis_title='Tiempo de Completado (horas)',
                    xaxis_title='Género',
                    height=600,
                    showlegend=False,
                    xaxis=dict(tickangle=-45)
                )
                
                # Apply theme
                fig_box = VisualTheme.apply_plotly_theme(fig_box)
                st.plotly_chart(fig_box, use_container_width=True)
                
                # Narrative text explaining length-genre relationships
                longest_genre = sorted_genres[0]
                longest_median = median_by_genre[longest_genre]
                shortest_genre = sorted_genres[-1]
                shortest_median = median_by_genre[shortest_genre]
                
                st.markdown(f"""
                <div style='background: rgba(139, 92, 246, 0.1); border-left: 4px solid #8B5CF6; border-radius: 4px; padding: 1rem; margin: 1rem 0;'>
                    <p style='color: #F1F5F9; margin: 0; font-size: 1rem;'>
                        <strong>Insight:</strong> <strong>{longest_genre}</strong> ofrece las experiencias más 
                        largas con una mediana de <strong>{longest_median:.1f} horas</strong>, mientras que 
                        <strong>{shortest_genre}</strong> proporciona experiencias más breves con 
                        <strong>{shortest_median:.1f} horas</strong>. Esta variación refleja las diferentes 
                        filosofías de diseño: algunos géneros priorizan narrativas épicas y mundos expansivos, 
                        mientras otros se enfocan en experiencias concentradas e intensas.
                    </p>
                </div>
                """, unsafe_allow_html=True)
                
                # Additional statistics table
                st.markdown("""
                <div style='background: #1E293B; border-radius: 12px; padding: 2rem; margin: 2rem 0; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);'>
                    <h3 style='color: #8B5CF6; margin-top: 0;'>Estadísticas Detalladas por Género</h3>
                    <p style='color: #94A3B8; font-size: 0.95rem; margin-top: 1rem;'>
                        Esta tabla muestra métricas clave del tiempo de juego para cada género:
                    </p>
                </div>
                """, unsafe_allow_html=True)
                
                # Create statistics table
                stats_by_genre = df_length_filtered.groupby(genre_col)[main_story_col].agg([
                    ('Promedio', 'mean'),
                    ('Mediana', 'median'),
                    ('Mínimo', 'min'),
                    ('Máximo', 'max'),
                    ('Juegos', 'count')
                ]).round(1)
                
                # Sort by median
                stats_by_genre = stats_by_genre.sort_values('Mediana', ascending=False)
                
                # Display table
                st.dataframe(
                    stats_by_genre,
                    use_container_width=True,
                    height=400
                )
                
                # Explanation of columns
                st.markdown("""
                <div style='background: rgba(59, 130, 246, 0.1); border-left: 4px solid #3B82F6; border-radius: 4px; padding: 1rem; margin: 1rem 0;'>
                    <p style='color: #F1F5F9; margin: 0; font-size: 0.95rem;'>
                        <strong>Explicación de las columnas:</strong><br>
                        • <strong>Promedio:</strong> Tiempo medio de completado para todos los juegos del género (en horas)<br>
                        • <strong>Mediana:</strong> Valor central - la mitad de los juegos toman más tiempo y la mitad menos (en horas)<br>
                        • <strong>Mínimo:</strong> El juego más corto del género (en horas)<br>
                        • <strong>Máximo:</strong> El juego más largo del género (en horas)<br>
                        • <strong>Juegos:</strong> Cantidad total de juegos analizados en este género
                    </p>
                </div>
                """, unsafe_allow_html=True)
            
            # Summary section
            st.markdown("""
            <div style='background: #1E293B; border-radius: 12px; padding: 2rem; margin: 2rem 0; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);'>
                <h3 style='color: #8B5CF6; margin-top: 0;'>La Experiencia del Jugador</h3>
                <p style='color: #F1F5F9; font-size: 1rem; line-height: 1.8;'>
                    El tiempo de juego es un factor crucial en la experiencia del jugador. Los datos revelan 
                    que diferentes géneros ofrecen compromisos de tiempo muy distintos, permitiendo a los 
                    jugadores elegir experiencias que se ajusten a su disponibilidad y preferencias. Desde 
                    aventuras épicas que requieren decenas de horas hasta experiencias concentradas que se 
                    pueden completar en una tarde, la industria ofrece opciones para todos los estilos de vida. 
                    Entender estos patrones ayuda tanto a jugadores a tomar decisiones informadas como a 
                    desarrolladores a diseñar experiencias que resuenen con su audiencia objetivo.
                </p>
            </div>
            """, unsafe_allow_html=True)
        
        else:
            st.warning("⚠️ No hay datos válidos de tiempo de completado (valores mayores a cero) para el análisis.")
    
    else:
        st.warning("⚠️ No se encontró la columna de tiempo de historia principal necesaria para el análisis.")

# ---------------------------------------------------------
# TAB 6 – Correlaciones (Conexiones Ocultas)
# ---------------------------------------------------------
with tab_corr:
    st.markdown("""
    <h2 style='color: #8B5CF6; text-align: center; margin-bottom: 1rem;'>Conexiones Ocultas: Análisis de Correlación
    </h2>
    <p style='text-align: center; font-size: 1.1rem; color: #94A3B8; margin-bottom: 2rem;'>
        Descubre las relaciones ocultas entre variables que revelan los secretos del éxito
    </p>
    """, unsafe_allow_html=True)
    
    # Introduction narrative
    st.markdown("""
    <div style='background: #1E293B; border-radius: 12px; padding: 2rem; margin: 2rem 0; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);'>
        <h3 style='color: #8B5CF6; margin-top: 0;'>Buscando Patrones Ocultos</h3>
        <p style='color: #F1F5F9; font-size: 1rem; line-height: 1.8;'>
            Más allá de las tendencias obvias, los datos esconden relaciones sutiles que pueden 
            revelar insights profundos. El análisis de correlación nos permite descubrir cómo 
            diferentes variables se relacionan entre sí, identificando patrones que no son 
            inmediatamente visibles pero que pueden ser cruciales para entender el éxito en 
            la industria de los videojuegos.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Select only important numeric columns for correlation analysis
    # Map technical column names to user-friendly Spanish names
    important_columns = {
        'Metrics_Sales': 'Ventas (millones)',
        'Metrics_Review_Score': 'Puntuación de Crítica',
        'Metrics_Used_Price': 'Precio Usado ($)',
        'Release_Year': 'Año de Lanzamiento',
        'Length_Main_Story_Average': 'Tiempo Historia Principal (hrs)',
        'Length_All_Styles_Average': 'Tiempo Todos los Estilos (hrs)',
        'Length_Completionists_Average': 'Tiempo Completionistas (hrs)',
        'Features_Max_Players': 'Jugadores Máximos'
    }
    
    # Find which columns exist in the dataframe
    available_columns = {}
    for tech_name, friendly_name in important_columns.items():
        col = find_col([tech_name])
        if col and col in df.columns:
            available_columns[col] = friendly_name
    
    # If we have at least 2 columns, proceed
    if len(available_columns) >= 2:
        # Select only the important columns
        numeric_df = df[list(available_columns.keys())].copy()
        
        # Rename columns to friendly names
        numeric_df.columns = [available_columns[col] for col in numeric_df.columns]
        
        # Calculate correlation matrix
        corr_matrix = numeric_df.corr()
        
        # Create correlation heatmap with diverging color scheme (red-white-blue)
        st.markdown("""
        <div style='background: #1E293B; border-radius: 12px; padding: 2rem; margin: 2rem 0; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);'>
            <h3 style='color: #8B5CF6; margin-top: 0;'>Mapa de Calor de Correlaciones</h3>
            <p style='color: #F1F5F9; font-size: 1rem; line-height: 1.6;'>
                Cada celda muestra la fuerza de la relación entre dos variables. 
                Azul indica correlación positiva, rojo indica correlación negativa.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Create Plotly heatmap for better interactivity
        fig_heatmap = go.Figure()
        
        # Prepare annotations for correlation values
        annotations = []
        threshold = 0.7  # Strong correlation threshold
        
        for i in range(len(corr_matrix)):
            for j in range(len(corr_matrix)):
                corr_value = corr_matrix.iloc[i, j]
                
                # Determine if this is a strong correlation (excluding diagonal)
                is_strong = (i != j) and (not pd.isna(corr_value)) and (abs(corr_value) > threshold)
                
                # Format annotation text
                if pd.isna(corr_value):
                    text = "N/A"
                    font_weight = "normal"
                else:
                    text = f"{corr_value:.2f}"
                    font_weight = "bold" if is_strong else "normal"
                
                # Determine text color based on background intensity
                # Use dark text for light backgrounds (values near 0), light text for dark backgrounds
                if pd.isna(corr_value):
                    text_color = VisualTheme.TEXT_PRIMARY
                elif abs(corr_value) < 0.3:
                    text_color = '#1E293B'  # Dark text for light background
                else:
                    text_color = 'white'  # Light text for dark background
                
                annotations.append(
                    dict(
                        x=j,
                        y=i,
                        text=text,
                        showarrow=False,
                        font=dict(
                            size=10 if is_strong else 9,
                            color=text_color,
                            family='Arial, sans-serif',
                        ),
                        xref='x',
                        yref='y'
                    )
                )
        
        # Add heatmap trace with diverging color scheme (RdYlBu - better contrast)
        fig_heatmap.add_trace(go.Heatmap(
            z=corr_matrix.values,
            x=corr_matrix.columns,
            y=corr_matrix.index,
            colorscale='RdYlBu_r',  # Red-Yellow-Blue reversed for better contrast
            zmid=0,  # Center the colorscale at 0
            zmin=-1,
            zmax=1,
            colorbar=dict(
                title=dict(text='Correlación', side='right'),
                tickmode='linear',
                tick0=-1,
                dtick=0.5
            ),
            hovertemplate='<b>%{y}</b> vs <b>%{x}</b><br>Correlación: %{z:.3f}<extra></extra>'
        ))
        
        fig_heatmap.update_layout(
            title=dict(
                text='Matriz de Correlación entre Variables Numéricas',
                font=dict(size=20, color=VisualTheme.TEXT_PRIMARY)
            ),
            xaxis=dict(
                tickangle=-45,
                side='bottom'
            ),
            yaxis=dict(
                autorange='reversed'
            ),
            height=max(600, len(corr_matrix) * 40),
            width=max(800, len(corr_matrix) * 40),
            annotations=annotations
        )
        
        # Apply theme
        fig_heatmap = VisualTheme.apply_plotly_theme(fig_heatmap)
        st.plotly_chart(fig_heatmap, use_container_width=True)
        
        # Variable explanation
        st.markdown("""
        <div style='background: rgba(59, 130, 246, 0.1); border-left: 4px solid #3B82F6; border-radius: 4px; padding: 1rem; margin: 1rem 0;'>
            <p style='color: #F1F5F9; margin: 0; font-size: 0.95rem;'>
                <strong>Explicación de Variables:</strong><br>
                • <strong>Ventas (millones):</strong> Unidades vendidas globalmente<br>
                • <strong>Puntuación de Crítica:</strong> Calificación promedio de críticos (0-100)<br>
                • <strong>Precio Usado ($):</strong> Precio de reventa en el mercado secundario<br>
                • <strong>Año de Lanzamiento:</strong> Año en que se publicó el juego<br>
                • <strong>Tiempo Historia Principal (hrs):</strong> Horas promedio para completar la historia<br>
                • <strong>Jugadores Máximos:</strong> Número máximo de jugadores simultáneos<br><br>
                <strong>Cómo leer:</strong> Los valores van de -1 (correlación negativa perfecta) a +1 (correlación positiva perfecta). 
                Valores cercanos a 0 indican poca o ninguna relación.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Find and highlight strong correlations
        st.markdown("""
        <div style='background: #1E293B; border-radius: 12px; padding: 2rem; margin: 2rem 0; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);'>
            <h3 style='color: #8B5CF6; margin-top: 0;'>Correlaciones Fuertes Detectadas</h3>
            <p style='color: #F1F5F9; font-size: 1rem; line-height: 1.6;'>
                Correlaciones con |r| > 0.7 que revelan relaciones significativas
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Find strong correlations (excluding diagonal)
        strong_correlations = []
        for i in range(len(corr_matrix)):
            for j in range(i+1, len(corr_matrix)):
                corr_value = corr_matrix.iloc[i, j]
                if not pd.isna(corr_value) and abs(corr_value) > threshold:
                    strong_correlations.append({
                        'Variable 1': corr_matrix.index[i],
                        'Variable 2': corr_matrix.columns[j],
                        'Correlación': corr_value,
                        'Tipo': 'Positiva' if corr_value > 0 else 'Negativa',
                        'Fuerza': abs(corr_value)
                    })
        
        if strong_correlations:
            # Sort by strength
            strong_correlations_df = pd.DataFrame(strong_correlations)
            strong_correlations_df = strong_correlations_df.sort_values('Fuerza', ascending=False)
            
            # Display strong correlations in a styled table
            st.dataframe(
                strong_correlations_df[['Variable 1', 'Variable 2', 'Correlación', 'Tipo']],
                use_container_width=True,
                height=min(400, len(strong_correlations_df) * 40 + 50)
            )
            
            # Narrative interpretation of key correlations
            st.markdown("""
            <div style='background: rgba(139, 92, 246, 0.1); border-left: 4px solid #8B5CF6; border-radius: 4px; padding: 1rem; margin: 1rem 0;'>
            """, unsafe_allow_html=True)
            
            # Interpret top correlations
            if len(strong_correlations_df) > 0:
                top_corr = strong_correlations_df.iloc[0]
                st.markdown(f"""
                <p style='color: #F1F5F9; margin: 0; font-size: 1rem;'>
                    <strong>Insight Principal:</strong> La correlación más fuerte es entre 
                    <strong>{top_corr['Variable 1']}</strong> y <strong>{top_corr['Variable 2']}</strong> 
                    (r={top_corr['Correlación']:.3f}), indicando una relación <strong>{top_corr['Tipo'].lower()}</strong> 
                    muy significativa. 
                    {'Cuando una aumenta, la otra tiende a aumentar también.' if top_corr['Tipo'] == 'Positiva' else 'Cuando una aumenta, la otra tiende a disminuir.'}
                </p>
                """, unsafe_allow_html=True)
            
            st.markdown("</div>", unsafe_allow_html=True)
            
            # Additional insights
            positive_count = len(strong_correlations_df[strong_correlations_df['Tipo'] == 'Positiva'])
            negative_count = len(strong_correlations_df[strong_correlations_df['Tipo'] == 'Negativa'])
            
            st.markdown(f"""
            <div style='background: rgba(139, 92, 246, 0.1); border-left: 4px solid #8B5CF6; border-radius: 4px; padding: 1rem; margin: 1rem 0;'>
                <p style='color: #F1F5F9; margin: 0; font-size: 1rem;'>
                    <strong>Resumen:</strong> Se detectaron <strong>{len(strong_correlations_df)}</strong> 
                    correlaciones fuertes en total: <strong>{positive_count}</strong> positivas y 
                    <strong>{negative_count}</strong> negativas. Estas relaciones pueden ayudar a 
                    predecir comportamientos y tomar decisiones estratégicas en el desarrollo y 
                    marketing de videojuegos.
                </p>
            </div>
            """, unsafe_allow_html=True)
        
        else:
            st.info("ℹ️ No se detectaron correlaciones fuertes (|r| > 0.7) en este dataset. Esto puede indicar que las variables son relativamente independientes entre sí.")
        
        # Interpretation guide
        st.markdown("""
        <div style='background: #1E293B; border-radius: 12px; padding: 2rem; margin: 2rem 0; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);'>
            <h3 style='color: #8B5CF6; margin-top: 0;'>Guía de Interpretación</h3>
            <div style='color: #F1F5F9; font-size: 1rem; line-height: 1.8;'>
                <p><strong>Valores de Correlación:</strong></p>
                <ul>
                    <li><strong>+1.0:</strong> Correlación positiva perfecta (cuando una sube, la otra sube proporcionalmente)</li>
                    <li><strong>+0.7 a +1.0:</strong> Correlación positiva fuerte</li>
                    <li><strong>+0.4 a +0.7:</strong> Correlación positiva moderada</li>
                    <li><strong>-0.4 a +0.4:</strong> Correlación débil o inexistente</li>
                    <li><strong>-0.7 a -0.4:</strong> Correlación negativa moderada</li>
                    <li><strong>-1.0 a -0.7:</strong> Correlación negativa fuerte</li>
                    <li><strong>-1.0:</strong> Correlación negativa perfecta (cuando una sube, la otra baja proporcionalmente)</li>
                </ul>
                <p style='margin-top: 1rem;'><strong>⚠️ Importante:</strong> Correlación no implica causalidad. 
                Una correlación fuerte indica que dos variables se mueven juntas, pero no necesariamente 
                que una cause a la otra.</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Summary section
        st.markdown("""
        <div style='background: #1E293B; border-radius: 12px; padding: 2rem; margin: 2rem 0; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);'>
            <h3 style='color: #8B5CF6; margin-top: 0;'>Conclusiones: El Poder de las Conexiones</h3>
            <p style='color: #F1F5F9; font-size: 1rem; line-height: 1.8;'>
                El análisis de correlación revela las conexiones ocultas que estructuran la industria 
                de los videojuegos. Estas relaciones no son coincidencias: son el resultado de dinámicas 
                de mercado, preferencias de jugadores, y decisiones de diseño que se refuerzan mutuamente. 
                Comprender estas correlaciones permite a desarrolladores, publishers, y analistas anticipar 
                tendencias, optimizar estrategias, y tomar decisiones basadas en datos. En un mercado 
                competitivo, reconocer y aprovechar estas conexiones puede ser la diferencia entre el 
                éxito y el fracaso.
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    else:
        st.warning("⚠️ No hay suficientes variables importantes disponibles para realizar un análisis de correlación significativo.")
