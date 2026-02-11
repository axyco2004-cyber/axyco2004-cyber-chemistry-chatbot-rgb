import json
from http.server import BaseHTTPRequestHandler
import re

# Periodic table data
PERIODIC_TABLE = {
    "H": {"name": "Hydrogen", "number": 1, "mass": 1.008, "category": "Nonmetal"},
    "He": {"name": "Helium", "number": 2, "mass": 4.003, "category": "Noble gas"},
    "Li": {"name": "Lithium", "number": 3, "mass": 6.941, "category": "Alkali metal"},
    "Be": {"name": "Beryllium", "number": 4, "mass": 9.012, "category": "Alkaline earth metal"},
    "B": {"name": "Boron", "number": 5, "mass": 10.81, "category": "Metalloid"},
    "C": {"name": "Carbon", "number": 6, "mass": 12.01, "category": "Nonmetal"},
    "N": {"name": "Nitrogen", "number": 7, "mass": 14.01, "category": "Nonmetal"},
    "O": {"name": "Oxygen", "number": 8, "mass": 16.00, "category": "Nonmetal"},
    "F": {"name": "Fluorine", "number": 9, "mass": 19.00, "category": "Halogen"},
    "Ne": {"name": "Neon", "number": 10, "mass": 20.18, "category": "Noble gas"},
    "Na": {"name": "Sodium", "number": 11, "mass": 22.99, "category": "Alkali metal"},
    "Mg": {"name": "Magnesium", "number": 12, "mass": 24.31, "category": "Alkaline earth metal"},
    "Al": {"name": "Aluminum", "number": 13, "mass": 26.98, "category": "Post-transition metal"},
    "Si": {"name": "Silicon", "number": 14, "mass": 28.09, "category": "Metalloid"},
    "P": {"name": "Phosphorus", "number": 15, "mass": 30.97, "category": "Nonmetal"},
    "S": {"name": "Sulfur", "number": 16, "mass": 32.07, "category": "Nonmetal"},
    "Cl": {"name": "Chlorine", "number": 17, "mass": 35.45, "category": "Halogen"},
    "Ar": {"name": "Argon", "number": 18, "mass": 39.95, "category": "Noble gas"},
    "K": {"name": "Potassium", "number": 19, "mass": 39.10, "category": "Alkali metal"},
    "Ca": {"name": "Calcium", "number": 20, "mass": 40.08, "category": "Alkaline earth metal"},
    "Fe": {"name": "Iron", "number": 26, "mass": 55.85, "category": "Transition metal"},
    "Cu": {"name": "Copper", "number": 29, "mass": 63.55, "category": "Transition metal"},
    "Zn": {"name": "Zinc", "number": 30, "mass": 65.38, "category": "Transition metal"},
    "Ag": {"name": "Silver", "number": 47, "mass": 107.87, "category": "Transition metal"},
    "Au": {"name": "Gold", "number": 79, "mass": 196.97, "category": "Transition metal"},
    "Hg": {"name": "Mercury", "number": 80, "mass": 200.59, "category": "Transition metal"},
    "Pb": {"name": "Lead", "number": 82, "mass": 207.2, "category": "Post-transition metal"},
    "U": {"name": "Uranium", "number": 92, "mass": 238.03, "category": "Actinide"},
}

# Common chemical reactions
REACTIONS = {
    "combustion": "Combustion reactions involve a substance reacting with oxygen to produce heat and light. General form: Fuel + O₂ → CO₂ + H₂O",
    "synthesis": "Synthesis reactions combine simpler substances to form a more complex compound. General form: A + B → AB",
    "decomposition": "Decomposition reactions break down a compound into simpler substances. General form: AB → A + B",
    "displacement": "Single displacement reactions occur when one element replaces another in a compound. General form: A + BC → AC + B",
    "double displacement": "Double displacement reactions involve the exchange of ions between two compounds. General form: AB + CD → AD + CB",
    "acid-base": "Acid-base reactions (neutralization) occur when an acid reacts with a base to produce salt and water. General form: Acid + Base → Salt + Water",
}


def calculate_molar_mass(formula):
    """Calculate molar mass of a simple chemical formula."""
    total_mass = 0
    i = 0
    while i < len(formula):
        # Match element symbol (uppercase followed by optional lowercase)
        if formula[i].isupper():
            element = formula[i]
            i += 1
            if i < len(formula) and formula[i].islower():
                element += formula[i]
                i += 1
            
            # Match count (optional number)
            count = ""
            while i < len(formula) and formula[i].isdigit():
                count += formula[i]
                i += 1
            
            count = int(count) if count else 1
            
            if element in PERIODIC_TABLE:
                total_mass += PERIODIC_TABLE[element]["mass"] * count
            else:
                return None
    
    return round(total_mass, 2) if total_mass > 0 else None


def get_element_info(element_symbol):
    """Get information about an element."""
    element_symbol = element_symbol.capitalize()
    if len(element_symbol) > 1:
        element_symbol = element_symbol[0].upper() + element_symbol[1:].lower()
    
    if element_symbol in PERIODIC_TABLE:
        elem = PERIODIC_TABLE[element_symbol]
        return f"{elem['name']} ({element_symbol}) - Atomic Number: {elem['number']}, Atomic Mass: {elem['mass']} u, Category: {elem['category']}"
    
    # Try to find by name
    for symbol, data in PERIODIC_TABLE.items():
        if data["name"].lower() == element_symbol.lower():
            return f"{data['name']} ({symbol}) - Atomic Number: {data['number']}, Atomic Mass: {data['mass']} u, Category: {data['category']}"
    
    return None


ELEMENT_QUERY_TRIGGERS = ["tell me about", "what is", "info about", "information about"]


def process_chemistry_query(message):
    """Process chemistry-related queries and return appropriate responses."""
    message_lower = message.lower()
    
    # Greeting responses
    if any(word in message_lower for word in ["hello", "hi", "hey", "greetings"]):
        return "Hello! I'm your chemistry chatbot. I can help you with chemistry questions, element information, molar mass calculations, and explain chemical reactions. What would you like to know?"
    
    # Help request
    if "help" in message_lower or "what can you do" in message_lower:
        return """I can assist you with:
        
🔬 Element information - Ask about any element (e.g., "Tell me about Carbon")
⚗️ Molar mass calculations - Calculate molecular mass (e.g., "Molar mass of H2O")
📊 Chemical reactions - Explain reaction types (combustion, synthesis, etc.)
🧪 Chemistry concepts - Answer general chemistry questions
⚛️ Periodic table data - Get atomic numbers, masses, and categories

Try asking me something like "What is the atomic mass of Gold?" or "Calculate molar mass of NaCl"!"""
    
    # Element information queries
    if "element" in message_lower or "atomic" in message_lower or any(word in message_lower for word in ELEMENT_QUERY_TRIGGERS):
        # First check for element names (more specific)
        for symbol, data in PERIODIC_TABLE.items():
            element_name = data["name"].lower()
            # Use word boundary matching for element names
            if re.search(r'\b' + re.escape(element_name) + r'\b', message_lower):
                return get_element_info(symbol)
        
        # Then check for element symbols (with word boundaries for short symbols)
        for symbol in PERIODIC_TABLE.keys():
            # For single-letter symbols, require word boundaries
            if len(symbol) == 1:
                if re.search(r'\b' + symbol.lower() + r'\b', message_lower):
                    return get_element_info(symbol)
            else:
                # For multi-letter symbols, simple substring is okay
                if symbol.lower() in message_lower:
                    return get_element_info(symbol)
    
    # Molar mass calculation
    if "molar mass" in message_lower or "molecular mass" in message_lower or "molecular weight" in message_lower:
        # Extract formula using regex
        formula_match = re.search(r'of\s+([A-Z][a-z]?\d*(?:[A-Z][a-z]?\d*)*)', message)
        if formula_match:
            formula = formula_match.group(1)
            mass = calculate_molar_mass(formula)
            if mass:
                return f"The molar mass of {formula} is {mass} g/mol"
            else:
                return f"I couldn't calculate the molar mass for {formula}. Please check the formula and try again."
    
    # Chemical reactions
    for reaction_type, description in REACTIONS.items():
        if reaction_type in message_lower:
            return description
    
    if "reaction" in message_lower and "types" in message_lower:
        return "There are several main types of chemical reactions:\n\n" + "\n\n".join([f"• {k.title()}: {v}" for k, v in REACTIONS.items()])
    
    # Balancing equations
    if "balance" in message_lower and "equation" in message_lower:
        return """To balance a chemical equation:

1. Write the unbalanced equation
2. Count atoms of each element on both sides
3. Add coefficients to balance each element
4. Check that all atoms are balanced
5. Simplify coefficients if possible

Example: H₂ + O₂ → H₂O
Balanced: 2H₂ + O₂ → 2H₂O

Would you like help balancing a specific equation?"""
    
    # pH and acids/bases
    if "ph" in message_lower or "acid" in message_lower or "base" in message_lower:
        if "scale" in message_lower or "what is ph" in message_lower:
            return "pH is a measure of acidity or basicity. The pH scale ranges from 0-14:\n• pH < 7: Acidic\n• pH = 7: Neutral\n• pH > 7: Basic (alkaline)\n\nThe pH is calculated as -log[H⁺], where [H⁺] is the hydrogen ion concentration."
    
    # Periodic table
    if "periodic table" in message_lower:
        return f"The periodic table organizes all known chemical elements by atomic number and properties. I have information on {len(PERIODIC_TABLE)} elements. You can ask me about specific elements like 'Tell me about Oxygen' or 'What is the atomic mass of Iron?'"
    
    # States of matter
    if "states of matter" in message_lower or "phases of matter" in message_lower:
        return "The main states of matter are:\n\n• Solid: Fixed shape and volume, particles are tightly packed\n• Liquid: Fixed volume but takes shape of container, particles flow freely\n• Gas: No fixed shape or volume, particles move rapidly\n• Plasma: Ionized gas at very high temperatures"
    
    # Chemical bonds
    if "chemical bond" in message_lower or "bonding" in message_lower:
        if "ionic" in message_lower:
            return "Ionic bonds form when electrons are transferred from one atom to another, creating oppositely charged ions that attract each other. Common in compounds between metals and nonmetals (e.g., NaCl)."
        elif "covalent" in message_lower:
            return "Covalent bonds form when atoms share electrons. They're common between nonmetals (e.g., H₂O, CO₂). Can be single, double, or triple bonds depending on the number of shared electron pairs."
        elif "metallic" in message_lower:
            return "Metallic bonds occur in metals where electrons are delocalized in a 'sea' around metal cations, allowing metals to conduct electricity and be malleable."
        else:
            return "There are three main types of chemical bonds:\n\n• Ionic: Transfer of electrons (e.g., NaCl)\n• Covalent: Sharing of electrons (e.g., H₂O)\n• Metallic: Delocalized electrons in metals (e.g., Fe, Cu)"
    
    # Avogadro's number
    if "avogadro" in message_lower:
        return "Avogadro's number is 6.022 × 10²³, representing the number of particles (atoms, molecules, ions) in one mole of a substance. This fundamental constant connects the atomic scale to the macroscopic scale."
    
    # Default response
    return "I'm here to help with chemistry! You can ask me about elements, calculate molar masses, learn about chemical reactions, or explore chemistry concepts. Try asking specific questions like 'What is the atomic number of Carbon?' or 'Explain combustion reactions.'"


class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        """Handle POST requests to the chatbot API."""
        try:
            # Read the request body
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length)
            data = json.loads(body.decode('utf-8'))
            
            # Extract the message
            message = data.get('message', '').strip()
            
            if not message:
                response = {"error": "No message provided"}
                status_code = 400
            else:
                # Process the chemistry query
                reply = process_chemistry_query(message)
                response = {"reply": reply}
                status_code = 200
            
            # Send response
            self.send_response(status_code)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
            self.send_header('Access-Control-Allow-Headers', 'Content-Type')
            self.end_headers()
            
            self.wfile.write(json.dumps(response).encode('utf-8'))
            
        except json.JSONDecodeError:
            self.send_response(400)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps({"error": "Invalid JSON"}).encode('utf-8'))
            
        except Exception as e:
            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps({"error": str(e)}).encode('utf-8'))
    
    def do_OPTIONS(self):
        """Handle CORS preflight requests."""
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
