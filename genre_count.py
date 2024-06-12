import pandas as pd
from collections import Counter
import ast

# Read the CSV file
df = pd.read_csv('train_movie_genres.csv')

# Initialize a Counter to store genre counts
genre_counts = Counter()

# Iterate over each row in the dataframe
for genres_str in df['genres']:
    # Convert the string representation of the list to an actual list
    genres_list = ast.literal_eval(genres_str)
    # Update the counter with genres from the current row
    genre_counts.update(genres_list)

# Sort the genre counts in descending order
sorted_genre_counts = sorted(genre_counts.items(), key=lambda x: x[1], reverse=True)

# Print the total number of occurrences for each genre in descending order
for genre, count in sorted_genre_counts:
    print(f"{genre}: {count}")

# If you want the total number of unique genres
total_unique_genres = len(genre_counts)
print(f"Total number of unique genres: {total_unique_genres}")
