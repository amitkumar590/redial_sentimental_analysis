import pandas as pd
import json
import re

# Function to read a JSONL file, replace movie mentions, and extract utterance texts
def extract_and_replace_mentions(jsonl_file):
    data = []
    with open(jsonl_file, 'r') as file:
        for line in file:
            conversation = json.loads(line)
            movie_mentions = conversation['movieMentions']
            for message in conversation['messages']:
                text = message['text']
                # # Replace all movie mentions in the text
                # for movie_id, movie_name in movie_mentions.items():
                #     text = re.sub(rf'@{movie_id}', movie_name, text)
                data.append(text)
    return data

# Extract and replace movie mentions from the JSONL file
utterance_texts = extract_and_replace_mentions('train_data.jsonl')

# Create a DataFrame
df = pd.DataFrame(utterance_texts, columns=['text'])

# Save the DataFrame to a CSV file
df.to_csv('train_utterance_texts.csv', index=False)

print(df)
