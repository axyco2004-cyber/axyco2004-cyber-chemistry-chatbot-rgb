package com.chemistry.chatbot;

import com.chemistry.chatbot.model.QAPair;
import com.chemistry.chatbot.model.Topic;
import com.google.gson.Gson;
import com.google.gson.JsonObject;

import java.io.BufferedReader;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.nio.charset.StandardCharsets;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.stream.Collectors;

/**
 * Manages the chemistry knowledge base.
 * Loads and provides access to chemistry topics and Q&A pairs.
 */
public class KnowledgeBase {
    private List<Topic> topics;

    /**
     * Creates a new KnowledgeBase and loads data from the JSON file.
     */
    public KnowledgeBase() {
        this.topics = new ArrayList<>();
        loadKnowledge();
    }

    /**
     * Loads chemistry knowledge from the JSON resource file.
     */
    private void loadKnowledge() {
        try {
            InputStream inputStream = getClass().getClassLoader()
                    .getResourceAsStream("chemistry_knowledge.json");
            
            if (inputStream == null) {
                System.err.println("Error: Could not find chemistry_knowledge.json");
                return;
            }

            BufferedReader reader = new BufferedReader(
                    new InputStreamReader(inputStream, StandardCharsets.UTF_8));
            String jsonContent = reader.lines().collect(Collectors.joining("\n"));
            reader.close();

            Gson gson = new Gson();
            JsonObject jsonObject = gson.fromJson(jsonContent, JsonObject.class);
            Topic[] topicsArray = gson.fromJson(jsonObject.get("topics"), Topic[].class);
            
            this.topics = Arrays.asList(topicsArray);
            
            System.out.println("✓ Loaded " + topics.size() + " chemistry topics successfully!");
            
        } catch (Exception e) {
            System.err.println("Error loading knowledge base: " + e.getMessage());
            e.printStackTrace();
        }
    }

    /**
     * Gets all topics in the knowledge base.
     *
     * @return List of all topics
     */
    public List<Topic> getAllTopics() {
        return topics;
    }

    /**
     * Finds a topic by name.
     *
     * @param topicName The name of the topic to find
     * @return The topic if found, null otherwise
     */
    public Topic getTopicByName(String topicName) {
        for (Topic topic : topics) {
            if (topic.getName().equalsIgnoreCase(topicName)) {
                return topic;
            }
        }
        return null;
    }

    /**
     * Gets all Q&A pairs from all topics.
     *
     * @return List of all Q&A pairs
     */
    public List<QAPair> getAllQAPairs() {
        List<QAPair> allPairs = new ArrayList<>();
        for (Topic topic : topics) {
            if (topic.getQaPairs() != null) {
                allPairs.addAll(topic.getQaPairs());
            }
        }
        return allPairs;
    }

    /**
     * Gets the total number of Q&A pairs in the knowledge base.
     *
     * @return Total number of Q&A pairs
     */
    public int getTotalQAPairs() {
        return getAllQAPairs().size();
    }
}
