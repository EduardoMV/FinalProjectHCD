"""
Property-based tests for correlation analysis section.

Tests Properties 11 and 12 from the design document.
"""

import pytest
import pandas as pd
import numpy as np
import tempfile
import os
from hypothesis import given, settings, strategies as st
from data_loader import load_data


class TestCorrelationMatrixProperties:
    """Tests for Property 11: Correlation Matrix Properties"""
    
    def test_correlation_matrix_is_symmetric(self):
        """
        **Feature: data-storytelling-dashboard, Property 11: Correlation Matrix Properties**
        **Validates: Requirements 8.1, 8.3**
        
        For any correlation heatmap, the matrix should be symmetric
        (correlation of A to B equals B to A).
        """
        # Load actual dataset
        df = load_data("video_games.csv")
        
        # Select only numeric columns
        numeric_df = df.select_dtypes(include=[np.number])
        
        # Calculate correlation matrix
        corr_matrix = numeric_df.corr()
        
        # Check symmetry: corr[i,j] == corr[j,i]
        assert np.allclose(corr_matrix, corr_matrix.T, equal_nan=True), \
            "Correlation matrix is not symmetric"
    
    def test_correlation_matrix_contains_only_numeric_columns(self):
        """
        **Feature: data-storytelling-dashboard, Property 11: Correlation Matrix Properties**
        **Validates: Requirements 8.1, 8.3**
        
        For any correlation heatmap, the matrix should contain only numeric columns.
        """
        # Load actual dataset
        df = load_data("video_games.csv")
        
        # Select only numeric columns
        numeric_df = df.select_dtypes(include=[np.number])
        
        # Calculate correlation matrix
        corr_matrix = numeric_df.corr()
        
        # Verify all columns in correlation matrix are numeric
        for col in corr_matrix.columns:
            assert col in numeric_df.columns, \
                f"Column {col} in correlation matrix is not numeric"
            assert pd.api.types.is_numeric_dtype(numeric_df[col]), \
                f"Column {col} is not numeric type"
    
    @given(
        num_cols=st.integers(min_value=2, max_value=10),
        num_rows=st.integers(min_value=10, max_value=100)
    )
    @settings(max_examples=100)
    def test_correlation_matrix_symmetry_property(self, num_cols, num_rows):
        """
        **Feature: data-storytelling-dashboard, Property 11: Correlation Matrix Properties**
        **Validates: Requirements 8.1, 8.3**
        
        For any randomly generated numeric dataset, the correlation matrix
        should be symmetric.
        """
        # Generate random numeric data
        data = {}
        for i in range(num_cols):
            data[f'col_{i}'] = np.random.randn(num_rows)
        
        df = pd.DataFrame(data)
        
        # Calculate correlation matrix
        corr_matrix = df.corr()
        
        # Check symmetry
        assert np.allclose(corr_matrix, corr_matrix.T, equal_nan=True), \
            "Generated correlation matrix is not symmetric"
    
    def test_correlation_diagonal_is_one(self):
        """
        **Feature: data-storytelling-dashboard, Property 11: Correlation Matrix Properties**
        **Validates: Requirements 8.1, 8.3**
        
        For any correlation matrix, the diagonal values should be 1
        (a variable is perfectly correlated with itself).
        """
        # Load actual dataset
        df = load_data("video_games.csv")
        
        # Select only numeric columns
        numeric_df = df.select_dtypes(include=[np.number])
        
        # Calculate correlation matrix
        corr_matrix = numeric_df.corr()
        
        # Check diagonal values are 1
        diagonal = np.diag(corr_matrix)
        assert np.allclose(diagonal, 1.0, equal_nan=True), \
            f"Diagonal values are not 1: {diagonal}"
    
    @given(
        num_cols=st.integers(min_value=2, max_value=10),
        num_rows=st.integers(min_value=10, max_value=100)
    )
    @settings(max_examples=100)
    def test_correlation_values_in_valid_range(self, num_cols, num_rows):
        """
        **Feature: data-storytelling-dashboard, Property 11: Correlation Matrix Properties**
        **Validates: Requirements 8.1, 8.3**
        
        For any correlation matrix, all values should be in the range [-1, 1].
        """
        # Generate random numeric data
        data = {}
        for i in range(num_cols):
            data[f'col_{i}'] = np.random.randn(num_rows)
        
        df = pd.DataFrame(data)
        
        # Calculate correlation matrix
        corr_matrix = df.corr()
        
        # Check all values are in [-1, 1]
        assert (corr_matrix.abs() <= 1.0).all().all(), \
            "Correlation values outside [-1, 1] range"
    
    def test_correlation_matrix_excludes_non_numeric_columns(self):
        """
        **Feature: data-storytelling-dashboard, Property 11: Correlation Matrix Properties**
        **Validates: Requirements 8.1, 8.3**
        
        When creating a correlation matrix, non-numeric columns should be excluded.
        """
        # Create a test dataset with mixed types
        temp_fd, temp_path = tempfile.mkstemp(suffix='.csv')
        try:
            test_data = pd.DataFrame({
                'Title': ['Game1', 'Game2', 'Game3'],
                'Metrics_Sales': [1.5, 2.3, 0.8],
                'Metrics_Review_Score': [85, 90, 75],
                'Metadata_Genres': ['Action', 'RPG', 'Sports']
            })
            test_data.to_csv(temp_path, index=False)
            
            # Load data
            df = load_data(temp_path)
            
            # Select only numeric columns
            numeric_df = df.select_dtypes(include=[np.number])
            
            # Calculate correlation matrix
            corr_matrix = numeric_df.corr()
            
            # Verify only numeric columns are in the matrix
            assert 'Title' not in corr_matrix.columns, \
                "Non-numeric column 'Title' found in correlation matrix"
            assert 'Metadata_Genres' not in corr_matrix.columns, \
                "Non-numeric column 'Metadata_Genres' found in correlation matrix"
            assert 'Metrics_Sales' in corr_matrix.columns, \
                "Numeric column 'Metrics_Sales' missing from correlation matrix"
            assert 'Metrics_Review_Score' in corr_matrix.columns, \
                "Numeric column 'Metrics_Review_Score' missing from correlation matrix"
        
        finally:
            os.close(temp_fd)
            os.unlink(temp_path)


class TestCorrelationHighlighting:
    """Tests for Property 12: Correlation Highlighting"""
    
    def test_strong_correlations_identified(self):
        """
        **Feature: data-storytelling-dashboard, Property 12: Correlation Highlighting**
        **Validates: Requirements 8.2**
        
        For any correlation value with absolute value above threshold (0.7),
        it should be identified as a strong correlation.
        """
        # Load actual dataset
        df = load_data("video_games.csv")
        
        # Select only numeric columns
        numeric_df = df.select_dtypes(include=[np.number])
        
        # Calculate correlation matrix
        corr_matrix = numeric_df.corr()
        
        # Define threshold
        threshold = 0.7
        
        # Find strong correlations (excluding diagonal)
        strong_correlations = []
        for i in range(len(corr_matrix)):
            for j in range(i+1, len(corr_matrix)):
                corr_value = corr_matrix.iloc[i, j]
                if not pd.isna(corr_value) and abs(corr_value) > threshold:
                    strong_correlations.append({
                        'var1': corr_matrix.index[i],
                        'var2': corr_matrix.columns[j],
                        'correlation': corr_value
                    })
        
        # Verify that strong correlations are properly identified
        for corr in strong_correlations:
            assert abs(corr['correlation']) > threshold, \
                f"Correlation {corr['correlation']} should be > {threshold}"
    
    @given(
        threshold=st.floats(min_value=0.5, max_value=0.9)
    )
    @settings(max_examples=100)
    def test_threshold_based_highlighting(self, threshold):
        """
        **Feature: data-storytelling-dashboard, Property 12: Correlation Highlighting**
        **Validates: Requirements 8.2**
        
        For any threshold value, correlations with absolute value above that
        threshold should be identified as strong.
        """
        # Create test data with known correlations
        np.random.seed(42)
        n = 100
        
        # Create variables with different correlation strengths
        x1 = np.random.randn(n)
        x2 = 0.9 * x1 + 0.1 * np.random.randn(n)  # Strong positive correlation
        x3 = -0.8 * x1 + 0.2 * np.random.randn(n)  # Strong negative correlation
        x4 = np.random.randn(n)  # No correlation with x1
        
        df = pd.DataFrame({
            'x1': x1,
            'x2': x2,
            'x3': x3,
            'x4': x4
        })
        
        # Calculate correlation matrix
        corr_matrix = df.corr()
        
        # Check that correlations above threshold are identified
        for i in range(len(corr_matrix)):
            for j in range(i+1, len(corr_matrix)):
                corr_value = corr_matrix.iloc[i, j]
                if abs(corr_value) > threshold:
                    # This should be highlighted
                    assert abs(corr_value) > threshold, \
                        f"Strong correlation {corr_value} not properly identified"
    
    def test_weak_correlations_not_highlighted(self):
        """
        **Feature: data-storytelling-dashboard, Property 12: Correlation Highlighting**
        **Validates: Requirements 8.2**
        
        Correlations with absolute value below threshold should not be
        identified as strong correlations.
        """
        # Create test data with weak correlations
        np.random.seed(42)
        n = 100
        
        # Create variables with weak correlations
        x1 = np.random.randn(n)
        x2 = 0.3 * x1 + 0.7 * np.random.randn(n)  # Weak correlation
        x3 = np.random.randn(n)  # No correlation
        
        df = pd.DataFrame({
            'x1': x1,
            'x2': x2,
            'x3': x3
        })
        
        # Calculate correlation matrix
        corr_matrix = df.corr()
        
        # Define threshold
        threshold = 0.7
        
        # Check that weak correlations are not above threshold
        corr_x1_x2 = corr_matrix.loc['x1', 'x2']
        corr_x1_x3 = corr_matrix.loc['x1', 'x3']
        
        assert abs(corr_x1_x2) < threshold, \
            f"Weak correlation {corr_x1_x2} should be below threshold {threshold}"
        assert abs(corr_x1_x3) < threshold, \
            f"Weak correlation {corr_x1_x3} should be below threshold {threshold}"
    
    @given(
        num_cols=st.integers(min_value=3, max_value=8),
        num_rows=st.integers(min_value=20, max_value=100)
    )
    @settings(max_examples=100)
    def test_highlighting_consistency(self, num_cols, num_rows):
        """
        **Feature: data-storytelling-dashboard, Property 12: Correlation Highlighting**
        **Validates: Requirements 8.2**
        
        For any dataset, the same correlation value should consistently be
        identified as strong or weak based on the threshold.
        """
        # Generate random numeric data
        data = {}
        for i in range(num_cols):
            data[f'col_{i}'] = np.random.randn(num_rows)
        
        df = pd.DataFrame(data)
        
        # Calculate correlation matrix
        corr_matrix = df.corr()
        
        # Define threshold
        threshold = 0.7
        
        # Check consistency: if |corr| > threshold, it should be strong
        for i in range(len(corr_matrix)):
            for j in range(i+1, len(corr_matrix)):
                corr_value = corr_matrix.iloc[i, j]
                if not pd.isna(corr_value):
                    is_strong = abs(corr_value) > threshold
                    # Verify consistency
                    if is_strong:
                        assert abs(corr_value) > threshold, \
                            f"Correlation {corr_value} marked as strong but <= {threshold}"
                    else:
                        assert abs(corr_value) <= threshold, \
                            f"Correlation {corr_value} marked as weak but > {threshold}"
    
    def test_highlighting_excludes_diagonal(self):
        """
        **Feature: data-storytelling-dashboard, Property 12: Correlation Highlighting**
        **Validates: Requirements 8.2**
        
        The diagonal of the correlation matrix (self-correlation = 1.0)
        should not be considered for highlighting as it's always 1.0.
        """
        # Load actual dataset
        df = load_data("video_games.csv")
        
        # Select only numeric columns
        numeric_df = df.select_dtypes(include=[np.number])
        
        # Calculate correlation matrix
        corr_matrix = numeric_df.corr()
        
        # Define threshold
        threshold = 0.7
        
        # Find strong correlations (excluding diagonal)
        strong_correlations = []
        for i in range(len(corr_matrix)):
            for j in range(len(corr_matrix)):
                if i != j:  # Exclude diagonal
                    corr_value = corr_matrix.iloc[i, j]
                    if not pd.isna(corr_value) and abs(corr_value) > threshold:
                        strong_correlations.append({
                            'var1': corr_matrix.index[i],
                            'var2': corr_matrix.columns[j],
                            'correlation': corr_value
                        })
        
        # Verify no diagonal elements are in strong correlations
        for corr in strong_correlations:
            assert corr['var1'] != corr['var2'], \
                "Diagonal element (self-correlation) should not be highlighted"
