# Design Document

## Overview

This design transforms the current interactive video games dashboard into a visually impactful data storytelling application. The application will automatically load the CORGIS video games dataset and present a curated narrative through carefully designed visualizations that reveal insights about the gaming industry. The focus is on creating a compelling visual experience that guides users through a data-driven story without requiring any manual interaction.

## Architecture

### Application Structure

The application follows a **narrative-driven single-page architecture** with the following layers:

1. **Data Layer**: Automatic CSV loading and preprocessing
2. **Story Layer**: Narrative structure with themed sections
3. **Visualization Layer**: High-impact charts and graphs
4. **Presentation Layer**: Streamlit UI with enhanced visual design

### Data Flow

```
video_games.csv → Auto-load → Data Cleaning → Column Normalization → Story Sections → Visualizations → User Display
```

### Technology Stack

- **Streamlit**: Web framework with custom CSS for enhanced visuals
- **Plotly**: Primary visualization library for interactive, polished charts
- **Seaborn**: Statistical visualizations with custom color palettes
- **Matplotlib**: Base plotting with custom styling
- **Pandas**: Data manipulation and aggregation

## Components and Interfaces

### 1. Data Loader Component

**Purpose**: Automatically load and prepare the dataset

**Interface**:
```python
def load_data() -> pd.DataFrame:
    """
    Load video_games.csv from project directory.
    Returns: Cleaned DataFrame with normalized columns
    Raises: FileNotFoundError with helpful message
    """
```

**Responsibilities**:
- Load CSV from relative path
- Normalize column names (replace dots/spaces with underscores)
- Handle missing file gracefully
- Return prepared DataFrame

### 2. Story Section Component

**Purpose**: Encapsulate themed narrative sections

**Interface**:
```python
def render_story_section(
    title: str,
    description: str,
    visualizations: List[Callable],
    layout: str = "single"
) -> None:
    """
    Render a story section with title, context, and visualizations.
    
    Args:
        title: Section heading
        description: Narrative context
        visualizations: List of visualization functions
        layout: "single", "columns", or "grid"
    """
```

**Story Sections**:
1. **Introducción**: Welcome and dataset overview
2. **El Mercado**: Sales analysis by genre and platform
3. **Calidad vs Popularidad**: Review scores and their relationship to sales
4. **Evolución Temporal**: Industry trends over time
5. **Experiencia del Jugador**: Game length and completion metrics
6. **Conexiones Ocultas**: Correlation analysis

### 3. Visualization Components

Each visualization component follows this pattern:

```python
def create_visualization_name(df: pd.DataFrame, **kwargs) -> plotly/matplotlib figure:
    """
    Create specific visualization with enhanced styling.
    
    Args:
        df: Source DataFrame
        **kwargs: Customization options
    
    Returns:
        Styled figure object
    """
```

**Key Visualizations**:
- `create_sales_by_genre_chart()`: Horizontal bar chart with gradient colors
- `create_platform_comparison()`: Grouped bar chart with annotations
- `create_score_sales_scatter()`: Scatter plot with trend line and color by genre
- `create_temporal_trends()`: Area chart showing releases and sales over time
- `create_genre_scores_violin()`: Violin plot for score distributions
- `create_completion_time_distribution()`: Histogram with KDE overlay
- `create_correlation_heatmap()`: Annotated heatmap with custom colormap

### 4. Visual Theme Manager

**Purpose**: Centralize visual styling for consistency and impact

**Interface**:
```python
class VisualTheme:
    """Manages color schemes, fonts, and styling across the application."""
    
    PRIMARY_COLORS: List[str]  # Main color palette
    ACCENT_COLORS: List[str]   # Highlight colors
    BACKGROUND_COLOR: str      # Page background
    TEXT_COLOR: str            # Primary text
    
    @staticmethod
    def apply_plotly_theme(fig) -> fig:
        """Apply consistent theme to Plotly figures"""
    
    @staticmethod
    def apply_matplotlib_theme() -> None:
        """Set matplotlib rcParams for consistent styling"""
    
    @staticmethod
    def inject_custom_css() -> None:
        """Inject custom CSS for Streamlit components"""
```

**Visual Design Principles**:
- **Color Palette**: Vibrant gaming-inspired colors (purples, blues, oranges)
- **Typography**: Bold headers, readable body text, proper hierarchy
- **Spacing**: Generous whitespace between sections
- **Contrast**: High contrast for readability
- **Animation**: Subtle transitions in Plotly charts

## Data Models

### DataFrame Schema (After Normalization)

```python
{
    'Title': str,
    'Features_Handheld': bool,
    'Features_Max_Players': int,
    'Features_Multiplatform': bool,
    'Features_Online': bool,
    'Metadata_Genres': str,  # Comma-separated
    'Metadata_Licensed': bool,
    'Metadata_Publishers': str,
    'Metadata_Sequel': bool,
    'Metrics_Review_Score': float,
    'Metrics_Sales': float,  # In millions
    'Metrics_Used_Price': float,
    'Release_Console': str,
    'Release_Rating': str,  # ESRB rating
    'Release_Re_release': bool,
    'Release_Year': int,
    'Length_Main_Story_Average': float,  # Hours
    # ... additional length metrics
}
```

### Aggregated Data Structures

**Sales by Genre**:
```python
{
    'genre': str,
    'total_sales': float,
    'avg_score': float,
    'game_count': int
}
```

**Temporal Trends**:
```python
{
    'year': int,
    'releases': int,
    'total_sales': float,
    'avg_score': float
}
```

## Correctness Properties

*A property is a characteristic or behavior that should hold true across all valid executions of a system—essentially, a formal statement about what the system should do. Properties serve as the bridge between human-readable specifications and machine-verifiable correctness guarantees.*

### Property 1: Automatic Data Loading

*For any* execution of the application, the video_games.csv file should be loaded automatically without user interaction, producing a valid DataFrame.

**Validates: Requirements 1.1**

### Property 2: Column Name Normalization

*For any* column name in the original CSV containing dots or spaces, after normalization those characters should be replaced with underscores.

**Validates: Requirements 1.4**

### Property 3: Welcome Message Accuracy

*For any* successful data load, the welcome message should display the correct count of games matching the actual number of rows in the loaded DataFrame.

**Validates: Requirements 1.3**

### Property 4: Dataset Statistics Calculation

*For any* loaded dataset, the calculated statistics (total games, year range, platform count) should accurately reflect the actual data values.

**Validates: Requirements 2.2**

### Property 5: Story Section Structure

*For any* story section rendered, it must include both a descriptive title and contextual explanation text.

**Validates: Requirements 3.2**

### Property 6: Sales Ranking Correctness

*For any* sales by genre visualization, the genres should be ordered by total sales in descending order (highest to lowest).

**Validates: Requirements 4.1**

### Property 7: Top Performer Identification

*For any* sales visualization, the top N performers (by sales volume) should be identifiable through visual emphasis or annotations.

**Validates: Requirements 4.3**

### Property 8: Score Aggregation Accuracy

*For any* genre, the average review score displayed should equal the mean of all review scores for games in that genre.

**Validates: Requirements 5.2**

### Property 9: Missing Data Handling

*For any* visualization function receiving data with missing values, the function should complete execution without raising exceptions.

**Validates: Requirements 5.5, 7.3**

### Property 10: Temporal Data Filtering

*For any* temporal visualization, all displayed year values should be within a valid range (1980-2025), with invalid years filtered out.

**Validates: Requirements 6.5**

### Property 11: Correlation Matrix Properties

*For any* correlation heatmap, the matrix should be symmetric (correlation of A to B equals B to A) and contain only numeric columns.

**Validates: Requirements 8.1, 8.3**

### Property 12: Correlation Highlighting

*For any* correlation value with absolute value above a threshold (e.g., 0.7), it should be visually highlighted in the heatmap.

**Validates: Requirements 8.2**

### Property 13: Tab Labeling Consistency

*For any* tab in the navigation, the tab label should correspond to its story section theme.

**Validates: Requirements 9.2**

### Property 14: Color Scheme Consistency

*For any* categorical variable (e.g., genre) displayed across multiple visualizations, the same category should use the same color in all charts.

**Validates: Requirements 10.1**

### Property 15: Chart Completeness

*For any* chart rendered, it must include a title, axis labels (where applicable), and a legend (when showing multiple categories).

**Validates: Requirements 10.2**

### Property 16: Spanish Language Compliance

*For any* text element in the UI (titles, labels, descriptions, axis labels), the text should be in Spanish.

**Validates: Requirements 10.5**

## Error Handling

### File Loading Errors

**Scenario**: video_games.csv not found

**Handling**:
```python
try:
    df = pd.read_csv('video_games.csv')
except FileNotFoundError:
    st.error("❌ No se encontró el archivo video_games.csv")
    st.info("Por favor, asegúrate de que el archivo esté en el directorio del proyecto.")
    st.stop()
```

### Data Quality Issues

**Scenario**: Missing or invalid data in visualizations

**Handling**:
- Filter out null values before aggregation
- Use `dropna()` for critical columns
- Display data availability warnings when appropriate
- Provide fallback visualizations for sparse data

### Visualization Errors

**Scenario**: Insufficient data for a specific chart

**Handling**:
```python
if len(filtered_data) < MIN_DATA_POINTS:
    st.warning("⚠️ Datos insuficientes para esta visualización")
    return None
```

## Testing Strategy

### Unit Testing

**Framework**: pytest

**Test Coverage**:
1. **Data Loading Tests**
   - Test successful CSV loading
   - Test file not found handling
   - Test column normalization

2. **Data Processing Tests**
   - Test aggregation functions
   - Test filtering logic
   - Test null handling

3. **Visualization Tests**
   - Test figure creation with valid data
   - Test handling of edge cases (empty data, single row)
   - Test color theme application

**Example Unit Test**:
```python
def test_column_normalization():
    """Test that column names are properly normalized"""
    original_cols = ["Metrics.Sales", "Release Year", "Title"]
    df = pd.DataFrame(columns=original_cols)
    normalized_df = normalize_columns(df)
    
    assert "Metrics_Sales" in normalized_df.columns
    assert "Release_Year" in normalized_df.columns
    assert "Title" in normalized_df.columns
```

### Property-Based Testing

**Framework**: Hypothesis (Python property-based testing library)

**Configuration**: Minimum 100 iterations per property test

**Property Tests**:

1. **Test Property 1: Data Loading Consistency**
   ```python
   @given(st.nothing())  # No random input needed
   def test_data_loading_consistency():
       """**Feature: data-storytelling-dashboard, Property 1: Data Loading Consistency**"""
       df1 = load_data()
       df2 = load_data()
       assert len(df1) == len(df2)
       assert list(df1.columns) == list(df2.columns)
   ```

2. **Test Property 2: Column Name Normalization**
   ```python
   @given(st.text(min_size=1))
   def test_column_normalization(column_name):
       """**Feature: data-storytelling-dashboard, Property 2: Column Name Normalization**"""
       normalized = normalize_column_name(column_name)
       assert '.' not in normalized
       assert ' ' not in normalized
       assert all(c.isalnum() or c == '_' for c in normalized)
   ```

3. **Test Property 4: Sales Aggregation Accuracy**
   ```python
   @given(st.data())
   def test_sales_aggregation_accuracy(data):
       """**Feature: data-storytelling-dashboard, Property 4: Sales Aggregation Accuracy**"""
       df = load_data()
       total_sales = df['Metrics_Sales'].sum()
       
       # Test genre aggregation
       genre_sales = df.groupby('Metadata_Genres')['Metrics_Sales'].sum()
       assert abs(genre_sales.sum() - total_sales) < 0.01  # Allow floating point tolerance
   ```

4. **Test Property 6: Correlation Matrix Symmetry**
   ```python
   def test_correlation_matrix_symmetry():
       """**Feature: data-storytelling-dashboard, Property 6: Correlation Matrix Symmetry**"""
       df = load_data()
       numeric_df = df.select_dtypes(include=[np.number])
       corr_matrix = numeric_df.corr()
       
       # Check symmetry
       assert np.allclose(corr_matrix, corr_matrix.T)
   ```

### Integration Testing

**Scope**: End-to-end story section rendering

**Tests**:
1. Test complete application load without errors
2. Test all story sections render successfully
3. Test navigation between sections
4. Test visual theme consistency across sections

### Visual Regression Testing

**Approach**: Manual review of visualizations

**Checklist**:
- [ ] All charts have proper titles and labels
- [ ] Color schemes are consistent
- [ ] Text is readable and properly sized
- [ ] Layouts are balanced and professional
- [ ] Spanish language is correct throughout

## Visual Design Specifications

### Color Palette

**Primary Colors** (Gaming-inspired):
```python
PRIMARY_PALETTE = [
    '#8B5CF6',  # Vibrant Purple
    '#3B82F6',  # Electric Blue
    '#10B981',  # Emerald Green
    '#F59E0B',  # Amber Orange
    '#EF4444',  # Red
    '#EC4899',  # Pink
]
```

**Background & Text**:
```python
BACKGROUND = '#0F172A'  # Dark slate
CARD_BACKGROUND = '#1E293B'  # Lighter slate
TEXT_PRIMARY = '#F1F5F9'  # Light gray
TEXT_SECONDARY = '#94A3B8'  # Medium gray
```

### Typography

**Headers**:
- H1: 48px, Bold, Primary color
- H2: 36px, Bold, White
- H3: 24px, Semi-bold, White

**Body**:
- Regular: 16px, Normal, Light gray
- Small: 14px, Normal, Medium gray

### Custom CSS Injection

```python
def inject_custom_css():
    st.markdown("""
    <style>
    /* Main container */
    .main {
        background: linear-gradient(135deg, #0F172A 0%, #1E293B 100%);
    }
    
    /* Headers */
    h1 {
        color: #8B5CF6;
        font-weight: 700;
        text-align: center;
        margin-bottom: 2rem;
    }
    
    h2 {
        color: #F1F5F9;
        font-weight: 600;
        border-bottom: 3px solid #8B5CF6;
        padding-bottom: 0.5rem;
        margin-top: 2rem;
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
    }
    
    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    
    .stTabs [data-baseweb="tab"] {
        background-color: #1E293B;
        border-radius: 8px 8px 0 0;
        color: #94A3B8;
        font-weight: 600;
    }
    
    .stTabs [aria-selected="true"] {
        background-color: #8B5CF6;
        color: white;
    }
    </style>
    """, unsafe_allow_html=True)
```

### Chart Styling

**Plotly Theme**:
```python
PLOTLY_THEME = {
    'layout': {
        'paper_bgcolor': '#1E293B',
        'plot_bgcolor': '#1E293B',
        'font': {'color': '#F1F5F9', 'family': 'Arial, sans-serif'},
        'title': {'font': {'size': 24, 'color': '#F1F5F9'}},
        'xaxis': {
            'gridcolor': '#334155',
            'linecolor': '#475569',
        },
        'yaxis': {
            'gridcolor': '#334155',
            'linecolor': '#475569',
        },
    }
}
```

**Matplotlib Theme**:
```python
plt.style.use('dark_background')
plt.rcParams.update({
    'figure.facecolor': '#1E293B',
    'axes.facecolor': '#1E293B',
    'axes.edgecolor': '#475569',
    'axes.labelcolor': '#F1F5F9',
    'text.color': '#F1F5F9',
    'xtick.color': '#94A3B8',
    'ytick.color': '#94A3B8',
    'grid.color': '#334155',
    'grid.alpha': 0.3,
})
```

## Implementation Notes

### Performance Considerations

- Cache data loading with `@st.cache_data`
- Pre-compute aggregations for faster rendering
- Use Plotly for large datasets (better performance than matplotlib)
- Lazy-load visualizations in tabs

### Accessibility

- Ensure sufficient color contrast (WCAG AA minimum)
- Provide alt text for visualizations
- Use semantic HTML structure
- Ensure keyboard navigation works

### Responsive Design

- Use Streamlit's responsive column system
- Set appropriate figure sizes for different screen widths
- Test on mobile devices (though primarily desktop-focused)

### Narrative Flow

The story should follow this arc:

1. **Hook**: Impressive overview statistics
2. **Context**: What the dataset contains
3. **Discovery**: Sales and market insights
4. **Depth**: Quality vs popularity analysis
5. **Timeline**: Historical perspective
6. **Engagement**: Player behavior patterns
7. **Revelation**: Hidden correlations
8. **Conclusion**: Key takeaways

Each section should:
- Start with a question or statement
- Present visualizations that answer it
- Provide interpretation and insights
- Transition smoothly to the next section
