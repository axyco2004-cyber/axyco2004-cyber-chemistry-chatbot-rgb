import os
from flask import Flask, request, jsonify, render_template_string
from dotenv import load_dotenv
import periodictable
import pubchempy as pcp
import numpy as np

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

Always be accurate, educational, and encouraging. Use emojis to make learning fun!
If you're unsure about something, say so rather than guessing."""

def get_chat_response(user_message, conversation_history=None):
    """Get a response from the chatbot with built-in chemistry knowledge."""
    if conversation_history is None:
        conversation_history = []

    lower_msg = user_message.lower()
    
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
        return "🧪 <b>I'm your Chemistry Assistant!</b> I can help with:<br>• Element info: 'element: sodium'<br>• Compound details: 'compound: ethanol'<br>• Molar mass: 'mass: NaCl'<br>• Balancing equations<br>• Periodic table info<br>• Chemical reactions<br>• pH and acids/bases<br><br>Ask me anything about chemistry!"
    
    # Default helpful response
    else:
        return f"🧪 Interesting question about '{user_message}'! Try these commands:<br>• <b>element:</b> [name] - Get element info<br>• <b>compound:</b> [name] - Get compound details<br>• <b>mass:</b> [formula] - Calculate molar mass<br><br>Or ask about: water, hydrogen, periodic table, balancing equations, pH, or molecules!"

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
                <br>📊 Problem solving
                <br><br>Try asking me something!
            </div>
        </div>
        <div class="quick-actions">
            <button class="quick-btn" onclick="sendQuick('Tell me about hydrogen')">🫧 Hydrogen</button>
            <button class="quick-btn" onclick="sendQuick('What is H2O?')">💧 Water</button>
            <button class="quick-btn" onclick="sendQuick('Balance: Fe + O2 -> Fe2O3')">⚖️ Balance</button>
            <button class="quick-btn" onclick="sendQuick('Explain the periodic table')">📋 Periodic Table</button>
        </div>
        <div class="chat-input">
            <input type="text" id="userInput" placeholder="Ask me a chemistry question..."
                   onkeypress="if(event.key==='Enter') sendMessage()">
            <button onclick="sendMessage()">Send 🚀</button>
        </div>
    </div>
    <script>
        async function sendMessage() {
            const input = document.getElementById('userInput');
            const msg = input.value.trim();
            if (!msg) return;
            addMessage(msg, 'user-msg');
            input.value = '';
            try {
                const res = await fetch('/chat', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({message: msg})
                });
                const data = await res.json();
                addMessage(data.response, 'bot-msg');
            } catch (e) {
                addMessage('⚠️ Connection error. Please try again.', 'bot-msg');
            }
        }
        function sendQuick(msg) {
            document.getElementById('userInput').value = msg;
            sendMessage();
        }
        function addMessage(text, cls) {
            const div = document.createElement('div');
            div.className = 'message ' + cls;
            div.innerHTML = text;
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

    else:
        response = get_chat_response(user_message)

    return jsonify({"response": response})

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