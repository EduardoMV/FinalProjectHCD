# Technology Stack

## Core Framework

- **Streamlit** - Main web application framework for interactive dashboards

## Data & Visualization Libraries

- **pandas** - Data manipulation and analysis
- **numpy** - Numerical operations
- **matplotlib** - Static plotting
- **seaborn** - Statistical visualizations
- **plotly.express** - Interactive charts

## Python Version

Python 3.x (specific version not specified in requirements)

## Common Commands

### Running the Application

```bash
streamlit run app.py
```

### Installing Dependencies

```bash
pip install -r requirements.txt
```

Note: `requirements.txt` currently empty - dependencies should include:
- streamlit
- pandas
- numpy
- matplotlib
- seaborn
- plotly

## Data Format

- Input: CSV file (`video_games.csv`)
- Expected columns include Title, Genre, Platform, Sales, Scores, and various game length metrics
- Column names are normalized (dots and spaces replaced with underscores)
