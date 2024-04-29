# NFL specific webscraper
from scraper import NflScraper

# data manipulation
import pandas as pd

# Used to implement delays while scraping (trying to avoid getting banned by simulating user interaction)
import time
import random

# notebooks (google colab / jupyter notebook)
#   - They are nice becuase you can truly run code step by step instead of having to run the whole thing over and over again.

# Prepare to post on github and use this to create a dataset that can be posted on kaggle.

# Should I have this connect to google bigquery?
# ^^^ I think this will be the next thing.

"""
GLOBAL VARIABLES:
path_to_webdriver - string - absolute path to webdriver on personal machine.
"""
path_to_webdriver = '/Users/keoni/VisualStudioCode/Python/SeleniumVE/myenv/bin/chromedriver'

def main():

    print("STARTING")

    # Initializing instance of NflScraper 
    scraper = NflScraper(path_to_webdriver)

    # Display all available seasons and weeks
    available_options = scraper.display_seasons_and_weeks()

    # # Preparing a loop
    # available_years = available_options["Season"].tolist()
    # available_weeks = available_options["Weeks"].tolist()
    # print(available_years)
    # # print(available_weeks)

    # # Simulate normal user on website
    # base_sleep = 5
    # random_additional_sleep = 5

    # for i in range(2,len(available_years),1):
    #     for j in available_weeks[i]:
    #         print(available_years[i] + " " + j)
    #         adding_data = scraper.get_game_week_data(available_years[i], j)
    #         scraper.data = pd.concat([scraper.data, adding_data], ignore_index=True)
    #         time.sleep(base_sleep + random.random() * random_additional_sleep)
    #     scraper.data.to_csv('{}_scores.csv'.format(available_years[i]), index=False)
    #     scraper.data = pd.DataFrame()

    # print(scraper.get_game_week_data("2017", "Preseason Week 4"))
    # print(scraper.get_game_week_data("2022", "Week 17"))
    # print(scraper.get_game_week_data("2022", "Week 11"))
    # print(scraper.get_game_week_data("2017", "Pro Bowl"))
    # print(scraper.get_game_week_data("2023", "Week 6"))
    # print(scraper.get_game_week_data("2023", "Super Bowl"))
    
    scraper.close_driver()
    
if __name__ == "__main__":
    main()