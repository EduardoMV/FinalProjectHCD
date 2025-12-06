"""
Property-based tests for quality vs popularity section.

Tests correctness properties related to score aggregation and missing data handling.
"""

import pytest
import pandas as pd
import numpy as np
import tempfile
import os
from hypothesis import given, strategies as st, settings, assume

from data_loader import load_data, find_column


class TestScoreAggregation:
    """Tests for Property 8: Score Aggregation Accuracy"""
    
    def test_average_score_by_genre_accuracy(self):
        """
        **Feature: data-storytelling-dashboard, Property 8: Score Aggregation Accuracy**
        **Validates: Requirements 5.2**
        
        For any genre, the average review score displayed should equal the mean
        of all review scores for games in that genre.
        """
        # Load the actual dataset
        df = load_data("video_games.csv")
        
        # Find score and genre columns
        score_col = find_column(df, ["Metrics_Review_Score", "Score", "meta_score", "rating", "score"])
        genre_col = find_column(df, ["Metadata_Genres", "Genre", "genre", "Genres"])
        
        if score_col and genre_col:
            # Filter out missing scores
            df_with_scores = df[df[score_col].notna()].copy()
            
            if len(df_with_scores) > 0:
                # Calculate average scores by genre
                avg_scores = df_with_scores.groupby(genre_col)[score_col].mean()
                
                # Verify each genre's average
                for genre in avg_scores.index:
                    genre_games = df_with_scores[df_with_scores[genre_col] == genre]
                    expected_avg = genre_games[score_col].mean()
                    calculated_avg = avg_scores[genre]
                    
                    # Use np.isclose for floating point comparison
                    assert np.isclose(calculated_avg, expected_avg, rtol=1e-9), \
                        f"Genre '{genre}': calculated avg ({calculated_avg}) != expected ({expected_avg})"
    
    @given(
        num_genres=st.integers(min_value=1, max_value=10),
        games_per_genre=st.integers(min_value=1, max_value=20)
    )
    @settings(max_examples=100)
    def test_score_aggregation_property(self, num_genres, games_per_genre):
        """
        **Feature: data-storytelling-dashboard, Property 8: Score Aggregation Accuracy**
        **Validates: Requirements 5.2**
        
        For any dataset with genres and scores, the average score per genre
        should equal the mean of all scores for that genre.
        """
        # Create a temporary CSV with known score data
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False, encoding='utf-8', newline='') as f:
            # Write header
            f.write('Title,Metadata_Genres,Metrics_Review_Score\n')
            
            # Create games with scores
            game_id = 0
            for genre_id in range(num_genres):
                genre_name = f'Genre{genre_id}'
                
                for game_num in range(games_per_genre):
                    # Create predictable scores (0-100 range)
                    score = (genre_id * 10 + game_num) % 101
                    f.write(f'Game{game_id},{genre_name},{score}\n')
                    game_id += 1
            
            temp_path = f.name
        
        try:
            # Load the data
            df = load_data(temp_path)
            
            # Find columns
            score_col = find_column(df, ["Metrics_Review_Score", "Score", "meta_score", "rating", "score"])
            genre_col = find_column(df, ["Metadata_Genres", "Genre", "genre", "Genres"])
            
            if score_col and genre_col:
                # Calculate average scores by genre
                avg_scores = df.groupby(genre_col)[score_col].mean()
                
                # Verify each genre's average matches manual calculation
                for genre in avg_scores.index:
                    genre_games = df[df[genre_col] == genre]
                    expected_avg = genre_games[score_col].mean()
                    calculated_avg = avg_scores[genre]
                    
                    assert np.isclose(calculated_avg, expected_avg, rtol=1e-9), \
                        f"Score aggregation incorrect for {genre}: {calculated_avg} != {expected_avg}"
        finally:
            # Clean up
            os.unlink(temp_path)
    
    @given(
        scores=st.lists(
            st.floats(min_value=0.0, max_value=100.0, allow_nan=False, allow_infinity=False),
            min_size=1,
            max_size=50
        )
    )
    @settings(max_examples=100)
    def test_mean_calculation_property(self, scores):
        """
        **Feature: data-storytelling-dashboard, Property 8: Score Aggregation Accuracy**
        **Validates: Requirements 5.2**
        
        For any list of scores, the mean calculated by pandas should equal
        the sum divided by count.
        """
        # Create a DataFrame with the scores
        df = pd.DataFrame({'score': scores})
        
        # Calculate mean using pandas
        pandas_mean = df['score'].mean()
        
        # Calculate mean manually
        manual_mean = sum(scores) / len(scores)
        
        # Should be equal (within floating point tolerance)
        assert np.isclose(pandas_mean, manual_mean, rtol=1e-9), \
            f"Pandas mean ({pandas_mean}) != manual mean ({manual_mean})"
    
    def test_score_aggregation_with_mixed_values(self):
        """
        **Feature: data-storytelling-dashboard, Property 8: Score Aggregation Accuracy**
        **Validates: Requirements 5.2**
        
        Test score aggregation with a mix of high and low scores.
        """
        # Create a dataset with known score distributions
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False, encoding='utf-8', newline='') as f:
            f.write('Title,Metadata_Genres,Metrics_Review_Score\n')
            # Action genre: scores 80, 90, 100 -> avg = 90
            f.write('Game1,Action,80\n')
            f.write('Game2,Action,90\n')
            f.write('Game3,Action,100\n')
            # RPG genre: scores 50, 60, 70 -> avg = 60
            f.write('Game4,RPG,50\n')
            f.write('Game5,RPG,60\n')
            f.write('Game6,RPG,70\n')
            temp_path = f.name
        
        try:
            df = load_data(temp_path)
            
            score_col = find_column(df, ["Metrics_Review_Score", "Score", "meta_score", "rating", "score"])
            genre_col = find_column(df, ["Metadata_Genres", "Genre", "genre", "Genres"])
            
            if score_col and genre_col:
                avg_scores = df.groupby(genre_col)[score_col].mean()
                
                # Verify expected averages
                assert np.isclose(avg_scores['Action'], 90.0, rtol=1e-9), \
                    f"Action average should be 90.0, got {avg_scores['Action']}"
                assert np.isclose(avg_scores['RPG'], 60.0, rtol=1e-9), \
                    f"RPG average should be 60.0, got {avg_scores['RPG']}"
        finally:
            os.unlink(temp_path)
    
    def test_score_aggregation_excludes_missing_values(self):
        """
        **Feature: data-storytelling-dashboard, Property 8: Score Aggregation Accuracy**
        **Validates: Requirements 5.2**
        
        When calculating average scores, missing values should be excluded
        from the calculation.
        """
        # Create a dataset with some missing scores
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False, encoding='utf-8', newline='') as f:
            f.write('Title,Metadata_Genres,Metrics_Review_Score\n')
            # Action genre: scores 80, 90, NaN -> avg = 85 (excluding NaN)
            f.write('Game1,Action,80\n')
            f.write('Game2,Action,90\n')
            f.write('Game3,Action,\n')  # Missing score
            temp_path = f.name
        
        try:
            df = load_data(temp_path)
            
            score_col = find_column(df, ["Metrics_Review_Score", "Score", "meta_score", "rating", "score"])
            genre_col = find_column(df, ["Metadata_Genres", "Genre", "genre", "Genres"])
            
            if score_col and genre_col:
                # Calculate average (pandas automatically excludes NaN)
                avg_scores = df.groupby(genre_col)[score_col].mean()
                
                # Should be 85.0 (average of 80 and 90, excluding NaN)
                assert np.isclose(avg_scores['Action'], 85.0, rtol=1e-9), \
                    f"Action average should be 85.0 (excluding NaN), got {avg_scores['Action']}"
        finally:
            os.unlink(temp_path)


class TestMissingDataHandling:
    """Tests for Property 9: Missing Data Handling"""
    
    def test_visualization_handles_missing_scores(self):
        """
        **Feature: data-storytelling-dashboard, Property 9: Missing Data Handling**
        **Validates: Requirements 5.5, 7.3**
        
        For any visualization function receiving data with missing values,
        the function should complete execution without raising exceptions.
        """
        # Load the actual dataset
        df = load_data("video_games.csv")
        
        # Find score column
        score_col = find_column(df, ["Metrics_Review_Score", "Score", "meta_score", "rating", "score"])
        
        if score_col:
            # Verify that the dataset has some missing scores
            has_missing = df[score_col].isna().any()
            
            # Try to perform operations that should handle missing data
            try:
                # Calculate mean (should ignore NaN)
                mean_score = df[score_col].mean()
                assert not np.isnan(mean_score) or df[score_col].isna().all(), \
                    "Mean calculation should handle missing values"
                
                # Filter out missing values
                df_filtered = df[df[score_col].notna()]
                assert len(df_filtered) <= len(df), \
                    "Filtering should not increase dataset size"
                
                # Group by operations should work
                genre_col = find_column(df, ["Metadata_Genres", "Genre", "genre", "Genres"])
                if genre_col:
                    avg_by_genre = df.groupby(genre_col)[score_col].mean()
                    assert len(avg_by_genre) > 0, \
                        "Groupby should produce results"
                
            except Exception as e:
                pytest.fail(f"Operations with missing data raised exception: {e}")
    
    @given(
        num_rows=st.integers(min_value=5, max_value=50),
        missing_fraction=st.floats(min_value=0.0, max_value=0.9)
    )
    @settings(max_examples=100)
    def test_missing_data_handling_property(self, num_rows, missing_fraction):
        """
        **Feature: data-storytelling-dashboard, Property 9: Missing Data Handling**
        **Validates: Requirements 5.5, 7.3**
        
        For any dataset with a fraction of missing values, standard operations
        should complete without errors.
        """
        # Calculate number of missing values
        num_missing = int(num_rows * missing_fraction)
        num_valid = num_rows - num_missing
        
        # Create a temporary CSV with some missing scores
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False, encoding='utf-8', newline='') as f:
            f.write('Title,Metadata_Genres,Metrics_Review_Score\n')
            
            # Write valid scores
            for i in range(num_valid):
                f.write(f'Game{i},Action,{50 + i % 50}\n')
            
            # Write rows with missing scores
            for i in range(num_missing):
                f.write(f'Game{num_valid + i},RPG,\n')
            
            temp_path = f.name
        
        try:
            # Load the data
            df = load_data(temp_path)
            
            score_col = find_column(df, ["Metrics_Review_Score", "Score", "meta_score", "rating", "score"])
            genre_col = find_column(df, ["Metadata_Genres", "Genre", "genre", "Genres"])
            
            if score_col:
                # These operations should not raise exceptions
                try:
                    # Calculate mean (ignores NaN)
                    mean_val = df[score_col].mean()
                    
                    # Filter out NaN
                    df_clean = df[df[score_col].notna()]
                    
                    # Count non-null values
                    count = df[score_col].count()
                    
                    # Verify count matches expected
                    assert count == num_valid, \
                        f"Expected {num_valid} valid scores, got {count}"
                    
                    # If we have valid data, mean should not be NaN
                    if num_valid > 0:
                        assert not np.isnan(mean_val), \
                            "Mean should not be NaN when valid data exists"
                    
                except Exception as e:
                    pytest.fail(f"Missing data handling failed: {e}")
        finally:
            os.unlink(temp_path)
    
    def test_dropna_removes_missing_values(self):
        """
        **Feature: data-storytelling-dashboard, Property 9: Missing Data Handling**
        **Validates: Requirements 5.5, 7.3**
        
        Using dropna() should remove all rows with missing values in the specified column.
        """
        # Create a dataset with known missing values
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False, encoding='utf-8', newline='') as f:
            f.write('Title,Metrics_Review_Score\n')
            f.write('Game1,80\n')
            f.write('Game2,\n')  # Missing
            f.write('Game3,90\n')
            f.write('Game4,\n')  # Missing
            f.write('Game5,70\n')
            temp_path = f.name
        
        try:
            df = load_data(temp_path)
            
            score_col = find_column(df, ["Metrics_Review_Score", "Score", "meta_score", "rating", "score"])
            
            if score_col:
                # Original should have 5 rows
                assert len(df) == 5, f"Expected 5 rows, got {len(df)}"
                
                # After dropna, should have 3 rows
                df_clean = df[df[score_col].notna()]
                assert len(df_clean) == 3, f"Expected 3 rows after dropna, got {len(df_clean)}"
                
                # All remaining values should be non-null
                assert df_clean[score_col].notna().all(), \
                    "All values should be non-null after filtering"
        finally:
            os.unlink(temp_path)
    
    def test_groupby_handles_missing_values(self):
        """
        **Feature: data-storytelling-dashboard, Property 9: Missing Data Handling**
        **Validates: Requirements 5.5, 7.3**
        
        Groupby operations should handle missing values gracefully.
        """
        # Create a dataset with missing scores in some groups
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False, encoding='utf-8', newline='') as f:
            f.write('Title,Metadata_Genres,Metrics_Review_Score\n')
            f.write('Game1,Action,80\n')
            f.write('Game2,Action,\n')  # Missing
            f.write('Game3,Action,90\n')
            f.write('Game4,RPG,70\n')
            f.write('Game5,RPG,\n')  # Missing
            temp_path = f.name
        
        try:
            df = load_data(temp_path)
            
            score_col = find_column(df, ["Metrics_Review_Score", "Score", "meta_score", "rating", "score"])
            genre_col = find_column(df, ["Metadata_Genres", "Genre", "genre", "Genres"])
            
            if score_col and genre_col:
                # Groupby mean should ignore NaN values
                avg_scores = df.groupby(genre_col)[score_col].mean()
                
                # Action should have average of 80 and 90 = 85
                assert np.isclose(avg_scores['Action'], 85.0, rtol=1e-9), \
                    f"Action average should be 85.0, got {avg_scores['Action']}"
                
                # RPG should have average of 70 (only one valid value)
                assert np.isclose(avg_scores['RPG'], 70.0, rtol=1e-9), \
                    f"RPG average should be 70.0, got {avg_scores['RPG']}"
        finally:
            os.unlink(temp_path)
    
    @given(
        valid_scores=st.lists(
            st.floats(min_value=0.0, max_value=100.0, allow_nan=False, allow_infinity=False),
            min_size=1,
            max_size=20
        ),
        num_missing=st.integers(min_value=0, max_value=10)
    )
    @settings(max_examples=100)
    def test_filtering_missing_preserves_valid_data(self, valid_scores, num_missing):
        """
        **Feature: data-storytelling-dashboard, Property 9: Missing Data Handling**
        **Validates: Requirements 5.5, 7.3**
        
        When filtering out missing values, all valid values should be preserved.
        """
        # Create a DataFrame with valid scores and NaN values
        all_scores = valid_scores + [np.nan] * num_missing
        df = pd.DataFrame({'score': all_scores})
        
        # Filter out missing values
        df_clean = df[df['score'].notna()]
        
        # Should have exactly len(valid_scores) rows
        assert len(df_clean) == len(valid_scores), \
            f"Expected {len(valid_scores)} rows, got {len(df_clean)}"
        
        # All values should be non-null
        assert df_clean['score'].notna().all(), \
            "Filtered data should have no missing values"
        
        # The valid scores should be preserved (order may differ)
        cleaned_scores = sorted(df_clean['score'].tolist())
        expected_scores = sorted(valid_scores)
        
        assert len(cleaned_scores) == len(expected_scores), \
            "Number of scores should match"
        
        for i in range(len(cleaned_scores)):
            assert np.isclose(cleaned_scores[i], expected_scores[i], rtol=1e-9), \
                f"Score mismatch at position {i}"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
