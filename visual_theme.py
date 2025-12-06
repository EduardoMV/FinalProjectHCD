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
    
    # Epic gaming-inspired neon color palette
    PRIMARY_COLORS = [
        '#00ffff',  # Neon Cyan
        '#ff00ff',  # Neon Magenta
        '#00ff88',  # Neon Green
        '#ffff00',  # Neon Yellow
        '#ff0080',  # Hot Pink
        '#0099ff',  # Electric Blue
        '#ff6600',  # Neon Orange
        '#00ffff',  # Neon Cyan (repeat for cycling)
    ]
    
    # Accent colors for highlights and glow effects
    ACCENT_COLORS = [
        '#a78bfa',  # Soft Purple
        '#60a5fa',  # Soft Blue
        '#34d399',  # Soft Green
        '#fbbf24',  # Soft Amber
        '#f472b6',  # Soft Pink
        '#38bdf8',  # Soft Cyan
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
        """Inject custom CSS for enhanced Streamlit component styling with gaming aesthetics."""
        st.markdown("""
        <style>
        /* Import gaming font */
        @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;500;700;900&family=Rajdhani:wght@300;400;500;600;700&display=swap');
        
        /* Hide Streamlit branding */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        
        /* Main container with animated gradient background */
        .main {
            background: linear-gradient(135deg, #0a0e27 0%, #1a1f3a 50%, #0f1419 100%);
            background-size: 400% 400%;
            animation: gradientShift 15s ease infinite;
        }
        
        @keyframes gradientShift {
            0% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
            100% { background-position: 0% 50%; }
        }
        
        /* Neon glow effect for headers */
        h1 {
            font-family: 'Orbitron', sans-serif;
            color: #00ffff;
            font-weight: 900;
            text-align: center;
            margin-bottom: 2rem;
            font-size: 3.5rem;
            text-shadow: 
                0 0 10px #00ffff,
                0 0 20px #00ffff,
                0 0 30px #00ffff,
                0 0 40px #0099ff,
                0 0 70px #0099ff,
                0 0 80px #0099ff,
                0 0 100px #0099ff;
            animation: neonPulse 2s ease-in-out infinite alternate;
            letter-spacing: 3px;
        }
        
        @keyframes neonPulse {
            from {
                text-shadow: 
                    0 0 10px #00ffff,
                    0 0 20px #00ffff,
                    0 0 30px #00ffff,
                    0 0 40px #0099ff,
                    0 0 70px #0099ff;
            }
            to {
                text-shadow: 
                    0 0 20px #00ffff,
                    0 0 30px #00ffff,
                    0 0 40px #00ffff,
                    0 0 50px #0099ff,
                    0 0 80px #0099ff,
                    0 0 90px #0099ff,
                    0 0 120px #0099ff;
            }
        }
        
        h2 {
            font-family: 'Orbitron', sans-serif;
            color: #ff00ff;
            font-weight: 700;
            border-bottom: 3px solid #ff00ff;
            padding-bottom: 0.5rem;
            margin-top: 2rem;
            margin-bottom: 1rem;
            text-shadow: 0 0 10px #ff00ff, 0 0 20px #ff00ff;
            letter-spacing: 2px;
        }
        
        h3 {
            font-family: 'Rajdhani', sans-serif;
            color: #00ff88;
            font-weight: 700;
            margin-top: 1.5rem;
            text-shadow: 0 0 5px #00ff88;
            letter-spacing: 1px;
        }
        
        /* Story section cards with neon borders */
        .story-card {
            background: rgba(30, 41, 59, 0.8);
            border-radius: 15px;
            padding: 2rem;
            margin: 1rem 0;
            box-shadow: 
                0 0 20px rgba(0, 255, 255, 0.3),
                0 4px 6px rgba(0, 0, 0, 0.5);
            border: 2px solid rgba(0, 255, 255, 0.3);
            backdrop-filter: blur(10px);
            transition: all 0.3s ease;
        }
        
        .story-card:hover {
            box-shadow: 
                0 0 30px rgba(0, 255, 255, 0.5),
                0 8px 12px rgba(0, 0, 0, 0.6);
            border-color: rgba(0, 255, 255, 0.6);
            transform: translateY(-5px);
        }
        
        /* Metrics display with gaming style */
        .metric-card {
            background: linear-gradient(135deg, 
                rgba(139, 92, 246, 0.2) 0%, 
                rgba(59, 130, 246, 0.2) 100%);
            border: 2px solid #8B5CF6;
            border-radius: 12px;
            padding: 1.5rem;
            text-align: center;
            color: white;
            box-shadow: 
                0 0 20px rgba(139, 92, 246, 0.4),
                inset 0 0 20px rgba(139, 92, 246, 0.1);
            backdrop-filter: blur(10px);
            transition: all 0.3s ease;
            position: relative;
            overflow: hidden;
        }
        
        .metric-card::before {
            content: '';
            position: absolute;
            top: -50%;
            left: -50%;
            width: 200%;
            height: 200%;
            background: linear-gradient(
                45deg,
                transparent,
                rgba(255, 255, 255, 0.1),
                transparent
            );
            transform: rotate(45deg);
            animation: shine 3s infinite;
        }
        
        @keyframes shine {
            0% { transform: translateX(-100%) translateY(-100%) rotate(45deg); }
            100% { transform: translateX(100%) translateY(100%) rotate(45deg); }
        }
        
        .metric-card:hover {
            transform: scale(1.05);
            box-shadow: 
                0 0 30px rgba(139, 92, 246, 0.6),
                inset 0 0 30px rgba(139, 92, 246, 0.2);
        }
        
        .metric-value {
            font-family: 'Orbitron', sans-serif;
            font-size: 2.8rem;
            font-weight: 900;
            margin: 0.5rem 0;
            text-shadow: 0 0 10px rgba(139, 92, 246, 0.8);
            position: relative;
            z-index: 1;
        }
        
        .metric-label {
            font-family: 'Rajdhani', sans-serif;
            font-size: 1.1rem;
            opacity: 0.9;
            text-transform: uppercase;
            letter-spacing: 2px;
            font-weight: 600;
            position: relative;
            z-index: 1;
        }
        
        /* Tab styling with gaming aesthetic */
        .stTabs [data-baseweb="tab-list"] {
            gap: 10px;
            background-color: transparent;
            padding: 10px 0;
        }
        
        .stTabs [data-baseweb="tab"] {
            font-family: 'Rajdhani', sans-serif;
            background: rgba(30, 41, 59, 0.6);
            border-radius: 10px 10px 0 0;
            color: #94A3B8;
            font-weight: 700;
            font-size: 1.1rem;
            padding: 14px 28px;
            border: 2px solid rgba(139, 92, 246, 0.3);
            border-bottom: none;
            transition: all 0.3s ease;
            letter-spacing: 1px;
        }
        
        .stTabs [data-baseweb="tab"]:hover {
            background: rgba(139, 92, 246, 0.2);
            color: #00ffff;
            box-shadow: 0 0 15px rgba(0, 255, 255, 0.3);
        }
        
        .stTabs [aria-selected="true"] {
            background: linear-gradient(135deg, #8B5CF6 0%, #3B82F6 100%);
            color: white;
            border-color: #00ffff;
            box-shadow: 
                0 0 20px rgba(0, 255, 255, 0.5),
                0 -5px 20px rgba(139, 92, 246, 0.4);
            text-shadow: 0 0 10px rgba(255, 255, 255, 0.5);
        }
        
        /* Dataframe styling with neon borders */
        .dataframe {
            background-color: rgba(30, 41, 59, 0.8);
            color: #F1F5F9;
            border: 1px solid rgba(0, 255, 255, 0.3);
            border-radius: 8px;
        }
        
        /* Info boxes with gaming style */
        .stAlert {
            background: rgba(30, 41, 59, 0.8);
            border-left: 4px solid #00ffff;
            border-radius: 8px;
            box-shadow: 0 0 15px rgba(0, 255, 255, 0.2);
        }
        
        /* Buttons with arcade style */
        .stButton > button {
            font-family: 'Rajdhani', sans-serif;
            background: linear-gradient(135deg, #8B5CF6 0%, #3B82F6 100%);
            color: white;
            border: 2px solid #00ffff;
            border-radius: 10px;
            padding: 0.7rem 2.5rem;
            font-weight: 700;
            font-size: 1.1rem;
            letter-spacing: 1px;
            transition: all 0.3s ease;
            box-shadow: 
                0 0 15px rgba(0, 255, 255, 0.3),
                0 4px 6px rgba(0, 0, 0, 0.3);
            text-transform: uppercase;
        }
        
        .stButton > button:hover {
            transform: translateY(-3px) scale(1.05);
            box-shadow: 
                0 0 25px rgba(0, 255, 255, 0.6),
                0 8px 15px rgba(0, 0, 0, 0.4);
            background: linear-gradient(135deg, #a78bfa 0%, #60a5fa 100%);
        }
        
        .stButton > button:active {
            transform: translateY(-1px) scale(1.02);
        }
        
        /* Markdown text with gaming font */
        .markdown-text-container {
            font-family: 'Rajdhani', sans-serif;
            color: #F1F5F9;
            line-height: 1.8;
        }
        
        /* Selectbox and input styling */
        .stSelectbox, .stTextInput {
            font-family: 'Rajdhani', sans-serif;
            color: #F1F5F9;
        }
        
        /* File uploader with neon effect */
        .stFileUploader {
            background: rgba(30, 41, 59, 0.6);
            border: 2px dashed rgba(0, 255, 255, 0.4);
            border-radius: 12px;
            padding: 1.5rem;
            transition: all 0.3s ease;
        }
        
        .stFileUploader:hover {
            border-color: rgba(0, 255, 255, 0.8);
            box-shadow: 0 0 20px rgba(0, 255, 255, 0.3);
        }
        
        /* Sidebar styling */
        .css-1d391kg, [data-testid="stSidebar"] {
            background: linear-gradient(180deg, #0a0e27 0%, #1a1f3a 100%);
            border-right: 2px solid rgba(0, 255, 255, 0.3);
        }
        
        /* Scrollbar styling */
        ::-webkit-scrollbar {
            width: 10px;
            height: 10px;
        }
        
        ::-webkit-scrollbar-track {
            background: #0a0e27;
        }
        
        ::-webkit-scrollbar-thumb {
            background: linear-gradient(135deg, #8B5CF6 0%, #3B82F6 100%);
            border-radius: 5px;
            box-shadow: 0 0 10px rgba(139, 92, 246, 0.5);
        }
        
        ::-webkit-scrollbar-thumb:hover {
            background: linear-gradient(135deg, #a78bfa 0%, #60a5fa 100%);
            box-shadow: 0 0 15px rgba(139, 92, 246, 0.8);
        }
        
        /* Loading animation */
        .stSpinner > div {
            border-top-color: #00ffff !important;
            border-right-color: #8B5CF6 !important;
        }
        
        /* Expander styling */
        .streamlit-expanderHeader {
            font-family: 'Rajdhani', sans-serif;
            background: rgba(30, 41, 59, 0.6);
            border: 1px solid rgba(139, 92, 246, 0.3);
            border-radius: 8px;
            font-weight: 600;
        }
        
        .streamlit-expanderHeader:hover {
            border-color: rgba(0, 255, 255, 0.6);
            box-shadow: 0 0 15px rgba(0, 255, 255, 0.2);
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
