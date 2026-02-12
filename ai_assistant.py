"""
AI Assistant Module
Integrates Google Gemini for comprehensive chemistry and materials science answers.
"""

import os
from google import genai
from knowledge_base import textbook_kb


class AIAssistant:
    """AI-powered assistant with textbook and chemistry knowledge using Google Gemini."""
    
    def __init__(self):
        self.api_key = os.getenv("GEMINI_API_KEY")
        if self.api_key:
            self.client = genai.Client(api_key=self.api_key)
            self.model = 'gemini-2.5-flash'  # Fast and efficient!
        else:
            self.client = None
            self.model = None
        
    def is_available(self) -> bool:
        """Check if AI assistant is available."""
        return self.client is not None and self.model is not None
    
    def get_relevant_context(self, query: str) -> str:
        """Get relevant context from textbook and chemistry knowledge."""
        context_parts = []
        
        # Search textbook for relevant information
        textbook_result = textbook_kb.smart_search(query)
        if textbook_result:
            context_parts.append(f"=== Materials Science Textbook ===\n{textbook_result[:2000]}")
        
        # Add chemistry context hints based on keywords
        query_lower = query.lower()
        
        if any(word in query_lower for word in ['element', 'atom', 'periodic']):
            context_parts.append("=== Chemistry Context ===\nUser can query elements with 'element: [name]' for detailed info.")
        
        if any(word in query_lower for word in ['compound', 'molecule', 'chemical formula']):
            context_parts.append("=== Chemistry Context ===\nUser can query compounds with 'compound: [name]' from PubChem database.")
        
        if any(word in query_lower for word in ['molar mass', 'molecular weight']):
            context_parts.append("=== Chemistry Context ===\nUser can calculate molar mass with 'mass: [formula]'.")
        
        if any(word in query_lower for word in ['calculate', 'solve', 'problem', 'solution', 'moles', 'grams']):
            context_parts.append("""=== Calculator Available ===
The chatbot has advanced calculators:
- Stoichiometry: moles_to_grams, grams_to_moles, moles_to_molecules
- Solutions: molarity, dilution (M1V1=M2V2)
- pH: calculate pH from H+ or OH- concentrations
- Gas Laws: ideal_gas (PV=nRT), combined_gas
- Composition: percent_composition, limiting_reactant

Format: calc: type | param=value | param2=value""")
        
        return "\n\n".join(context_parts) if context_parts else ""
    
    def generate_response(self, user_message: str, conversation_history: list = None) -> str:
        """Generate AI response with context from textbook and chemistry knowledge."""
        if not self.is_available():
            return None  # Fall back to basic responses
        
        try:
            # Get relevant context
            context = self.get_relevant_context(user_message)
            
            # Build system prompt
            system_prompt = """You are Chemistry Chatbot RGB 🧪, an expert chemistry and materials science assistant.

You have access to:
1. A comprehensive Materials Science & Engineering textbook (Callister 8th Edition)
2. Chemistry databases for elements and compounds
3. Advanced calculators for stoichiometry, solutions, pH, gas laws, etc.

Your role:
- Provide clear, accurate, and COMPLETE answers to chemistry and materials science questions
- Use the textbook context when available to give detailed explanations
- Explain concepts in an educational and encouraging way
- When appropriate, suggest using the chatbot's built-in tools (element:, compound:, mass:, calc:)
- Use emojis to make learning engaging
- If calculations are needed, show the setup and guide users to use the calc: commands
- Keep responses concise but complete (3-5 sentences for simple questions, more for complex ones)
- Remember previous messages in the conversation and provide contextual responses

Always be accurate and educational."""

            # Add context if available
            if context:
                system_prompt += f"\n\n=== AVAILABLE CONTEXT ===\n{context}"
            
            # Build conversation context with history
            conversation_text = f"{system_prompt}\n\n"
            
            # Add conversation history if available
            if conversation_history and len(conversation_history) > 1:
                conversation_text += "=== Conversation History ===\n"
                # Include last few exchanges for context (skip the current message)
                for msg in conversation_history[-6:-1]:  # Last 3 exchanges
                    role = msg.get('role', 'user')
                    content = msg.get('content', '')
                    if role == 'user':
                        conversation_text += f"User: {content}\n"
                    else:
                        # Strip HTML tags for cleaner context
                        import re
                        clean_content = re.sub('<[^<]+?>', '', content)
                        conversation_text += f"Assistant: {clean_content}\n"
                conversation_text += "\n"
            
            # Add current question
            conversation_text += f"=== Current Question ===\nUser: {user_message}\n\nProvide a complete, helpful answer:"
            
            # Generate response
            response = self.client.models.generate_content(
                model=self.model,
                contents=conversation_text
            )
            
            return response.text
            
        except Exception as e:
            print(f"AI Error: {e}")
            return None  # Fall back to basic responses
    
    def generate_calculation_explanation(self, calc_type: str, result: dict) -> str:
        """Generate a natural language explanation of calculation results."""
        if not self.is_available():
            return None
        
        try:
            prompt = f"""Explain this chemistry calculation result in 2-3 sentences.
Be educational and encouraging. Use emojis.

Calculation Type: {calc_type}
Result: {result}

Provide a brief, friendly explanation of what this result means."""

            response = self.client.models.generate_content(
                model=self.model,
                contents=prompt
            )
            
            return response.text
            
        except Exception as e:
            print(f"AI Explanation Error: {e}")
            return None


# Global instance
ai_assistant = AIAssistant()
