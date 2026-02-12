"""
Knowledge Base Module for Materials Science Textbook Integration
Provides search and retrieval functionality for the materials science textbook.
"""

import os
import re
from typing import List, Dict, Optional

class TextbookKnowledgeBase:
    def __init__(self, textbook_path: str = "materials-science-textbook.txt"):
        """Initialize the knowledge base with the textbook."""
        self.textbook_path = textbook_path
        self.content = None
        self.load_textbook()
    
    def load_textbook(self):
        """Load the textbook content into memory."""
        try:
            if os.path.exists(self.textbook_path):
                with open(self.textbook_path, 'r', encoding='utf-8', errors='ignore') as f:
                    self.content = f.read()
                print(f"✅ Loaded textbook: {len(self.content)} characters")
            else:
                print(f"⚠️ Textbook not found at {self.textbook_path}")
                self.content = ""
        except Exception as e:
            print(f"❌ Error loading textbook: {e}")
            self.content = ""
    
    def search_keyword(self, keyword: str, context_lines: int = 5, max_results: int = 3) -> List[Dict[str, str]]:
        """
        Search for a keyword in the textbook and return relevant excerpts.
        
        Args:
            keyword: The search term
            context_lines: Number of lines to include before and after the match
            max_results: Maximum number of results to return
            
        Returns:
            List of dictionaries containing matched excerpts and context
        """
        if not self.content:
            return []
        
        results = []
        lines = self.content.split('\n')
        keyword_lower = keyword.lower()
        
        for i, line in enumerate(lines):
            if keyword_lower in line.lower():
                # Get context around the match
                start = max(0, i - context_lines)
                end = min(len(lines), i + context_lines + 1)
                context = '\n'.join(lines[start:end])
                
                results.append({
                    'line_number': i + 1,
                    'matched_line': line.strip(),
                    'context': context.strip()
                })
                
                if len(results) >= max_results:
                    break
        
        return results
    
    def search_topics(self, topics: List[str]) -> Dict[str, List[Dict]]:
        """
        Search for multiple topics and return organized results.
        
        Args:
            topics: List of topic keywords to search
            
        Returns:
            Dictionary mapping topics to their search results
        """
        topic_results = {}
        for topic in topics:
            results = self.search_keyword(topic, context_lines=3, max_results=2)
            if results:
                topic_results[topic] = results
        return topic_results
    
    def find_section(self, section_name: str) -> Optional[str]:
        """
        Find a specific section or chapter in the textbook.
        
        Args:
            section_name: Name of the section to find
            
        Returns:
            The section content or None if not found
        """
        if not self.content:
            return None
        
        # Look for section headers (common patterns)
        patterns = [
            rf"(?i)^{re.escape(section_name)}\s*$",
            rf"(?i)^Chapter.*{re.escape(section_name)}",
            rf"(?i)^Section.*{re.escape(section_name)}",
        ]
        
        lines = self.content.split('\n')
        for i, line in enumerate(lines):
            for pattern in patterns:
                if re.search(pattern, line):
                    # Return the next 20 lines as the section content
                    end = min(len(lines), i + 20)
                    return '\n'.join(lines[i:end])
        
        return None
    
    def get_material_properties(self, material: str) -> Optional[str]:
        """
        Search for properties of a specific material.
        
        Args:
            material: Name of the material to look up
            
        Returns:
            Information about the material's properties
        """
        # Search for material with key property terms
        property_terms = ['density', 'strength', 'modulus', 'hardness', 'structure']
        results = []
        
        lines = self.content.split('\n')
        material_lower = material.lower()
        
        for i, line in enumerate(lines):
            if material_lower in line.lower():
                # Check if any property terms are nearby
                context_start = max(0, i - 2)
                context_end = min(len(lines), i + 3)
                context_lines = lines[context_start:context_end]
                context_text = ' '.join(context_lines).lower()
                
                if any(term in context_text for term in property_terms):
                    results.append('\n'.join(context_lines))
                    if len(results) >= 2:
                        break
        
        return '\n\n---\n\n'.join(results) if results else None
    
    def smart_search(self, query: str) -> Optional[str]:
        """
        Perform an intelligent search based on the query content.
        
        Args:
            query: User's question or search query
            
        Returns:
            Relevant excerpt from the textbook
        """
        if not self.content:
            return None
        
        # Extract key terms from query (remove common words)
        stop_words = {'what', 'is', 'are', 'the', 'a', 'an', 'how', 'why', 'when', 
                      'where', 'which', 'about', 'of', 'in', 'on', 'to', 'for'}
        
        words = query.lower().split()
        keywords = [w for w in words if w not in stop_words and len(w) > 2]
        
        if not keywords:
            return None
        
        # Search for the most relevant keyword
        for keyword in keywords:
            results = self.search_keyword(keyword, context_lines=5, max_results=1)
            if results:
                return results[0]['context']
        
        return None
    
    def format_response(self, search_results: List[Dict], query: str) -> str:
        """
        Format search results into a readable chatbot response.
        
        Args:
            search_results: List of search result dictionaries
            query: The original query
            
        Returns:
            Formatted HTML response for the chatbot
        """
        if not search_results:
            return None
        
        response = f"📚 <b>From Materials Science Textbook:</b><br><br>"
        
        for i, result in enumerate(search_results[:2], 1):  # Limit to 2 results
            excerpt = result['context'][:500]  # Limit excerpt length
            response += f"{excerpt}<br><br>"
            if i < len(search_results) and i < 2:
                response += "---<br><br>"
        
        return response.strip()


# Global instance for easy import
textbook_kb = TextbookKnowledgeBase()
