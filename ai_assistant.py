"""
AI Assistant Module
Integrates OpenAI for comprehensive chemistry and materials science answers.
"""

import os
from openai import OpenAI
from knowledge_base import textbook_kb


class AIAssistant:
    """AI-powered assistant with textbook and chemistry knowledge."""
    
    def __init__(self):
        self.api_key = os.getenv("OPENAI_API_KEY")
        self.client = OpenAI(api_key=self.api_key) if self.api_key else None
        self.model = "gpt-4o-mini"  # Fast and cost-effective
        
    def is_available(self) -> bool:
        """Check if AI assistant is available."""
        return self.client is not None
    
    def get_relevant_context(self, query: str) -> str:
        """Get relevant context from textbook and chemistry knowledge."""
        context_parts = []
        
        # Search textbook for relevant information
        textbook_result = textbook_kb.smart_search(query)
        if textbook_result:
            context_parts.append(f"=== Materials Science Textbook ===\n{textbook_result[:1500]}")
        
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
- Provide clear, accurate, and complete answers to chemistry and materials science questions
- Use the textbook context when available to give detailed explanations
- Explain concepts in an educational and encouraging way
- When appropriate, suggest using the chatbot's built-in tools (element:, compound:, mass:, calc:)
- Use emojis to make learning engaging
- If calculations are needed, show the setup and guide users to use the calc: commands

Always be accurate and cite when information comes from the textbook."""

            # Add context if available
            if context:
                system_prompt += f"\n\n=== AVAILABLE CONTEXT ===\n{context}"
            
            # Build messages
            messages = [{"role": "system", "content": system_prompt}]
            
            # Add conversation history if provided
            if conversation_history:
                messages.extend(conversation_history[-6:])  # Last 3 exchanges
            
            # Add current user message
            messages.append({"role": "user", "content": user_message})
            
            # Generate response
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=0.7,
                max_tokens=800
            )
            
            return response.choices[0].message.content
            
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

            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7,
                max_tokens=200
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            print(f"AI Explanation Error: {e}")
            return None


# Global instance
ai_assistant = AIAssistant()
