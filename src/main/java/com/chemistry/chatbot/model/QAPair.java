package com.chemistry.chatbot.model;

import java.util.List;

/**
 * Represents a Question-Answer pair in the chemistry knowledge base.
 * Contains question variations and a corresponding answer.
 */
public class QAPair {
    private List<String> questions;
    private String answer;
    private List<String> keywords;

    /**
     * Default constructor for JSON deserialization.
     */
    public QAPair() {
    }

    /**
     * Creates a new QAPair with the specified questions, answer, and keywords.
     *
     * @param questions List of question variations
     * @param answer    The answer to the questions
     * @param keywords  Keywords associated with this Q&A pair
     */
    public QAPair(List<String> questions, String answer, List<String> keywords) {
        this.questions = questions;
        this.answer = answer;
        this.keywords = keywords;
    }

    /**
     * Gets the list of question variations.
     *
     * @return List of question variations
     */
    public List<String> getQuestions() {
        return questions;
    }

    /**
     * Sets the list of question variations.
     *
     * @param questions List of question variations
     */
    public void setQuestions(List<String> questions) {
        this.questions = questions;
    }

    /**
     * Gets the answer.
     *
     * @return The answer string
     */
    public String getAnswer() {
        return answer;
    }

    /**
     * Sets the answer.
     *
     * @param answer The answer string
     */
    public void setAnswer(String answer) {
        this.answer = answer;
    }

    /**
     * Gets the list of keywords.
     *
     * @return List of keywords
     */
    public List<String> getKeywords() {
        return keywords;
    }

    /**
     * Sets the list of keywords.
     *
     * @param keywords List of keywords
     */
    public void setKeywords(List<String> keywords) {
        this.keywords = keywords;
    }
}
