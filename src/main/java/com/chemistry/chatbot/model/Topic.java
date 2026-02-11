package com.chemistry.chatbot.model;

import java.util.List;

/**
 * Represents a chemistry topic with associated Q&A pairs.
 */
public class Topic {
    private String name;
    private String description;
    private List<QAPair> qaPairs;

    /**
     * Default constructor for JSON deserialization.
     */
    public Topic() {
    }

    /**
     * Creates a new Topic with the specified name, description, and Q&A pairs.
     *
     * @param name        The topic name
     * @param description Brief description of the topic
     * @param qaPairs     List of Q&A pairs for this topic
     */
    public Topic(String name, String description, List<QAPair> qaPairs) {
        this.name = name;
        this.description = description;
        this.qaPairs = qaPairs;
    }

    /**
     * Gets the topic name.
     *
     * @return The topic name
     */
    public String getName() {
        return name;
    }

    /**
     * Sets the topic name.
     *
     * @param name The topic name
     */
    public void setName(String name) {
        this.name = name;
    }

    /**
     * Gets the topic description.
     *
     * @return The topic description
     */
    public String getDescription() {
        return description;
    }

    /**
     * Sets the topic description.
     *
     * @param description The topic description
     */
    public void setDescription(String description) {
        this.description = description;
    }

    /**
     * Gets the list of Q&A pairs.
     *
     * @return List of Q&A pairs
     */
    public List<QAPair> getQaPairs() {
        return qaPairs;
    }

    /**
     * Sets the list of Q&A pairs.
     *
     * @param qaPairs List of Q&A pairs
     */
    public void setQaPairs(List<QAPair> qaPairs) {
        this.qaPairs = qaPairs;
    }
}
