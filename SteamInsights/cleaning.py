import pandas as pd
import numpy as np

# Reviews Dataset ------------------

rw = pd.read_csv('data/reviews.csv')
reviews = rw.loc[:, ['name', 'recent_reviews', 'all_reviews',
                     'popular_tags', 'achievements']]
reviews.dropna(subset=['all_reviews'], inplace=True)

# use regex to separate out the numbers in recent and all reviews
pattern = r'([a-zA-Z\s]+),\(([\d,]+)\),-\s(\d+)%' #will handle if the number has a comma

# create the 3 new columns for recent and all reviews
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
sales['Year_of_Release'] = sales['Year_of_Release'].fillna(0).astype(int)


# Games Dataset ------------------
# Read in games.csv
games_df = pd.read_csv('data/games.csv')

# Remove not needed columns
games = games_df.loc[:, ~games_df.columns.str.contains('url', case=False)]

# Games that support English
games = games[games['Supported languages'].str.contains('english', case=False)]

# Remove columns
columns_to_remove = ['Supported languages','Required age','Positive','Negative','Score rank','Achievements','Website','Support email','Reviews','Header image','Full audio languages', 'Tags', 'Screenshots', 'Movies', 'About the game', 'Peak CCU', 'Notes']
games = games.drop(columns=columns_to_remove, errors='ignore')

# Make Estimated Owners average
# Extract minimum and maximum values using regular expressions
owners_range = games['Estimated owners'].str.extract(r'(\d+) - (\d+)')
min_owners = owners_range[0].astype(float)
max_owners = owners_range[1].astype(float)

# Calculate the average and replace the 'Estimated owners' column
games['Estimated owners'] = (min_owners + max_owners) / 2


# Ratings Dataset ------------------
# does not need any cleaning
