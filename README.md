# 🧪 Chemistry Chatbot RGB

✨ **NEW: AI-Powered Responses!** ✨

A comprehensive **AI-powered** chemistry chatbot with **built-in calculation solvers** and **Materials Science knowledge** (Callister's 8th Edition textbook). Uses GPT-4 to provide complete, detailed answers. Perfect for students, educators, and chemistry enthusiasts!

## 📖 About
### 🤖 AI-Powered Intelligence
- **Complete answers** using GPT-4o-mini for speed and accuracy
- **Context-aware** - searches textbook and chemistry databases
- **Educational explanations** for calculations
- Automatic fallback to pattern-based responses if API unavailable

### ✨ Core Features
Chemistry Chatbot RGB is an intelligent assistant that can:

- 🔬 Answer chemistry questions
- ⚗️ Explain chemical reactions and equations
- 🧬 Provide element and compound information
- 🧮 **NEW: Solve chemistry calculation problems!**
  - Stoichiometry (moles ↔ grams ↔ molecules)
  - Solution chemistry (molarity, dilution)
  - pH calculations
  - Gas laws (PV=nRT, combined gas law)
  - Percent composition
  - Limiting reactant problems
- 📚 Materials Science topics including:
  - Material properties and structures (FCC, BCC, HCP crystals)
  - Mechanical properties (stress, strain, elasticity)
  - Phase diagrams and transformations
  - Metallurgy and alloys (steel, aluminum, etc.)
  - Ceramics, polymers, and composites

### 🧮 Advanced Calculators
- **Stoichiometry**: moles ↔ grams ↔ molecules
- **Solution Chemistry**: molarity, dilution (M₁V₁ = M₂V₂)
- **pH Calculations**: from H⁺ or OH⁻ concentrations
- **Gas Laws**: PV=nRT, combined gas law
- **Percent Composition**: elemental analysis
- **Limiting Reactants**: find limiting reagent

### 💎 Materials Science
- Crystal structures (FCC, BCC, HCP)
- Mechanical properties (stress, strain, elasticity)
- Phase diagrams and transformations
- Metallurgy and alloys
- Ceramics, polymers, composites

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

3. **Set up OpenAI API (for AI responses):**
   ```bash
   # Copy the example env file
   copy .env.example .env
   
   # Edit .env and add your OpenAI API key:
   # OPENAI_API_KEY=sk-your-key-here
   ```
   
   ⚠️ **Get your API key from:** https://platform.openai.com/api-keys
   
   📌 **Note:** The chatbot works without an API key (using pattern-based responses), but AI-powered complete answers require one.

4. Run the chatbot:
   ```bash
   python main.py
   ```

5. Open http://localhost:5000 in your browser

## 💬 Usage

The chatbot supports various commands and natural language queries:

### Chemistry Commands:
- `element: [name]` - Get detailed element information (e.g., "element: sodium")
- `compound: [name]` - Get compound details from PubChem (e.g., "compound: ethanol")
- `mass: [formula]` - Calculate molar mass (e.g., "mass: H2O")

### Materials Science Commands:
- `textbook: [query]` - Search the Materials Science textbook (e.g., "textbook: crystal structures")
- `material: [query]` - Look up specific material properties (e.g., "material: steel properties")

### 🧮 Calculator Commands:

**Stoichiometry:**
```
calc: moles_to_grams | formula=H2O | moles=2
calc: grams_to_moles | formula=NaCl | grams=10
calc: moles_to_molecules | moles=0.5
calc: molecules_to_moles | molecules=3.01e23
```

**Solution Chemistry:**
```
calc: molarity | moles=0.5 | volume=2
calc: molarity | grams=10 | formula=NaCl | volume=1
calc: dilution | M1=2 | V1=10 | V2=50
```

**pH Calculations:**
```
calc: ph | H=0.001
calc: poh | OH=1e-5
calc: ph_value | pH=3.5
```

**Gas Laws:**
```
calc: ideal_gas | P=1 | V=22.4 | T=273
calc: combined_gas | P1=1 | V1=10 | T1=300 | V2=20 | T2=350
```

**Composition & Limiting Reactants:**
```
calc: percent | formula=H2O
calc: limiting | r1=Fe | g1=10 | c1=4 | r2=O2 | g2=5 | c2=3
```

### Natural Language:
Just ask questions naturally! The bot will automatically search chemistry databases or the textbook:
- "What is hydrogen?"
- "Tell me about steel"
- "Explain phase diagrams"
- "Balance: Fe + O2 -> Fe2O3"
- "What are crystal structures?"
- "help" - See all features
- "calc examples" - View calculator examples

## ☁️ Deploy to Vercel

This project is configured for serverless deployment on Vercel.

### Quick Deploy:

1. **Push to GitHub** (already done! ✅)
   ```bash
   git push origin main
   ```

2. **Import to Vercel:**
   - Go to https://vercel.com/new
   - Import `axyco2004-cyber-chemistry-chatbot-rgb` from GitHub
   - Click Deploy

3. **Add Environment Variable (Important!):**
   - Go to Project Settings → Environment Variables
   - Add: `OPENAI_API_KEY` = `your-api-key-here`
   - Redeploy for changes to take effect

4. **Access your live app!** 🎉
   - URL: `https://your-project.vercel.app`

### 💡 Benefits:
- ✅ Auto-deploys on every GitHub push
- ✅ AI-powered complete answers (with API key)
- ✅ Free tier available
- ✅ Global CDN for fast access

This project is configured for Vercel deployment with Python runtime.

1. Push your changes to GitHub
2. In Vercel, import the repository
3. **Add Environment Variable:**
   - Key: `OPENAI_API_KEY`
   - Value: Your OpenAI API key
4. Deploy!

The chatbot will auto-detect environment variables and enable AI features when the API key is present.

## 🤝 Contributing

Contributions are welcome! Feel free to open an issue or submit a pull request.

## 📄 License

This project is open source and available under the [MIT License](LICENSE).