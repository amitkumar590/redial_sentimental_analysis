import pandas as pd

# List of movies provided
movies_list = [
    "The Sixth Battalion (1998)",
    "Annabelle 2 (2017)",
    "Annabelle 2 (2017)",
    "A Nightmare on Elm Street 2: Freddy's Revenge (1985)",
    "A Nightmare on Elm Street 2: Freddy's Revenge (1985)",
    "A Nightmare on Elm Street 5: The Dream Child (1989)",
    "Annabelle 2 (2017)",
    "Annabelle 2 (2017)",
    "Killer Clowns from Outer Space (1988)",
    "Z movie",
    "The Sowers (1916)",
    "Voices of Spring (1933)",
    "Voices of Spring (1933)",
    "Airhawk (1981)",
    "Kill Bill: Volume 1 (2003)",
    "Barbie Thumbelina",
    "Making a Murderer",
    "Kill Bill: Volume 1 (2003)",
    "(2007)",
    "Insidious: Chapter 4 (2018)",
    "Killer Clowns from Outer Space (1988)",
    "Tucker & Dale vs. Evil (2010)",
    "12 Monkeys (1995)",
    "The 40-Year-Old Virgin (2005)",
    "Sex and Lucia (2001)",
    "American Psycho 2 (2002)",
    "Malèna (2000)",
    "Highlander III: The Sorcerer (1994)",
    "Kill Bill: Volume 1 (2003)",
    "Kill Bill: Volume 1 (2003)",
    "12 Monkeys (1995)",
    "The 40-Year-Old Virgin (2005)",
    "Night of the Living Dead 3D: Re-Animation (2012)",
    "Tucker & Dale vs. Evil (2010)",
    "Wes Craven's New Nightmare (1994)",
    "Way of the Dragon (1972)",
    "Way of the Dragon (1972)",
    "The 40-Year-Old Virgin (2005)",
    "The 40-Year-Old Virgin (2005)",
    "Star Wars: Episode VIII – The Last Jedi (2017)",
    "The 40-Year-Old Virgin (2005)",
    "Tucker & Dale vs. Evil (2010)",
    "WALL-E (2008)",
    "WALL-E (2008)",
    "Tucker & Dale vs. Evil (2010)",
    "The 40-Year-Old Virgin (2005)",
    "O Brother, Where Art Thou%3F (2000)",
    "Who's Afraid of Virginia Woolf%3F (1966)",
    "Tucker & Dale vs. Evil (2010)",
    "Tucker & Dale vs. Evil (2010)",
    "Tucker & Dale vs. Evil (2010)",
    "The Divergent Series",
    "Star Wars: Episode VIII – The Last Jedi (2017)",
    "Harry Potter and the Deathly Hallows – Part 2 (2011)",
    "Tucker & Dale vs. Evil (2010)",
    "Tucker & Dale vs. Evil (2010)",
    "Tucker & Dale vs. Evil (2010)",
    "The Dark Knight Trilogy",
    "The 40-Year-Old Virgin (2005)",
    "Making a Murderer",
    "WALL-E (2008)",
    "WALL-E (2008)",
    "The Taking of Pelham 123 (2009)",
    "Spiders 3D (2013)",
    "H. G. Wells' The War of the Worlds (2005)",
    "Star Wars: Episode VIII – The Last Jedi (2017)",
    "Glee: The 3D Concert Movie (2011)",
    "WALL-E (2008)",
    "WALL-E (2008)",
    "WALL-E (2008)",
    "WALL-E (2008)",
    "Kill Bill: Volume 1 (2003)",
    "I've Lost My Husband! (1937)",
    "List of accolades received by Inception",
    "Kill Bill: Volume 1 (2003)",
    "Up Denali 3D (2003)",
    "The Adventures of Sharkboy and Lavagirl in 3-D (2005)",
    "Spiders 3D (2013)",
    "Superman Classic",
    "Batman Revealed (2012)",
    "Spiders 3D (2013)",
    "Batman Revealed (2012)",
    "Batman Revealed (2012)",
    "Kill Bill: Volume 1 (2003)",
    "Kill Bill: Volume 2 (2004)",
    "Batman Revealed (2012)",
    "Batman Revealed (2012)",
    "Dance Star (2010)",
    "Batman Revealed (2012)"
]

# Remove duplicates from the list
unique_movies = list(set(movies_list))

# Sort the list to maintain a consistent order
unique_movies.sort()

# Write the cleaned list to a new CSV file
df_unique_movies = pd.DataFrame(unique_movies, columns=['Movie'])
df_unique_movies.to_csv('cleaned_movies.csv', index=False)

print("Duplicates removed and cleaned list saved to 'cleaned_movies.csv'.")