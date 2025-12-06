# Implementation Plan

- [x] 1. Set up project structure and visual theme system





  - Create visual theme module with color palettes and styling constants
  - Implement CSS injection function for custom Streamlit styling
  - Configure Plotly and Matplotlib themes for consistent dark mode aesthetics
  - Update requirements.txt with all necessary dependencies
  - _Requirements: 10.1, 10.2_

- [x] 1.1 Write property test for color consistency


  - **Property 14: Color Scheme Consistency**
  - **Validates: Requirements 10.1**

- [x] 2. Implement automatic data loading and preprocessing





  - Create data loader function that reads video_games.csv from project directory
  - Implement column name normalization (replace dots and spaces with underscores)
  - Add error handling for missing file with user-friendly Spanish error messages
  - Add data validation to ensure required columns exist
  - _Requirements: 1.1, 1.2, 1.4_

- [x] 2.1 Write property test for automatic data loading


  - **Property 1: Automatic Data Loading**
  - **Validates: Requirements 1.1**

- [x] 2.2 Write property test for column normalization


  - **Property 2: Column Name Normalization**
  - **Validates: Requirements 1.4**

- [x] 2.3 Write unit test for file not found error handling

  - Test that appropriate error message displays when CSV is missing
  - _Requirements: 1.2_

- [x] 3. Create introduction section with dataset overview





  - Implement welcome header with emoji and engaging Spanish title
  - Calculate and display key statistics (total games, year range, platform count)
  - Create metric cards with gradient backgrounds for visual impact
  - Display sample data preview in styled container
  - _Requirements: 1.3, 2.1, 2.2, 2.4_

- [x] 3.1 Write property test for welcome message accuracy


  - **Property 3: Welcome Message Accuracy**
  - **Validates: Requirements 1.3**

- [x] 3.2 Write property test for dataset statistics


  - **Property 4: Dataset Statistics Calculation**
  - **Validates: Requirements 2.2**

- [x] 4. Build "El Mercado" section - Sales analysis





  - Create horizontal bar chart for sales by genre with gradient colors
  - Implement platform comparison visualization with annotations
  - Add top performer highlighting with color emphasis
  - Include narrative text explaining sales patterns in Spanish
  - Use Plotly for interactive charts with hover details
  - _Requirements: 4.1, 4.2, 4.3, 4.5_

- [x] 4.1 Write property test for sales ranking


  - **Property 6: Sales Ranking Correctness**
  - **Validates: Requirements 4.1**

- [x] 4.2 Write property test for top performer identification


  - **Property 7: Top Performer Identification**
  - **Validates: Requirements 4.3**

- [x] 5. Build "Calidad vs Popularidad" section - Review scores analysis





  - Create scatter plot showing review scores vs sales with trend line
  - Implement violin plot for score distributions across genres
  - Add color coding by genre for pattern recognition
  - Handle missing score data gracefully with filtering
  - Include narrative interpretation in Spanish
  - _Requirements: 5.1, 5.2, 5.3, 5.5_

- [x] 5.1 Write property test for score aggregation


  - **Property 8: Score Aggregation Accuracy**
  - **Validates: Requirements 5.2**

- [x] 5.2 Write property test for missing data handling

  - **Property 9: Missing Data Handling**
  - **Validates: Requirements 5.5, 7.3**

- [x] 6. Build "Evolución Temporal" section - Time series analysis







  - Create area chart showing game releases over time
  - Implement line chart for sales trends by year
  - Filter out invalid year data (outside 1980-2025 range)
  - Add annotations for significant periods
  - Include narrative highlighting industry evolution in Spanish
  - _Requirements: 6.1, 6.2, 6.3, 6.5_

- [x] 6.1 Write property test for temporal data filtering


  - **Property 10: Temporal Data Filtering**
  - **Validates: Requirements 6.5**

- [x] 7. Build "Experiencia del Jugador" section - Game length analysis





  - Create histogram with KDE overlay for main story completion times
  - Implement box plot comparing completion times across genres
  - Handle zero and missing length data appropriately
  - Use color palette consistent with other sections
  - Add narrative explaining length-genre relationships in Spanish
  - _Requirements: 7.1, 7.2, 7.3, 7.5_

- [x] 8. Build "Conexiones Ocultas" section - Correlation analysis





  - Create correlation heatmap for numeric variables only
  - Implement diverging color scheme (red-white-blue)
  - Add annotations for correlation values
  - Highlight strong correlations (|r| > 0.7) with bold text
  - Include narrative interpretation of key correlations in Spanish
  - _Requirements: 8.1, 8.2, 8.3, 8.5_

- [x] 8.1 Write property test for correlation matrix properties


  - **Property 11: Correlation Matrix Properties**
  - **Validates: Requirements 8.1, 8.3**

- [x] 8.2 Write property test for correlation highlighting


  - **Property 12: Correlation Highlighting**
  - **Validates: Requirements 8.2**

- [x] 9. Implement navigation and layout structure





  - Set up Streamlit tabs for story sections with Spanish labels
  - Configure wide layout mode for maximum visualization space
  - Ensure consistent spacing and padding across sections
  - Add smooth transitions between tabs
  - _Requirements: 9.1, 9.2, 9.4_

- [x] 9.1 Write property test for tab labeling


  - **Property 13: Tab Labeling Consistency**
  - **Validates: Requirements 9.2**

- [x] 9.2 Write property test for story section structure



  - **Property 5: Story Section Structure**
  - **Validates: Requirements 3.2**

- [x] 10. Polish visualizations and ensure completeness





  - Add proper titles to all charts in Spanish
  - Ensure all axes have clear labels in Spanish
  - Add legends where multiple categories are shown
  - Verify color consistency across related visualizations
  - Test all charts with actual dataset
  - _Requirements: 10.2, 10.5_

- [x] 10.1 Write property test for chart completeness


  - **Property 15: Chart Completeness**
  - **Validates: Requirements 10.2**

- [x] 10.2 Write property test for Spanish language compliance


  - **Property 16: Spanish Language Compliance**
  - **Validates: Requirements 10.5**

- [x] 11. Final integration and testing





  - Integrate all sections into main app.py
  - Test complete narrative flow from introduction to conclusion
  - Verify all visualizations render correctly
  - Check responsive behavior with different window sizes
  - Ensure all text is in Spanish with proper accents
  - _Requirements: 3.3, 9.3, 10.3, 10.4_


- [x] 12. Checkpoint - Ensure all tests pass




  - Ensure all tests pass, ask the user if questions arise.
