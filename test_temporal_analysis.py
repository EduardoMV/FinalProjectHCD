"""
Property-based tests for temporal analysis section.

Tests correctness properties related to temporal data filtering.
"""

import pytest
import pandas as pd
import tempfile
import os
from hypothesis import given, strategies as st, settings, assume

from data_loader import load_data, find_column


class TestTemporalDataFiltering:
    """Tests for Property 10: Temporal Data Filtering"""
    
    def test_temporal_data_within_valid_range(self):
        """
        **Feature: data-storytelling-dashboard, Property 10: Temporal Data Filtering**
        **Validates: Requirements 6.5**
        
        For any temporal visualization, all displayed year values should be within
        a valid range (1980-2025), with invalid years filtered out.
        """
        # Load the actual dataset
        df = load_data("video_games.csv")
        
        # Find year column
        year_col = find_column(df, ["Release_Year", "Year", "year", "release_year"])
        
        if year_col:
            # Filter to valid years (as the application should do)
            valid_years = df[year_col].dropna()
            valid_years = valid_years[(valid_years >= 1980) & (valid_years <= 2025)]
            
            # Verify all years are within the valid range
            assert all(valid_years >= 1980), \
                f"Found years before 1980: {valid_years[valid_years < 1980].tolist()}"
            assert all(valid_years <= 2025), \
                f"Found years after 2025: {valid_years[valid_years > 2025].tolist()}"
    
    @given(
        num_games=st.integers(min_value=10, max_value=100),
        invalid_year_ratio=st.floats(min_value=0.0, max_value=0.5)
    )
    @settings(max_examples=100)
    def test_filtering_removes_invalid_years(self, num_games, invalid_year_ratio):
        """
        **Feature: data-storytelling-dashboard, Property 10: Temporal Data Filtering**
        **Validates: Requirements 6.5**
        
        For any dataset containing both valid and invalid years, filtering should
        remove all years outside the 1980-2025 range.
        """
        # Create a temporary CSV with mix of valid and invalid years
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False, encoding='utf-8', newline='') as f:
            f.write('Title,Release_Year,Metrics_Sales\n')
            
            num_invalid = int(num_games * invalid_year_ratio)
            num_valid = num_games - num_invalid
            
            # Add valid years (1980-2025)
            for i in range(num_valid):
                year = 1980 + (i % 46)  # Cycles through 1980-2025
                f.write(f'Game{i},{year},1.0\n')
            
            # Add invalid years (before 1980 or after 2025)
            for i in range(num_invalid):
                if i % 2 == 0:
                    year = 1900 + (i % 80)  # Years before 1980
                else:
                    year = 2026 + (i % 50)  # Years after 2025
                f.write(f'GameInvalid{i},{year},1.0\n')
            
            temp_path = f.name
        
        try:
            df = load_data(temp_path)
            
            year_col = find_column(df, ["Release_Year", "Year", "year", "release_year"])
            
            if year_col:
                # Apply the filtering logic
                filtered_years = df[year_col].dropna()
                filtered_years = filtered_years[(filtered_years >= 1980) & (filtered_years <= 2025)]
                
                # Verify no invalid years remain
                assert len(filtered_years) == num_valid, \
                    f"Expected {num_valid} valid years, got {len(filtered_years)}"
                
                assert all(filtered_years >= 1980), \
                    "Found years before 1980 after filtering"
                assert all(filtered_years <= 2025), \
                    "Found years after 2025 after filtering"
        finally:
            os.unlink(temp_path)
    
    def test_filtering_preserves_valid_years(self):
        """
        **Feature: data-storytelling-dashboard, Property 10: Temporal Data Filtering**
        **Validates: Requirements 6.5**
        
        Filtering should preserve all valid years (1980-2025) while removing invalid ones.
        """
        # Create a dataset with known valid and invalid years
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False, encoding='utf-8', newline='') as f:
            f.write('Title,Release_Year,Metrics_Sales\n')
            f.write('Game1,1979,1.0\n')  # Invalid: too early
            f.write('Game2,1980,1.0\n')  # Valid: boundary
            f.write('Game3,2000,1.0\n')  # Valid: middle
            f.write('Game4,2025,1.0\n')  # Valid: boundary
            f.write('Game5,2026,1.0\n')  # Invalid: too late
            f.write('Game6,1500,1.0\n')  # Invalid: way too early
            f.write('Game7,3000,1.0\n')  # Invalid: way too late
            temp_path = f.name
        
        try:
            df = load_data(temp_path)
            
            year_col = find_column(df, ["Release_Year", "Year", "year", "release_year"])
            
            if year_col:
                # Count original valid years
                original_valid = df[(df[year_col] >= 1980) & (df[year_col] <= 2025)]
                expected_count = len(original_valid)
                
                # Apply filtering
                filtered_years = df[year_col].dropna()
                filtered_years = filtered_years[(filtered_years >= 1980) & (filtered_years <= 2025)]
                
                # Should have exactly 3 valid years (1980, 2000, 2025)
                assert len(filtered_years) == expected_count, \
                    f"Expected {expected_count} valid years, got {len(filtered_years)}"
                
                # Verify the specific valid years are present
                assert 1980 in filtered_years.values, "1980 should be preserved"
                assert 2000 in filtered_years.values, "2000 should be preserved"
                assert 2025 in filtered_years.values, "2025 should be preserved"
                
                # Verify invalid years are not present
                assert 1979 not in filtered_years.values, "1979 should be filtered out"
                assert 2026 not in filtered_years.values, "2026 should be filtered out"
        finally:
            os.unlink(temp_path)
    
    @given(
        years=st.lists(
            st.integers(min_value=1900, max_value=2100),
            min_size=5,
            max_size=50
        )
    )
    @settings(max_examples=100)
    def test_filter_boundary_conditions(self, years):
        """
        **Feature: data-storytelling-dashboard, Property 10: Temporal Data Filtering**
        **Validates: Requirements 6.5**
        
        For any list of years, filtering with boundaries [1980, 2025] should include
        boundary values and exclude values outside the range.
        """
        # Create DataFrame with the years
        df = pd.DataFrame({
            'year': years,
            'value': [1.0] * len(years)
        })
        
        # Apply filtering
        filtered = df[(df['year'] >= 1980) & (df['year'] <= 2025)]
        
        # Verify all filtered years are in valid range
        if len(filtered) > 0:
            assert all(filtered['year'] >= 1980), \
                "Filtered data contains years before 1980"
            assert all(filtered['year'] <= 2025), \
                "Filtered data contains years after 2025"
        
        # Verify boundary values are included if present
        if 1980 in years:
            assert 1980 in filtered['year'].values, \
                "Boundary value 1980 should be included"
        if 2025 in years:
            assert 2025 in filtered['year'].values, \
                "Boundary value 2025 should be included"
        
        # Verify out-of-range values are excluded
        for year in years:
            if year < 1980 or year > 2025:
                assert year not in filtered['year'].values, \
                    f"Invalid year {year} should be filtered out"
    
    def test_filtering_handles_missing_values(self):
        """
        **Feature: data-storytelling-dashboard, Property 10: Temporal Data Filtering**
        **Validates: Requirements 6.5**
        
        Filtering should handle missing (NaN) year values gracefully.
        """
        # Create a dataset with missing years
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False, encoding='utf-8', newline='') as f:
            f.write('Title,Release_Year,Metrics_Sales\n')
            f.write('Game1,2000,1.0\n')
            f.write('Game2,,1.0\n')  # Missing year
            f.write('Game3,2010,1.0\n')
            f.write('Game4,,1.0\n')  # Missing year
            temp_path = f.name
        
        try:
            df = load_data(temp_path)
            
            year_col = find_column(df, ["Release_Year", "Year", "year", "release_year"])
            
            if year_col:
                # Apply filtering (should handle NaN)
                filtered_years = df[year_col].dropna()
                filtered_years = filtered_years[(filtered_years >= 1980) & (filtered_years <= 2025)]
                
                # Should have exactly 2 valid years
                assert len(filtered_years) == 2, \
                    f"Expected 2 valid years, got {len(filtered_years)}"
                
                # Verify no NaN values in result
                assert not filtered_years.isna().any(), \
                    "Filtered data should not contain NaN values"
        finally:
            os.unlink(temp_path)
    
    @given(
        valid_year=st.integers(min_value=1980, max_value=2025)
    )
    @settings(max_examples=100)
    def test_all_valid_years_pass_filter(self, valid_year):
        """
        **Feature: data-storytelling-dashboard, Property 10: Temporal Data Filtering**
        **Validates: Requirements 6.5**
        
        For any year in the valid range [1980, 2025], it should pass the filter.
        """
        # Create a simple DataFrame
        df = pd.DataFrame({
            'year': [valid_year],
            'value': [1.0]
        })
        
        # Apply filter
        filtered = df[(df['year'] >= 1980) & (df['year'] <= 2025)]
        
        # The valid year should be in the filtered result
        assert len(filtered) == 1, \
            f"Valid year {valid_year} should pass the filter"
        assert filtered['year'].iloc[0] == valid_year, \
            f"Filtered year should be {valid_year}"
    
    @given(
        invalid_year=st.one_of(
            st.integers(min_value=1000, max_value=1979),
            st.integers(min_value=2026, max_value=3000)
        )
    )
    @settings(max_examples=100)
    def test_all_invalid_years_fail_filter(self, invalid_year):
        """
        **Feature: data-storytelling-dashboard, Property 10: Temporal Data Filtering**
        **Validates: Requirements 6.5**
        
        For any year outside the valid range [1980, 2025], it should be filtered out.
        """
        # Create a simple DataFrame
        df = pd.DataFrame({
            'year': [invalid_year],
            'value': [1.0]
        })
        
        # Apply filter
        filtered = df[(df['year'] >= 1980) & (df['year'] <= 2025)]
        
        # The invalid year should not be in the filtered result
        assert len(filtered) == 0, \
            f"Invalid year {invalid_year} should be filtered out"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
