#!/usr/bin/env python3
"""
Chemistry Chatbot RGB - An interactive chemistry learning assistant
"""

import re
import sys
from colorama import Fore, Style, init

# Initialize colorama for colored terminal output
init(autoreset=True)


# Built-in periodic table data (33 common elements)
PERIODIC_TABLE = {
    "H": {
        "name": "Hydrogen",
        "atomic_number": 1,
        "symbol": "H",
        "atomic_mass": 1.008,
        "category": "Nonmetal",
        "description": "The lightest and most abundant element in the universe."
    },
    "He": {
        "name": "Helium",
        "atomic_number": 2,
        "symbol": "He",
        "atomic_mass": 4.003,
        "category": "Noble Gas",
        "description": "A colorless, odorless, tasteless noble gas."
    },
    "Li": {
        "name": "Lithium",
        "atomic_number": 3,
        "symbol": "Li",
        "atomic_mass": 6.941,
        "category": "Alkali Metal",
        "description": "A soft, silvery-white alkali metal used in batteries."
    },
    "Be": {
        "name": "Beryllium",
        "atomic_number": 4,
        "symbol": "Be",
        "atomic_mass": 9.012,
        "category": "Alkaline Earth Metal",
        "description": "A lightweight, strong metal used in aerospace applications."
    },
    "B": {
        "name": "Boron",
        "atomic_number": 5,
        "symbol": "B",
        "atomic_mass": 10.81,
        "category": "Metalloid",
        "description": "A metalloid used in glass and ceramic production."
    },
    "C": {
        "name": "Carbon",
        "atomic_number": 6,
        "symbol": "C",
        "atomic_mass": 12.01,
        "category": "Nonmetal",
        "description": "The basis of organic chemistry and all life on Earth."
    },
    "N": {
        "name": "Nitrogen",
        "atomic_number": 7,
        "symbol": "N",
        "atomic_mass": 14.01,
        "category": "Nonmetal",
        "description": "Makes up about 78% of Earth's atmosphere."
    },
    "O": {
        "name": "Oxygen",
        "atomic_number": 8,
        "symbol": "O",
        "atomic_mass": 16.00,
        "category": "Nonmetal",
        "description": "Essential for respiration and combustion."
    },
    "F": {
        "name": "Fluorine",
        "atomic_number": 9,
        "symbol": "F",
        "atomic_mass": 19.00,
        "category": "Halogen",
        "description": "The most reactive and electronegative element."
    },
    "Ne": {
        "name": "Neon",
        "atomic_number": 10,
        "symbol": "Ne",
        "atomic_mass": 20.18,
        "category": "Noble Gas",
        "description": "A noble gas used in neon signs and lighting."
    },
    "Na": {
        "name": "Sodium",
        "atomic_number": 11,
        "symbol": "Na",
        "atomic_mass": 22.99,
        "category": "Alkali Metal",
        "description": "A highly reactive metal, essential for life."
    },
    "Mg": {
        "name": "Magnesium",
        "atomic_number": 12,
        "symbol": "Mg",
        "atomic_mass": 24.31,
        "category": "Alkaline Earth Metal",
        "description": "A lightweight structural metal used in alloys."
    },
    "Al": {
        "name": "Aluminum",
        "atomic_number": 13,
        "symbol": "Al",
        "atomic_mass": 26.98,
        "category": "Metal",
        "description": "A lightweight, corrosion-resistant metal."
    },
    "Si": {
        "name": "Silicon",
        "atomic_number": 14,
        "symbol": "Si",
        "atomic_mass": 28.09,
        "category": "Metalloid",
        "description": "The second most abundant element in Earth's crust."
    },
    "P": {
        "name": "Phosphorus",
        "atomic_number": 15,
        "symbol": "P",
        "atomic_mass": 30.97,
        "category": "Nonmetal",
        "description": "Essential for DNA, RNA, and ATP in living organisms."
    },
    "S": {
        "name": "Sulfur",
        "atomic_number": 16,
        "symbol": "S",
        "atomic_mass": 32.07,
        "category": "Nonmetal",
        "description": "A yellow element used in fertilizers and chemicals."
    },
    "Cl": {
        "name": "Chlorine",
        "atomic_number": 17,
        "symbol": "Cl",
        "atomic_mass": 35.45,
        "category": "Halogen",
        "description": "A reactive halogen used in water purification."
    },
    "Ar": {
        "name": "Argon",
        "atomic_number": 18,
        "symbol": "Ar",
        "atomic_mass": 39.95,
        "category": "Noble Gas",
        "description": "An inert gas used in welding and lighting."
    },
    "K": {
        "name": "Potassium",
        "atomic_number": 19,
        "symbol": "K",
        "atomic_mass": 39.10,
        "category": "Alkali Metal",
        "description": "An essential nutrient for plant and animal life."
    },
    "Ca": {
        "name": "Calcium",
        "atomic_number": 20,
        "symbol": "Ca",
        "atomic_mass": 40.08,
        "category": "Alkaline Earth Metal",
        "description": "Essential for bones, teeth, and cellular processes."
    },
    "Fe": {
        "name": "Iron",
        "atomic_number": 26,
        "symbol": "Fe",
        "atomic_mass": 55.85,
        "category": "Transition Metal",
        "description": "The most common element on Earth by mass."
    },
    "Cu": {
        "name": "Copper",
        "atomic_number": 29,
        "symbol": "Cu",
        "atomic_mass": 63.55,
        "category": "Transition Metal",
        "description": "An excellent conductor used in electrical wiring."
    },
    "Zn": {
        "name": "Zinc",
        "atomic_number": 30,
        "symbol": "Zn",
        "atomic_mass": 65.39,
        "category": "Transition Metal",
        "description": "Used in galvanization and as a nutritional supplement."
    },
    "Ag": {
        "name": "Silver",
        "atomic_number": 47,
        "symbol": "Ag",
        "atomic_mass": 107.87,
        "category": "Transition Metal",
        "description": "A precious metal with the highest electrical conductivity."
    },
    "Au": {
        "name": "Gold",
        "atomic_number": 79,
        "symbol": "Au",
        "atomic_mass": 196.97,
        "category": "Transition Metal",
        "description": "A precious metal valued for its beauty and rarity."
    },
    "Hg": {
        "name": "Mercury",
        "atomic_number": 80,
        "symbol": "Hg",
        "atomic_mass": 200.59,
        "category": "Transition Metal",
        "description": "The only metal that is liquid at room temperature."
    },
    "Pb": {
        "name": "Lead",
        "atomic_number": 82,
        "symbol": "Pb",
        "atomic_mass": 207.2,
        "category": "Metal",
        "description": "A heavy, dense metal historically used in plumbing."
    },
    "Br": {
        "name": "Bromine",
        "atomic_number": 35,
        "symbol": "Br",
        "atomic_mass": 79.90,
        "category": "Halogen",
        "description": "One of only two elements that is liquid at room temperature."
    },
    "I": {
        "name": "Iodine",
        "atomic_number": 53,
        "symbol": "I",
        "atomic_mass": 126.90,
        "category": "Halogen",
        "description": "Essential for thyroid function in humans."
    },
    "Kr": {
        "name": "Krypton",
        "atomic_number": 36,
        "symbol": "Kr",
        "atomic_mass": 83.80,
        "category": "Noble Gas",
        "description": "A noble gas used in some types of lighting."
    },
    "Xe": {
        "name": "Xenon",
        "atomic_number": 54,
        "symbol": "Xe",
        "atomic_mass": 131.29,
        "category": "Noble Gas",
        "description": "A noble gas used in flash lamps and ion propulsion."
    },
    "Mn": {
        "name": "Manganese",
        "atomic_number": 25,
        "symbol": "Mn",
        "atomic_mass": 54.94,
        "category": "Transition Metal",
        "description": "Used in steel production and as an alloy."
    },
    "Ni": {
        "name": "Nickel",
        "atomic_number": 28,
        "symbol": "Ni",
        "atomic_mass": 58.69,
        "category": "Transition Metal",
        "description": "Used in stainless steel and rechargeable batteries."
    }
}


# Chemistry Q&A knowledge base
CHEMISTRY_QA = {
    "ph": {
        "question": "What is pH?",
        "answer": "pH is a measure of how acidic or basic a solution is. It ranges from 0 to 14, with 7 being neutral. Values below 7 are acidic, and values above 7 are basic (alkaline). The pH scale is logarithmic, meaning each unit represents a tenfold difference in acidity."
    },
    "avogadro": {
        "question": "What is Avogadro's number?",
        "answer": "Avogadro's number is 6.022 × 10²³, which represents the number of particles (atoms, molecules, ions, etc.) in one mole of a substance. It's a fundamental constant in chemistry named after Amedeo Avogadro."
    },
    "states of matter": {
        "question": "What are the states of matter?",
        "answer": "The common states of matter are: solid (fixed shape and volume), liquid (fixed volume but variable shape), gas (variable shape and volume), and plasma (ionized gas at very high temperatures). There are also more exotic states like Bose-Einstein condensates."
    },
    "ionic bond": {
        "question": "What is an ionic bond?",
        "answer": "An ionic bond is a chemical bond formed through the electrostatic attraction between oppositely charged ions. It typically forms between a metal (which loses electrons) and a nonmetal (which gains electrons)."
    },
    "covalent bond": {
        "question": "What is a covalent bond?",
        "answer": "A covalent bond is a chemical bond formed when two atoms share one or more pairs of electrons. This type of bonding typically occurs between nonmetal atoms."
    },
    "mole": {
        "question": "What is a mole?",
        "answer": "A mole is a unit of measurement in chemistry that represents 6.022 × 10²³ particles (Avogadro's number). It's used to measure amounts of substances and is abbreviated as 'mol'."
    },
    "acid": {
        "question": "What is an acid?",
        "answer": "An acid is a substance that donates hydrogen ions (H⁺) or protons when dissolved in water. Acids have a pH less than 7 and taste sour. Examples include hydrochloric acid (HCl) and acetic acid (CH₃COOH)."
    },
    "base": {
        "question": "What is a base?",
        "answer": "A base is a substance that accepts hydrogen ions (H⁺) or donates hydroxide ions (OH⁻) when dissolved in water. Bases have a pH greater than 7 and feel slippery. Examples include sodium hydroxide (NaOH) and ammonia (NH₃)."
    },
    "catalyst": {
        "question": "What is a catalyst?",
        "answer": "A catalyst is a substance that increases the rate of a chemical reaction without being consumed in the process. It works by lowering the activation energy required for the reaction to occur."
    },
    "oxidation": {
        "question": "What is oxidation?",
        "answer": "Oxidation is a chemical process in which an atom, ion, or molecule loses electrons. It's often associated with the addition of oxygen or the removal of hydrogen. Oxidation always occurs with reduction in redox reactions."
    }
}


class ChemistryChatbot:
    """Main chatbot class for handling chemistry queries"""
    
    def __init__(self):
        self.running = True
    
    def greet(self):
        """Display welcome message"""
        print(f"\n{Fore.CYAN}{'=' * 70}")
        print(f"{Fore.MAGENTA}{Style.BRIGHT}🧪 Welcome to Chemistry Chatbot RGB! 🧪")
        print(f"{Fore.CYAN}{'=' * 70}{Style.RESET_ALL}\n")
        
        print(f"{Fore.GREEN}I can help you with:")
        print(f"{Fore.YELLOW}  🔬 Element lookups (e.g., 'tell me about Oxygen', 'what is Carbon')")
        print(f"{Fore.YELLOW}  ⚗️  Chemical equation balancing (e.g., 'balance H2 + O2 -> H2O')")
        print(f"{Fore.YELLOW}  📊 Molar mass calculations (e.g., 'molar mass of H2O', 'mass of NaCl')")
        print(f"{Fore.YELLOW}  💡 General chemistry questions (e.g., 'what is pH', 'what is Avogadro's number')")
        print(f"{Fore.RED}\nType 'quit', 'exit', or 'bye' to leave.\n{Style.RESET_ALL}")
    
    def find_element(self, query):
        """Find an element based on name or symbol"""
        query_lower = query.lower()
        
        # Search by symbol (case-insensitive)
        for symbol, data in PERIODIC_TABLE.items():
            if symbol.lower() == query_lower:
                return data
        
        # Search by name
        for symbol, data in PERIODIC_TABLE.items():
            if data["name"].lower() == query_lower:
                return data
        
        return None
    
    def handle_element_query(self, query):
        """Handle element lookup queries"""
        # Extract element name from query
        query = query.lower()
        words = query.split()
        
        # Look for element names in the query
        for word in words:
            element = self.find_element(word)
            if element:
                self.display_element_info(element)
                return True
        
        # Check if query contains "atomic number of"
        if "atomic number" in query:
            for symbol, data in PERIODIC_TABLE.items():
                if data["name"].lower() in query or symbol.lower() in query:
                    print(f"{Fore.GREEN}The atomic number of {data['name']} ({data['symbol']}) is {data['atomic_number']}.{Style.RESET_ALL}")
                    return True
        
        return False
    
    def display_element_info(self, element):
        """Display detailed information about an element"""
        print(f"\n{Fore.CYAN}{'─' * 60}")
        print(f"{Fore.MAGENTA}{Style.BRIGHT}Element: {element['name']} ({element['symbol']})")
        print(f"{Fore.CYAN}{'─' * 60}{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}Atomic Number: {Fore.WHITE}{element['atomic_number']}")
        print(f"{Fore.YELLOW}Atomic Mass: {Fore.WHITE}{element['atomic_mass']} u")
        print(f"{Fore.YELLOW}Category: {Fore.WHITE}{element['category']}")
        print(f"{Fore.YELLOW}Description: {Fore.WHITE}{element['description']}")
        print(f"{Fore.CYAN}{'─' * 60}{Style.RESET_ALL}\n")
    
    def calculate_molar_mass(self, formula):
        """Calculate the molar mass of a chemical formula"""
        try:
            # Parse the chemical formula
            # Pattern to match element symbols and their counts
            pattern = r'([A-Z][a-z]?)(\d*)'
            matches = re.findall(pattern, formula)
            
            if not matches:
                return None
            
            total_mass = 0.0
            composition = []
            
            for element_symbol, count in matches:
                if element_symbol in PERIODIC_TABLE:
                    count = int(count) if count else 1
                    mass = PERIODIC_TABLE[element_symbol]["atomic_mass"] * count
                    total_mass += mass
                    composition.append(f"{element_symbol}: {count} × {PERIODIC_TABLE[element_symbol]['atomic_mass']:.3f} u")
                else:
                    print(f"{Fore.RED}Error: Element '{element_symbol}' not found in database.{Style.RESET_ALL}")
                    return None
            
            print(f"\n{Fore.CYAN}{'─' * 60}")
            print(f"{Fore.MAGENTA}{Style.BRIGHT}Molar Mass Calculation for {formula}")
            print(f"{Fore.CYAN}{'─' * 60}{Style.RESET_ALL}")
            for comp in composition:
                print(f"{Fore.YELLOW}{comp}{Style.RESET_ALL}")
            print(f"{Fore.CYAN}{'─' * 60}{Style.RESET_ALL}")
            print(f"{Fore.GREEN}{Style.BRIGHT}Total Molar Mass: {total_mass:.3f} g/mol{Style.RESET_ALL}\n")
            
            return total_mass
            
        except Exception as e:
            print(f"{Fore.RED}Error calculating molar mass: {str(e)}{Style.RESET_ALL}")
            return None
    
    def handle_molar_mass_query(self, query):
        """Handle molar mass calculation queries"""
        query = query.lower()
        
        # Look for patterns like "molar mass of X" or "mass of X"
        patterns = [
            r'molar mass of ([A-Za-z0-9]+)',
            r'mass of ([A-Za-z0-9]+)',
            r'calculate ([A-Za-z0-9]+)',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, query)
            if match:
                formula = match.group(1)
                # Capitalize element symbols properly for formulas like "h2o" -> "H2O", "nacl" -> "NaCl"
                # This handles two-letter elements (like Cl, Na) and single-letter elements (like H, O)
                formula_proper = ""
                for char in formula:
                    if char.isalpha() and (not formula_proper or not formula_proper[-1].isupper() or formula_proper[-1].isdigit()):
                        # Start of a new element symbol
                        formula_proper += char.upper()
                    else:
                        formula_proper += char
                
                self.calculate_molar_mass(formula_proper)
                return True
        
        return False
    
    def balance_equation(self, equation):
        """Basic chemical equation balancing (simplified implementation)"""
        print(f"{Fore.YELLOW}Note: This is a basic implementation for simple equations.{Style.RESET_ALL}")
        
        # Common balanced equations database
        balanced_equations = {
            "h2+o2->h2o": "2H₂ + O₂ → 2H₂O",
            "h2+o2=h2o": "2H₂ + O₂ → 2H₂O",
            "ch4+o2->co2+h2o": "CH₄ + 2O₂ → CO₂ + 2H₂O",
            "ch4+o2=co2+h2o": "CH₄ + 2O₂ → CO₂ + 2H₂O",
            "n2+h2->nh3": "N₂ + 3H₂ → 2NH₃",
            "n2+h2=nh3": "N₂ + 3H₂ → 2NH₃",
            "fe+o2->fe2o3": "4Fe + 3O₂ → 2Fe₂O₃",
            "fe+o2=fe2o3": "4Fe + 3O₂ → 2Fe₂O₃",
            "c3h8+o2->co2+h2o": "C₃H₈ + 5O₂ → 3CO₂ + 4H₂O",
            "c3h8+o2=co2+h2o": "C₃H₈ + 5O₂ → 3CO₂ + 4H₂O",
            "na+cl2->nacl": "2Na + Cl₂ → 2NaCl",
            "na+cl2=nacl": "2Na + Cl₂ → 2NaCl",
        }
        
        # Normalize the equation
        normalized = equation.lower().replace(" ", "").replace("->", "=")
        
        if normalized in balanced_equations:
            result = balanced_equations[normalized]
            print(f"\n{Fore.GREEN}{Style.BRIGHT}Balanced Equation:{Style.RESET_ALL}")
            print(f"{Fore.CYAN}{result}{Style.RESET_ALL}\n")
            return True
        else:
            print(f"{Fore.YELLOW}I can balance common simple equations. Try equations like:")
            print(f"{Fore.CYAN}  • H2 + O2 -> H2O")
            print(f"{Fore.CYAN}  • CH4 + O2 -> CO2 + H2O")
            print(f"{Fore.CYAN}  • N2 + H2 -> NH3{Style.RESET_ALL}\n")
            return False
    
    def handle_balance_query(self, query):
        """Handle equation balancing queries"""
        query = query.lower()
        
        if "balance" in query:
            # Extract equation after "balance"
            parts = query.split("balance")
            if len(parts) > 1:
                equation = parts[1].strip()
                self.balance_equation(equation)
                return True
        
        return False
    
    def handle_general_qa(self, query):
        """Handle general chemistry questions"""
        query_lower = query.lower()
        
        # Check for keywords in the knowledge base
        for key, qa in CHEMISTRY_QA.items():
            if key in query_lower:
                print(f"\n{Fore.CYAN}{'─' * 60}")
                print(f"{Fore.MAGENTA}{Style.BRIGHT}Q: {qa['question']}")
                print(f"{Fore.CYAN}{'─' * 60}{Style.RESET_ALL}")
                print(f"{Fore.GREEN}A: {qa['answer']}{Style.RESET_ALL}\n")
                return True
        
        return False
    
    def process_query(self, query):
        """Process user query and route to appropriate handler"""
        query = query.strip()
        
        if not query:
            return
        
        # Check for exit commands
        if query.lower() in ['quit', 'exit', 'bye', 'goodbye']:
            print(f"{Fore.MAGENTA}Thank you for using Chemistry Chatbot RGB! Goodbye! 👋{Style.RESET_ALL}\n")
            self.running = False
            return
        
        # Try different query handlers
        handled = False
        
        # Check for molar mass queries first
        if not handled and any(word in query.lower() for word in ['molar mass', 'mass of', 'calculate']):
            handled = self.handle_molar_mass_query(query)
        
        # Check for balance queries
        if not handled and 'balance' in query.lower():
            handled = self.handle_balance_query(query)
        
        # Check for element queries
        if not handled and any(word in query.lower() for word in ['element', 'atom', 'tell me about', 'what is', 'atomic number']):
            handled = self.handle_element_query(query)
        
        # Check for general Q&A
        if not handled:
            handled = self.handle_general_qa(query)
        
        # If nothing matched, provide a helpful message
        if not handled:
            print(f"{Fore.YELLOW}I'm not sure how to answer that. Try asking about:")
            print(f"{Fore.CYAN}  • An element (e.g., 'tell me about Oxygen')")
            print(f"{Fore.CYAN}  • Molar mass (e.g., 'molar mass of H2O')")
            print(f"{Fore.CYAN}  • Balancing equations (e.g., 'balance H2 + O2 -> H2O')")
            print(f"{Fore.CYAN}  • Chemistry concepts (e.g., 'what is pH', 'what is Avogadro's number'){Style.RESET_ALL}\n")
    
    def run(self):
        """Main chatbot loop"""
        self.greet()
        
        while self.running:
            try:
                # Get user input with colored prompt
                user_input = input(f"{Fore.GREEN}{Style.BRIGHT}You: {Style.RESET_ALL}")
                self.process_query(user_input)
                
            except KeyboardInterrupt:
                print(f"\n{Fore.MAGENTA}Goodbye! 👋{Style.RESET_ALL}\n")
                break
            except EOFError:
                print(f"\n{Fore.MAGENTA}Goodbye! 👋{Style.RESET_ALL}\n")
                break
            except Exception as e:
                print(f"{Fore.RED}An error occurred: {str(e)}{Style.RESET_ALL}")


def main():
    """Entry point for the chatbot"""
    chatbot = ChemistryChatbot()
    chatbot.run()


if __name__ == "__main__":
    main()
