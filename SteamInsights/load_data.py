"""
This script loads the raw data for the games, tags, and ratings files.
"""

import pkg_resources
import pandas as pd


def load_data(name = 'all_games'):
    """
    Function to load data from the Steam Insights Packages.
    """

    if name == 'all_games':
        path = 'data/all_games_cleaned.csv'
    elif name == 'tags':
        path = 'data/tags.csv'
    elif name == 'ratings':
        path = 'data/ratings.csv'
    else:
        raise NameError("{} is not recognized. The only names are 'all_games', 'tags', and 'ratings'.".format(name))

    data_path = pkg_resources.resource_filename('SteamInsights', path)
    return pd.read_csv(data_path)

