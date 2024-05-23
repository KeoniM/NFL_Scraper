# NFL specific webscraper
from scraper import NflScraper

# data manipulation
import pandas as pd

# Used to implement delays while scraping (trying to avoid getting banned by simulating user interaction)
import time
import random

"""
GLOBAL VARIABLES:
path_to_webdriver - string - absolute path to webdriver on personal machine.
"""

relative_path_to_webdriver = 'bin/chromedriver'

def main():

    print("STARTING")

    # Initializing instance of NflScraper 
    scraper = NflScraper(relative_path_to_webdriver)

    # Display all available seasons and weeks
    available_options = scraper.display_seasons_and_weeks()

    # Preparing a loop
    available_years = available_options["Season"].tolist()
    available_weeks = available_options["Weeks"].tolist()

    # Avoid overloading server
    base_sleep = 3
    random_additional_sleep = 5

    # Grabbing all scores from every week in every season & output each season results in .csv file
    for i in range(0,len(available_years),1):
        for j in available_weeks[i]:
            print(available_years[i] + " " + j)
            adding_data = scraper.get_game_week_scores(available_years[i], j)
            scraper.data = pd.concat([scraper.data, adding_data], ignore_index=True)
            time.sleep(base_sleep + random.random() * random_additional_sleep)
        scraper.data.to_csv('{}_scores.csv'.format(available_years[i]), index=False)
        scraper.data = pd.DataFrame()

    scraper.close_driver()
    
if __name__ == "__main__":
    main()