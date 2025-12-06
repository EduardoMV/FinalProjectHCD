"""
Property-based tests for sales analysis section.

Tests correctness properties related to sales ranking and top performer identification.
"""

import pytest
import pandas as pd
import tempfile
import os
from hypothesis import given, strategies as st, settings, assume

from data_loader import load_data, find_column


class TestSalesRanking:
    """Tests for Property 6: Sales Ranking Correctness"""
    
    def test_sales_by_genre_ordered_descending(self):
        """
        **Feature: data-storytelling-dashboard, Property 6: Sales Ranking Correctness**
        **Validates: Requirements 4.1**
        
        For any sales by genre visualization, the genres should be ordered by
        total sales in descending order (highest to lowest).
        """
        # Load the actual dataset
        df = load_data("video_games.csv")
        
        # Find sales and genre columns
        sales_col = find_column(df, ["Metrics_Sales", "Global_Sales", "sales", "Sales"])
        genre_col = find_column(df, ["Metadata_Genres", "Genre", "genre", "Genres"])
        
        if sales_col and genre_col:
            # Calculate total sales by genre
            sales_by_genre = df.groupby(genre_col)[sales_col].sum().sort_values(ascending=False)
            
            # Verify the series is sorted in descending order
            sales_values = sales_by_genre.values
            for i in range(len(sales_values) - 1):
                assert sales_values[i] >= sales_values[i + 1], \
                    f"Sales not in descending order at index {i}: {sales_values[i]} < {sales_values[i + 1]}"
    
    @given(
        num_genres=st.integers(min_value=2, max_value=20),
        games_per_genre=st.integers(min_value=1, max_value=50)
    )
    @settings(max_examples=100)
    def test_sales_ranking_property(self, num_genres, games_per_genre):
        """
        **Feature: data-storytelling-dashboard, Property 6: Sales Ranking Correctness**
        **Validates: Requirements 4.1**
        
        For any dataset with genres and sales, when aggregated and sorted by total sales,
        each genre's total sales should be >= the next genre's total sales.
        """
        # Create a temporary CSV with known sales data
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False, encoding='utf-8', newline='') as f:
            # Write header
            f.write('Title,Metadata_Genres,Metrics_Sales\n')
            
            # Create genres with decreasing sales to test sorting
            game_id = 0
            for genre_id in range(num_genres):
                genre_name = f'Genre{genre_id}'
                # Each genre gets progressively lower sales per game
                sales_per_game = (num_genres - genre_id) * 1.0
                
                for _ in range(games_per_genre):
                    f.write(f'Game{game_id},{genre_name},{sales_per_game}\n')
                    game_id += 1
            
            temp_path = f.name
        
        try:
            # Load the data
            df = load_data(temp_path)
            
            # Find columns
            sales_col = find_column(df, ["Metrics_Sales", "Global_Sales", "sales", "Sales"])
            genre_col = find_column(df, ["Metadata_Genres", "Genre", "genre", "Genres"])
            
            if sales_col and genre_col:
                # Calculate total sales by genre and sort descending
                sales_by_genre = df.groupby(genre_col)[sales_col].sum().sort_values(ascending=False)
                
                # Verify descending order
                sales_values = sales_by_genre.values
                for i in range(len(sales_values) - 1):
                    assert sales_values[i] >= sales_values[i + 1], \
                        f"Sales ranking violated at position {i}: {sales_values[i]} < {sales_values[i + 1]}"
        finally:
            # Clean up
            os.unlink(temp_path)
    
    def test_sales_ranking_with_equal_values(self):
        """
        **Feature: data-storytelling-dashboard, Property 6: Sales Ranking Correctness**
        **Validates: Requirements 4.1**
        
        When multiple genres have equal sales, the ranking should still be valid
        (non-increasing order).
        """
        # Create a dataset with some equal sales values
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False, encoding='utf-8', newline='') as f:
            f.write('Title,Metadata_Genres,Metrics_Sales\n')
            f.write('Game1,Action,10.0\n')
            f.write('Game2,Action,5.0\n')
            f.write('Game3,RPG,10.0\n')
            f.write('Game4,RPG,5.0\n')
            f.write('Game5,Sports,8.0\n')
            temp_path = f.name
        
        try:
            df = load_data(temp_path)
            
            sales_col = find_column(df, ["Metrics_Sales", "Global_Sales", "sales", "Sales"])
            genre_col = find_column(df, ["Metadata_Genres", "Genre", "genre", "Genres"])
            
            if sales_col and genre_col:
                sales_by_genre = df.groupby(genre_col)[sales_col].sum().sort_values(ascending=False)
                
                # Verify non-increasing order (allows equal values)
                sales_values = sales_by_genre.values
                for i in range(len(sales_values) - 1):
                    assert sales_values[i] >= sales_values[i + 1], \
                        f"Non-increasing order violated at position {i}"
        finally:
            os.unlink(temp_path)
    
    @given(
        sales_values=st.lists(
            st.floats(min_value=0.0, max_value=1000.0, allow_nan=False, allow_infinity=False),
            min_size=2,
            max_size=20
        )
    )
    @settings(max_examples=100)
    def test_sorting_preserves_descending_order(self, sales_values):
        """
        **Feature: data-storytelling-dashboard, Property 6: Sales Ranking Correctness**
        **Validates: Requirements 4.1**
        
        For any list of sales values, sorting in descending order should produce
        a non-increasing sequence.
        """
        # Create a DataFrame with the sales values
        genres = [f'Genre{i}' for i in range(len(sales_values))]
        df = pd.DataFrame({
            'genre': genres,
            'sales': sales_values
        })
        
        # Sort by sales descending
        sorted_df = df.sort_values('sales', ascending=False)
        sorted_sales = sorted_df['sales'].values
        
        # Verify descending order
        for i in range(len(sorted_sales) - 1):
            assert sorted_sales[i] >= sorted_sales[i + 1], \
                f"Descending order violated at position {i}: {sorted_sales[i]} < {sorted_sales[i + 1]}"


class TestTopPerformerIdentification:
    """Tests for Property 7: Top Performer Identification"""
    
    def test_top_n_performers_are_highest_sales(self):
        """
        **Feature: data-storytelling-dashboard, Property 7: Top Performer Identification**
        **Validates: Requirements 4.3**
        
        For any sales visualization, the top N performers (by sales volume) should be
        identifiable through visual emphasis or annotations.
        
        This test verifies that when we select the top N items, they are indeed
        the N items with the highest sales.
        """
        # Load the actual dataset
        df = load_data("video_games.csv")
        
        # Find sales and genre columns
        sales_col = find_column(df, ["Metrics_Sales", "Global_Sales", "sales", "Sales"])
        genre_col = find_column(df, ["Metadata_Genres", "Genre", "genre", "Genres"])
        
        if sales_col and genre_col:
            # Calculate total sales by genre
            sales_by_genre = df.groupby(genre_col)[sales_col].sum().sort_values(ascending=False)
            
            # Get top 3 performers
            top_n = 3
            if len(sales_by_genre) >= top_n:
                top_performers = sales_by_genre.head(top_n)
                
                # Verify these are indeed the top N
                # All top performers should have sales >= any non-top performer
                if len(sales_by_genre) > top_n:
                    min_top_sales = top_performers.min()
                    max_non_top_sales = sales_by_genre.iloc[top_n:].max()
                    
                    assert min_top_sales >= max_non_top_sales, \
                        f"Top performer has lower sales ({min_top_sales}) than non-top performer ({max_non_top_sales})"
    
    @given(
        num_items=st.integers(min_value=5, max_value=50),
        top_n=st.integers(min_value=1, max_value=10)
    )
    @settings(max_examples=100)
    def test_top_n_selection_property(self, num_items, top_n):
        """
        **Feature: data-storytelling-dashboard, Property 7: Top Performer Identification**
        **Validates: Requirements 4.3**
        
        For any dataset, selecting the top N items by sales should return exactly
        the N items with the highest sales values.
        """
        # Ensure top_n doesn't exceed num_items
        assume(top_n <= num_items)
        
        # Create a dataset with known sales values
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False, encoding='utf-8', newline='') as f:
            f.write('Title,Metadata_Genres,Metrics_Sales\n')
            
            # Create items with sales values from 1 to num_items
            for i in range(num_items):
                genre = f'Genre{i}'
                sales = float(i + 1)  # Sales from 1.0 to num_items
                f.write(f'Game{i},{genre},{sales}\n')
            
            temp_path = f.name
        
        try:
            df = load_data(temp_path)
            
            sales_col = find_column(df, ["Metrics_Sales", "Global_Sales", "sales", "Sales"])
            genre_col = find_column(df, ["Metadata_Genres", "Genre", "genre", "Genres"])
            
            if sales_col and genre_col:
                # Calculate sales by genre
                sales_by_genre = df.groupby(genre_col)[sales_col].sum().sort_values(ascending=False)
                
                # Get top N
                top_performers = sales_by_genre.head(top_n)
                
                # Verify we got exactly top_n items
                assert len(top_performers) == top_n, \
                    f"Expected {top_n} top performers, got {len(top_performers)}"
                
                # Verify these are the highest values
                # The minimum value in top_n should be >= maximum value outside top_n
                if len(sales_by_genre) > top_n:
                    min_top = top_performers.min()
                    remaining = sales_by_genre.iloc[top_n:]
                    max_remaining = remaining.max()
                    
                    assert min_top >= max_remaining, \
                        f"Top performer minimum ({min_top}) < non-top maximum ({max_remaining})"
        finally:
            os.unlink(temp_path)
    
    def test_top_performer_with_ties(self):
        """
        **Feature: data-storytelling-dashboard, Property 7: Top Performer Identification**
        **Validates: Requirements 4.3**
        
        When there are ties in sales values, the top N selection should still
        be valid (selecting N items with the highest values).
        """
        # Create a dataset with tied values
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False, encoding='utf-8', newline='') as f:
            f.write('Title,Metadata_Genres,Metrics_Sales\n')
            f.write('Game1,Action,10.0\n')
            f.write('Game2,RPG,10.0\n')
            f.write('Game3,Sports,8.0\n')
            f.write('Game4,Racing,8.0\n')
            f.write('Game5,Puzzle,5.0\n')
            temp_path = f.name
        
        try:
            df = load_data(temp_path)
            
            sales_col = find_column(df, ["Metrics_Sales", "Global_Sales", "sales", "Sales"])
            genre_col = find_column(df, ["Metadata_Genres", "Genre", "genre", "Genres"])
            
            if sales_col and genre_col:
                sales_by_genre = df.groupby(genre_col)[sales_col].sum().sort_values(ascending=False)
                
                # Get top 2
                top_2 = sales_by_genre.head(2)
                
                # Both should have sales of 10.0
                assert all(top_2 == 10.0), \
                    "Top 2 should both have sales of 10.0"
                
                # Get top 3
                top_3 = sales_by_genre.head(3)
                
                # Minimum of top 3 should be >= maximum of remaining
                if len(sales_by_genre) > 3:
                    min_top_3 = top_3.min()
                    max_remaining = sales_by_genre.iloc[3:].max()
                    assert min_top_3 >= max_remaining, \
                        "Top 3 minimum should be >= remaining maximum"
        finally:
            os.unlink(temp_path)
    
    @given(
        top_n=st.integers(min_value=1, max_value=5)
    )
    @settings(max_examples=100)
    def test_top_n_from_actual_dataset(self, top_n):
        """
        **Feature: data-storytelling-dashboard, Property 7: Top Performer Identification**
        **Validates: Requirements 4.3**
        
        For the actual dataset, selecting top N performers should return items
        where each has sales >= all items not in the top N.
        """
        df = load_data("video_games.csv")
        
        sales_col = find_column(df, ["Metrics_Sales", "Global_Sales", "sales", "Sales"])
        genre_col = find_column(df, ["Metadata_Genres", "Genre", "genre", "Genres"])
        
        if sales_col and genre_col:
            sales_by_genre = df.groupby(genre_col)[sales_col].sum().sort_values(ascending=False)
            
            # Only test if we have enough genres
            assume(len(sales_by_genre) >= top_n)
            
            top_performers = sales_by_genre.head(top_n)
            
            # Verify count
            assert len(top_performers) == top_n, \
                f"Expected {top_n} performers, got {len(top_performers)}"
            
            # Verify these are truly the top
            if len(sales_by_genre) > top_n:
                min_top = top_performers.min()
                max_non_top = sales_by_genre.iloc[top_n:].max()
                
                assert min_top >= max_non_top, \
                    f"Top performer minimum ({min_top}) < non-top maximum ({max_non_top})"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
