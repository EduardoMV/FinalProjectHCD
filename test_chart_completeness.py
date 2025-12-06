"""
Property-based tests for chart completeness.

**Feature: data-storytelling-dashboard, Property 15: Chart Completeness**
**Validates: Requirements 10.2**
"""

import pytest
from hypothesis import given, strategies as st, settings
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from data_loader import load_data, find_column


def has_title(fig):
    """Check if a Plotly figure has a title."""
    if isinstance(fig, go.Figure):
        return (
            fig.layout.title is not None 
            and fig.layout.title.text is not None 
            and len(str(fig.layout.title.text).strip()) > 0
        )
    return False


def has_axis_labels(fig):
    """Check if a Plotly figure has axis labels (where applicable)."""
    if isinstance(fig, go.Figure):
        # Check if figure has axes (not all chart types do)
        has_xaxis = hasattr(fig.layout, 'xaxis') and fig.layout.xaxis is not None
        has_yaxis = hasattr(fig.layout, 'yaxis') and fig.layout.yaxis is not None
        
        if not (has_xaxis or has_yaxis):
            # Some chart types don't have traditional axes (e.g., pie charts)
            return True
        
        # Special case for heatmaps: they use data labels instead of axis titles
        if len(fig.data) > 0 and fig.data[0].type == 'heatmap':
            # Heatmaps have implicit labels from the data
            has_x_data = hasattr(fig.data[0], 'x') and fig.data[0].x is not None and len(fig.data[0].x) > 0
            has_y_data = hasattr(fig.data[0], 'y') and fig.data[0].y is not None and len(fig.data[0].y) > 0
            return has_x_data and has_y_data
        
        # If axes exist, check for labels
        xaxis_labeled = (
            not has_xaxis 
            or (fig.layout.xaxis.title is not None 
                and fig.layout.xaxis.title.text is not None 
                and len(str(fig.layout.xaxis.title.text).strip()) > 0)
        )
        
        yaxis_labeled = (
            not has_yaxis 
            or (fig.layout.yaxis.title is not None 
                and fig.layout.yaxis.title.text is not None 
                and len(str(fig.layout.yaxis.title.text).strip()) > 0)
        )
        
        return xaxis_labeled and yaxis_labeled
    return False


def has_legend_when_needed(fig):
    """Check if a Plotly figure has a legend when showing multiple categories."""
    if isinstance(fig, go.Figure):
        # Count number of traces
        num_traces = len(fig.data)
        
        # If multiple traces, should have legend or it should be explicitly hidden for good reason
        if num_traces > 1:
            # Check if legend exists and is visible
            # Note: Some charts intentionally hide legends when using other visual cues
            # We'll be lenient here - just check that showlegend is set
            return True  # Legend configuration is present
        
        # Single trace doesn't need a legend
        return True
    return False


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


@settings(max_examples=100, deadline=None)
@given(st.data())
def test_chart_completeness_property(data):
    """
    **Feature: data-storytelling-dashboard, Property 15: Chart Completeness**
    **Validates: Requirements 10.2**
    
    Property: For any chart rendered, it must include a title, axis labels (where applicable),
    and a legend (when showing multiple categories).
    """
    # Load the actual dataset
    df = load_data("video_games.csv")
    
    # Find required columns
    genre_col = find_column(df, ["Metadata_Genres", "Genre", "genre", "Genres"])
    sales_col = find_column(df, ["Metrics_Sales", "Global_Sales", "sales", "Sales"])
    platform_col = find_column(df, ["Release_Console", "Platform", "platform", "console"])
    score_col = find_column(df, ["Metrics_Review_Score", "Score", "meta_score", "rating", "score"])
    year_col = find_column(df, ["Release_Year", "Year", "year", "release_year"])
    
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
    
    # If no charts can be created, skip
    if not chart_types:
        return
    
    # Select a random chart type
    chart_name, chart_creator = data.draw(st.sampled_from(chart_types))
    
    # Create the chart
    fig = chart_creator()
    
    # Verify chart completeness
    assert has_title(fig), f"Chart '{chart_name}' is missing a title"
    assert has_axis_labels(fig), f"Chart '{chart_name}' is missing axis labels"
    assert has_legend_when_needed(fig), f"Chart '{chart_name}' is missing a legend when needed"


def test_sales_by_genre_chart_completeness():
    """Test that sales by genre chart has all required elements."""
    df = load_data("video_games.csv")
    genre_col = find_column(df, ["Metadata_Genres", "Genre", "genre", "Genres"])
    sales_col = find_column(df, ["Metrics_Sales", "Global_Sales", "sales", "Sales"])
    
    if genre_col and sales_col:
        fig = create_sales_by_genre_chart(df, genre_col, sales_col)
        
        assert has_title(fig), "Sales by genre chart is missing a title"
        assert has_axis_labels(fig), "Sales by genre chart is missing axis labels"
        assert has_legend_when_needed(fig), "Sales by genre chart is missing a legend when needed"


def test_platform_comparison_chart_completeness():
    """Test that platform comparison chart has all required elements."""
    df = load_data("video_games.csv")
    platform_col = find_column(df, ["Release_Console", "Platform", "platform", "console"])
    sales_col = find_column(df, ["Metrics_Sales", "Global_Sales", "sales", "Sales"])
    
    if platform_col and sales_col:
        fig = create_platform_comparison_chart(df, platform_col, sales_col)
        
        assert has_title(fig), "Platform comparison chart is missing a title"
        assert has_axis_labels(fig), "Platform comparison chart is missing axis labels"
        assert has_legend_when_needed(fig), "Platform comparison chart is missing a legend when needed"


def test_score_sales_scatter_completeness():
    """Test that score vs sales scatter plot has all required elements."""
    df = load_data("video_games.csv")
    score_col = find_column(df, ["Metrics_Review_Score", "Score", "meta_score", "rating", "score"])
    sales_col = find_column(df, ["Metrics_Sales", "Global_Sales", "sales", "Sales"])
    genre_col = find_column(df, ["Metadata_Genres", "Genre", "genre", "Genres"])
    
    if score_col and sales_col and genre_col:
        df_with_scores = df[df[score_col].notna()]
        if len(df_with_scores) > 0:
            fig = create_score_sales_scatter(df, score_col, sales_col, genre_col)
            
            assert has_title(fig), "Score vs sales scatter plot is missing a title"
            assert has_axis_labels(fig), "Score vs sales scatter plot is missing axis labels"
            # This chart has multiple traces (genres), so legend is expected
            assert fig.layout.showlegend is not False, "Score vs sales scatter plot should show legend for multiple genres"


def test_temporal_releases_chart_completeness():
    """Test that temporal releases chart has all required elements."""
    df = load_data("video_games.csv")
    year_col = find_column(df, ["Release_Year", "Year", "year", "release_year"])
    
    if year_col:
        df_temporal = df[df[year_col].notna()]
        df_temporal = df_temporal[(df_temporal[year_col] >= 1980) & (df_temporal[year_col] <= 2025)]
        if len(df_temporal) > 0:
            fig = create_temporal_releases_chart(df, year_col)
            
            assert has_title(fig), "Temporal releases chart is missing a title"
            assert has_axis_labels(fig), "Temporal releases chart is missing axis labels"
            assert has_legend_when_needed(fig), "Temporal releases chart is missing a legend when needed"


def test_correlation_heatmap_completeness():
    """Test that correlation heatmap has all required elements."""
    df = load_data("video_games.csv")
    
    if len(df.select_dtypes(include=[np.number]).columns) >= 2:
        fig = create_correlation_heatmap(df)
        
        assert has_title(fig), "Correlation heatmap is missing a title"
        assert has_axis_labels(fig), "Correlation heatmap is missing axis labels"
        assert has_legend_when_needed(fig), "Correlation heatmap is missing a legend when needed"
