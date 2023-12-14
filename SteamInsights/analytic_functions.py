"""
These are functions to use for analyzing and visualizing the steam dataset.
"""

import pandas as pd
import numpy as np
from scipy.stats import pearsonr
from scipy.stats import pointbiserialr
import matplotlib.pyplot as plt
import seaborn as sns
import pkg_resources

data_path = pkg_resources.resource_filename('SteamInsights', 'data/all_games_cleaned.csv')
all_games = pd.read_csv(data_path)

tag_path = pkg_resources.resource_filename('SteamInsights', 'data/tags.csv')
tags = pd.read_csv(tag_path)


def graph(col1, col2, col_types='cont-cont'):
    """
    Generate and display plots for the relationship between two columns in a DataFrame.

    Parameters
    ----------
    col1 : str
        The name of the first column.
    col2 : str
        The name of the second column.
    col_types : {'cont-cont', 'cont-cat', 'cat-cat'}, optional
        The types of the columns for analysis:
        - 'cont-cont': Continuous vs. Continuous
        - 'cont-cat': Continuous vs. Categorical
        - 'cat-cat': Categorical vs. Categorical
        Default is 'cont-cont'.

    Returns
    -------
    str or None
        If the analysis is not possible due to insufficient data, a message is returned.
        Otherwise, None is returned.

    Examples
    --------
    >>> graph('price', 'global_sales', col_types='cont-cont')
    # (Plots based on the col_types)

    Notes
    -----
    - The function may return a message if the dataset has less than 15 values after dropping NA rows.
    """

    columns = [col1, col2]
    df = all_games.dropna(subset=columns)
    df = df.loc[:, columns]

    # if the length of the df is now less than 15, it might be wrong to analyse the relationship?
    if df.shape[0] < 15:
        return ("This relationship has less than 15 values to analyze")

    if (col_types == 'cont-cont'):
        plt.figure(figsize=(12, 8))
        sns.jointplot(x=col1, y=col2, data=df)
        plt.show()

        plt.figure(figsize=(12, 8))
        sns.pairplot(df)
        plt.show()

        plt.figure(figsize=(12, 8))
        sns.regplot(x=col1, y=col2, data=df)
        plt.show()


    elif (col_types == 'cont-cat'):
        plt.figure(figsize=(12, 8))
        sns.boxplot(x=col2, y=col1, data=df)
        plt.show()

        plt.figure(figsize=(12, 8))
        sns.barplot(x=col2, y=col1, data=df)
        plt.show()

        plt.figure(figsize=(12, 8))
        sns.countplot(x=col2, data=df)
        plt.show()

    elif (col_types == 'cat-cat'):
        plt.figure(figsize=(12, 8))
        sns.countplot(x=col1, hue=col2, data=df)
        plt.show()

        pivot_table = df.pivot_table(index=col1, columns=col2, aggfunc='size', fill_value=0)
        plt.figure(figsize=(12, 8))
        sns.heatmap(pivot_table, annot=True, cmap='viridis')
        plt.show()

    else:
        return ("Please input a valid value for col_types, such as cont-cont, cont-cat, or cat-cat")
    return


def analyze(col1, col2, col_types='cont-cont', plot=False):
    """
    Analyze the relationship between two columns in a DataFrame.

    Parameters
    ----------
    col1 : str
        The name of the first column.
    col2 : str
        The name of the second column.
    col_types : {'cont-cont', 'cont-cat', 'cat-cat'}, optional
        The types of the columns for analysis:
        - 'cont-cont': Continuous vs. Continuous
        - 'cont-cat': Continuous vs. Categorical
        - 'cat-cat': Categorical vs. Categorical
        Default is 'cont-cont'.
    plot : bool, optional
        If True, generate and display relevant plots based on the analysis.
        Default is False.

    Returns
    -------
    str or None
        If the analysis is not possible due to insufficient data, a message is returned.
        Otherwise, None is returned.

    Examples
    --------
    >>> analyze('price', 'global_sales', col_types='cont-cont', plot=True)
    The correlation coefficient is: 0.75
    The P value for the hypothesis test is: 0.02
    # (Output for other col_types)

    Notes
    -----
    - For 'cont-cat' analysis, certain metrics may not be meaningful for certain columns, like 'price'.
    - The function may return a message if the dataset has less than 15 values after dropping NA rows.
    """

    if not all(col in all_games.columns for col in [col1, col2]):
        # if they don't have both column names
        return str(f"One or both column names have not been found, check them for typos: 1st: {col1}, 2nd: {col2}")

    # drop all rows with NA values in these two columns
    columns = [col1, col2]
    df = all_games.dropna(subset=columns)
    df = df.loc[:, columns]

    # if the length of the df is now less than 20, it might be wrong to analyse the relationship?
    if (df.shape[0] < 15):
        return ("This relationship has less than 15 values to analyze")

    if (col_types == 'cont-cont'):

        correlation_coef, p_value = pearsonr(df[col1], df[col2])
        print(f'The correlation coefficient is: {correlation_coef}')
        print(f'The P value for the hypothesis test is: {p_value}')

    elif (col_types == 'cont-cat'):
        descriptive_stats = df.groupby(col2)[col1].describe()
        print(descriptive_stats)

    elif (col_types == 'cat-cat'):
        cross_tab = pd.crosstab(df[col1], df[col2], margins=True)  # look at joint distribution table
        print(cross_tab)
    else:
        return ("Please input a valid value for col_types, such as cont-cont, cont-cat, or cat-cat")

    if (plot == True):
        graph(col1, col2, col_types)
    return str(f"successfully analyzed relationship - {col_types}")


def summary_stats_by_tag(chosen_tag, drop_zeroes=True):
    """
    Calculate summary statistics (min, max, mean) for the prices of games associated with a specified tag.

    Parameters
    ----------
    chosen_tag : str
        The tag for which to calculate the summary statistics.
    drop_zeroes : bool, optional
        If True, exclude games with a price of 0 from the calculation.
        Default is True.

    Returns
    -------
    dict
        A dictionary containing the summary statistics:
        - 'min': Minimum price
        - 'max': Maximum price
        - 'mean': Mean price

    Notes
    -----
    This function filters the 'all_games' DataFrame based on the presence of the
    specified tag in the 'tags' DataFrame. It then calculates the minimum, maximum,
    and mean prices of the filtered games. Optionally, games with a price of 0 can
    be excluded from the calculation by setting `drop_zeroes` to True.
    """

    if not chosen_tag in tags.columns:
        return str(f"The tag {chosen_tag} was not found.")

    df = tags[tags[chosen_tag] == 1].iloc[:, 0]
    tag_df = all_games[all_games['name'].isin(df)]

    if drop_zeroes:
        tag_df = tag_df[tag_df['price'] != 0]

    summary_stats = {
        'min': tag_df['price'].min(),
        'mean': tag_df['price'].mean(),
        'max': tag_df['price'].max()

    }

    return summary_stats


def graph_mean_tag_prices(which='common', num=10, drop_zeroes=True):
    """
    Visualize mean prices for game tags in a bar plot.

    Parameters
    ----------
    which : str, optional
        Specifies the criteria for selecting tags. Options are 'common' (top N most common),
        'most_exp' (top N most expensive), or 'least_exp' (top N least expensive). Default is 'common'.
    num : int, optional
        Number of tags to display in the plot. Should be no greater than 20 for readability.
        Default is 10.
    drop_zeroes : bool, optional
        If True, exclude games with a price of 0 from the mean price calculation.
        Default is True.

    Returns
    -------
    None
        Displays a bar plot of mean prices for selected tags.

    Notes
    -----
    This function calculates the mean prices for specified tags and visualizes the results in a bar plot.
    The tags are selected based on the specified criteria ('common', 'most_exp', or 'least_exp').
    If 'common' is chosen, it selects the top N most common tags. If 'most_exp' or 'least_exp' is chosen,
    it selects the top N most or least expensive tags, respectively.
    The plot displays the mean prices on the y-axis and tag names on the x-axis.

    Examples
    --------
    To plot the mean prices for the top 10 most common tags:
    >>> graph_mean_tag_prices()

    To plot the mean prices for the top 5 most expensive tags:
    >>> graph_mean_tag_prices(which='most_exp', num=5)

    To plot the mean prices for the top 8 least expensive tags:
    >>> graph_mean_tag_prices(which='least_exp', num=8)
    """
    num = num+1
    if which == 'common':
        top_tags = tags.iloc[:, 1:num].columns
    else:
        top_tags = tags.iloc[:, 1:].columns

    mean_prices_list = []
    for tag in top_tags:
        mean_price = summary_stats_by_tag(tag, drop_zeroes)['mean']
        mean_prices_list.append(mean_price)

    tags_data = {
        'tag': top_tags,
        'mean_price': mean_prices_list
    }

    tags_data = pd.DataFrame(tags_data)

    if which == 'most_exp':
        tags_data = tags_data.sort_values(by='mean_price', ascending=False)
    elif which == 'least_exp':
        tags_data = tags_data.sort_values(by='mean_price', ascending=True)
    tags_data = tags_data.iloc[0:num, :]

    plt.figure(figsize=(10, 6))
    plt.bar(tags_data['tag'], tags_data['mean_price'])
    plt.xlabel('Tags')
    plt.ylabel('Mean Price ($)')
    plt.title('Mean Price for Each Tag')
    plt.xticks(rotation=45, ha='right')  # Rotate x-axis labels for better visibility
    plt.show()
    return


def compare_two_tags(tag1, tag2):
    """
    Compare two binary tags in a DataFrame using correlation and a cross-tabulation heatmap.

    Parameters
    ----------
    tag1 : str
        The name of the first binary tag for comparison.
    tag2 : str
        The name of the second binary tag for comparison.

    Returns
    -------
    None
        Displays correlation information and a cross-tabulation heatmap.

    Notes
    -----
    This function compares two binary tags in a DataFrame by calculating the point-biserial correlation
    coefficient and visualizing the cross-tabulation results using a heatmap. The correlation coefficient
    indicates the strength and direction of the relationship between the two tags. This function can be
    used to observe how often two different tags are used together to describe one game.

    Parameters:
    - tag1 (str): The name of the first binary tag.
    - tag2 (str): The name of the second binary tag.

    Examples
    --------
    To compare the tags 'Action' and 'Adventure':
    >>> compare_two_tags('Action', 'Adventure')
    """

    if not tag1 in tags.columns:
        return str(f"The tag {tag1} was not found.")

    if not tag2 in tags.columns:
        return str(f"The tag {tag2} was not found.")

    correlation, p_value = pointbiserialr(tags[tag1], tags[tag2])
    print(f'Correlation coefficient: {correlation}')
    print(f'P-value: {p_value}')

    cross_table = pd.crosstab(tags[tag1], tags[tag2])

    plt.figure(figsize=(8, 6))
    sns.heatmap(cross_table, annot=True, fmt='d', cmap='Blues')
    plt.ylabel(tag1)
    plt.xlabel(tag2)
    plt.title('Cross-tabulation Heatmap')
    plt.show()
    return str(f"Successfully compared {tag1} and {tag2}")


def tags_related_plot(result):
    """
    Visualize the frequency of tag pair combinations using a bar plot.

    Parameters
    ----------
    result : list of tuples
        A list where each tuple contains a tag pair and its corresponding cross-tabulation table values for ones.

    Returns
    -------
    None

    Notes
    -----
    This function is meant to be used in tandem with the tags_related(num, plot) function when plot is set
    to true and should not be called manually by the user. It takes in the result of tags_related(), which
    is a list of tuples, where each tuple contains a tag pair and the count of ones in the cross-tabulation.
    It visualizes the results using a bar plot with tag pairs on the x-axis and counts on the y-axis.

    Parameters:
    - result (list of tuples): A list where each tuple contains a tag pair and its corresponding count of ones.

    Examples
    --------
    To visualize the results for a given list of tag pairs and counts:
    >>> tags_related_plot(result)
    """
    sns.barplot(x=[f'{pair[0]}-{pair[1]}' for pair, count in result], y=[count for pair, count in result],
                palette='viridis')
    plt.xlabel('Tag Pairs')
    plt.ylabel('Count')
    plt.title('Frequency of Tag Pair Combinations')
    plt.xticks(rotation=45, ha='right')
    plt.show()
    return


def tags_related(num=5, plot=False):
    """
    Analyze and visualize the frequency of tag pair combinations.

    Parameters
    ----------
    num : int, optional
        The number of tags to consider for analysis. Default is 5.
    plot : bool, optional
        If True, plot the results using `tags_related_plot`. Default is False.

    Returns
    -------
    list of tuples or None
        A sorted list where each tuple contains a tag pair and its corresponding cross-tabulation table values for ones.
        If `plot` is True, the function returns None.

    Notes
    -----
    This function analyzes the frequency of combinations of two tags in a DataFrame by calculating cross-tabulation tables.
    It returns a sorted list of tuples, where each tuple contains a tag pair and the count of ones in the cross-tabulation.
    If `plot` is True, the function also calls `tags_related_plot` to visualize the results using a bar plot.

    Parameters:
    - num (int, optional): The number of tags to consider for analysis. Default is 5.
    - plot (bool, optional): If True, plot the results. Default is False.

    Examples
    --------
    To analyze the relationships for the top 5 tags:
    >>> result = tags_related(5)
    >>> print(result)

    To analyze and plot the relationships for the top 10 tags:
    >>> tags_related(10, plot=True)
    """
    if (num < 2):
        return str(f"{num} is too small. Please input a number between 2 and 50.")
    if (num > 50):
        return str(f"{num} is too large. Please input a number between 2 and 50.")

    df = tags.iloc[:, 1:num + 1]
    tag_names = df.columns
    result = []

    for i in range(len(tag_names)):
        for j in range(i + 1, len(tag_names)):
            tag1, tag2 = tag_names[i], tag_names[j]
            cross_table_ones = pd.crosstab(tags[tag1], tags[tag2]).iloc[1, 1]
            result.append(((tag1, tag2), cross_table_ones))

    # Sort the result in descending order based on cross-tabulation values
    result = sorted(result, key=lambda x: x[1], reverse=True)

    if plot:
        tags_related_plot(result)
    else:
        return result


def top_n_values(column='developers', criteria='price', top_n=5, plot=False):
    """
        Generate a summary of the top N values for a specified column based on a given criteria.

        Parameters
        ----------
        column : str, optional
            The column to group and analyze. Default is 'developers'.
        criteria : str, optional
            The criteria for analysis. Choose from 'price', 'metacritic_score', or 'global_sales'.
            Default is 'price'.
        top_n : int, optional
            The number of top values to display. Default is 5.
        plot : bool, optional
            If True, a bar chart of the top values is plotted. Default is False.

        Returns
        -------
        pandas.DataFrame
            A DataFrame containing the top N values for the specified column based on the given criteria.

        Raises
        ------
        ValueError
            If an invalid criteria is provided.

        Examples
        --------
        >>> top_n_values(column='developers', criteria='metacritic_score', top_n=10, plot=False)
        # DataFrame with the top 10 developers based on metacritic_score

        >>> top_n_values(column='publishers', criteria='global_sales', top_n=5, plot=True)
        # DataFrame with the top 5 publishers based on global_sales, and a corresponding bar chart plot

        Notes
        -----
        - The function calculates the mean of the specified criteria for each group in the specified column.
        - It returns the top N groups based on the mean value of the criteria.
        - If plot=True, a bar chart is generated to visually represent the top N values.

        """

    df = all_games.copy()

    if criteria not in ['price', 'metacritic_score', 'global_sales']:
        return str("Invalid criteria. Choose from 'price', 'metacritic_score', or 'global_sales'.")

    # Group by developers and calculate the mean for the specified criteria
    grouped_df = df.groupby(column)[criteria].mean()

    # Get the top n producers
    top_group = grouped_df.nlargest(top_n).reset_index()

    # Plot the top values on a bar chart if plot=True
    if plot:
        plt.figure(figsize=(10, 6))
        bar_plot = sns.barplot(x=column, y=criteria, data=top_group, palette='viridis')
        plt.title(f'Top {top_n} {column} by {criteria}')
        plt.xlabel(column)
        plt.ylabel(criteria)
        bar_plot.set_xticklabels(bar_plot.get_xticklabels(), rotation=45, horizontalalignment='right')

        plt.show()

    return top_group


def analyze_single_vs_multiplayer():
    """
    Analyze and compare sales and ratings of single-player and multiplayer games.

    Returns:
    - A DataFrame with the summary statistics for single-player and multiplayer games.
    """

    df = all_games.copy()
    # Filter single-player and multiplayer games
    single_player_games = df[df['single_player'] == True]
    multiplayer_games = df[df['single_player'] == False]

    # Calculate average sales and sentiment for each category
    single_player_sales = single_player_games['global_sales'].mean()
    multiplayer_sales = multiplayer_games['global_sales'].mean()

    single_player_sentiment = single_player_games['all_positive_percentage'].mean()
    multiplayer_sentiment = multiplayer_games['all_positive_percentage'].mean()

    # Create a DataFrame with the analysis results
    analysis_results = pd.DataFrame({
        'Category': ['Single Player', 'Multiplayer'],
        'Average Sales': [single_player_sales, multiplayer_sales],
        'Average Sentiment': [single_player_sentiment, multiplayer_sentiment]
    })

    # Plot the comparison
    # plt.figure(figsize=(12, 6))

    # Sales Comparison
    # plt.subplot(1, 2, 1)
    # sns.barplot(x=sales_summary.index, y='mean', hue='index', data=sales_summary.melt(), palette='Set2')
    # plt.title('Global Sales Comparison')
    # plt.ylabel('Global Sales')
    # plt.xlabel('Game Type')

    # Ratings Comparison
    # plt.subplot(1, 2, 2)
    # sns.barplot(x=ratings_summary.index, y='value', hue='index', data=ratings_summary.melt(), palette='Set2')
    # plt.title('Ratings Comparison')
    # plt.ylabel('Average Rating')
    # plt.xlabel('Game Type')

    # plt.tight_layout()
    # plt.show()

    return analysis_results


def recommend(num_games=5, price_min=0.00, price_max=60.00, tags_to_filter=[],
              developers=[], publishers=[], players="single/multi", os='windows', reviews='Mixed'):
    """
    Recommends a specified number of games based on user-defined metrics.

    Parameters:
    - num_games (int): Number of games to recommend.
    - price_min (float): Minimum price filter for games.
    - price_max (float): Maximum price filter for games.
    - tags_to_filter (list): List of tags to filter games by.
    - developers (list): List of developers to filter games by.
    - publishers (list): List of publishers to filter games by.
    - players (str): Type of players ('single', 'multi', or 'single/multi').
    - OS (str): Operating system filter ('windows', 'mac', or 'linux').
    - reviews (str): Sentiment level to filter games by.

    Returns:
    - pandas.Series: Series containing the names of the recommended games.

    Example usage:
    >>> recommend(num_games=10, tags_to_filter=['Action', 'Adventure'])
    >>> recommend(num_games=10, developers=['Valve'])
    >>> recommend(num_games=5, publishers=['Valve'])
    >>> recommend(num_games=10, players="single", os="mac")
    >>> recommend(num_games=10, reviews="Positive")
    >>> recommend(num_games=1, price_min=0, price_max=10)
    """

    # filter all_games by games that appear in the right range:
    df = all_games[(all_games['price'] >= price_min) & (all_games['price'] <= price_max)]

    # filter priced by games that have these tags
    if tags_to_filter:
        tag_filter_condition = tags[tags_to_filter].eq(1).all(axis=1)
        df = df[df['name'].isin(tags[tag_filter_condition]['name'])]

    # filter by certain developer(s) if not empty
    if developers:
        df = df[df['developers'].isin(developers)]

    # filter by certain publisher(s) if not empty
    if publishers:
        df = df[df['publishers'].isin(publishers)]

    # filter to the number of players specified
    if players == "single":
        df = df[df['players'] == 'single']
    elif players == "multi":
        df = df[df['players'] == 'multi']
    # else do nothing

    # filter to a certain operating system
    if os == "mac":
        df = df[df['mac'] == 1]
    elif os == "linux":
        df = df[df['linux'] == 1]
    # else windows --> do nothing

    sentiment_mapping = {
        'Overwhelmingly Negative': ['Overwhelmingly Negative', 'Mostly Negative', 'Very Negative', 'Negative', 'Mixed',
                                    'Positive', 'Very Positive', 'Mostly Positive', 'Overwhelmingly Positive'],
        'Mostly Negative': ['Mostly Negative', 'Very Negative', 'Negative', 'Mixed', 'Positive', 'Very Positive',
                            'Mostly Positive', 'Overwhelmingly Positive'],
        'Very Negative': ['Very Negative', 'Negative', 'Mixed', 'Positive', 'Very Positive', 'Mostly Positive',
                          'Overwhelmingly Positive'],
        'Negative': ['Negative', 'Mixed', 'Positive', 'Very Positive', 'Mostly Positive', 'Overwhelmingly Positive'],
        'Mixed': ['Mixed', 'Positive', 'Very Positive', 'Mostly Positive', 'Overwhelmingly Positive'],
        'Positive': ['Positive', 'Very Positive', 'Mostly Positive', 'Overwhelmingly Positive'],
        'Very Positive': ['Very Positive', 'Mostly Positive', 'Overwhelmingly Positive'],
        'Mostly Positive': ['Mostly Positive', 'Overwhelmingly Positive'],
        'Overwhelmingly Positive': ['Overwhelmingly Positive']
    }

    sentiment_values = sentiment_mapping.get(reviews, [])
    df = df[df['all_sentiment'].isin(sentiment_values)]

    df = df.sort_values(by='all_review_number', ascending=False)
    df = df.drop_duplicates(subset='name')

    return df['name'].head(num_games)


