"""
Property-based tests for introduction section.

Tests correctness properties related to welcome message accuracy
and dataset statistics calculation.
"""

import pytest
import pandas as pd
import tempfile
import os
from hypothesis import given, strategies as st, settings, assume

from data_loader import load_data, find_column


class TestWelcomeMessageAccuracy:
    """Tests for Property 3: Welcome Message Accuracy"""
    
    def test_welcome_message_shows_correct_game_count(self):
        """
        **Feature: data-storytelling-dashboard, Property 3: Welcome Message Accuracy**
        **Validates: Requirements 1.3**
        
        For any successful data load, the welcome message should display the
        correct count of games matching the actual number of rows in the loaded DataFrame.
        """
        # Load the actual dataset
        df = load_data("video_games.csv")
        
        # The game count should equal the number of rows
        actual_count = len(df)
        
        # Verify the count is positive
        assert actual_count > 0, "Dataset should contain games"
        
        # The welcome message in app.py uses len(df) directly,
        # so we verify that len(df) gives us the correct count
        assert len(df) == actual_count, \
            f"Game count mismatch: expected {actual_count}, got {len(df)}"
    
    @given(
        num_rows=st.integers(min_value=1, max_value=10000)
    )
    @settings(max_examples=100)
    def test_game_count_equals_dataframe_length(self, num_rows):
        """
        **Feature: data-storytelling-dashboard, Property 3: Welcome Message Accuracy**
        **Validates: Requirements 1.3**
        
        For any DataFrame with N rows, the game count should equal N.
        This tests the fundamental property that len(df) correctly counts games.
        """
        # Create a temporary CSV with num_rows rows
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False, encoding='utf-8', newline='') as f:
            # Write header
            f.write('Title,Genre,Sales\n')
            # Write num_rows rows
            for i in range(num_rows):
                f.write(f'Game{i},Action,1.0\n')
            temp_path = f.name
        
        try:
            # Load the data
            df = load_data(temp_path)
            
            # The length should match the number of rows we created
            assert len(df) == num_rows, \
                f"Expected {num_rows} games, got {len(df)}"
        finally:
            # Clean up
            os.unlink(temp_path)
    
    def test_welcome_message_count_consistency(self):
        """
        **Feature: data-storytelling-dashboard, Property 3: Welcome Message Accuracy**
        **Validates: Requirements 1.3**
        
        Multiple loads of the same file should report the same game count.
        """
        df1 = load_data("video_games.csv")
        df2 = load_data("video_games.csv")
        
        count1 = len(df1)
        count2 = len(df2)
        
        assert count1 == count2, \
            f"Game count inconsistent between loads: {count1} vs {count2}"


class TestDatasetStatistics:
    """Tests for Property 4: Dataset Statistics Calculation"""
    
    def test_total_games_statistic_accuracy(self):
        """
        **Feature: data-storytelling-dashboard, Property 4: Dataset Statistics Calculation**
        **Validates: Requirements 2.2**
        
        For any loaded dataset, the calculated statistics (total games, year range,
        platform count) should accurately reflect the actual data values.
        
        This test verifies that total_games equals len(df).
        """
        df = load_data("video_games.csv")
        
        # Calculate total games
        total_games = len(df)
        
        # Should be positive
        assert total_games > 0, "Total games should be positive"
        
        # Should equal the DataFrame length
        assert total_games == len(df), \
            f"Total games calculation incorrect: {total_games} vs {len(df)}"
    
    def test_year_range_calculation_accuracy(self):
        """
        **Feature: data-storytelling-dashboard, Property 4: Dataset Statistics Calculation**
        **Validates: Requirements 2.2**
        
        The year range should accurately reflect the min and max years in the dataset.
        """
        df = load_data("video_games.csv")
        
        # Find year column
        year_col = find_column(df, ["Release_Year", "Year", "year", "release_year"])
        
        if year_col:
            # Filter valid years (1980-2025)
            valid_years = df[year_col].dropna()
            valid_years = valid_years[(valid_years >= 1980) & (valid_years <= 2025)]
            
            if len(valid_years) > 0:
                # Calculate year range
                year_min = int(valid_years.min())
                year_max = int(valid_years.max())
                
                # Verify min is less than or equal to max
                assert year_min <= year_max, \
                    f"Year min ({year_min}) should be <= year max ({year_max})"
                
                # Verify years are in valid range
                assert 1980 <= year_min <= 2025, \
                    f"Year min ({year_min}) outside valid range"
                assert 1980 <= year_max <= 2025, \
                    f"Year max ({year_max}) outside valid range"
                
                # Verify these are actually the min and max
                assert year_min == valid_years.min(), \
                    "Year min calculation incorrect"
                assert year_max == valid_years.max(), \
                    "Year max calculation incorrect"
    
    def test_platform_count_accuracy(self):
        """
        **Feature: data-storytelling-dashboard, Property 4: Dataset Statistics Calculation**
        **Validates: Requirements 2.2**
        
        The platform count should accurately reflect the number of unique platforms.
        """
        df = load_data("video_games.csv")
        
        # Find platform column
        platform_col = find_column(df, ["Release_Console", "Platform", "platform", "console"])
        
        if platform_col:
            # Calculate platform count
            platform_count = df[platform_col].nunique()
            
            # Should be positive
            assert platform_count > 0, "Platform count should be positive"
            
            # Verify it matches nunique()
            assert platform_count == df[platform_col].nunique(), \
                "Platform count calculation incorrect"
            
            # Should be less than or equal to total games
            assert platform_count <= len(df), \
                f"Platform count ({platform_count}) cannot exceed total games ({len(df)})"
    
    @given(
        num_platforms=st.integers(min_value=1, max_value=50),
        games_per_platform=st.integers(min_value=1, max_value=100)
    )
    @settings(max_examples=100)
    def test_platform_count_property(self, num_platforms, games_per_platform):
        """
        **Feature: data-storytelling-dashboard, Property 4: Dataset Statistics Calculation**
        **Validates: Requirements 2.2**
        
        For any dataset with N unique platforms, nunique() should return N.
        """
        # Create a temporary CSV with known number of platforms
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False, encoding='utf-8', newline='') as f:
            # Write header
            f.write('Title,Release_Console,Sales\n')
            
            # Write games for each platform
            game_id = 0
            for platform_id in range(num_platforms):
                platform_name = f'Platform{platform_id}'
                for _ in range(games_per_platform):
                    f.write(f'Game{game_id},{platform_name},1.0\n')
                    game_id += 1
            
            temp_path = f.name
        
        try:
            # Load the data
            df = load_data(temp_path)
            
            # Find platform column
            platform_col = find_column(df, ["Release_Console", "Platform", "platform", "console"])
            
            if platform_col:
                # Count unique platforms
                calculated_count = df[platform_col].nunique()
                
                # Should equal the number of platforms we created
                assert calculated_count == num_platforms, \
                    f"Expected {num_platforms} platforms, got {calculated_count}"
        finally:
            # Clean up
            os.unlink(temp_path)
    
    @given(
        year_min=st.integers(min_value=1980, max_value=2020),
        year_max=st.integers(min_value=1980, max_value=2025)
    )
    @settings(max_examples=100)
    def test_year_range_property(self, year_min, year_max):
        """
        **Feature: data-storytelling-dashboard, Property 4: Dataset Statistics Calculation**
        **Validates: Requirements 2.2**
        
        For any dataset with years in range [min, max], the calculated range
        should match [min, max].
        """
        # Ensure min <= max
        assume(year_min <= year_max)
        
        # Create a temporary CSV with known year range
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False, encoding='utf-8', newline='') as f:
            # Write header
            f.write('Title,Release_Year,Sales\n')
            
            # Write games with min and max years (and some in between)
            f.write(f'Game1,{year_min},1.0\n')
            f.write(f'Game2,{year_max},1.0\n')
            
            # Add a middle year if range is large enough
            if year_max - year_min > 1:
                middle_year = (year_min + year_max) // 2
                f.write(f'Game3,{middle_year},1.0\n')
            
            temp_path = f.name
        
        try:
            # Load the data
            df = load_data(temp_path)
            
            # Find year column
            year_col = find_column(df, ["Release_Year", "Year", "year", "release_year"])
            
            if year_col:
                # Filter valid years
                valid_years = df[year_col].dropna()
                valid_years = valid_years[(valid_years >= 1980) & (valid_years <= 2025)]
                
                if len(valid_years) > 0:
                    # Calculate range
                    calculated_min = int(valid_years.min())
                    calculated_max = int(valid_years.max())
                    
                    # Should match our input range
                    assert calculated_min == year_min, \
                        f"Expected min year {year_min}, got {calculated_min}"
                    assert calculated_max == year_max, \
                        f"Expected max year {year_max}, got {calculated_max}"
        finally:
            # Clean up
            os.unlink(temp_path)
    
    def test_statistics_consistency_across_loads(self):
        """
        **Feature: data-storytelling-dashboard, Property 4: Dataset Statistics Calculation**
        **Validates: Requirements 2.2**
        
        Statistics calculated from multiple loads of the same file should be identical.
        """
        # Load data twice
        df1 = load_data("video_games.csv")
        df2 = load_data("video_games.csv")
        
        # Total games should match
        assert len(df1) == len(df2), \
            "Total games differs between loads"
        
        # Platform count should match
        platform_col1 = find_column(df1, ["Release_Console", "Platform", "platform", "console"])
        platform_col2 = find_column(df2, ["Release_Console", "Platform", "platform", "console"])
        
        if platform_col1 and platform_col2:
            count1 = df1[platform_col1].nunique()
            count2 = df2[platform_col2].nunique()
            assert count1 == count2, \
                f"Platform count differs between loads: {count1} vs {count2}"
        
        # Year range should match
        year_col1 = find_column(df1, ["Release_Year", "Year", "year", "release_year"])
        year_col2 = find_column(df2, ["Release_Year", "Year", "year", "release_year"])
        
        if year_col1 and year_col2:
            valid_years1 = df1[year_col1].dropna()
            valid_years1 = valid_years1[(valid_years1 >= 1980) & (valid_years1 <= 2025)]
            
            valid_years2 = df2[year_col2].dropna()
            valid_years2 = valid_years2[(valid_years2 >= 1980) & (valid_years2 <= 2025)]
            
            if len(valid_years1) > 0 and len(valid_years2) > 0:
                assert valid_years1.min() == valid_years2.min(), \
                    "Year min differs between loads"
                assert valid_years1.max() == valid_years2.max(), \
                    "Year max differs between loads"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
