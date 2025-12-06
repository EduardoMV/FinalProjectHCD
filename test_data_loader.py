"""
Property-based and unit tests for data loading module.

Tests correctness properties related to automatic data loading,
column normalization, and error handling.
"""

import pytest
import pandas as pd
import tempfile
import os
from hypothesis import given, strategies as st, settings

from data_loader import load_data, normalize_column_name, validate_required_columns, find_column


class TestAutomaticDataLoading:
    """Tests for Property 1: Automatic Data Loading"""
    
    def test_data_loading_consistency(self):
        """
        **Feature: data-storytelling-dashboard, Property 1: Automatic Data Loading**
        **Validates: Requirements 1.1**
        
        For any execution of the application, the video_games.csv file should be
        loaded automatically without user interaction, producing a valid DataFrame.
        
        This test verifies that loading the same file multiple times produces
        consistent results.
        """
        # Load data twice
        df1 = load_data("video_games.csv")
        df2 = load_data("video_games.csv")
        
        # Should have same shape
        assert df1.shape == df2.shape, \
            f"Inconsistent loading: {df1.shape} vs {df2.shape}"
        
        # Should have same columns
        assert list(df1.columns) == list(df2.columns), \
            "Column names differ between loads"
        
        # Should have same number of rows
        assert len(df1) == len(df2), \
            f"Row count differs: {len(df1)} vs {len(df2)}"
    
    def test_automatic_loading_produces_valid_dataframe(self):
        """
        **Feature: data-storytelling-dashboard, Property 1: Automatic Data Loading**
        **Validates: Requirements 1.1**
        
        Loading should produce a valid, non-empty DataFrame.
        """
        df = load_data("video_games.csv")
        
        # Should be a DataFrame
        assert isinstance(df, pd.DataFrame), \
            f"Expected DataFrame, got {type(df)}"
        
        # Should not be empty
        assert not df.empty, "Loaded DataFrame is empty"
        
        # Should have columns
        assert len(df.columns) > 0, "DataFrame has no columns"
        
        # Should have rows
        assert len(df) > 0, "DataFrame has no rows"
    
    def test_loaded_data_has_normalized_columns(self):
        """
        **Feature: data-storytelling-dashboard, Property 1: Automatic Data Loading**
        **Validates: Requirements 1.1**
        
        Automatically loaded data should have normalized column names
        (no dots or spaces).
        """
        df = load_data("video_games.csv")
        
        # Check that no column has dots or spaces
        for col in df.columns:
            assert '.' not in col, f"Column '{col}' contains dots"
            assert ' ' not in col, f"Column '{col}' contains spaces"


class TestColumnNormalization:
    """Tests for Property 2: Column Name Normalization"""
    
    @given(column_name=st.text(min_size=1, max_size=100))
    @settings(max_examples=100)
    def test_dots_replaced_with_underscores(self, column_name):
        """
        **Feature: data-storytelling-dashboard, Property 2: Column Name Normalization**
        **Validates: Requirements 1.4**
        
        For any column name in the original CSV containing dots or spaces,
        after normalization those characters should be replaced with underscores.
        """
        normalized = normalize_column_name(column_name)
        
        # No dots should remain
        assert '.' not in normalized, \
            f"Dots not removed: '{column_name}' -> '{normalized}'"
        
        # No spaces should remain
        assert ' ' not in normalized, \
            f"Spaces not removed: '{column_name}' -> '{normalized}'"
    
    @given(column_name=st.text(min_size=1, max_size=100))
    @settings(max_examples=100)
    def test_normalization_is_idempotent(self, column_name):
        """
        **Feature: data-storytelling-dashboard, Property 2: Column Name Normalization**
        **Validates: Requirements 1.4**
        
        Normalizing a column name twice should produce the same result as
        normalizing it once (idempotence property).
        """
        normalized_once = normalize_column_name(column_name)
        normalized_twice = normalize_column_name(normalized_once)
        
        assert normalized_once == normalized_twice, \
            f"Normalization not idempotent: '{normalized_once}' vs '{normalized_twice}'"
    
    @given(
        column_names=st.lists(
            st.text(
                alphabet=st.characters(
                    min_codepoint=32,
                    max_codepoint=126,
                    blacklist_characters=',\n\r"'
                ),
                min_size=1,
                max_size=50
            ).filter(lambda x: x.strip() != ''),  # Exclude empty/whitespace-only strings
            min_size=1,
            max_size=20,
            unique=True
        )
    )
    @settings(max_examples=100)
    def test_dataframe_column_normalization(self, column_names):
        """
        **Feature: data-storytelling-dashboard, Property 2: Column Name Normalization**
        **Validates: Requirements 1.4**
        
        When loading a DataFrame, all column names should be normalized.
        """
        # Create a temporary CSV with the given column names
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False, encoding='utf-8', newline='') as f:
            # Write header
            f.write(','.join(column_names) + '\n')
            # Write one row of data
            f.write(','.join(['0'] * len(column_names)) + '\n')
            temp_path = f.name
        
        try:
            # Load the data
            df = load_data(temp_path)
            
            # All columns should be normalized
            for col in df.columns:
                assert '.' not in col, f"Column '{col}' still contains dots"
                assert ' ' not in col, f"Column '{col}' still contains spaces"
        finally:
            # Clean up
            os.unlink(temp_path)
    
    def test_specific_normalization_examples(self):
        """
        **Feature: data-storytelling-dashboard, Property 2: Column Name Normalization**
        **Validates: Requirements 1.4**
        
        Test specific examples of column normalization.
        """
        test_cases = [
            ("Metrics.Sales", "Metrics_Sales"),
            ("Release Year", "Release_Year"),
            ("Features.Max Players", "Features_Max_Players"),
            ("Metadata.Genres", "Metadata_Genres"),
            ("Already_Normalized", "Already_Normalized"),
        ]
        
        for original, expected in test_cases:
            result = normalize_column_name(original)
            assert result == expected, \
                f"Expected '{expected}', got '{result}' for '{original}'"


class TestFileNotFoundHandling:
    """Tests for error handling when file is not found"""
    
    def test_missing_file_raises_file_not_found_error(self):
        """
        **Feature: data-storytelling-dashboard, Unit Test**
        **Validates: Requirements 1.2**
        
        Test that appropriate error message displays when CSV is missing.
        When the dataset fails to load, the system should display a clear
        error message with troubleshooting guidance.
        """
        nonexistent_file = "this_file_does_not_exist_12345.csv"
        
        with pytest.raises(FileNotFoundError) as exc_info:
            load_data(nonexistent_file)
        
        # Error message should be in Spanish
        error_message = str(exc_info.value)
        assert "No se encontró el archivo" in error_message, \
            "Error message should be in Spanish"
        assert nonexistent_file in error_message, \
            "Error message should mention the missing file"
    
    def test_error_message_provides_guidance(self):
        """
        **Feature: data-storytelling-dashboard, Unit Test**
        **Validates: Requirements 1.2**
        
        Error message should provide troubleshooting guidance.
        """
        nonexistent_file = "missing.csv"
        
        with pytest.raises(FileNotFoundError) as exc_info:
            load_data(nonexistent_file)
        
        error_message = str(exc_info.value)
        
        # Should provide helpful guidance
        assert any(keyword in error_message.lower() for keyword in 
                  ["asegúrate", "existe", "directorio", "permisos"]), \
            "Error message should provide troubleshooting guidance"
    
    def test_empty_csv_raises_value_error(self):
        """
        **Feature: data-storytelling-dashboard, Unit Test**
        **Validates: Requirements 1.2**
        
        Test that empty CSV files are handled gracefully.
        """
        # Create an empty CSV file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
            temp_path = f.name
        
        try:
            with pytest.raises((ValueError, pd.errors.EmptyDataError)):
                load_data(temp_path)
        finally:
            os.unlink(temp_path)


class TestDataValidation:
    """Tests for data validation functionality"""
    
    def test_validate_required_columns_success(self):
        """Test that validation passes when required columns exist"""
        df = pd.DataFrame({
            'Title': ['Game1', 'Game2'],
            'Metrics_Sales': [1.0, 2.0],
            'Release_Year': [2020, 2021]
        })
        
        required = ['Title', 'Metrics_Sales']
        assert validate_required_columns(df, required) is True
    
    def test_validate_required_columns_failure(self):
        """Test that validation fails when required columns are missing"""
        df = pd.DataFrame({
            'Title': ['Game1', 'Game2'],
            'Metrics_Sales': [1.0, 2.0]
        })
        
        required = ['Title', 'NonExistent_Column']
        
        with pytest.raises(ValueError) as exc_info:
            validate_required_columns(df, required)
        
        error_message = str(exc_info.value)
        assert 'NonExistent_Column' in error_message


class TestColumnFinding:
    """Tests for flexible column detection"""
    
    def test_find_column_returns_first_match(self):
        """Test that find_column returns the first matching option"""
        df = pd.DataFrame({
            'Title': [1, 2],
            'Name': [3, 4],
            'Other': [5, 6]
        })
        
        result = find_column(df, ['Title', 'Name', 'Other'])
        assert result == 'Title'
    
    def test_find_column_returns_none_when_no_match(self):
        """Test that find_column returns None when no options match"""
        df = pd.DataFrame({
            'Column1': [1, 2],
            'Column2': [3, 4]
        })
        
        result = find_column(df, ['NonExistent1', 'NonExistent2'])
        assert result is None
    
    def test_find_column_with_empty_options(self):
        """Test that find_column handles empty options list"""
        df = pd.DataFrame({'Column1': [1, 2]})
        
        result = find_column(df, [])
        assert result is None


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
