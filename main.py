# NFL specific webscraper
from scraper import NflScraper

# data manipulation
import pandas as pd

# Used to implement delays while scraping (trying to avoid overloading the website server)
import time
import random

"""
GLOBAL VARIABLES:
path_to_webdriver - string - absolute path to webdriver on personal machine.
"""
relative_path_to_webdriver = 'bin/chromedriver'

"""
PURPOSE:
    - Demonstrate how to use get_game_week_scores() method.
INPUT PARAMETERS:
              scraper -      object        - instance of NFLScraper
              seasons -   list (string)    - All desired seasons 
                weeks -  2D list (string)  - A list of lists containing all desired weeks 
                                           - Weeks must be associated with season, each season has a different set of weeks
    unique_file_names -   list (string)    - All desired file names for each file created
RETURN:
    - Each specified season will have their own .csv file containing all specified week outcomes
"""
def get_scores_given_seasons_and_weeks(scraper, seasons, weeks, unique_file_names=None):
    for i in range(len(seasons)):
        for j in weeks[i]:
            print(seasons[i] + " " + j)
            adding_data = scraper.get_game_week_scores(seasons[i], j)
            scraper.data = pd.concat([scraper.data, adding_data], ignore_index=True)
        if unique_file_names == None:
            scraper.data.to_csv('{}_scores.csv'.format(seasons[i]), index=False)
        else:
            scraper.data.to_csv('{}.csv'.format(unique_file_names[i]))
        scraper.data = pd.DataFrame()
    return

"""
PURPOSE:
    - Demonstrate how to use get_game_week_play_by_play() method.
INPUT PARAMETERS:
              scraper -      object        - instance of NFLScraper
              seasons -   list (string)    - All desired seasons 
                weeks -  2D list (string)  - A list of lists containing all desired weeks 
                                           - Weeks must be associated with season, each season has a different set of weeks
    unique_file_names -   list (string)    - All desired file names for each file created
RETURN:
    - Each specified week within a desired season will have their own .csv file containing all plays that were ran that week
"""
def get_plays_given_seasons_and_weeks(scraper, seasons, weeks, unique_file_names=None):
    for i in range(len(seasons)):
        for j in weeks[i]:
            print(seasons[i] + " " + j)
            scraper.data = scraper.get_game_week_play_by_play(seasons[i], j)
            if unique_file_names == None:
                scraper.data.to_csv('{}_{}_plays.csv'.format(seasons[i], j), index=False)
            else:
                scraper.data.to_csv('{}.csv'.format(unique_file_names[i]))
            scraper.data = pd.DataFrame()
    return

def main():

    print("STARTING")

    # Initializing instance of NflScraper 
    scraper = NflScraper(relative_path_to_webdriver)

    # Printing a dataframe containing all available seasons and weeks
    available_seasons_and_weeks = scraper.display_seasons_and_weeks()
    print(available_seasons_and_weeks)

    # List of Available seasons & List of Available weeks
    all_available_seasons = available_seasons_and_weeks["Season"].tolist()
    all_available_weeks_for_associated_seasons = available_seasons_and_weeks["Weeks"].tolist()


    #########################################
    # EXAMPLES ON HOW TO GRAB GAME OUTCOMES #
    #########################################


    # # Example 1 (get_scores_given_seasons_and_weeks)
    # # - Grabbing specified scores given a list of seasons, weeks, and file names for csv files
    # example_seasons = ['2020', '2021', '2022', '2023']
    # example_weeks = [['Week 1'], ['Week 1', 'Week 2'], ['Super Bowl'], ['Super Bowl']]
    # example_file_names = ['2020_week_1', '2021_week_1_2', '2022_SB', '2023_SB']
    # get_scores_given_seasons_and_weeks(scraper, 
    #                                    example_seasons, 
    #                                    example_weeks, 
    #                                    example_file_names)
    
    # # Example 2 (get_scores_given_seasons_and_weeks)
    # # - Grabbing all available scores from every week in every season
    # get_scores_given_seasons_and_weeks(scraper, 
    #                                    all_available_seasons, 
    #                                    all_available_weeks_for_associated_seasons)


    ######################################
    # EXAMPLES ON HOW TO GRAB GAME PLAYS #
    ######################################


    # # Example 1 (get_plays_given_seasons_and_weeks)
    # # - Grabbing plays from specified list of seasons and weeks
    # example_seasons = ['2017', '2023']
    # example_weeks = [['Week 1', 'Week 2'], ['Super Bowl']]
    # example_file_names = ['2017_week1_week2_plays', ['2023_SB_plays']]
    # get_plays_given_seasons_and_weeks(scraper, example_seasons, example_weeks, example_file_names)

    # Example 2 (get_plays_given_seasons_and_weeks)
    # - Grabbing all plays from a specified season and starting at desired week
    index_of_desired_season = all_available_seasons.index("2019")
    example_season = [all_available_seasons[index_of_desired_season]] # Needs to be a list of lists
    example_weeks = all_available_weeks_for_associated_seasons[index_of_desired_season]
    example_start_week = example_weeks.index("Week 1")
    example_week_start = [example_weeks[example_start_week::]] # Needs to be a list of lists
    get_plays_given_seasons_and_weeks(scraper, example_season, example_week_start)

    # # Example 3 (get_plays_given_seasons_and_weeks)
    # # - Grabbing all plays from every season available 
    # get_plays_given_seasons_and_weeks(scraper, all_available_seasons, all_available_weeks_for_associated_seasons)

    scraper.close_driver()

if __name__ == "__main__":
    main()