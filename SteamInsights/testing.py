"""
A collection of functions to test written functions in summary.py and analytic_functions.py
"""

from SteamInsights import summary
from SteamInsights import analytic_functions
import pandas as pd


def test_game_summary():
    """
    Test that game summary returns the correct information.
    """
    game = 'Farming Simulator 17'
    data = {
        'name': ['Farming Simulator 17'],
        'publishers': ['GIANTS Software'],
        'developers': ['GIANTS Software'],
        'all_sentiment': ['Very Positive'],
        'global_sales': [1.62],
        'release_year': [2016]
    }
    # assert (summary.game_summary(game) == pd.DataFrame(data))
    assert (summary.game_summary(game).equals(pd.DataFrame(data)))


def test_get_sentiment():
    """
    Test that get sentiment returns the correct information.
    """
    game = 'Farming Simulator 17'
    data = {
        'name': ['Farming Simulator 17'],
        'recent_sentiment': ['Very Positive'],
        'recent_review_number': [88.0],
        'recent_positive_percentage': [88.0],
        'all_sentiment': ['Very Positive'],
        'all_review_number': [11267.0],
        'all_positive_percentage': [91.0]
    }
    # assert (summary.get_sentiment(game) == pd.DataFrame(data))
    assert (summary.get_sentiment(game).equals(pd.DataFrame(data)))


def test_get_sales_info():
    """
    Test that get sales info returns the correct information.
    """
    game = 'Farming Simulator 17'
    data = {
        'name': ['Farming Simulator 17'],
        'price': [14.99],
        'estimated_owners': [1500000.0],
        'global_sales': [1.62],
        'release_year': [2016]
    }
    # assert (summary.get_sales_info(game) == pd.DataFrame(data))
    assert (summary.get_sales_info(game).equals(pd.DataFrame(data)))


def test_get_genre():
    """
    Test that get genre returns the correct information.
    """
    game = 'Farming Simulator 17'
    data = {
        'name': ['Farming Simulator 17'],
        'achievements': [17],
        'single_player': [True],
        'genres': ['Simulation']
    }
    # assert (summary.get_genre(game) == pd.DataFrame(data))
    assert (summary.get_genre(game).equals(pd.DataFrame(data)))


def test_get_tags():
    """
    Test that get tags returns the correct information.
    """
    game = 'Farming Simulator 17'
    data = [
        'Singleplayer',
        'Multiplayer',
        'Great Soundtrack',
        'Strategy',
        'Open World',
        'Third Person',
        'Simulation',
        'First-Person',
        'Co-op',
        'Sandbox',
        'Moddable',
        'Online Co-Op',
        'Management',
        'Family Friendly',
        'Automobile Sim',
        'Realistic',
        'Economy',
        'Driving',
        'Agriculture',
        'Farming Sim'
    ]
    assert (summary.get_tags(game) == data)  # might be ok


def test_get_comp_req():
    """
    Test that get computer requirements returns the correct information.
    """
    game = 'Farming Simulator 17'
    data = {
        'name': ['Farming Simulator 17'],
        'windows': [True],
        'mac': [True],
        'linux': [False]
    }
    # assert (summary.get_comp_req(game) == pd.DataFrame(data))
    assert (summary.get_comp_req(game).equals(pd.DataFrame(data)))


def test_company_summary():
    """
    Test that get company summary returns the correct information.
    """
    EA_F = 'Found them successfully - max_price:59.99, min_price:0.0, total_games:20'
    assert (summary.company_summary('Electronic Arts', False) == EA_F)

    EA_T = 'Not a developer'
    assert (summary.company_summary('Electronic Arts', True) == EA_T)

    # This company is listed in both the developers and publishers columns
    assert (summary.company_summary('Square Enix', True) == summary.company_summary('Square Enix', False))


def test_analyze():
    """
    Tests that analyze returns successfully.
    """

    # could make some more changes to analyze function so we can test exactly what it returns
    assert (analytic_functions.analyze('price', 'global_sales', col_types=('cont-cont'),
                                       plot=False) == 'successfully analyzed relationship - cont-cont')
    assert (analytic_functions.analyze('price', 'single_player', col_types=('cont-cat'),
                                       plot=False) == 'successfully analyzed relationship - cont-cat')
    assert (analytic_functions.analyze('price_category', 'genres', col_types=('cat-cat'),
                                       plot=False) == 'successfully analyzed relationship - cat-cat')
    assert (analytic_functions.analyze('price_category', 'genres', col_types=('typo'),
                                       plot=False) == 'Please input a valid value for col_types, such as cont-cont, cont-cat, or cat-cat')
    assert (analytic_functions.analyze('price_category', 'typo', col_types=('cat-cat'),
                                       plot=False) == 'One or both column names have not been found, check them for typos: 1st: price_category, 2nd: typo')


def test_summary_stats_by_tag():
    """
    Tests that summary stats by tag returns the correct info.
    """

    assert (analytic_functions.summary_stats_by_tag("typo") == 'The tag typo was not found.')
    assert (analytic_functions.summary_stats_by_tag("Adventure") == {'min': 0.51, 'mean': 14.978346774193549,
                                                                     'max': 59.99})


def test_compare_two_tags():
    """
    Tests that compare two tags returns the correct info.
    """
    assert (analytic_functions.compare_two_tags("Action", "Adventure") == 'Successfully compared Action and Adventure')
    assert (analytic_functions.compare_two_tags("Action", "typo") == 'The tag typo was not found.')


def test_tags_related():
    """
    Tests that tags related returns the correct info.
    """
    assert (analytic_functions.tags_related(0) == '0 is too small. Please input a number between 2 and 50.')
    assert (analytic_functions.tags_related(100) == '100 is too large. Please input a number between 2 and 50.')
    five_data = [(('Singleplayer', 'Action'), 264),
                 (('Singleplayer', 'Adventure'), 227),
                 (('Action', 'Adventure'), 199),
                 (('Singleplayer', 'Multiplayer'), 177),
                 (('Singleplayer', 'Great Soundtrack'), 168),
                 (('Action', 'Multiplayer'), 145),
                 (('Action', 'Great Soundtrack'), 137),
                 (('Adventure', 'Great Soundtrack'), 125),
                 (('Adventure', 'Multiplayer'), 95),
                 (('Multiplayer', 'Great Soundtrack'), 67)]
    assert (analytic_functions.tags_related(5) == five_data)


def test_top_n_values():
    """
    Tests that top n values returns the correct info.
    """

    assert (analytic_functions.top_n_values(
        criteria='typo') == "Invalid criteria. Choose from 'price', 'metacritic_score', or 'global_sales'.")


# functions that don't really need testing right now
# def test_graph(): #hard to test a graphing function
# def test_graph_mean_tag_prices(): #also hard to test
# def test_tags_related_plot(): # should only be called by compare_two_tags and not by user
# def test_analyze_single_vs_multiplayer(): will return the same thing every time anyway


def run_all_tests():
    test_game_summary()
    test_get_sentiment()
    test_get_sales_info()
    test_get_genre()
    test_get_tags()
    test_get_comp_req()
    test_company_summary()

    test_analyze()
    test_summary_stats_by_tag()
    test_compare_two_tags()
    test_tags_related()
    test_top_n_values()

    print("All of the tests were run successfully")


if __name__ == '__main__':
    run_all_tests()
