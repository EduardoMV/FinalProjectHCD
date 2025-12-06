"""
Property-based tests for visual theme module.

Tests correctness properties related to color consistency,
theme application, and visual styling.
"""

import pytest
from hypothesis import given, strategies as st, settings
import plotly.graph_objects as go
import matplotlib.pyplot as plt

from visual_theme import VisualTheme


class TestColorConsistency:
    """Tests for Property 14: Color Scheme Consistency"""
    
    @given(
        category=st.text(min_size=1, max_size=50),
        categories=st.lists(st.text(min_size=1, max_size=50), min_size=1, max_size=20, unique=True)
    )
    @settings(max_examples=100)
    def test_same_category_gets_same_color(self, category, categories):
        """
        **Feature: data-storytelling-dashboard, Property 14: Color Scheme Consistency**
        **Validates: Requirements 10.1**
        
        For any categorical variable (e.g., genre) displayed across multiple visualizations,
        the same category should use the same color in all charts.
        
        This test verifies that calling get_color_for_category with the same category
        and category list always returns the same color.
        """
        # Ensure the category is in the list
        if category not in categories:
            categories.append(category)
        
        # Get color twice for the same category
        color1 = VisualTheme.get_color_for_category(category, categories)
        color2 = VisualTheme.get_color_for_category(category, categories)
        
        # Should be identical
        assert color1 == color2, \
            f"Same category '{category}' returned different colors: {color1} vs {color2}"
    
    @given(
        categories=st.lists(st.text(min_size=1, max_size=50), min_size=2, max_size=20, unique=True)
    )
    @settings(max_examples=100)
    def test_color_consistency_across_calls(self, categories):
        """
        **Feature: data-storytelling-dashboard, Property 14: Color Scheme Consistency**
        **Validates: Requirements 10.1**
        
        For any list of categories, each category should consistently map to the same color
        regardless of how many times we query it.
        """
        # Build a color mapping
        color_map = {}
        for category in categories:
            color_map[category] = VisualTheme.get_color_for_category(category, categories)
        
        # Query again and verify consistency
        for category in categories:
            new_color = VisualTheme.get_color_for_category(category, categories)
            assert new_color == color_map[category], \
                f"Category '{category}' color changed from {color_map[category]} to {new_color}"
    
    @given(
        categories=st.lists(st.text(min_size=1, max_size=50), min_size=2, max_size=20, unique=True)
    )
    @settings(max_examples=100)
    def test_different_categories_can_have_different_colors(self, categories):
        """
        **Feature: data-storytelling-dashboard, Property 14: Color Scheme Consistency**
        **Validates: Requirements 10.1**
        
        While the same category must have the same color, different categories
        should be distinguishable (though colors may repeat if there are more
        categories than colors in the palette).
        """
        colors = [VisualTheme.get_color_for_category(cat, categories) for cat in categories]
        
        # All colors should be valid hex codes
        for color in colors:
            assert color.startswith('#'), f"Invalid color format: {color}"
            assert len(color) == 7, f"Invalid hex color length: {color}"
        
        # Colors should come from the PRIMARY_COLORS palette
        for color in colors:
            assert color in VisualTheme.PRIMARY_COLORS, \
                f"Color {color} not in PRIMARY_COLORS palette"
    
    def test_color_palette_not_empty(self):
        """
        **Feature: data-storytelling-dashboard, Property 14: Color Scheme Consistency**
        **Validates: Requirements 10.1**
        
        The PRIMARY_COLORS palette must contain at least one color.
        """
        assert len(VisualTheme.PRIMARY_COLORS) > 0, \
            "PRIMARY_COLORS palette is empty"
    
    def test_all_colors_are_valid_hex(self):
        """
        **Feature: data-storytelling-dashboard, Property 14: Color Scheme Consistency**
        **Validates: Requirements 10.1**
        
        All colors in the PRIMARY_COLORS palette must be valid hex color codes.
        """
        for color in VisualTheme.PRIMARY_COLORS:
            assert color.startswith('#'), f"Color {color} doesn't start with #"
            assert len(color) == 7, f"Color {color} is not 7 characters long"
            # Verify it's valid hex
            try:
                int(color[1:], 16)
            except ValueError:
                pytest.fail(f"Color {color} is not a valid hex code")


class TestThemeApplication:
    """Tests for theme application functions"""
    
    def test_plotly_theme_preserves_figure(self):
        """
        Applying the Plotly theme should not destroy the figure,
        it should return a valid figure object.
        """
        fig = go.Figure(data=[go.Scatter(x=[1, 2, 3], y=[1, 2, 3])])
        themed_fig = VisualTheme.apply_plotly_theme(fig)
        
        assert themed_fig is not None
        assert isinstance(themed_fig, go.Figure)
        # Verify data is preserved
        assert len(themed_fig.data) == 1
    
    def test_matplotlib_theme_sets_params(self):
        """
        Applying matplotlib theme should set rcParams without errors.
        """
        # This should not raise any exceptions
        VisualTheme.apply_matplotlib_theme()
        
        # Verify some key params are set
        assert plt.rcParams['figure.facecolor'] == VisualTheme.CARD_BACKGROUND
        assert plt.rcParams['axes.facecolor'] == VisualTheme.CARD_BACKGROUND


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
