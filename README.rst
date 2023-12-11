README - Steam Project
=================

A project for analyzing the relationship between sales and ratings for games sold on the Steam platform.

Documentation
-------------

For documentation, please visit `ReadTheDocs: Steam Project <https://jbhiltscher.github.io/steam_project/>`_.

Installation and updating
-------------------------

Use the package manager `pip` to install steam_project. Rerun this command to check for and install updates. Installation should take no more than 5 minutes. The package requires `python>=3.7`.

.. code-block:: bash

    pip install git+https://github.com/jbhiltscher/steam_project.git

Quick Demo
----------

Below is a quick demo of how to load in data using the package:

.. code-block:: python

    from rfphate import RFPHATE
    from load_data import *
    import pkg_resources
    import pandas as pd

    data = pd.read_csv('datasets/titanic.csv')
    x, y = dataprep(data)

    rfphate = RFPHATE(y=y, random_state=0)
    # Alternatively, rfphate = RFPHATE(prediction_type='classification', random_state=0)

    embedding = rfphate.fit_transform(x, y)
    sns.scatterplot(x=embedding[:, 0], y=embedding[:, 1], hue=pd.Categorical(data.iloc[:, 0]))

.. image:: figures/titanic.png

We can visually explore the relationships between the response (survival) and other feature variables:

By passenger class:

.. code-block:: python

    sns.scatterplot(x=embedding[:, 0], y=embedding[:, 1], hue=pd.Categorical(data.iloc[:, 1]))
    plt.legend(title='By Class')

.. image:: figures/titanic_class.png

By passenger sex:

.. code-block:: python

    sns.scatterplot(x=embedding[:, 0], y=embedding[:, 1], hue=pd.Categorical(data.iloc[:, 2]))
    plt.legend(title='By Sex')

.. image:: figures/titanic_sex.png

If you find the RF-PHATE method useful, please cite:

.. [1] 
    Rhodes, J.S., Aumon, A., Morin, S., et al.: Gaining Biological Insights through Supervised
    Data Visualization. bioRxiv (2023). https://doi.org/10.1101/2023.11.22.568384.