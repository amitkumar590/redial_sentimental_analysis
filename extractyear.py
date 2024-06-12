import pandas as pd
import re

# Read the CSV file
df = pd.read_csv('movies_with_mentions.csv')

# Function to extract year and clean movie name
def extract_year(movie_name):
    match = re.search(r'\((\d{4})\)', movie_name)
    if match:
        year = match.group(1)
        name = re.sub(r'\s*\(\d{4}\)', '', movie_name)
        return name, year
    else:
        return movie_name, None

# Apply the function to the DataFrame
df[['movieName', 'year']] = df['movieName'].apply(lambda x: pd.Series(extract_year(x)))

# Save the modified DataFrame back to a CSV file
df.to_csv('movies_modified.csv', index=False)

print(df)
