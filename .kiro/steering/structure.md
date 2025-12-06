# Project Structure

## Root Files

- `app.py` - Main Streamlit application with all dashboard logic
- `video_games.csv` - Sample dataset (CORGIS video games data)
- `requirements.txt` - Python dependencies (currently empty)
- `README.md` - Project documentation (currently empty)

## Folders

- `.kiro/` - Kiro AI assistant configuration and steering rules
- `.vscode/` - VS Code workspace settings
- `notebooks/` - Jupyter notebooks for analysis (contains `Sugerencias` file)

## Application Architecture

The app follows a **single-file monolithic structure**:

1. **Configuration** - Page setup and imports at top
2. **Header & File Upload** - Title and CSV uploader
3. **Data Processing** - Column name normalization and detection
4. **Tab-based UI** - Five tabs for different analysis views:
   - Introducción (Introduction)
   - Vista General (Overview)
   - Distribuciones (Distributions)
   - Comparaciones (Comparisons)
   - Correlaciones (Correlations)

## Code Conventions

- Column names are dynamically detected using helper function `find_col()`
- Spanish language used for all UI text and comments
- Streamlit layout uses columns and tabs for organization
- Matplotlib/Seaborn for static plots, Plotly for interactive charts
- Defensive coding: checks for column existence before plotting
