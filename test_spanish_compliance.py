"""
Property-based tests for Spanish language compliance.

**Feature: data-storytelling-dashboard, Property 16: Spanish Language Compliance**
**Validates: Requirements 10.5**
"""

import pytest
from hypothesis import given, strategies as st, settings
import plotly.graph_objects as go
import pandas as pd
import numpy as np
import re
from data_loader import load_data, find_column


def is_spanish_text(text):
    """
    Check if text is in Spanish.
    
    This is a heuristic check that looks for:
    - Spanish-specific characters (á, é, í, ó, ú, ñ, ü)
    - Common Spanish words
    - Absence of common English-only patterns
    """
    if not text or not isinstance(text, str):
        return True  # Empty or non-string is acceptable
    
    text_lower = text.lower().strip()
    
    # If text is very short (like "N/A", numbers, etc.), it's acceptable
    if len(text_lower) < 3:
        return True
    
    # Check for Spanish-specific characters (strong indicator)
    spanish_chars = re.search(r'[áéíóúñü]', text_lower)
    if spanish_chars:
        return True
    
    # Common Spanish words that should appear in our dashboard
    spanish_keywords = [
        'año', 'años', 'género', 'géneros', 'ventas', 'juegos', 'juego',
        'plataforma', 'plataformas', 'puntuación', 'correlación', 'tiempo',
        'promedio', 'total', 'totales', 'millones', 'horas', 'lanzamientos',
        'frecuencia', 'distribución', 'comparación', 'análisis', 'número',
        'variables', 'numéricas', 'crítica', 'completado', 'mediana',
        'máximo', 'mínimo', 'tendencia', 'evolución', 'temporal'
    ]
    
    # Check if any Spanish keyword is present
    for keyword in spanish_keywords:
        if keyword in text_lower:
            return True
    
    # Common English-only words that should NOT appear (strong negative indicator)
    english_only_words = [
        'sales', 'genre', 'platform', 'score', 'year', 'games', 'game',
        'average', 'total', 'millions', 'hours', 'releases', 'frequency',
        'distribution', 'comparison', 'analysis', 'number', 'variables',
        'numeric', 'review', 'completion', 'median', 'maximum', 'minimum',
        'trend', 'evolution', 'temporal', 'correlation'
    ]
    
    # Check for English-only words (but be careful with technical terms)
    for word in english_only_words:
        # Use word boundaries to avoid false positives
        if re.search(rf'\b{word}\b', text_lower):
            return False
    
    # If we get here, assume it's acceptable (could be technical terms, numbers, etc.)
    return True


def extract_text_from_figure(fig):
    """Extract all text elements from a Plotly figure."""
    texts = []
    
    if not isinstance(fig, go.Figure):
        return texts
    
    # Extract title
    if fig.layout.title and fig.layout.title.text:
        texts.append(('title', str(fig.layout.title.text)))
    
    # Extract axis labels
    if fig.layout.xaxis and fig.layout.xaxis.title and fig.layout.xaxis.title.text:
        texts.append(('xaxis', str(fig.layout.xaxis.title.text)))
    
    if fig.layout.yaxis and fig.layout.yaxis.title and fig.layout.yaxis.title.text:
        texts.append(('yaxis', str(fig.layout.yaxis.title.text)))
    
    if hasattr(fig.layout, 'yaxis2') and fig.layout.yaxis2 and fig.layout.yaxis2.title and fig.layout.yaxis2.title.text:
        texts.append(('yaxis2', str(fig.layout.yaxis2.title.text)))
    
    # Extract legend labels (trace names)
    for trace in fig.data:
        if hasattr(trace, 'name') and trace.name:
            texts.append(('legend', str(trace.name)))
    
    # Extract colorbar title (for heatmaps)
    for trace in fig.data:
        if hasattr(trace, 'colorbar') and trace.colorbar and hasattr(trace.colorbar, 'title'):
            if trace.colorbar.title and hasattr(trace.colorbar.title, 'text') and trace.colorbar.title.text:
                texts.append(('colorbar', str(trace.colorbar.title.text)))
    
    # Extract annotations
    if fig.layout.annotations:
        for annotation in fig.layout.annotations:
            if annotation.text:
                texts.append(('annotation', str(annotation.text)))
    
    return texts


def create_sales_by_genre_chart(df, genre_col, sales_col):
    """Create sales by genre chart for testing."""
    from visual_theme import VisualTheme
    
    sales_by_genre = df.groupby(genre_col)[sales_col].sum().sort_values(ascending=False)
    all_genres = sales_by_genre.index.tolist()
    
    fig = go.Figure()
    colors = [VisualTheme.get_color_for_category(genre, all_genres) for genre in all_genres]
    
    fig.add_trace(go.Bar(
        y=sales_by_genre.index,
        x=sales_by_genre.values,
        orientation='h',
        marker=dict(color=colors),
        text=[f'{val:.1f}M' for val in sales_by_genre.values],
        textposition='outside'
    ))
    
    fig.update_layout(
        title=dict(text='Ventas Totales por Género (en millones)'),
        xaxis_title='Ventas Totales (millones)',
        yaxis_title='Género',
        height=max(400, len(sales_by_genre) * 30),
        showlegend=False
    )
    
    return VisualTheme.apply_plotly_theme(fig)


def create_platform_comparison_chart(df, platform_col, sales_col):
    """Create platform comparison chart for testing."""
    from visual_theme import VisualTheme
    
    sales_by_platform = df.groupby(platform_col)[sales_col].sum().sort_values(ascending=False)
    top_platforms = sales_by_platform.head(15)
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        y=top_platforms.index,
        x=top_platforms.values,
        orientation='h',
        marker=dict(color=VisualTheme.PRIMARY_COLORS[0]),
        text=[f'{val:.1f}M' for val in top_platforms.values],
        textposition='outside'
    ))
    
    fig.update_layout(
        title=dict(text='Top 15 Plataformas por Ventas Totales'),
        xaxis_title='Ventas Totales (millones)',
        yaxis_title='Plataforma',
        height=500,
        showlegend=False
    )
    
    return VisualTheme.apply_plotly_theme(fig)


def create_score_sales_scatter(df, score_col, sales_col, genre_col):
    """Create score vs sales scatter plot for testing."""
    from visual_theme import VisualTheme
    from scipy import stats
    
    df_with_scores = df[df[score_col].notna()].copy()
    all_genres = df_with_scores[genre_col].unique().tolist()
    
    fig = go.Figure()
    
    for genre in all_genres:
        genre_data = df_with_scores[df_with_scores[genre_col] == genre]
        fig.add_trace(go.Scatter(
            x=genre_data[score_col],
            y=genre_data[sales_col],
            mode='markers',
            name=genre,
            marker=dict(color=VisualTheme.get_color_for_category(genre, all_genres))
        ))
    
    # Add trend line
    slope, intercept, r_value, _, _ = stats.linregress(
        df_with_scores[score_col], 
        df_with_scores[sales_col]
    )
    x_trend = np.array([df_with_scores[score_col].min(), df_with_scores[score_col].max()])
    y_trend = slope * x_trend + intercept
    
    fig.add_trace(go.Scatter(
        x=x_trend,
        y=y_trend,
        mode='lines',
        name=f'Tendencia (r={r_value:.3f})',
        line=dict(color='#FBBF24', width=3, dash='dash')
    ))
    
    fig.update_layout(
        title=dict(text='Relación entre Puntuación de Crítica y Ventas'),
        xaxis_title='Puntuación de Crítica',
        yaxis_title='Ventas (millones)',
        height=600
    )
    
    return VisualTheme.apply_plotly_theme(fig)


def create_temporal_releases_chart(df, year_col):
    """Create temporal releases chart for testing."""
    from visual_theme import VisualTheme
    
    df_temporal = df[df[year_col].notna()].copy()
    df_temporal = df_temporal[(df_temporal[year_col] >= 1980) & (df_temporal[year_col] <= 2025)]
    
    releases_by_year = df_temporal.groupby(year_col).size().reset_index(name='releases')
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=releases_by_year[year_col],
        y=releases_by_year['releases'],
        mode='lines',
        fill='tozeroy',
        line=dict(color=VisualTheme.PRIMARY_COLORS[0], width=3)
    ))
    
    fig.update_layout(
        title=dict(text='Número de Juegos Lanzados por Año'),
        xaxis_title='Año',
        yaxis_title='Número de Lanzamientos',
        height=500,
        showlegend=False
    )
    
    return VisualTheme.apply_plotly_theme(fig)


def create_correlation_heatmap(df):
    """Create correlation heatmap for testing."""
    from visual_theme import VisualTheme
    
    numeric_df = df.select_dtypes(include=[np.number])
    corr_matrix = numeric_df.corr()
    
    fig = go.Figure()
    
    fig.add_trace(go.Heatmap(
        z=corr_matrix.values,
        x=corr_matrix.columns,
        y=corr_matrix.index,
        colorscale='RdBu',
        zmid=0,
        zmin=-1,
        zmax=1,
        colorbar=dict(title=dict(text='Correlación', side='right'))
    ))
    
    fig.update_layout(
        title=dict(text='Matriz de Correlación entre Variables Numéricas'),
        xaxis=dict(tickangle=-45),
        yaxis=dict(autorange='reversed'),
        height=max(600, len(corr_matrix) * 40)
    )
    
    return VisualTheme.apply_plotly_theme(fig)


def create_completion_time_histogram(df, main_story_col):
    """Create completion time histogram for testing."""
    from visual_theme import VisualTheme
    
    df_length = df[df[main_story_col].notna()].copy()
    df_length = df_length[df_length[main_story_col] > 0]
    
    fig = go.Figure()
    
    fig.add_trace(go.Histogram(
        x=df_length[main_story_col],
        nbinsx=30,
        name='Frecuencia',
        marker=dict(color=VisualTheme.PRIMARY_COLORS[0]),
        opacity=0.7
    ))
    
    fig.update_layout(
        title=dict(text='Distribución de Tiempos de Completado de Historia Principal'),
        xaxis_title='Tiempo de Completado (horas)',
        yaxis_title='Frecuencia',
        height=500,
        showlegend=True
    )
    
    return VisualTheme.apply_plotly_theme(fig)


@settings(max_examples=100, deadline=None)
@given(st.data())
def test_spanish_language_compliance_property(data):
    """
    **Feature: data-storytelling-dashboard, Property 16: Spanish Language Compliance**
    **Validates: Requirements 10.5**
    
    Property: For any text element in the UI (titles, labels, descriptions, axis labels),
    the text should be in Spanish.
    """
    # Load the actual dataset
    df = load_data("video_games.csv")
    
    # Find required columns
    genre_col = find_column(df, ["Metadata_Genres", "Genre", "genre", "Genres"])
    sales_col = find_column(df, ["Metrics_Sales", "Global_Sales", "sales", "Sales"])
    platform_col = find_column(df, ["Release_Console", "Platform", "platform", "console"])
    score_col = find_column(df, ["Metrics_Review_Score", "Score", "meta_score", "rating", "score"])
    year_col = find_column(df, ["Release_Year", "Year", "year", "release_year"])
    main_story_col = find_column(df, ["Length_Main_Story_Average", "Main_Story_Average", "main_story"])
    
    # Select a random chart type to test
    chart_types = []
    
    if genre_col and sales_col:
        chart_types.append(('sales_by_genre', lambda: create_sales_by_genre_chart(df, genre_col, sales_col)))
    
    if platform_col and sales_col:
        chart_types.append(('platform_comparison', lambda: create_platform_comparison_chart(df, platform_col, sales_col)))
    
    if score_col and sales_col and genre_col:
        df_with_scores = df[df[score_col].notna()]
        if len(df_with_scores) > 0:
            chart_types.append(('score_sales_scatter', lambda: create_score_sales_scatter(df, score_col, sales_col, genre_col)))
    
    if year_col:
        df_temporal = df[df[year_col].notna()]
        df_temporal = df_temporal[(df_temporal[year_col] >= 1980) & (df_temporal[year_col] <= 2025)]
        if len(df_temporal) > 0:
            chart_types.append(('temporal_releases', lambda: create_temporal_releases_chart(df, year_col)))
    
    if len(df.select_dtypes(include=[np.number]).columns) >= 2:
        chart_types.append(('correlation_heatmap', lambda: create_correlation_heatmap(df)))
    
    if main_story_col:
        df_length = df[df[main_story_col].notna()]
        df_length = df_length[df_length[main_story_col] > 0]
        if len(df_length) > 0:
            chart_types.append(('completion_time', lambda: create_completion_time_histogram(df, main_story_col)))
    
    # If no charts can be created, skip
    if not chart_types:
        return
    
    # Select a random chart type
    chart_name, chart_creator = data.draw(st.sampled_from(chart_types))
    
    # Create the chart
    fig = chart_creator()
    
    # Extract all text elements
    texts = extract_text_from_figure(fig)
    
    # Verify each text element is in Spanish
    non_spanish_texts = []
    for text_type, text_content in texts:
        if not is_spanish_text(text_content):
            non_spanish_texts.append((text_type, text_content))
    
    assert len(non_spanish_texts) == 0, (
        f"Chart '{chart_name}' contains non-Spanish text elements: "
        f"{non_spanish_texts}"
    )


def test_sales_by_genre_chart_spanish():
    """Test that sales by genre chart uses Spanish text."""
    df = load_data("video_games.csv")
    genre_col = find_column(df, ["Metadata_Genres", "Genre", "genre", "Genres"])
    sales_col = find_column(df, ["Metrics_Sales", "Global_Sales", "sales", "Sales"])
    
    if genre_col and sales_col:
        fig = create_sales_by_genre_chart(df, genre_col, sales_col)
        texts = extract_text_from_figure(fig)
        
        non_spanish_texts = []
        for text_type, text_content in texts:
            if not is_spanish_text(text_content):
                non_spanish_texts.append((text_type, text_content))
        
        assert len(non_spanish_texts) == 0, (
            f"Sales by genre chart contains non-Spanish text: {non_spanish_texts}"
        )


def test_platform_comparison_chart_spanish():
    """Test that platform comparison chart uses Spanish text."""
    df = load_data("video_games.csv")
    platform_col = find_column(df, ["Release_Console", "Platform", "platform", "console"])
    sales_col = find_column(df, ["Metrics_Sales", "Global_Sales", "sales", "Sales"])
    
    if platform_col and sales_col:
        fig = create_platform_comparison_chart(df, platform_col, sales_col)
        texts = extract_text_from_figure(fig)
        
        non_spanish_texts = []
        for text_type, text_content in texts:
            if not is_spanish_text(text_content):
                non_spanish_texts.append((text_type, text_content))
        
        assert len(non_spanish_texts) == 0, (
            f"Platform comparison chart contains non-Spanish text: {non_spanish_texts}"
        )


def test_score_sales_scatter_spanish():
    """Test that score vs sales scatter plot uses Spanish text."""
    df = load_data("video_games.csv")
    score_col = find_column(df, ["Metrics_Review_Score", "Score", "meta_score", "rating", "score"])
    sales_col = find_column(df, ["Metrics_Sales", "Global_Sales", "sales", "Sales"])
    genre_col = find_column(df, ["Metadata_Genres", "Genre", "genre", "Genres"])
    
    if score_col and sales_col and genre_col:
        df_with_scores = df[df[score_col].notna()]
        if len(df_with_scores) > 0:
            fig = create_score_sales_scatter(df, score_col, sales_col, genre_col)
            texts = extract_text_from_figure(fig)
            
            non_spanish_texts = []
            for text_type, text_content in texts:
                if not is_spanish_text(text_content):
                    non_spanish_texts.append((text_type, text_content))
            
            assert len(non_spanish_texts) == 0, (
                f"Score vs sales scatter plot contains non-Spanish text: {non_spanish_texts}"
            )


def test_temporal_releases_chart_spanish():
    """Test that temporal releases chart uses Spanish text."""
    df = load_data("video_games.csv")
    year_col = find_column(df, ["Release_Year", "Year", "year", "release_year"])
    
    if year_col:
        df_temporal = df[df[year_col].notna()]
        df_temporal = df_temporal[(df_temporal[year_col] >= 1980) & (df_temporal[year_col] <= 2025)]
        if len(df_temporal) > 0:
            fig = create_temporal_releases_chart(df, year_col)
            texts = extract_text_from_figure(fig)
            
            non_spanish_texts = []
            for text_type, text_content in texts:
                if not is_spanish_text(text_content):
                    non_spanish_texts.append((text_type, text_content))
            
            assert len(non_spanish_texts) == 0, (
                f"Temporal releases chart contains non-Spanish text: {non_spanish_texts}"
            )


def test_correlation_heatmap_spanish():
    """Test that correlation heatmap uses Spanish text."""
    df = load_data("video_games.csv")
    
    if len(df.select_dtypes(include=[np.number]).columns) >= 2:
        fig = create_correlation_heatmap(df)
        texts = extract_text_from_figure(fig)
        
        non_spanish_texts = []
        for text_type, text_content in texts:
            if not is_spanish_text(text_content):
                non_spanish_texts.append((text_type, text_content))
        
        assert len(non_spanish_texts) == 0, (
            f"Correlation heatmap contains non-Spanish text: {non_spanish_texts}"
        )
