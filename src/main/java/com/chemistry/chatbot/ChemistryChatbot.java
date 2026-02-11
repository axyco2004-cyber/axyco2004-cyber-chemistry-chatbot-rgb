package com.chemistry.chatbot;

import java.util.Scanner;

/**
 * Main entry point for the Chemistry Chatbot application.
 * Provides an interactive command-line interface for students to ask chemistry questions.
 */
public class ChemistryChatbot {
    private final ChatEngine chatEngine;
    private final Scanner scanner;
    private boolean running;

    /**
     * Creates a new ChemistryChatbot instance.
     */
    public ChemistryChatbot() {
        KnowledgeBase knowledgeBase = new KnowledgeBase();
        this.chatEngine = new ChatEngine(knowledgeBase);
        this.scanner = new Scanner(System.in);
        this.running = true;
    }

    /**
     * Main method - entry point for the application.
     *
     * @param args Command line arguments (not used)
     */
    public static void main(String[] args) {
        ChemistryChatbot chatbot = new ChemistryChatbot();
        chatbot.start();
    }

    /**
     * Starts the chatbot and runs the main interaction loop.
     */
    public void start() {
        displayWelcome();
        
        while (running) {
            System.out.print("\n💬 You: ");
            String input = scanner.nextLine().trim();

            if (input.isEmpty()) {
                continue;
            }

            handleInput(input);
        }

        scanner.close();
        System.out.println("\n👋 Thanks for using Chemistry Chatbot! Happy learning!");
    }

    /**
     * Displays the welcome message and instructions.
     */
    private void displayWelcome() {
        System.out.println("\n" + "=".repeat(70));
        System.out.println("🧪 WELCOME TO CHEMISTRY CHATBOT 🧪");
        System.out.println("=".repeat(70));
        System.out.println("\nYour interactive assistant for learning chemistry!");
        System.out.println("\nI can help you with:");
        System.out.println("  • Atomic structure and the periodic table");
        System.out.println("  • Chemical bonding and reactions");
        System.out.println("  • Acids, bases, and pH");
        System.out.println("  • Stoichiometry and moles");
        System.out.println("  • Gas laws and states of matter");
        System.out.println("  • Organic chemistry basics");
        System.out.println("  • Solutions and concentrations");
        System.out.println("\nCommands:");
        System.out.println("  help     - Show this help message");
        System.out.println("  topics   - List all available topics");
        System.out.println("  browse <topic> - View questions for a specific topic");
        System.out.println("  quit/exit - Exit the chatbot");
        System.out.println("\n" + "=".repeat(70));
        System.out.println("Ask me anything about chemistry!");
    }

    /**
     * Handles user input and executes appropriate commands.
     *
     * @param input User input string
     */
    private void handleInput(String input) {
        String lowerInput = input.toLowerCase().trim();

        // Handle commands
        if (lowerInput.equals("quit") || lowerInput.equals("exit")) {
            running = false;
            return;
        }

        if (lowerInput.equals("help")) {
            displayHelp();
            return;
        }

        if (lowerInput.equals("topics")) {
            System.out.println(chatEngine.getTopicsList());
            return;
        }

        if (lowerInput.startsWith("browse ")) {
            String topicName = input.substring(7).trim();
            System.out.println(chatEngine.browseTopic(topicName));
            return;
        }

        // Process as a regular question
        String response = chatEngine.processInput(input);
        System.out.println("\n🤖 Bot: " + response);
    }

    /**
     * Displays the help message with available commands.
     */
    private void displayHelp() {
        System.out.println("\n" + "=".repeat(70));
        System.out.println("📖 HELP - Available Commands");
        System.out.println("=".repeat(70));
        System.out.println("\nCommands:");
        System.out.println("  help              - Display this help message");
        System.out.println("  topics            - List all available chemistry topics");
        System.out.println("  browse <topic>    - View sample questions for a specific topic");
        System.out.println("                      Example: browse Atomic Structure");
        System.out.println("  quit or exit      - Exit the chatbot");
        System.out.println("\nExample Questions:");
        System.out.println("  • What is an atom?");
        System.out.println("  • Define ionic bond");
        System.out.println("  • What is pH?");
        System.out.println("  • What is a mole?");
        System.out.println("  • What are the states of matter?");
        System.out.println("  • What is an alkane?");
        System.out.println("  • How do you balance a chemical equation?");
        System.out.println("  • What is Boyle's Law?");
        System.out.println("\nTips:");
        System.out.println("  • Be specific in your questions");
        System.out.println("  • Use chemistry terminology when possible");
        System.out.println("  • Try different phrasings if you don't get the answer you need");
        System.out.println("=".repeat(70));
    }
}
