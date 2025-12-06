"""
Visual Theme Module for Data Storytelling Dashboard

This module centralizes all visual styling including color palettes,
typography, and theme configurations for Plotly and Matplotlib.
"""

import streamlit as st
import plotly.graph_objects as go
import matplotlib.pyplot as plt


class VisualTheme:
    """Manages color schemes, fonts, and styling across the application."""
    
    # Gaming-inspired color palette
    PRIMARY_COLORS = [
        '#8B5CF6',  # Vibrant Purple
        '#3B82F6',  # Electric Blue
        '#10B981',  # Emerald Green
        '#F59E0B',  # Amber Orange
        '#EF4444',  # Red
        '#EC4899',  # Pink
        '#06B6D4',  # Cyan
        '#8B5CF6',  # Purple (repeat for cycling)
    ]
    
    # Accent colors for highlights
    ACCENT_COLORS = [
        '#A78BFA',  # Light Purple
        '#60A5FA',  # Light Blue
        '#34D399',  # Light Green
        '#FBBF24',  # Light Amber
    ]
    
    # Background and text colors
    BACKGROUND_COLOR = '#0F172A'  # Dark slate
    CARD_BACKGROUND = '#1E293B'   # Lighter slate
    TEXT_PRIMARY = '#F1F5F9'      # Light gray
    TEXT_SECONDARY = '#94A3B8'    # Medium gray
    
    # Chart-specific colors
    GRID_COLOR = '#334155'
    LINE_COLOR = '#475569'
    
    @staticmethod
    def get_color_for_category(category: str, all_categories: list) -> str:
        """
        Get consistent color for a category across visualizations.
        
        Args:
            category: The category name
            all_categories: List of all categories (for consistent indexing)
            
        Returns:
            Hex color code
        """
        try:
            index = all_categories.index(category)
            return VisualTheme.PRIMARY_COLORS[index % len(VisualTheme.PRIMARY_COLORS)]
        except ValueError:
            return VisualTheme.PRIMARY_COLORS[0]
    
    @staticmethod
    def apply_plotly_theme(fig: go.Figure) -> go.Figure:
        """
        Apply consistent dark theme to Plotly figures.
        
        Args:
            fig: Plotly figure object
            
        Returns:
            Styled figure object
        """
        fig.update_layout(
            paper_bgcolor=VisualTheme.CARD_BACKGROUND,
            plot_bgcolor=VisualTheme.CARD_BACKGROUND,
            font=dict(
                color=VisualTheme.TEXT_PRIMARY,
                family='Arial, sans-serif',
                size=12
            ),
            title=dict(
                font=dict(
                    size=24,
                    color=VisualTheme.TEXT_PRIMARY
                )
            ),
            xaxis=dict(
                gridcolor=VisualTheme.GRID_COLOR,
                linecolor=VisualTheme.LINE_COLOR,
                color=VisualTheme.TEXT_PRIMARY
            ),
            yaxis=dict(
                gridcolor=VisualTheme.GRID_COLOR,
                linecolor=VisualTheme.LINE_COLOR,
                color=VisualTheme.TEXT_PRIMARY
            ),
            legend=dict(
                bgcolor=VisualTheme.CARD_BACKGROUND,
                bordercolor=VisualTheme.LINE_COLOR,
                font=dict(color=VisualTheme.TEXT_PRIMARY)
            ),
            hovermode='closest',
            hoverlabel=dict(
                bgcolor=VisualTheme.CARD_BACKGROUND,
                font_size=12,
                font_family='Arial, sans-serif'
            )
        )
        return fig
    
    @staticmethod
    def apply_matplotlib_theme() -> None:
        """Set matplotlib rcParams for consistent dark theme styling."""
        plt.style.use('dark_background')
        plt.rcParams.update({
            'figure.facecolor': VisualTheme.CARD_BACKGROUND,
            'axes.facecolor': VisualTheme.CARD_BACKGROUND,
            'axes.edgecolor': VisualTheme.LINE_COLOR,
            'axes.labelcolor': VisualTheme.TEXT_PRIMARY,
            'text.color': VisualTheme.TEXT_PRIMARY,
            'xtick.color': VisualTheme.TEXT_SECONDARY,
            'ytick.color': VisualTheme.TEXT_SECONDARY,
            'grid.color': VisualTheme.GRID_COLOR,
            'grid.alpha': 0.3,
            'legend.facecolor': VisualTheme.CARD_BACKGROUND,
            'legend.edgecolor': VisualTheme.LINE_COLOR,
            'font.size': 10,
        })
    
    @staticmethod
    def inject_custom_css() -> None:
        """Inject custom CSS for enhanced Streamlit component styling."""
        st.markdown("""
        <style>
        /* Main container with gradient background */
        .main {
            background: linear-gradient(135deg, #0F172A 0%, #1E293B 100%);
        }
        
        /* Headers */
        h1 {
            color: #8B5CF6;
            font-weight: 700;
            text-align: center;
            margin-bottom: 2rem;
            font-size: 3rem;
        }
        
        h2 {
            color: #F1F5F9;
            font-weight: 600;
            border-bottom: 3px solid #8B5CF6;
            padding-bottom: 0.5rem;
            margin-top: 2rem;
            margin-bottom: 1rem;
        }
        
        h3 {
            color: #F1F5F9;
            font-weight: 600;
            margin-top: 1.5rem;
        }
        
        /* Story section cards */
        .story-card {
            background: #1E293B;
            border-radius: 12px;
            padding: 2rem;
            margin: 1rem 0;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
        }
        
        /* Metrics display */
        .metric-card {
            background: linear-gradient(135deg, #8B5CF6 0%, #3B82F6 100%);
            border-radius: 8px;
            padding: 1.5rem;
            text-align: center;
            color: white;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.2);
        }
        
        .metric-value {
            font-size: 2.5rem;
            font-weight: 700;
            margin: 0.5rem 0;
        }
        
        .metric-label {
            font-size: 1rem;
            opacity: 0.9;
            text-transform: uppercase;
            letter-spacing: 1px;
        }
        
        /* Tab styling */
        .stTabs [data-baseweb="tab-list"] {
            gap: 8px;
            background-color: transparent;
        }
        
        .stTabs [data-baseweb="tab"] {
            background-color: #1E293B;
            border-radius: 8px 8px 0 0;
            color: #94A3B8;
            font-weight: 600;
            padding: 12px 24px;
            border: none;
        }
        
        .stTabs [aria-selected="true"] {
            background-color: #8B5CF6;
            color: white;
        }
        
        /* Dataframe styling */
        .dataframe {
            background-color: #1E293B;
            color: #F1F5F9;
        }
        
        /* Info boxes */
        .stAlert {
            background-color: #1E293B;
            border-left: 4px solid #8B5CF6;
        }
        
        /* Buttons */
        .stButton > button {
            background: linear-gradient(135deg, #8B5CF6 0%, #3B82F6 100%);
            color: white;
            border: none;
            border-radius: 8px;
            padding: 0.5rem 2rem;
            font-weight: 600;
            transition: transform 0.2s;
        }
        
        .stButton > button:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(139, 92, 246, 0.4);
        }
        
        /* Markdown text */
        .markdown-text-container {
            color: #F1F5F9;
        }
        
        /* Selectbox and input styling */
        .stSelectbox, .stTextInput {
            color: #F1F5F9;
        }
        
        /* File uploader */
        .stFileUploader {
            background-color: #1E293B;
            border-radius: 8px;
            padding: 1rem;
        }
        </style>
        """, unsafe_allow_html=True)
    
    @staticmethod
    def create_metric_card_html(value: str, label: str) -> str:
        """
        Create HTML for a styled metric card.
        
        Args:
            value: The metric value to display
            label: The metric label
            
        Returns:
            HTML string for the metric card
        """
        return f"""
        <div class="metric-card">
            <div class="metric-value">{value}</div>
            <div class="metric-label">{label}</div>
        </div>
        """
