from tmdbv3api import TMDb, Movie
import pandas as pd
import re

# Set up TMDb API
tmdb = TMDb()
tmdb.api_key = 'dfc904b74bf93c815115bce045f5babc'
movie = Movie()

# Read the text file
with open('train_utterance_texts.csv', 'r') as file:
    text = file.read()

# Read the movie names file
movie_names_df = pd.read_csv('movies_with_mentions.csv')

# Extract movie mentions from the text
movie_mentions = re.findall(r'@(\d+)', text)

# Initialize dictionary to store movie genres and a list to track skipped movies
movie_genres = {}
skipped_movies = []

# Fetch genres for each movie mentioned
for mention in movie_mentions:
    movie_id = int(mention)
    if movie_id in movie_names_df['movieId'].values:
        movie_name = movie_names_df.loc[movie_names_df['movieId'] == movie_id, 'movieName'].iloc[0]
        # Remove the year and parentheses from the movie name
        match = re.search(r'\s\((\d{4})\)', movie_name)
        if match:
            year = match.group(1)
            movie_name_clean = re.sub(r'\s\(\d{4}\)', '', movie_name).strip()
        else:
            year = None
            movie_name_clean = movie_name.strip()
            
        try:
            search_result = movie.search(movie_name_clean)
        except Exception as e:
            print(f"Error searching for movie '{movie_name_clean}': {e}")
            skipped_movies.append(movie_name)
            continue

        # Print search result for debugging
        print(f"Search result for '{movie_name_clean}':")
        for result in search_result:
            if isinstance(result, str):
                print(f"Skipping invalid search result: {result}")
                continue
            release_date = getattr(result, 'release_date', None)
            if release_date:
                print(f" - {result.title} ({release_date})")
            else:
                print(f" - {result.title}")

        if search_result:
            found = False
            for result in search_result:
                if not isinstance(result, str):
                    result_title = result.title.lower()
                    result_year = result.release_date.split('-')[0] if getattr(result, 'release_date', None) else None
                    # Match based on title and optionally year
                    if result_title == movie_name_clean.lower() and (year is None or result_year == year):
                        print(f"Matching result found: {result.title} ({result.release_date})")
                        try:
                            movie_details = movie.details(result.id)
                            genres = [genre['name'] for genre in movie_details.genres]
                            movie_genres[movie_name] = genres
                            found = True
                            break
                        except Exception as e:
                            print(f"Error fetching details for movie '{result.title}': {e}")
                            skipped_movies.append(movie_name)
                            break
            
            if not found:
                # If no exact year match, pick the first title match
                for result in search_result:
                    if not isinstance(result, str) and result.title.lower() == movie_name_clean.lower():
                        print(f"Matching result found (ignoring year): {result.title} ({result.release_date})")
                        try:
                            movie_details = movie.details(result.id)
                            genres = [genre['name'] for genre in movie_details.genres]
                            movie_genres[movie_name] = genres
                            found = True
                            break
                        except Exception as e:
                            print(f"Error fetching details for movie '{result.title}': {e}")
                            skipped_movies.append(movie_name)
                            break
            
            if not found:
                if year:
                    print(f"No exact match found for movie '{movie_name_clean}' with year '{year}'.")
                else:
                    print(f"No exact match found for movie '{movie_name_clean}'.")
                skipped_movies.append(movie_name)
        else:
            print(f"No search results found for movie '{movie_name_clean}'.")
            skipped_movies.append(movie_name)
    else:
        print(f"Movie ID '{movie_id}' not found in the movie names file.")
        skipped_movies.append(movie_name)

# Save the movie genres to a CSV file
df_genres = pd.DataFrame(movie_genres.items(), columns=['movie', 'genres'])
df_genres.to_csv('train_movie_genres.csv', index=False)

# Print the list of skipped movies
print("Skipped movies:")
for movie in skipped_movies:
    print(movie)

print(df_genres)
