"""
These are functions to use for generating summary statistics for games and producers by various metrics.
"""

import pandas as pd
import pkg_resources


data_path = pkg_resources.resource_filename('SteamInsights', 'data/all_games_cleaned.csv')
all_games = pd.read_csv(data_path)

tag_path = pkg_resources.resource_filename('SteamInsights', 'data/tags.csv')
tags = pd.read_csv(tag_path)


def game_summary(game_name):
    """
    Retrieve a summary of the specified game.

    Parameters
    ----------
    game_name : str
        The name of the game for which to retrieve the summary.

    Returns
    -------
    pandas.DataFrame
        A DataFrame containing the summary information for the specified game.
        Columns included: 'name', 'publishers', 'developers', 'all_sentiment', 'global_sales', 'release_year.

<<<<<<< HEAD
    Example
    -------
    >>> summary = game_summary('Example Game')
=======
    Example:
    >>> summary = game_summary('Farming Simulator 17')
>>>>>>> origin/main
    >>> print(summary)
              name       publishers     developers  all_sentiment  global_sales  release_year
    123  Example Game  Example Publisher  Example Dev   Positive       10.5          2020
    """

    summary = all_games[all_games['name'] == game_name]
    summary.reset_index(inplace=True)
    return summary.loc[:, ['name', 'publishers', 'developers', 'all_sentiment', 'global_sales', 'release_year']]


def get_sentiment(game_name):
    """
    Retrieve sentiment information for the specified game.

    Parameters
    ----------
    game_name : str
        The name of the game for which to retrieve sentiment information.

    Returns
    -------
    pandas.DataFrame
        A DataFrame containing sentiment details for the specified game.
        Columns included: 'name', 'recent_sentiment', 'recent_review_number', 'recent_positive_percentage',
        'all_sentiment', 'all_review_number', 'all_positive_percentage.

<<<<<<< HEAD
    Example
    -------
    >>> sentiment_data = get_sentiment('Example Game')
=======
    Example:
    >>> sentiment_data = get_sentiment('Farming Simulator 17')
>>>>>>> origin/main
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

<<<<<<< HEAD
    Example:
    >>> sales_data = get_sales_info('Example Game')
    >>> print(sales_data)
                name  price  estimated_owners  global_sales  release_year
    123  Example Game  29.99  5000000           10.5          2020
    """
=======
        Example:
        >>> sales_data = get_sales_info('Farming Simulator 17')
        >>> print(sales_data)
                   name  price  estimated_owners  global_sales  release_year
        123  Example Game  29.99  5000000           10.5          2020
        """
>>>>>>> origin/main

    sale = all_games[all_games['name'] == game_name]
    sale.reset_index(inplace=True)
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
    >>> genre_data = get_genre('Farming Simulator 17')
    >>> print(genre_data)
               name  achievements  single_player  categories         genres                tags            popular_tags
    123  Example Game  50            True           Action, RPG  Action, RPG, Adventure  Action, Adventure   Open World, Story Rich
    """

    genres = all_games[all_games['name'] == game_name]
    genres.reset_index(inplace=True)
    return genres.loc[:, ['name', 'achievements', 'single_player', 'genres']]


def get_tags(game_name):
    """
    Retrieve tags associated with the specified game.

    Parameters:
    - game_name (str): The name of the game for which to retrieve tags.

    Returns:
    - List[str]: A list of tags associated with the specified game.

    Example:
    >>> game_tags = get_tags('Farming Simulator 17')
    >>> print(game_tags)
    ['Action', 'Adventure', 'Classic', 'Platformer']

    """

    game_tags = tags[tags['name'] == game_name]
    game_tags.reset_index(inplace=True)
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
    >>> system_requirements = get_comp_req('Farming Simulator 17')
    >>> print(system_requirements)
          name  windows  mac  linux
    123  Example Game  True  False  True
    """

    requirements = all_games[all_games['name'] == game_name]
    requirements.reset_index(inplace=True)
    return requirements.loc[:, ['name', 'windows', 'mac', 'linux']]


def company_summary(company_name, developer=True):
    """
    Generate a summary of games published or developed by a specified company.

    Parameters
    ----------
    company_name : str
        The name of the company for which to generate the summary.
    developer : bool, optional
        If True, consider games developed by the company. If False, consider games published by the company. Default is True.

    Returns
    -------
    None

    Notes
    -----
    This function generates a summary of games associated with a specified company, including the total number of games,
    the most common sentiment among those games, and information about the price range.

    Parameters:
    - company_name (str): The name of the gaming company to summarize.
    - developer (bool, optional): If True, the function searches for the company in the 'developers' column.
                                  If False, it searches in the 'publishers' column. Default is True.

    Returns:
    None: The function prints a summary of the company's presence on Steam.

    Example:
    >>> company_summary('Electronic Arts', False)
    """
    # Check if there are rows for both 'developers' and 'publishers'
    if not all_games[(all_games['developers'].str.contains(company_name, na=False)) &
                     (all_games['publishers'].str.contains(company_name, na=False))].empty:
        df_d = all_games[all_games['developers'].str.strip().str.contains(company_name, na=False)]
        df_p = all_games[all_games['publishers'].str.strip().str.contains(company_name, na=False)]
        df = pd.concat([df_d, df_p], ignore_index=True)
    else:
        # Check if developer or publisher data is available
        if developer:
            if not all_games[all_games['developers'].str.strip().str.contains(company_name, na=False)].empty:
                df = all_games[all_games['developers'].str.strip().str.contains(company_name, na=False)]
            else:
                print(f'The company {company_name} is not listed as a developer.')
                return str("Not a developer")
        else:
            if not all_games[all_games['publishers'].str.strip().str.contains(company_name, na=False)].empty:
                df = all_games[all_games['publishers'].str.strip().str.contains(company_name, na=False)]
            else:
                print(f'The company {company_name} is not listed as a publisher.')
                return str("Not a publisher")

    # Compute sentiment value counts
    vc = df['all_sentiment'].value_counts()

    # Find max and min prices
    max_price = df['price'].max()
    min_price = df['price'].min()

    # Print summary information
    print(f'{company_name} has {len(df)} total games on Steam.')
    print(f'The most common sentiment is {vc.idxmax()} from {vc[0]} of their {len(df)} games.')

    if min_price == 0 and max_price == 0:
        print(f'All of their games are free.')
    elif min_price == 0:
        print(f'Their most expensive game is ${max_price}, while their least expensive game is free.')
    elif max_price == min_price:
        print(f'All of their games are ${max_price}')
    else:
        print(f'Their most expensive game is ${max_price}, while their least expensive game is ${min_price}.')
    return

