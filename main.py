import os
from flask import Flask, request, jsonify, render_template_string
from dotenv import load_dotenv
import periodictable
import pubchempy as pcp
import numpy as np
from knowledge_base import textbook_kb
from chemistry_calculator import calculator
from ai_assistant import ai_assistant

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "default-secret-key")

# ──────────────────────────────────────────────
# Chemistry Helper Functions
# ──────────────────────────────────────────────

def get_element_info(symbol_or_name):
    """Retrieve information about a chemical element."""
    try:
        for el in periodictable.elements:
            if el.symbol.lower() == symbol_or_name.lower() or el.name.lower() == symbol_or_name.lower():
                return {
                    "name": el.name,
                    "symbol": el.symbol,
                    "number": el.number,
                    "mass": round(el.mass, 4),
                    "density": el.density if hasattr(el, "density") else "N/A",
                }
        return None
    except Exception as e:
        return {"error": str(e)}

def get_compound_info(compound_name):
    """Retrieve information about a chemical compound from PubChem."""
    try:
        results = pcp.get_compounds(compound_name, "name")
        if results:
            compound = results[0]
            return {
                "name": compound.iupac_name or compound_name,
                "molecular_formula": compound.molecular_formula,
                "molecular_weight": compound.molecular_weight,
                "smiles": compound.isomeric_smiles,
                "cid": compound.cid,
            }
        return None
    except Exception as e:
        return {"error": str(e)}

def calculate_molar_mass(formula):
    """Calculate the molar mass of a chemical formula."""
    try:
        f = periodictable.formula(formula)
        return round(f.mass, 4)
    except Exception as e:
        return {"error": str(e)}

# ──────────────────────────────────────────────
# Chat Function
# ──────────────────────────────────────────────

SYSTEM_PROMPT = """You are Chemistry Chatbot RGB 🧪, a friendly and knowledgeable chemistry assistant.
You help users with:
- Answering chemistry-related questions
- Explaining chemical reactions and equations
- Providing information on elements and compounds
- Helping with chemistry problem-solving
- Balancing chemical equations
- Explaining molecular structures
- Materials science and engineering topics (with access to Callister's Materials Science textbook)

You have access to a comprehensive Materials Science and Engineering textbook that covers:
- Material properties and structures
- Mechanical properties of materials
- Phase diagrams and transformations
- Metallurgy and ceramics
- Polymers and composites
- Electronic, thermal, and magnetic properties

Always be accurate, educational, and encouraging. Use emojis to make learning fun!
If you're unsure about something, say so rather than guessing."""

def get_chat_response(user_message, conversation_history=None):
    """Get a response from the chatbot with AI or built-in knowledge."""
    if conversation_history is None:
        conversation_history = []

    lower_msg = user_message.lower()
    
    # Try AI assistant first for comprehensive answers
    if ai_assistant.is_available():
        ai_response = ai_assistant.generate_response(user_message, conversation_history)
        if ai_response:
            return ai_response
    
    # Fall back to pattern-based responses if AI unavailable
    
    # Materials Science topics - check textbook first
    materials_keywords = ['material', 'steel', 'alloy', 'crystal structure', 'fcc', 'bcc', 
                          'hcp', 'ceramic', 'polymer', 'composite', 'stress', 'strain',
                          'modulus', 'elasticity', 'plasticity', 'hardness', 'tensile',
                          'phase diagram', 'microstructure', 'grain', 'dislocation',
                          'annealing', 'quenching', 'tempering', 'diffusion', 'corrosion',
                          'fracture', 'fatigue', 'creep', 'iron-carbon', 'aluminum oxide',
                          'silicon carbide', 'thermal properties', 'electrical properties']
    
    # Check if query is about materials science
    if any(keyword in lower_msg for keyword in materials_keywords):
        textbook_result = textbook_kb.smart_search(user_message)
        if textbook_result:
            return f"📚 <b>From Materials Science & Engineering Textbook:</b><br><br>{textbook_result[:800]}..."
    
    # Water/H2O questions
    if "water" in lower_msg or "h2o" in lower_msg or "h₂o" in lower_msg:
        return "💧 <b>Water (H₂O)</b> is a chemical compound made of two hydrogen atoms and one oxygen atom. It's essential for life, has a bent molecular shape (104.5° bond angle), and is an excellent solvent. Molecular weight: 18.015 g/mol. Try 'compound: water' for more details!"
    
    # Hydrogen questions
    elif ("hydrogen" in lower_msg or "h" == lower_msg.strip()) and not lower_msg.startswith("element:"):
        return "🫧 <b>Hydrogen (H)</b> is the lightest and most abundant element in the universe! It's a colorless, odorless, highly flammable gas. Atomic number: 1, Atomic mass: 1.008 u. It forms water when combined with oxygen. Try 'element: hydrogen' for complete details!"
    
    # Periodic table questions
    elif "periodic table" in lower_msg:
        return "📋 <b>The Periodic Table</b> organizes all 118 known chemical elements by atomic number, electron configuration, and recurring chemical properties. Elements are arranged in rows (periods) and columns (groups/families). It was created by Dmitri Mendeleev in 1869. Use 'element: [name]' to learn about specific elements!"
    
    # Balance/equation questions
    elif "balance" in lower_msg or "equation" in lower_msg:
        if "fe" in lower_msg and "o2" in lower_msg:
            return "⚖️ To balance <b>Fe + O₂ → Fe₂O₃</b>:<br>4Fe + 3O₂ → 2Fe₂O₃<br><br>Remember: Count atoms on each side and adjust coefficients until equal!"
        else:
            return "⚖️ <b>Balancing Chemical Equations:</b><br>1. Count atoms of each element on both sides<br>2. Adjust coefficients (not subscripts)<br>3. Start with the most complex molecule<br>4. Balance remaining elements<br>Example: 2H₂ + O₂ → 2H₂O<br><br>What equation would you like help with?"
    
    # Oxygen questions
    elif "oxygen" in lower_msg and not lower_msg.startswith("element:"):
        return "💨 <b>Oxygen (O)</b> is essential for life and combustion! Atomic number: 8, makes up 21% of Earth's atmosphere. It's highly reactive and forms oxides with most elements. Try 'element: oxygen' for full details!"
    
    # Carbon questions
    elif "carbon" in lower_msg and not lower_msg.startswith("element:"):
        return "⚫ <b>Carbon (C)</b> is the basis of all organic chemistry and life! Atomic number: 6. It can form millions of compounds due to its ability to bond with itself and other elements. Found in diamonds, graphite, and all living things. Try 'element: carbon' for more!"
    
    # Chemical reaction questions
    elif "reaction" in lower_msg or "react" in lower_msg:
        return "⚗️ <b>Chemical Reactions</b> occur when substances interact to form new products. Types include:<br>• Synthesis (A + B → AB)<br>• Decomposition (AB → A + B)<br>• Single replacement<br>• Double replacement<br>• Combustion<br><br>What type of reaction are you interested in?"
    
    # pH questions
    elif "ph" in lower_msg or "acid" in lower_msg or "base" in lower_msg:
        return "🧪 <b>pH Scale</b> measures acidity/basicity from 0-14:<br>• pH < 7: Acidic (lemon juice, vinegar)<br>• pH = 7: Neutral (pure water)<br>• pH > 7: Basic/Alkaline (soap, bleach)<br><br>pH = -log[H⁺]. Each unit is 10x difference in H⁺ concentration!"
    
    # Molecule/molecular questions
    elif "molecule" in lower_msg or "molecular" in lower_msg:
        return "🧬 <b>Molecules</b> are two or more atoms bonded together. Examples:<br>• H₂O (water): bent shape<br>• CO₂ (carbon dioxide): linear<br>• CH₄ (methane): tetrahedral<br>• NH₃ (ammonia): trigonal pyramidal<br><br>Use 'compound: [name]' for specific molecules!"
    
    # General chemistry question
    elif "chemistry" in lower_msg or "help" in lower_msg or "what can you" in lower_msg:
        return "🧪 <b>I'm your Chemistry & Materials Science Assistant!</b> I can help with:<br><br><b>Info Lookups:</b><br>• Element info: 'element: sodium'<br>• Compound details: 'compound: ethanol'<br>• Molar mass: 'mass: NaCl'<br><br><b>Calculations (calc: type | params):</b><br>• Stoichiometry: moles_to_grams, grams_to_moles<br>• Solutions: molarity, dilution<br>• pH: ph, poh, ph_value<br>• Gas Laws: ideal_gas, combined_gas<br>• Composition: percent, limiting_reactant<br><br><b>Knowledge:</b><br>• Balancing equations, reactions, pH<br>• <b>Materials Science</b> textbook search<br><br>Ask anything or try 'calc examples' for calculation help!"
    
    # Calculation examples
    elif "calc" in lower_msg and ("example" in lower_msg or "help" in lower_msg):
        return """🧮 <b>Calculator Examples:</b><br><br>
<b>Stoichiometry:</b><br>
• calc: moles_to_grams | formula=H2O | moles=2<br>
• calc: grams_to_moles | formula=NaCl | grams=10<br>
• calc: moles_to_molecules | moles=0.5<br><br>
<b>Solutions:</b><br>
• calc: molarity | moles=0.5 | volume=2<br>
• calc: dilution | M1=2 | V1=10 | V2=50<br><br>
<b>pH:</b><br>
• calc: ph | H=0.001<br>
• calc: ph_value | pH=3.5<br><br>
<b>Gas Laws:</b><br>
• calc: ideal_gas | P=1 | V=22.4 | T=273<br>
• calc: combined_gas | P1=1 | V1=10 | T1=300 | V2=20 | T2=350<br><br>
<b>Other:</b><br>
• calc: percent | formula=H2O<br>
• calc: limiting | r1=Fe | g1=10 | c1=4 | r2=O2 | g2=5 | c2=3
        """
    
    # Default helpful response
    else:
        # Try searching the textbook as a fallback
        textbook_result = textbook_kb.smart_search(user_message)
        if textbook_result:
            return f"📚 <b>From Materials Science Textbook:</b><br><br>{textbook_result[:700]}..."
        
        return f"🧪 Interesting question about '{user_message}'! Try these commands:<br>• <b>element:</b> [name]<br>• <b>compound:</b> [name]<br>• <b>mass:</b> [formula]<br>• <b>calc:</b> [type] | [params] (try 'calc examples')<br><br>Or ask about: water, hydrogen, equations, pH, materials science, or calculations!"

# ──────────────────────────────────────────────
# HTML Template
# ──────────────────────────────────────────────

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🧪 Chemistry Chatbot RGB</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
        }
        .chat-container {
            width: 90%; max-width: 700px;
            background: #fff; border-radius: 20px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            overflow: hidden; display: flex;
            flex-direction: column; height: 85vh;
        }
        .chat-header {
            background: linear-gradient(135deg, #e74c3c, #2ecc71, #3498db);
            color: white; padding: 20px; text-align: center;
            font-size: 1.4em; font-weight: bold;
        }
        .chat-header span { font-size: 0.6em; display: block; opacity: 0.9; }
        .chat-messages {
            flex: 1; overflow-y: auto; padding: 20px;
            display: flex; flex-direction: column; gap: 12px;
        }
        .message {
            max-width: 80%; padding: 12px 16px;
            border-radius: 16px; line-height: 1.5; font-size: 0.95em;
        }
        .user-msg {
            align-self: flex-end;
            background: linear-gradient(135deg, #667eea, #764ba2);
            color: white; border-bottom-right-radius: 4px;
        }
        .bot-msg {
            align-self: flex-start;
            background: #f0f0f0; color: #333;
            border-bottom-left-radius: 4px;
        }
        .chat-input {
            display: flex; padding: 15px; border-top: 1px solid #eee;
            background: #fafafa;
        }
        .chat-input input {
            flex: 1; padding: 12px 16px; border: 2px solid #ddd;
            border-radius: 25px; font-size: 1em; outline: none;
            transition: border-color 0.3s;
        }
        .chat-input input:focus { border-color: #667eea; }
        .chat-input button {
            margin-left: 10px; padding: 12px 24px;
            background: linear-gradient(135deg, #e74c3c, #3498db);
            color: white; border: none; border-radius: 25px;
            font-size: 1em; cursor: pointer; transition: transform 0.2s;
        }
        .chat-input button:hover { transform: scale(1.05); }
        .quick-actions {
            display: flex; gap: 8px; padding: 10px 20px;
            flex-wrap: wrap; border-top: 1px solid #eee;
        }
        .quick-btn {
            padding: 6px 12px; background: #e8e8e8;
            border: none; border-radius: 15px;
            font-size: 0.8em; cursor: pointer;
            transition: background 0.2s;
        }
        .quick-btn:hover { background: #d0d0d0; }
    </style>
</head>
<body>
    <div class="chat-container">
        <div class="chat-header">
            🧪 Chemistry Chatbot RGB
            <span>Your intelligent chemistry assistant</span>
        </div>
        <div class="chat-messages" id="chatMessages">
            <div class="message bot-msg">
                👋 Hello! I'm <b>Chemistry Chatbot RGB</b>! I can help you with:
                <br>🔬 Chemistry questions
                <br>⚗️ Chemical reactions
                <br>🧬 Element & compound info
                <br>🧮 <b>NEW: Chemistry Calculations!</b>
                <br>📚 Materials Science (Callister's textbook)
                <br><br>Try 'help' or 'calc examples' to see what I can do!
            </div>
        </div>
        <div class="quick-actions">
            <button class="quick-btn" onclick="sendQuick('help')">❓ Help</button>
            <button class="quick-btn" onclick="sendQuick('calc examples')">🧮 Calculators</button>
            <button class="quick-btn" onclick="sendQuick('element: hydrogen')">🫧 Elements</button>
            <button class="quick-btn" onclick="sendQuick('What is pH?')">🧪 pH</button>
            <button class="quick-btn" onclick="sendQuick('What is steel?')">🔩 Materials</button>
            <button class="quick-btn" onclick="sendQuick('calc: moles_to_grams | formula=H2O | moles=2')">⚗️ Calculate</button>
        </div>
        <div class="chat-input">
            <input type="text" id="userInput" placeholder="Ask me a chemistry question..."
                   onkeypress="if(event.key==='Enter') sendMessage()">
            <button onclick="sendMessage()">Send 🚀</button>
        </div>
    </div>
    <script>
        let conversationHistory = [];
        
        async function sendMessage() {
            const input = document.getElementById('userInput');
            const msg = input.value.trim();
            if (!msg) return;
            
            // Add user message
            addMessage(msg, 'user-msg');
            input.value = '';
            
            // Show thinking indicator
            const thinkingId = 'thinking-' + Date.now();
            addMessage('🤔 Thinking...', 'bot-msg', thinkingId);
            
            // Add user message to history
            conversationHistory.push({role: 'user', content: msg});
            
            try {
                const res = await fetch('/chat', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({
                        message: msg,
                        history: conversationHistory
                    })
                });
                
                if (!res.ok) {
                    throw new Error(`Server returned ${res.status}`);
                }
                
                const data = await res.json();
                
                // Remove thinking indicator
                const thinkingEl = document.getElementById(thinkingId);
                if (thinkingEl) thinkingEl.remove();
                
                // Add bot response
                addMessage(data.response, 'bot-msg');
                
                // Add bot response to history
                conversationHistory.push({role: 'assistant', content: data.response});
                
                // Keep history limited to last 10 exchanges (20 messages)
                if (conversationHistory.length > 20) {
                    conversationHistory = conversationHistory.slice(-20);
                }
                
                console.log('Conversation history:', conversationHistory.length, 'messages');
                
            } catch (e) {
                console.error('Chat error:', e);
                // Remove thinking indicator
                const thinkingEl = document.getElementById(thinkingId);
                if (thinkingEl) thinkingEl.remove();
                
                addMessage('⚠️ Connection error. Please try again. ' + e.message, 'bot-msg');
            }
        }
        function sendQuick(msg) {
            document.getElementById('userInput').value = msg;
            sendMessage();
        }
        function addMessage(text, cls, id) {
            const div = document.createElement('div');
            div.className = 'message ' + cls;
            div.innerHTML = text;
            if (id) div.id = id;
            document.getElementById('chatMessages').appendChild(div);
            div.scrollIntoView({behavior: 'smooth'});
        }
    </script>
</body>
</html>
"""

# ──────────────────────────────────────────────
# Flask Routes
# ──────────────────────────────────────────────

@app.route("/")
def index():
    """Serve the chatbot UI."""
    return render_template_string(HTML_TEMPLATE)

@app.route("/chat", methods=["POST"])
def chat():
    """Handle chat messages."""
    data = request.get_json()
    user_message = data.get("message", "").strip()
    conversation_history = data.get("history", [])

    if not user_message:
        return jsonify({"response": "Please enter a message! 🧪"})

    # Check for element lookup commands
    lower_msg = user_message.lower()

    if lower_msg.startswith("element:"):
        query = user_message[8:].strip()
        info = get_element_info(query)
        if info and "error" not in info:
            response = (
                f"🔬 <b>{info['name']}</b> ({info['symbol']})<br>"
                f"Atomic Number: {info['number']}<br>"
                f"Atomic Mass: {info['mass']} u<br>"
                f"Density: {info['density']} g/cm³"
            )
        else:
            response = get_chat_response(user_message)

    elif lower_msg.startswith("compound:"):
        query = user_message[9:].strip()
        info = get_compound_info(query)
        if info and "error" not in info:
            response = (
                f"🧬 <b>{info['name']}</b><br>"
                f"Formula: {info['molecular_formula']}<br>"
                f"Molecular Weight: {info['molecular_weight']} g/mol<br>"
                f"SMILES: {info['smiles']}<br>"
                f"PubChem CID: {info['cid']}"
            )
        else:
            response = get_chat_response(user_message)

    elif lower_msg.startswith("mass:"):
        formula = user_message[5:].strip()
        result = calculate_molar_mass(formula)
        if isinstance(result, float):
            response = f"⚖️ Molar mass of <b>{formula}</b>: {result} g/mol"
        else:
            response = get_chat_response(user_message)

    elif lower_msg.startswith("textbook:") or lower_msg.startswith("material:"):
        # Extract the query after the command
        query = user_message.split(":", 1)[1].strip()
        textbook_result = textbook_kb.smart_search(query)
        if textbook_result:
            response = f"📚 <b>From Materials Science & Engineering Textbook:</b><br><br>{textbook_result[:800]}..."
        else:
            response = f"🔍 No results found in textbook for '{query}'. Try different keywords or ask a general question!"

    # ==================== CALCULATION COMMANDS ====================
    
    elif lower_msg.startswith("calc:"):
        # Parse calculation commands: calc: type | param1=value | param2=value
        try:
            parts = user_message[5:].strip().split("|")
            calc_type = parts[0].strip().lower()
            params = {}
            
            for part in parts[1:]:
                if "=" in part:
                    key, value = part.split("=", 1)
                    key = key.strip()
                    value = value.strip()
                    try:
                        params[key] = float(value)
                    except:
                        params[key] = value
            
            # Route to appropriate calculator
            if calc_type in ["moles_to_grams", "moles to grams", "mol to g"]:
                result = calculator.moles_to_grams(params.get("formula"), params.get("moles"))
            elif calc_type in ["grams_to_moles", "grams to moles", "g to mol"]:
                result = calculator.grams_to_moles(params.get("formula"), params.get("grams"))
            elif calc_type in ["moles_to_molecules", "mol to molecules"]:
                result = calculator.moles_to_molecules(params.get("moles"))
            elif calc_type in ["molecules_to_moles", "molecules to mol"]:
                result = calculator.molecules_to_moles(params.get("molecules"))
            elif calc_type in ["molarity", "concentration"]:
                result = calculator.calculate_molarity(
                    moles=params.get("moles"),
                    grams=params.get("grams"),
                    formula=params.get("formula"),
                    volume_L=params.get("volume")
                )
            elif calc_type in ["dilution", "m1v1=m2v2"]:
                result = calculator.dilution(
                    M1=params.get("M1"),
                    V1=params.get("V1"),
                    M2=params.get("M2"),
                    V2=params.get("V2")
                )
            elif calc_type in ["ph", "ph_from_h"]:
                result = calculator.calculate_pH(params.get("H"))
            elif calc_type in ["poh", "ph_from_oh"]:
                result = calculator.calculate_pOH(params.get("OH"))
            elif calc_type in ["ph_value", "ph info"]:
                result = calculator.pH_from_value(params.get("pH"))
            elif calc_type in ["ideal_gas", "pv=nrt", "gas law"]:
                result = calculator.ideal_gas_law(
                    P=params.get("P"),
                    V=params.get("V"),
                    n=params.get("n"),
                    T=params.get("T")
                )
            elif calc_type in ["combined_gas", "gas laws"]:
                result = calculator.combined_gas_law(
                    P1=params.get("P1"),
                    V1=params.get("V1"),
                    T1=params.get("T1"),
                    P2=params.get("P2"),
                    V2=params.get("V2"),
                    T2=params.get("T2")
                )
            elif calc_type in ["percent", "percent_composition", "composition"]:
                result = calculator.percent_composition(params.get("formula"))
            elif calc_type in ["limiting", "limiting_reactant", "limiting reagent"]:
                result = calculator.limiting_reactant(
                    reactant1_formula=params.get("r1"),
                    reactant1_grams=params.get("g1"),
                    reactant1_coef=int(params.get("c1", 1)),
                    reactant2_formula=params.get("r2"),
                    reactant2_grams=params.get("g2"),
                    reactant2_coef=int(params.get("c2", 1))
                )
            else:
                result = {"error": f"Unknown calculation type '{calc_type}'"}
            
            # Format response
            if "error" in result:
                response = f"❌ <b>Calculation Error:</b> {result['error']}"
            else:
                # Get AI explanation if available
                ai_explanation = ai_assistant.generate_calculation_explanation(calc_type, result)
                
                response = f"🧮 <b>Calculation Result:</b><br><pre>{format_calc_result(result)}</pre>"
                
                if ai_explanation:
                    response += f"<br><br>💡 {ai_explanation}"
        
        except Exception as e:
            response = f"❌ <b>Calculation Error:</b> {str(e)}<br><br>📝 <b>Format:</b> calc: type | param1=value | param2=value<br>Example: calc: moles_to_grams | formula=H2O | moles=2"

    else:
        response = get_chat_response(user_message, conversation_history)

    return jsonify({"response": response})

def format_calc_result(result: dict) -> str:
    """Format calculation results for display."""
    formatted = ""
    for key, value in result.items():
        formatted += f"{key}: {value}\n"
    return formatted

@app.route("/element/<symbol>", methods=["GET"])
def element(symbol):
    """API endpoint to get element info."""
    info = get_element_info(symbol)
    if info:
        return jsonify(info)
    return jsonify({"error": "Element not found"}), 404

@app.route("/compound/<name>", methods=["GET"])
def compound(name):
    """API endpoint to get compound info."""
    info = get_compound_info(name)
    if info:
        return jsonify(info)
    return jsonify({"error": "Compound not found"}), 404

# ──────────────────────────────────────────────
# Main Entry Point
# ──────────────────────────────────────────────

if __name__ == "__main__":
    port = int(os.getenv("FLASK_PORT", 5000))
    debug = os.getenv("FLASK_DEBUG", "False") == "True"
    print("🧪 Chemistry Chatbot RGB is starting...")
    print(f"🌐 Open http://localhost:{port} in your browser")
    app.run(host="0.0.0.0", port=port, debug=debug)