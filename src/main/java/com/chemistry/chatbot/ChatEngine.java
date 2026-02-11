package com.chemistry.chatbot;

import com.chemistry.chatbot.model.QAPair;
import com.chemistry.chatbot.model.Topic;

import java.util.List;

/**
 * Core chatbot engine that processes user input and generates responses.
 */
public class ChatEngine {
    private final KnowledgeBase knowledgeBase;
    private final TopicMatcher topicMatcher;

    /**
     * Creates a new ChatEngine with the given knowledge base.
     *
     * @param knowledgeBase The chemistry knowledge base
     */
    public ChatEngine(KnowledgeBase knowledgeBase) {
        this.knowledgeBase = knowledgeBase;
        this.topicMatcher = new TopicMatcher();
    }

    /**
     * Processes a user question and returns an appropriate response.
     *
     * @param userInput The user's question or input
     * @return The chatbot's response
     */
    public String processInput(String userInput) {
        if (userInput == null || userInput.trim().isEmpty()) {
            return "Please ask me a chemistry question!";
        }

        String input = userInput.trim();

        // Handle special commands
        if (isGreeting(input)) {
            return "Hello! I'm here to help you with chemistry questions. What would you like to know?";
        }

        if (isThanks(input)) {
            return "You're welcome! Feel free to ask more chemistry questions anytime.";
        }

        // Try to find matching answer
        List<QAPair> allPairs = knowledgeBase.getAllQAPairs();
        QAPair bestMatch = topicMatcher.findBestMatch(input, allPairs);

        if (bestMatch != null) {
            return bestMatch.getAnswer();
        }

        // No match found
        return generateNoMatchResponse();
    }

    /**
     * Checks if the input is a greeting.
     *
     * @param input User input
     * @return true if input is a greeting
     */
    private boolean isGreeting(String input) {
        String lower = input.toLowerCase();
        return lower.matches(".*(hello|hi|hey|greetings|good morning|good afternoon).*");
    }

    /**
     * Checks if the input is a thank you message.
     *
     * @param input User input
     * @return true if input is a thank you
     */
    private boolean isThanks(String input) {
        String lower = input.toLowerCase();
        return lower.matches(".*(thank|thanks|appreciate).*");
    }

    /**
     * Generates a helpful response when no match is found.
     *
     * @return A helpful no-match response
     */
    private String generateNoMatchResponse() {
        return "I'm not sure about that. Try asking about:\n" +
               "  • Atomic structure (atoms, protons, electrons)\n" +
               "  • The periodic table (elements, groups, periods)\n" +
               "  • Chemical bonding (ionic, covalent, metallic)\n" +
               "  • Chemical reactions (types, balancing)\n" +
               "  • Acids and bases\n" +
               "  • Stoichiometry and moles\n" +
               "  • States of matter and gas laws\n" +
               "  • Organic chemistry basics\n" +
               "  • Solutions and concentrations\n" +
               "Type 'topics' to see all available topics.";
    }

    /**
     * Gets a formatted list of all available topics.
     *
     * @return String containing all topics and their descriptions
     */
    public String getTopicsList() {
        List<Topic> topics = knowledgeBase.getAllTopics();
        StringBuilder sb = new StringBuilder();
        sb.append("\n📚 Available Chemistry Topics:\n");
        sb.append("=" .repeat(50)).append("\n\n");

        for (int i = 0; i < topics.size(); i++) {
            Topic topic = topics.get(i);
            sb.append(String.format("%d. %s\n", i + 1, topic.getName()));
            sb.append(String.format("   %s\n", topic.getDescription()));
            sb.append(String.format("   (%d Q&A pairs)\n\n", 
                    topic.getQaPairs() != null ? topic.getQaPairs().size() : 0));
        }

        return sb.toString();
    }

    /**
     * Gets detailed information about a specific topic.
     *
     * @param topicName The name of the topic
     * @return Formatted string with topic Q&A pairs
     */
    public String browseTopic(String topicName) {
        Topic topic = knowledgeBase.getTopicByName(topicName);
        
        if (topic == null) {
            return "Topic not found: " + topicName + "\nType 'topics' to see available topics.";
        }

        StringBuilder sb = new StringBuilder();
        sb.append("\n📖 Topic: ").append(topic.getName()).append("\n");
        sb.append("=".repeat(50)).append("\n");
        sb.append(topic.getDescription()).append("\n\n");

        if (topic.getQaPairs() != null && !topic.getQaPairs().isEmpty()) {
            sb.append("Sample Questions:\n\n");
            
            for (int i = 0; i < topic.getQaPairs().size(); i++) {
                QAPair pair = topic.getQaPairs().get(i);
                sb.append(String.format("%d. %s\n", i + 1, 
                        pair.getQuestions() != null && !pair.getQuestions().isEmpty() 
                        ? pair.getQuestions().get(0) : ""));
            }
        }

        return sb.toString();
    }

    /**
     * Gets the knowledge base instance.
     *
     * @return The knowledge base
     */
    public KnowledgeBase getKnowledgeBase() {
        return knowledgeBase;
    }
}
