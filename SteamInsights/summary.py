import pandas as pd
import numpy as np

all_games = pd.read_csv('data/all_games_cleaned.csv')
tags = pd.read_csv('data/tags.csv')

def game_summary(game_name):
    """
    Retrieve a summary of the specified game.

    Parameters:
    - game_name (str): The name of the game for which to retrieve the summary.

    Returns:
    - pandas.DataFrame: A DataFrame containing the summary information for the specified game.
      Columns included: 'name', 'publishers', 'developers', 'all_sentiment', 'global_sales', 'release_year'.

    Example:
    >>> summary = game_summary('Example Game')
    >>> print(summary)
               name       publishers     developers  all_sentiment  global_sales  release_year
    123  Example Game  Example Publisher  Example Dev   Positive       10.5          2020
    """
    summary = all_games[all_games['name'] == game_name]
    return summary.loc[:, ['name', 'publishers', 'developers', 'all_sentiment', 'global_sales', 'release_year']]
# game_summary('Farming Simulator 17')


def get_sentiment(game_name):
    """
    Retrieve sentiment information for the specified game.

    Parameters:
    - game_name (str): The name of the game for which to retrieve sentiment information.

    Returns:
    - pandas.DataFrame: A DataFrame containing sentiment details for the specified game.
      Columns included: 'name', 'recent_sentiment', 'recent_review_number', 'recent_positive_percentage',
      'all_sentiment', 'all_review_number', 'all_positive_percentage'.

    Example:
    >>> sentiment_data = get_sentiment('Example Game')
    >>> print(sentiment_data)
               name recent_sentiment  recent_review_number  recent_positive_percentage  all_sentiment  all_review_number  all_positive_percentage
    123  Example Game  Mostly Positive  500                   80.0                         Positive       1000               75.0
    """
    sentiment = all_games[all_games['name'] == game_name]
    return sentiment.loc[:, ['name', 'recent_sentiment', 'recent_review_number', 'recent_positive_percentage', 'all_sentiment', 'all_review_number', 'all_positive_percentage' ]]


def get_sales_info(game_name):
    """
        Retrieve sales information for the specified game.

        Parameters:
        - game_name (str): The name of the game for which to retrieve sales information.

        Returns:
        - pandas.DataFrame: A DataFrame containing sales details for the specified game.
          Columns included: 'name', 'price', 'estimated_owners', 'global_sales', 'release_year'.

        Example:
        >>> sales_data = get_sales_info('Example Game')
        >>> print(sales_data)
                   name  price  estimated_owners  global_sales  release_year
        123  Example Game  29.99  5000000           10.5          2020
        """
    sale = all_games[all_games['name'] == game_name]
    return sale.loc[:, ['name', 'price', 'estimated_owners', 'global_sales', 'release_year']]


def get_genre(game_name):
    """
    Retrieve genre information for the specified game.

    Parameters:
    - game_name (str): The name of the game for which to retrieve genre information.

    Returns:
    - pandas.DataFrame: A DataFrame containing genre details for the specified game.
      Columns included: 'name', 'achievements', 'single_player', 'categories', 'genres', 'tags', 'popular_tags'.

    Example:
    >>> genre_data = get_genre('Example Game')
    >>> print(genre_data)
               name  achievements  single_player  categories         genres                tags            popular_tags
    123  Example Game  50            True           Action, RPG  Action, RPG, Adventure  Action, Adventure   Open World, Story Rich
    """
    genres = all_games[all_games['name'] == game_name]
    return genres.loc[:, ['name', 'achievements', 'single_player', 'categories', 'genres', 'tags', 'popular_tags']]


def get_tags(game_name):
    """
    Retrieve tags associated with the specified game.

    Parameters:
    - game_name (str): The name of the game for which to retrieve tags.

    Returns:
    - List[str]: A list of tags associated with the specified game.

    Example:
    >>> game_tags = get_tags('Example Game')
    >>> print(game_tags)
    ['Action', 'Adventure', 'Classic', 'Platformer']
    """
    game_tags = tags[tags['name'] == game_name]
    return game_tags.columns[game_tags.iloc[0] == 1].tolist()



def get_comp_req(game_name):
    """
    Retrieve the system requirements for a specified game.

    Parameters:
    - game_name (str): The name of the game for which to retrieve system requirements.

    Returns:
    - pandas.DataFrame: A DataFrame containing system requirements for the specified game.
      Columns included: 'name', 'windows', 'mac', 'linux'.

    Example:
    >>> system_requirements = get_comp_req('Example Game')
    >>> print(system_requirements)
          name  windows  mac  linux
    123  Example Game  True  False  True
    """
    requirements = all_games[all_games['name'] == game_name]
    return requirements.loc[:, ['name', 'windows', 'mac', 'linux']]


