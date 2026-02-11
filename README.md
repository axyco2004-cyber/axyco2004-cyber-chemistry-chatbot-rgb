# 🧪 Chemistry Chatbot RGB

A chemistry chatbot designed to help users explore and learn about chemistry concepts interactively. Built with Python serverless functions and deployed on Vercel.

## 📖 About

Chemistry Chatbot RGB is an intelligent chatbot with a colorful, RGB-themed interface that can assist with:

- 🔬 Answering chemistry-related questions
- ⚗️ Explaining chemical reactions and equations
- 🧬 Providing information on elements and compounds (atomic number, mass, category)
- 📊 Helping with chemistry problem-solving (molar mass calculations, equation balancing)
- ⚛️ Periodic table data and element properties

## ✨ Features

- **Interactive Chat Interface**: Clean, colorful UI with gradient animations
- **Serverless Backend**: Python API running on Vercel serverless functions
- **Chemistry Knowledge Base**: Built-in periodic table data and reaction information
- **Real-time Responses**: Fast API responses with typing indicators
- **Mobile Responsive**: Works seamlessly on desktop and mobile devices

## 🚀 Deployment

### Deploy to Vercel (Recommended)

#### Option 1: Deploy via GitHub (Easiest)

1. Fork or push this repository to your GitHub account
2. Go to [vercel.com](https://vercel.com) and sign in
3. Click "New Project"
4. Import your GitHub repository
5. Vercel will auto-detect the configuration from `vercel.json`
6. Click "Deploy"
7. Your chatbot will be live at `https://your-project.vercel.app`

#### Option 2: Deploy via Vercel CLI

1. Install Vercel CLI:
   ```bash
   npm install -g vercel
   ```

2. Clone the repository:
   ```bash
   git clone https://github.com/axyco2004-cyber/axyco2004-cyber-chemistry-chatbot-rgb.git
   cd axyco2004-cyber-chemistry-chatbot-rgb
   ```

3. Deploy to Vercel:
   ```bash
   vercel
   ```

4. Follow the prompts to link your project and deploy

## 💻 Local Development

To test the chatbot locally:

1. Clone the repository:
   ```bash
   git clone https://github.com/axyco2004-cyber/axyco2004-cyber-chemistry-chatbot-rgb.git
   cd axyco2004-cyber-chemistry-chatbot-rgb
   ```

2. Install Vercel CLI (if not already installed):
   ```bash
   npm install -g vercel
   ```

3. Run the development server:
   ```bash
   vercel dev
   ```

4. Open your browser to `http://localhost:3000`

## 🎯 How to Use

Once deployed, simply:

1. Open the web interface in your browser
2. Type your chemistry question in the input field
3. Press "Send" or hit Enter
4. The chatbot will respond with helpful information

### Example Questions

Try asking:
- "Tell me about Carbon"
- "Molar mass of H2O"
- "What is pH?"
- "Explain combustion reactions"
- "What are the types of chemical bonds?"
- "Balance equation help"

## 🏗️ Project Structure

```
├── api/
│   └── chatbot.py          # Serverless Python function for chatbot API
├── public/
│   └── index.html          # Frontend chat interface
├── requirements.txt        # Python dependencies (none required)
├── vercel.json            # Vercel deployment configuration
└── README.md              # This file
```

## 🛠️ Technology Stack

- **Frontend**: HTML, CSS (with gradient animations), Vanilla JavaScript
- **Backend**: Python 3.9 (Vercel serverless functions)
- **Deployment**: Vercel
- **API**: RESTful JSON API with CORS support

## 🤝 Contributing

Contributions are welcome! Feel free to open an issue or submit a pull request.

## 📄 License

This project is open source and available under the [MIT License](LICENSE).