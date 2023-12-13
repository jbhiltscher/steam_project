from setuptools import setup, find_packages

def parse_requirements(filename):
    with open(filename, 'r') as file:
        lines = file.readlines()
        return [line.strip() for line in lines]


with open('README.rst', 'r', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='steaminsights',
    version='0.1.1',
    description='The package is used to analyse data about video games sold on Steam.',
    author='Caroline Jarman, Jake Hiltscher',
    author_email='carolinerosejarman@gmail.com',
    packages=find_packages(), #list individual modules here, or put in sub directory and point to that
    # packages= ['SteamInsights.summary', 'SteamInsights.analytic_functions', 'SteamInsights.load_data'],
    install_requires=parse_requirements('requirements.txt'),
    package_data={'SteamInsights': ['data/*.csv']},
    long_description=long_description
)
# need to have a long description for this...