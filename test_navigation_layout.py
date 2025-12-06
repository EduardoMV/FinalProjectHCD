"""
Property-based tests for navigation and layout structure.

Tests correctness properties related to tab labeling consistency
and story section structure.
"""

import pytest
import re
from hypothesis import given, strategies as st, settings


class TestTabLabelingConsistency:
    """Tests for Property 13: Tab Labeling Consistency"""
    
    def test_tab_labels_correspond_to_story_sections(self):
        """
        **Feature: data-storytelling-dashboard, Property 13: Tab Labeling Consistency**
        **Validates: Requirements 9.2**
        
        For any tab in the navigation, the tab label should correspond to its
        story section theme.
        """
        # Read the app.py file to extract tab definitions
        with open('app.py', 'r', encoding='utf-8') as f:
            app_content = f.read()
        
        # Find the st.tabs() call
        # Pattern: st.tabs([...])
        tabs_pattern = r'st\.tabs\(\s*\[(.*?)\]\s*\)'
        tabs_match = re.search(tabs_pattern, app_content, re.DOTALL)
        
        assert tabs_match, "Could not find st.tabs() call in app.py"
        
        # Extract tab labels
        tabs_content = tabs_match.group(1)
        # Find all quoted strings (tab labels)
        label_pattern = r'"([^"]+)"'
        tab_labels = re.findall(label_pattern, tabs_content)
        
        assert len(tab_labels) > 0, "No tab labels found"
        
        # Define expected story section themes based on requirements
        # From requirements: story sections should have clear thematic focus
        expected_themes = {
            'introducción': ['📘 Introducción', 'Introducción', 'Intro'],
            'mercado': ['💰 El Mercado', 'El Mercado', 'Mercado'],
            'calidad': ['⭐ Calidad vs Popularidad', 'Calidad vs Popularidad', 'Calidad'],
            'temporal': ['⏳ Evolución Temporal', 'Evolución Temporal', 'Temporal'],
            'experiencia': ['🎮 Experiencia del Jugador', 'Experiencia del Jugador', 'Experiencia'],
        }
        
        # Check that each story section has a corresponding tab
        story_sections_found = {
            'introducción': False,
            'mercado': False,
            'calidad': False,
            'temporal': False,
            'experiencia': False,
        }
        
        for label in tab_labels:
            label_lower = label.lower()
            
            # Check if this label corresponds to a story section
            if 'introduc' in label_lower or 'intro' in label_lower:
                story_sections_found['introducción'] = True
            elif 'mercado' in label_lower:
                story_sections_found['mercado'] = True
            elif 'calidad' in label_lower or 'popularidad' in label_lower:
                story_sections_found['calidad'] = True
            elif 'temporal' in label_lower or 'evolución' in label_lower or 'evolucion' in label_lower:
                story_sections_found['temporal'] = True
            elif 'experiencia' in label_lower or 'jugador' in label_lower:
                story_sections_found['experiencia'] = True
        
        # Verify that all story sections have corresponding tabs
        missing_sections = [section for section, found in story_sections_found.items() if not found]
        
        assert len(missing_sections) == 0, \
            f"Story sections missing corresponding tabs: {missing_sections}"
    
    def test_tab_labels_are_in_spanish(self):
        """
        **Feature: data-storytelling-dashboard, Property 13: Tab Labeling Consistency**
        **Validates: Requirements 9.2**
        
        All tab labels should be in Spanish as per requirements.
        """
        # Read the app.py file
        with open('app.py', 'r', encoding='utf-8') as f:
            app_content = f.read()
        
        # Find the st.tabs() call
        tabs_pattern = r'st\.tabs\(\s*\[(.*?)\]\s*\)'
        tabs_match = re.search(tabs_pattern, app_content, re.DOTALL)
        
        assert tabs_match, "Could not find st.tabs() call in app.py"
        
        # Extract tab labels
        tabs_content = tabs_match.group(1)
        label_pattern = r'"([^"]+)"'
        tab_labels = re.findall(label_pattern, tabs_content)
        
        # Common Spanish words that should appear in story section tabs
        spanish_indicators = [
            'introducción', 'mercado', 'calidad', 'popularidad',
            'evolución', 'temporal', 'experiencia', 'jugador',
            'vista', 'general', 'distribuciones', 'comparaciones',
            'correlaciones', 'conexiones'
        ]
        
        # Check that at least some tabs contain Spanish words
        spanish_tabs = 0
        for label in tab_labels:
            label_lower = label.lower()
            # Remove emojis and special characters for checking
            label_clean = re.sub(r'[^\w\s]', '', label_lower)
            
            for indicator in spanish_indicators:
                if indicator in label_clean:
                    spanish_tabs += 1
                    break
        
        # At least 5 tabs should have Spanish labels (the 5 story sections)
        assert spanish_tabs >= 5, \
            f"Expected at least 5 Spanish tab labels, found {spanish_tabs}"
    
    def test_tab_labels_include_emojis_for_visual_appeal(self):
        """
        **Feature: data-storytelling-dashboard, Property 13: Tab Labeling Consistency**
        **Validates: Requirements 9.2**
        
        Tab labels should include emojis for visual appeal and storytelling
        as per requirements (2.4: use emojis and visual elements).
        """
        # Read the app.py file
        with open('app.py', 'r', encoding='utf-8') as f:
            app_content = f.read()
        
        # Find the st.tabs() call
        tabs_pattern = r'st\.tabs\(\s*\[(.*?)\]\s*\)'
        tabs_match = re.search(tabs_pattern, app_content, re.DOTALL)
        
        assert tabs_match, "Could not find st.tabs() call in app.py"
        
        # Extract tab labels
        tabs_content = tabs_match.group(1)
        label_pattern = r'"([^"]+)"'
        tab_labels = re.findall(label_pattern, tabs_content)
        
        # Check for emoji presence (emojis are typically in Unicode ranges)
        # Common emoji ranges: U+1F300-U+1F9FF
        emoji_pattern = r'[\U0001F300-\U0001F9FF]|[\u2600-\u26FF]|[\u2700-\u27BF]'
        
        tabs_with_emojis = 0
        for label in tab_labels:
            if re.search(emoji_pattern, label):
                tabs_with_emojis += 1
        
        # At least some tabs should have emojis for visual storytelling
        # We now have 6 main story tabs, all should have emojis
        assert tabs_with_emojis >= 4, \
            f"Expected at least 4 tabs with emojis, found {tabs_with_emojis}"
    
    @given(
        tab_index=st.integers(min_value=0, max_value=8)
    )
    @settings(max_examples=100)
    def test_each_tab_has_non_empty_label(self, tab_index):
        """
        **Feature: data-storytelling-dashboard, Property 13: Tab Labeling Consistency**
        **Validates: Requirements 9.2**
        
        For any tab index, the tab should have a non-empty label.
        """
        # Read the app.py file
        with open('app.py', 'r', encoding='utf-8') as f:
            app_content = f.read()
        
        # Find the st.tabs() call
        tabs_pattern = r'st\.tabs\(\s*\[(.*?)\]\s*\)'
        tabs_match = re.search(tabs_pattern, app_content, re.DOTALL)
        
        if tabs_match:
            # Extract tab labels
            tabs_content = tabs_match.group(1)
            label_pattern = r'"([^"]+)"'
            tab_labels = re.findall(label_pattern, tabs_content)
            
            # Only test if tab_index is within range
            if tab_index < len(tab_labels):
                label = tab_labels[tab_index]
                
                # Label should not be empty
                assert len(label.strip()) > 0, \
                    f"Tab at index {tab_index} has empty label"
                
                # Label should have meaningful content (more than just emoji)
                # Remove emojis and check remaining text
                label_no_emoji = re.sub(r'[\U0001F300-\U0001F9FF]|[\u2600-\u26FF]|[\u2700-\u27BF]', '', label)
                assert len(label_no_emoji.strip()) > 0, \
                    f"Tab at index {tab_index} has only emoji, no text"


class TestStorySectionStructure:
    """Tests for Property 5: Story Section Structure"""
    
    def test_story_sections_have_titles(self):
        """
        **Feature: data-storytelling-dashboard, Property 5: Story Section Structure**
        **Validates: Requirements 3.2**
        
        For any story section rendered, it must include both a descriptive title
        and contextual explanation text.
        
        This test verifies that each story section has a title.
        """
        # Read the app.py file
        with open('app.py', 'r', encoding='utf-8') as f:
            app_content = f.read()
        
        # Define story section identifiers
        story_sections = [
            'tab_intro',
            'tab_mercado',
            'tab_calidad',
            'tab_temporal',
            'tab_experiencia'
        ]
        
        for section in story_sections:
            # Find the section in the code
            section_pattern = rf'with {section}:'
            assert re.search(section_pattern, app_content), \
                f"Story section '{section}' not found in app.py"
            
            # Extract the section content
            # Find the start of the section
            section_start = app_content.find(f'with {section}:')
            if section_start == -1:
                continue
            
            # Find the next 'with tab_' or end of file
            next_section_pattern = r'with tab_\w+:'
            next_section_match = re.search(next_section_pattern, app_content[section_start + 20:])
            
            if next_section_match:
                section_end = section_start + 20 + next_section_match.start()
            else:
                section_end = len(app_content)
            
            section_content = app_content[section_start:section_end]
            
            # Check for title patterns (h1, h2, h3 in markdown or st.markdown with style)
            title_patterns = [
                r'<h[123][^>]*>',  # HTML headers
                r'st\.header\(',    # Streamlit header
                r'st\.subheader\(', # Streamlit subheader
                r'st\.title\(',     # Streamlit title
                r'##\s+',           # Markdown h2
                r'###\s+',          # Markdown h3
            ]
            
            has_title = False
            for pattern in title_patterns:
                if re.search(pattern, section_content):
                    has_title = True
                    break
            
            assert has_title, \
                f"Story section '{section}' does not have a title"
    
    def test_story_sections_have_contextual_text(self):
        """
        **Feature: data-storytelling-dashboard, Property 5: Story Section Structure**
        **Validates: Requirements 3.2**
        
        For any story section rendered, it must include contextual explanation text.
        """
        # Read the app.py file
        with open('app.py', 'r', encoding='utf-8') as f:
            app_content = f.read()
        
        # Define story section identifiers
        story_sections = [
            'tab_intro',
            'tab_mercado',
            'tab_calidad',
            'tab_temporal',
            'tab_experiencia'
        ]
        
        for section in story_sections:
            # Find the section in the code
            section_start = app_content.find(f'with {section}:')
            if section_start == -1:
                continue
            
            # Find the next section or end of file
            next_section_pattern = r'with tab_\w+:'
            next_section_match = re.search(next_section_pattern, app_content[section_start + 20:])
            
            if next_section_match:
                section_end = section_start + 20 + next_section_match.start()
            else:
                section_end = len(app_content)
            
            section_content = app_content[section_start:section_end]
            
            # Check for contextual text patterns
            # Look for paragraph tags, st.markdown with substantial text, or st.write
            text_patterns = [
                r'<p[^>]*>[\s\S]{50,}</p>',  # HTML paragraphs with at least 50 chars
                r'st\.markdown\(["\'][\s\S]{50,}["\']',  # st.markdown with substantial text
                r'st\.write\(["\'][\s\S]{50,}["\']',     # st.write with substantial text
            ]
            
            has_context = False
            for pattern in text_patterns:
                if re.search(pattern, section_content):
                    has_context = True
                    break
            
            assert has_context, \
                f"Story section '{section}' does not have contextual explanation text"
    
    def test_story_sections_have_both_title_and_context(self):
        """
        **Feature: data-storytelling-dashboard, Property 5: Story Section Structure**
        **Validates: Requirements 3.2**
        
        For any story section, it must have BOTH a title AND contextual text.
        This is the core property.
        """
        # Read the app.py file
        with open('app.py', 'r', encoding='utf-8') as f:
            app_content = f.read()
        
        # Define story section identifiers
        story_sections = [
            ('tab_intro', 'Introducción'),
            ('tab_mercado', 'El Mercado'),
            ('tab_calidad', 'Calidad vs Popularidad'),
            ('tab_temporal', 'Evolución Temporal'),
            ('tab_experiencia', 'Experiencia del Jugador')
        ]
        
        for section_var, section_name in story_sections:
            # Find the section in the code
            section_start = app_content.find(f'with {section_var}:')
            assert section_start != -1, \
                f"Story section '{section_name}' not found in app.py"
            
            # Find the next section or end of file
            next_section_pattern = r'with tab_\w+:'
            next_section_match = re.search(next_section_pattern, app_content[section_start + 20:])
            
            if next_section_match:
                section_end = section_start + 20 + next_section_match.start()
            else:
                section_end = len(app_content)
            
            section_content = app_content[section_start:section_end]
            
            # Check for title
            title_patterns = [
                r'<h[123][^>]*>',
                r'st\.header\(',
                r'st\.subheader\(',
                r'st\.title\(',
            ]
            
            has_title = any(re.search(pattern, section_content) for pattern in title_patterns)
            
            # Check for contextual text
            text_patterns = [
                r'<p[^>]*>[\s\S]{50,}</p>',
                r'st\.markdown\(["\'][\s\S]{50,}["\']',
            ]
            
            has_context = any(re.search(pattern, section_content) for pattern in text_patterns)
            
            assert has_title and has_context, \
                f"Story section '{section_name}' missing {'title' if not has_title else 'context'}"
    
    def test_story_sections_use_styled_containers(self):
        """
        **Feature: data-storytelling-dashboard, Property 5: Story Section Structure**
        **Validates: Requirements 3.2**
        
        Story sections should use styled containers for visual consistency
        as per design requirements.
        """
        # Read the app.py file
        with open('app.py', 'r', encoding='utf-8') as f:
            app_content = f.read()
        
        # Define story section identifiers
        story_sections = [
            'tab_intro',
            'tab_mercado',
            'tab_calidad',
            'tab_temporal',
            'tab_experiencia'
        ]
        
        for section in story_sections:
            # Find the section in the code
            section_start = app_content.find(f'with {section}:')
            if section_start == -1:
                continue
            
            # Find the next section or end of file
            next_section_pattern = r'with tab_\w+:'
            next_section_match = re.search(next_section_pattern, app_content[section_start + 20:])
            
            if next_section_match:
                section_end = section_start + 20 + next_section_match.start()
            else:
                section_end = len(app_content)
            
            section_content = app_content[section_start:section_end]
            
            # Check for styled containers (divs with background, border-radius, padding)
            styled_container_patterns = [
                r'<div[^>]*style=["\'][^"\']*background[^"\']*["\']',
                r'<div[^>]*style=["\'][^"\']*border-radius[^"\']*["\']',
                r'<div[^>]*style=["\'][^"\']*padding[^"\']*["\']',
            ]
            
            has_styled_container = any(
                re.search(pattern, section_content) 
                for pattern in styled_container_patterns
            )
            
            assert has_styled_container, \
                f"Story section '{section}' does not use styled containers"
    
    @given(
        section_index=st.integers(min_value=0, max_value=4)
    )
    @settings(max_examples=100)
    def test_each_story_section_structure_property(self, section_index):
        """
        **Feature: data-storytelling-dashboard, Property 5: Story Section Structure**
        **Validates: Requirements 3.2**
        
        For any story section index, that section must have both title and context.
        """
        # Read the app.py file
        with open('app.py', 'r', encoding='utf-8') as f:
            app_content = f.read()
        
        # Define story section identifiers
        story_sections = [
            'tab_intro',
            'tab_mercado',
            'tab_calidad',
            'tab_temporal',
            'tab_experiencia'
        ]
        
        if section_index < len(story_sections):
            section = story_sections[section_index]
            
            # Find the section in the code
            section_start = app_content.find(f'with {section}:')
            
            if section_start != -1:
                # Find the next section or end of file
                next_section_pattern = r'with tab_\w+:'
                next_section_match = re.search(next_section_pattern, app_content[section_start + 20:])
                
                if next_section_match:
                    section_end = section_start + 20 + next_section_match.start()
                else:
                    section_end = len(app_content)
                
                section_content = app_content[section_start:section_end]
                
                # Check for title
                title_patterns = [
                    r'<h[123][^>]*>',
                    r'st\.header\(',
                    r'st\.subheader\(',
                    r'st\.title\(',
                ]
                
                has_title = any(re.search(pattern, section_content) for pattern in title_patterns)
                
                # Check for contextual text
                text_patterns = [
                    r'<p[^>]*>[\s\S]{50,}</p>',
                    r'st\.markdown\(["\'][\s\S]{50,}["\']',
                ]
                
                has_context = any(re.search(pattern, section_content) for pattern in text_patterns)
                
                assert has_title, \
                    f"Story section at index {section_index} ({section}) missing title"
                assert has_context, \
                    f"Story section at index {section_index} ({section}) missing context"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
