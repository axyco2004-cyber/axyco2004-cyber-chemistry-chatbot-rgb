# 🧪 Chemistry Chatbot RGB

A chemistry chatbot designed to help users explore and learn about chemistry concepts interactively. Now enhanced with **Materials Science & Engineering** knowledge from Callister's 8th Edition textbook!

## 📖 About

Chemistry Chatbot RGB is an intelligent chatbot that can assist with:

- 🔬 Answering chemistry-related questions
- ⚗️ Explaining chemical reactions and equations
- 🧬 Providing information on elements and compounds
- 📊 Helping with chemistry problem-solving
- 📚 **NEW: Materials Science topics** including:
  - Material properties and structures (FCC, BCC, HCP crystals)
  - Mechanical properties (stress, strain, elasticity)
  - Phase diagrams and transformations
  - Metallurgy and alloys (steel, aluminum, etc.)
  - Ceramics, polymers, and composites
  - Thermal, electrical, and magnetic properties

## 🚀 Getting Started

### Prerequisites

- Python 3.8+
- pip

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/axyco2004-cyber/axyco2004-cyber-chemistry-chatbot-rgb.git
   cd axyco2004-cyber-chemistry-chatbot-rgb
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the chatbot:
   ```bash
   python main.py
   ```

## 💬 Usage

The chatbot supports several commands and natural language queries:

### Chemistry Commands:
- `element: [name]` - Get detailed element information (e.g., "element: sodium")
- `compound: [name]` - Get compound details from PubChem (e.g., "compound: ethanol")
- `mass: [formula]` - Calculate molar mass (e.g., "mass: H2O")

### Materials Science Commands:
- `textbook: [query]` - Search the Materials Science textbook (e.g., "textbook: crystal structures")
- `material: [query]` - Look up specific material properties (e.g., "material: steel properties")

### Natural Language:
Just ask questions naturally! The bot will automatically search chemistry databases or the textbook:
- "What is hydrogen?"
- "Tell me about steel"
- "Explain phase diagrams"
- "Balance: Fe + O2 -> Fe2O3"
- "What are crystal structures?"

## ☁️ Deploy to Vercel

This project is configured for Vercel using the Python runtime. The entrypoint is
`api/index.py`, which exposes the Flask `app`.

1. Push your changes to GitHub.
2. In Vercel, import the repository and deploy.
3. No API keys required - the chatbot has built-in chemistry knowledge!
4. Deploy and open the assigned Vercel URL.

## 🤝 Contributing

Contributions are welcome! Feel free to open an issue or submit a pull request.

## 📄 License

This project is open source and available under the [MIT License](LICENSE).