from tmdbv3api import TMDb, Movie
import pandas as pd
import re
import urllib.parse

# Set up TMDb API
tmdb = TMDb()
tmdb.api_key = 'dfc904b74bf93c815115bce045f5babc'
movie = Movie()

# Read the skipped movies file, handling quoted movie names
skipped_movies_df = pd.read_csv('skipped_movies.csv', header=None, names=['movieName'], quotechar='"')

# Initialize dictionary to store movie genres and a list to track skipped movies
movie_genres = {}
skipped_movies = []

# Function to normalize movie names
def normalize_movie_name(name):
    # Remove year in parentheses and special characters
    name = re.sub(r'\s\(\d{4}\)', '', name)
    name = re.sub(r'[^\w\s]', '', name)
    name = name.strip().lower()
    return name

# Fetch genres for each skipped movie
for index, row in skipped_movies_df.iterrows():
    movie_name = row['movieName']
    # Remove the year and parentheses from the movie name if present
    match = re.search(r'\s\((\d{4})\)', movie_name)
    if match:
        year = match.group(1)
        movie_name_clean = re.sub(r'\s\(\d{4}\)', '', movie_name).strip()
    else:
        year = None
        movie_name_clean = movie_name.strip()
    
    # Normalize movie name for search
    normalized_movie_name = normalize_movie_name(movie_name_clean)
    
    try:
        # URL encode the movie name for search
        search_result = movie.search(urllib.parse.quote(movie_name_clean))
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
                result_title = normalize_movie_name(result.title)
                result_year = result.release_date.split('-')[0] if getattr(result, 'release_date', None) else None
                # Match based on title and optionally year
                if result_title == normalized_movie_name and (year is None or result_year == year):
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
            # If no exact match, try prefix matching
            prefix_match = None
            for result in search_result:
                if not isinstance(result, str) and normalize_movie_name(result.title).startswith(normalized_movie_name):
                    prefix_match = result
                    break

            if prefix_match:
                print(f"Prefix matching result found: {prefix_match.title} ({prefix_match.release_date})")
                try:
                    movie_details = movie.details(prefix_match.id)
                    genres = [genre['name'] for genre in movie_details.genres]
                    movie_genres[movie_name] = genres
                except Exception as e:
                    print(f"Error fetching details for movie '{prefix_match.title}': {e}")
                    skipped_movies.append(movie_name)
            else:
                # If no prefix match, fall back to the first title match
                first_match = None
                for result in search_result:
                    if not isinstance(result, str) and normalize_movie_name(result.title) == normalized_movie_name:
                        first_match = result
                        break
                
                if first_match:
                    print(f"Matching result found (ignoring year): {first_match.title} ({first_match.release_date})")
                    try:
                        movie_details = movie.details(first_match.id)
                        genres = [genre['name'] for genre in movie_details.genres]
                        movie_genres[movie_name] = genres
                    except Exception as e:
                        print(f"Error fetching details for movie '{first_match.title}': {e}")
                        skipped_movies.append(movie_name)
                else:
                    print(f"No exact or prefix match found for movie '{movie_name_clean}'. Adding to skipped list for manual review.")
                    skipped_movies.append(movie_name)
    else:
        print(f"No search results found for movie '{movie_name_clean}'.")
        skipped_movies.append(movie_name)

# Save the movie genres to a CSV file
df_genres = pd.DataFrame(movie_genres.items(), columns=['movie', 'genres'])
df_genres.to_csv('skipped_movie_genres.csv', index=False)

# Print the list of skipped movies
print("Skipped movies:")
for movie in skipped_movies:
    print(movie)

print(df_genres)