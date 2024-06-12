import json
from transformers import pipeline

# Load the sentiment-analysis pipeline
sentiment_analysis = pipeline("sentiment-analysis")

# Function to analyze sentiments for a single conversation
def analyze_conversation(conversation):
    movie_sentiments = {}
    movie_mentions = conversation.get("movieMentions", {})
    messages = conversation.get("messages", [])

    # Create a mapping of message ID to text
    message_texts = {message["messageId"]: message["text"] for message in messages}

    for movie_id, movie_name in movie_mentions.items():
        # Find user responses related to this movie ID
        for message in messages:
            if movie_id in message["text"]:
                response_text = message["text"]
                sentiment = sentiment_analysis(response_text)[0]
                sentiment_label = sentiment['label']

                # Store the sentiment and sentence for the movie ID
                if movie_id not in movie_sentiments:
                    movie_sentiments[movie_id] = []
                movie_sentiments[movie_id].append((sentiment_label, response_text))

    return movie_sentiments

# Load and analyze the dataset
movie_sentiments = {}

with open('short_data.jsonl', 'r') as file:
    for line in file:
        conversation = json.loads(line)
        conversation_sentiments = analyze_conversation(conversation)

        # Merge sentiments from this conversation into the overall results
        for movie_id, sentiments in conversation_sentiments.items():
            if movie_id not in movie_sentiments:
                movie_sentiments[movie_id] = []
            movie_sentiments[movie_id].extend(sentiments)

# Print the results
for movie_id, sentiments in movie_sentiments.items():
    print(f"Movie ID: {movie_id}")
    for sentiment, sentence in sentiments:
        print(f"  Sentiment: {sentiment}, Sentence: {sentence}")
