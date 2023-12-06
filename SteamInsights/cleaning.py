import pandas as pd
import numpy as np

# Reviews Dataset ------------------

rw = pd.read_csv('data/reviews.csv')
reviews = rw.loc[:, ['name', 'recent_reviews', 'all_reviews', 'popular_tags',]]
reviews.dropna(subset=['all_reviews'], inplace=True)
pattern = r'([a-zA-Z\s]+),\(([\d,]+)\),-\s(\d+)%' #will handle if the number has a comma
reviews[['recent_sentiment', 'recent_review_number', 'recent_positive_percentage']] = reviews['recent_reviews'].str.extract(pattern)
reviews[['all_sentiment', 'all_review_number', 'all_positive_percentage']] = reviews['all_reviews'].str.extract(pattern)
reviews['recent_review_number'] = reviews['recent_review_number'].str.replace(',', '')
reviews['recent_review_number'] = pd.to_numeric(reviews['recent_review_number'])
reviews['recent_positive_percentage'] = pd.to_numeric(reviews['recent_positive_percentage'])
reviews['all_review_number'] = reviews['all_review_number'].str.replace(',', '')
reviews['all_review_number'] = pd.to_numeric(reviews['all_review_number'])
reviews['all_positive_percentage'] = pd.to_numeric(reviews['all_positive_percentage'])
reviews.drop(columns=['recent_reviews', 'all_reviews'], inplace=True)
reviews.reset_index(inplace=True)
reviews.columns = reviews.columns.str.lower().str.replace(' ', '_')
reviews.to_csv('data/reviews_cleaned.csv', index=False)

# Sales Dataset ------------------

sales2016 = pd.read_csv('data/sales2016.csv')
sales2017 = pd.read_csv('data/sales2017.csv')
s16 = sales2016.loc[:, ['Name', 'Platform', 'Year_of_Release', 'Genre', 'Global_Sales']]
s17 = sales2017.loc[:, ['Name', 'Platform', 'Year_of_Release', 'Genre', 'Global_Sales']]
sales = pd.merge(s16, s17, on=['Name', 'Platform', 'Year_of_Release', 'Genre',], how='outer', suffixes=('_2016', '_2017'))
sales['Global_Sales_2016'].fillna(0, inplace=True)
sales['Global_Sales_2017'].fillna(0, inplace=True)
sales['Global_Sales'] = sales[['Global_Sales_2016', 'Global_Sales_2017']].max(axis=1)
sales.drop(['Global_Sales_2016', 'Global_Sales_2017'], axis=1, inplace=True)
sales['Global_Sales'].replace(0, np.nan, inplace=True)
sales = sales.groupby('Name', as_index=False)['Global_Sales'].sum()
sales.columns = sales.columns.str.lower().str.replace(' ', '_')
sales.to_csv('data/sales_cleaned.csv', index=False)


# Games Dataset ------------------
# Read in games.csv
games_df = pd.read_csv('data/games.csv')

# Remove not needed columns
games = games_df.loc[:, ~games_df.columns.str.contains('url', case=False)]

# Games that support English
games = games[games['Supported languages'].str.contains('english', case=False)]

# Remove columns
# columns_to_remove = ['Supported languages','Required age','Positive','Negative','Score rank','Achievements','Website','Support email','Reviews','Header image','Full audio languages', 'Tags', 'Screenshots', 'Movies', 'About the game', 'Peak CCU', 'Notes']
columns_to_remove = ['Supported languages','Required age','Positive','Negative','Score rank','Website','Support email','Reviews','Header image','Full audio languages', 'Screenshots', 'Movies', 'About the game', 'Peak CCU', 'Notes']
games = games.drop(columns=columns_to_remove, errors='ignore')

# Make Estimated Owners average
# Extract minimum and maximum values using regular expressions
owners_range = games['Estimated owners'].str.extract(r'(\d+) - (\d+)')
min_owners = owners_range[0].astype(float)
max_owners = owners_range[1].astype(float)

# Calculate the average and replace the 'Estimated owners' column
games['Estimated owners'] = (min_owners + max_owners) / 2



# desired_columns = ['Name', 'Release date', 'Estimated owners', 'Price', 'Achievements', 'Windows', 'Mac', 'Linux', 'Developers', 'Publishers', 'Categories', 'Genres', 'Tags']
# games = pd.read_csv('data/games.csv', usecols=desired_columns)
games.dropna(subset=['Name'], inplace=True)
games['Single Player'] = games['Categories'].str.contains('Single-player', case=False, na=False)
games['Release date'] = pd.to_datetime(games['Release date'], format='mixed')
games['Release Year'] = games['Release date'].dt.year
games.drop('Release date', axis=1, inplace=True)
games['players'] = 'NA'
games.loc[games['Categories'].str.contains('Multi') & ~games['Categories'].str.contains('Single').isna(), 'players'] = 'multi'
games.loc[games['Categories'].str.contains('Single') & ~games['Categories'].str.contains('Multi').isna(), 'players'] = 'single'
games.loc[games['Categories'].str.contains('Single') & games['Categories'].str.contains('Multi'), 'players'] = 'single/multi'
games.drop('Categories', axis=1, inplace=True)
games['price_rounded'] = games['Price'].round()
bins = [0, .01, 5, 10, 15, 20, 30, 40, 50, 60, float('inf')]
labels = ['free', '0-5', '5-10', '10-15', '15-20', '20-30', '30-40', '40-50', '50-60', '60+']
games['price_category'] = pd.cut(games['price_rounded'], bins=bins, labels=labels, right=False)
games.columns = games.columns.str.lower().str.replace(' ', '_')
games.to_csv('data/games_cleaned.csv', index=False)



# Ratings Dataset ------------------
# does not need any cleaning

# Joining Games, Reviews, and Sales datasets ------------------
all_games = pd.merge(games, reviews, on='name').merge(sales, on='name')
all_games.drop(columns = ['index'], inplace=True)
all_games.to_csv('data/all_games_cleaned.csv', index=False)


# Tags Dataset ------------------
tags_split = all_games['tags'].str.split(',', expand=True)
unique_tags = tags_split.stack().unique().tolist()
tags_encoded = pd.DataFrame(0, index=all_games.index, columns=unique_tags)
for tag in unique_tags:
    tags_encoded[tag] = tags_split.apply(lambda row: 1 if tag in row.values else 0, axis=1)
tags = pd.concat([all_games['name'], tags_encoded], axis=1)
names = tags['name']
t = tags.copy()
t.set_index('name', inplace=True)
t_sort = t.sum().sort_values(ascending=False)
t = tags[t_sort.index]
t['name'] = names
t.insert(0, 'name', t.pop('name'))
tags = t.copy()
tags.to_csv('data/tags.csv', index=False)
