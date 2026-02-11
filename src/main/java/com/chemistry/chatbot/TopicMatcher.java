package com.chemistry.chatbot;

import com.chemistry.chatbot.model.QAPair;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

/**
 * Matches user questions to relevant Q&A pairs using keyword matching
 * and similarity scoring.
 */
public class TopicMatcher {
    
    /**
     * Finds the best matching Q&A pairs for a user's question.
     *
     * @param userQuestion The user's question
     * @param qaPairs      List of available Q&A pairs
     * @param maxResults   Maximum number of results to return
     * @return List of matching Q&A pairs, ordered by relevance
     */
    public List<QAPair> findMatches(String userQuestion, List<QAPair> qaPairs, int maxResults) {
        if (userQuestion == null || userQuestion.trim().isEmpty()) {
            return new ArrayList<>();
        }

        // Normalize the user question
        String normalizedQuestion = normalizeText(userQuestion);
        String[] questionWords = normalizedQuestion.split("\\s+");

        // Score each Q&A pair
        Map<QAPair, Double> scores = new HashMap<>();
        
        for (QAPair pair : qaPairs) {
            double score = calculateScore(normalizedQuestion, questionWords, pair);
            if (score > 0) {
                scores.put(pair, score);
            }
        }

        // Sort by score and return top matches
        List<QAPair> matches = new ArrayList<>(scores.keySet());
        matches.sort((a, b) -> Double.compare(scores.get(b), scores.get(a)));

        // Return up to maxResults
        return matches.subList(0, Math.min(maxResults, matches.size()));
    }

    /**
     * Calculates a relevance score for a Q&A pair based on the user question.
     *
     * @param normalizedQuestion Full normalized question
     * @param questionWords      Individual words from the question
     * @param pair               The Q&A pair to score
     * @return Relevance score (higher is better)
     */
    private double calculateScore(String normalizedQuestion, String[] questionWords, QAPair pair) {
        double score = 0.0;

        // Check for exact question match (highest score)
        if (pair.getQuestions() != null) {
            for (String question : pair.getQuestions()) {
                String normalizedPairQuestion = normalizeText(question);
                if (normalizedPairQuestion.equals(normalizedQuestion)) {
                    return 1000.0; // Perfect match
                }
                // Check for substring match
                if (normalizedPairQuestion.contains(normalizedQuestion) || 
                    normalizedQuestion.contains(normalizedPairQuestion)) {
                    score += 500.0;
                }
            }
        }

        // Check keyword matches
        if (pair.getKeywords() != null) {
            for (String keyword : pair.getKeywords()) {
                String normalizedKeyword = normalizeText(keyword);
                
                // Full keyword match in question
                if (normalizedQuestion.contains(normalizedKeyword)) {
                    score += 50.0;
                }

                // Individual word matches
                for (String word : questionWords) {
                    if (word.length() > 2) { // Ignore very short words
                        if (normalizedKeyword.equals(word)) {
                            score += 30.0;
                        } else if (normalizedKeyword.contains(word) || word.contains(normalizedKeyword)) {
                            score += 10.0;
                        }
                    }
                }
            }
        }

        // Check for word matches in stored questions
        if (pair.getQuestions() != null) {
            for (String question : pair.getQuestions()) {
                String normalizedPairQuestion = normalizeText(question);
                String[] pairWords = normalizedPairQuestion.split("\\s+");
                
                for (String userWord : questionWords) {
                    if (userWord.length() > 3) { // Longer words are more significant
                        for (String pairWord : pairWords) {
                            if (userWord.equals(pairWord)) {
                                score += 5.0;
                            }
                        }
                    }
                }
            }
        }

        return score;
    }

    /**
     * Normalizes text for matching by converting to lowercase and removing punctuation.
     *
     * @param text The text to normalize
     * @return Normalized text
     */
    private String normalizeText(String text) {
        if (text == null) {
            return "";
        }
        return text.toLowerCase()
                .replaceAll("[^a-z0-9\\s]", " ")
                .replaceAll("\\s+", " ")
                .trim();
    }

    /**
     * Finds the single best match for a user question.
     *
     * @param userQuestion The user's question
     * @param qaPairs      List of available Q&A pairs
     * @return The best matching Q&A pair, or null if no good match found
     */
    public QAPair findBestMatch(String userQuestion, List<QAPair> qaPairs) {
        List<QAPair> matches = findMatches(userQuestion, qaPairs, 1);
        return matches.isEmpty() ? null : matches.get(0);
    }
}
