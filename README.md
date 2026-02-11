# 🧪 Chemistry Chatbot

An interactive Java-based chatbot application that helps students learn chemistry by answering questions about various chemistry topics.

## 📖 About

Chemistry Chatbot is an educational tool that provides instant answers to chemistry questions. It uses a comprehensive knowledge base covering key chemistry concepts and employs intelligent keyword matching to understand and respond to student queries.

### Features

- 🔬 **Comprehensive Knowledge Base** - Covers 9 major chemistry topics with 60 Q&A pairs
- 💬 **Interactive CLI Interface** - Easy-to-use command-line interface
- 🎯 **Smart Question Matching** - Fuzzy matching supports various ways of asking questions
- 📚 **Topic Browsing** - Explore topics and see example questions
- ⚡ **No External APIs Required** - Works completely offline with local data

### Topics Covered

1. **Atomic Structure** - Atoms, protons, neutrons, electrons, isotopes
2. **Periodic Table** - Elements, groups, periods, metals, nonmetals
3. **Chemical Bonding** - Ionic, covalent, metallic bonds, electronegativity
4. **Chemical Reactions** - Types of reactions, balancing equations, combustion
5. **Acids, Bases, and pH** - Acid-base chemistry, pH scale, neutralization
6. **Stoichiometry** - Moles, molar mass, limiting reactants, percent yield
7. **States of Matter and Gas Laws** - Solids, liquids, gases, Boyle's Law, Charles's Law
8. **Organic Chemistry Basics** - Hydrocarbons, alkanes, alkenes, alkynes, functional groups
9. **Solutions and Concentrations** - Solutes, solvents, molarity, solubility, dilution

## 🚀 Getting Started

### Prerequisites

- **Java Development Kit (JDK) 17 or higher**
- **Maven 3.6+** (for building the project)

### Installation and Building

1. Clone the repository:
   ```bash
   git clone https://github.com/axyco2004-cyber/axyco2004-cyber-chemistry-chatbot-rgb.git
   cd axyco2004-cyber-chemistry-chatbot-rgb
   ```

2. Build the project using Maven:
   ```bash
   mvn clean package
   ```

3. Run the chatbot:
   ```bash
   java -jar target/chemistry-chatbot-1.0-SNAPSHOT.jar
   ```

   Or use Maven to run directly:
   ```bash
   mvn exec:java -Dexec.mainClass="com.chemistry.chatbot.ChemistryChatbot"
   ```

## 💡 Usage

### Available Commands

- `help` - Display help message with available commands and example questions
- `topics` - List all available chemistry topics with descriptions
- `browse <topic>` - View sample questions for a specific topic (e.g., `browse Atomic Structure`)
- `quit` or `exit` - Exit the chatbot

### Example Questions

Here are some questions you can ask the chatbot:

**Atomic Structure:**
- What is an atom?
- What is a proton?
- What are isotopes?
- Define atomic number

**Periodic Table:**
- What is the periodic table?
- What are noble gases?
- What are valence electrons?
- Define group

**Chemical Bonding:**
- What is a chemical bond?
- Define ionic bond
- What is a covalent bond?
- What is electronegativity?

**Chemical Reactions:**
- What is a chemical reaction?
- How do you balance a chemical equation?
- What is a synthesis reaction?
- What is combustion?

**Acids and Bases:**
- What is an acid?
- What is pH?
- Define neutralization
- What are indicators?

**Stoichiometry:**
- What is a mole?
- What is molar mass?
- What is the limiting reactant?
- How do you calculate percent yield?

**Gas Laws:**
- What are the states of matter?
- What is Boyle's Law?
- What is the Ideal Gas Law?
- What is STP?

**Organic Chemistry:**
- What is organic chemistry?
- What is a hydrocarbon?
- Define alkane
- What is a functional group?

**Solutions:**
- What is a solution?
- What is molarity?
- What is solubility?
- How do you dilute a solution?

### Sample Interaction

```
💬 You: What is an atom?
🤖 Bot: An atom is the smallest unit of matter that retains the properties 
of an element. It consists of a nucleus containing protons and neutrons, 
surrounded by electrons in energy levels or shells.

💬 You: topics
📚 Available Chemistry Topics:
==================================================

1. Atomic Structure
   Understanding atoms, electrons, protons, and neutrons
   (7 Q&A pairs)

2. Periodic Table
   Elements, groups, periods, and properties
   (7 Q&A pairs)
...

💬 You: quit
👋 Thanks for using Chemistry Chatbot! Happy learning!
```

## 🏗️ Project Structure

```
├── src/
│   └── main/
│       ├── java/
│       │   └── com/
│       │       └── chemistry/
│       │           └── chatbot/
│       │               ├── ChemistryChatbot.java    # Main entry point & CLI
│       │               ├── ChatEngine.java          # Core chatbot logic
│       │               ├── KnowledgeBase.java       # Knowledge management
│       │               ├── TopicMatcher.java        # Question matching
│       │               └── model/
│       │                   ├── Topic.java           # Topic model
│       │                   └── QAPair.java          # Q&A pair model
│       └── resources/
│           └── chemistry_knowledge.json             # Knowledge base data
├── pom.xml                                          # Maven configuration
└── README.md                                        # This file
```

## 🛠️ Technology Stack

- **Language:** Java 17
- **Build Tool:** Maven
- **JSON Processing:** Gson 2.10.1
- **No external AI APIs** - Works completely offline

## 🧑‍💻 Development

### Adding New Topics

To add new chemistry topics:

1. Open `src/main/resources/chemistry_knowledge.json`
2. Add a new topic object with questions, answers, and keywords
3. Rebuild the project with `mvn clean package`

### Extending Functionality

The modular architecture makes it easy to extend:

- **KnowledgeBase.java** - Add new data sources or formats
- **TopicMatcher.java** - Improve matching algorithms
- **ChatEngine.java** - Add new response types or features
- **ChemistryChatbot.java** - Add new commands or UI features

## 🤝 Contributing

Contributions are welcome! Feel free to:
- Report bugs or issues
- Suggest new features or topics
- Submit pull requests with improvements

## 📄 License

This project is open source and available under the [MIT License](LICENSE).