# Imports
# Driver tools
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

# Data manipulation
import pandas as pd
import numpy as np

# Imports for waiting until elements are ready to load
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Custom Waits
from custom_conditions import enough_elements_present
from custom_conditions import dropdown_search_and_select
from custom_conditions import child_element_to_be_present
from custom_conditions import enough_child_elements_present
from custom_conditions import get_dropdown_options
from custom_conditions import one_or_the_other_child

# exceptions
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException

"""
PURPOSE: 
  - Webscraping data from the National Football League's website (nfl.com)
    - The goal is to create a webdriver that will be able to retreive nfl data 
      that people can use to create their own custom nfl datasets.
INPUT PARAMETERS:
       self - Object Reference - Instance of NFL Webscraper
driver_path -      String      - Personal path to webdriver
ATTRIBUTES:
    self.driver - Web Driver - A tool used to automate Chrome browser actions
      self.data - Dataframe  - Used to store data that the webdriver is currently looking at
"""

class NflScraper:
  def __init__(self, driver_path):
    cService = webdriver.ChromeService(executable_path=driver_path)
    self.driver = webdriver.Chrome(service = cService)
    self.data = pd.DataFrame()

  # Close Chromedriver safely
  def close_driver(self):
      if self.driver:
        self.driver.quit()


  ##########################################################################################################################
  ##########################################################################################################################
  ##                                                                                                                      ##
  ##                                     METHODS TO OPEN VARIOUS PAGES IN NFL.COM                                         ##
  ##                                                                                                                      ##
  ##########################################################################################################################
  ##########################################################################################################################

  # # Version 1 (Outdated)
  # # NFL main site
  # def _open_nfl_website(self):
  #   self.driver.get("https://www.nfl.com/")

  # # NFL scores page
  # def _open_nfl_scores_page(self):
  #   self.driver.get("https://www.nfl.com/scores/")

  # """
  # PURPOSE:
  #   - Opens the 'scores' page to a specified season and week.
  # INPUT PARAMETERS:
  #     chosen_year - String - Users choice of year (Season) that they would like to grab game data from
  #     chosen_week - String - Users choice of week that they would like to grab data from
  #    max_attempts -  int   - The maximum amount of errors allowed to occur when searching webelements before quitting.
  # RETURN:
  #   - A state of the website open to the desired season and week.
  # """
  # def select_year_and_week(self, chosen_year, chosen_week, max_attempts=5):
  #     # Check to see if driver is on scores page. If not, will open scores page.
  #     if(self.driver.current_url != "https://www.nfl.com/scores/"):
  #         self._open_nfl_scores_page()

  #     wait = WebDriverWait(self.driver, 20)

  #     try:
  #       wait.until(dropdown_search_and_select((By.ID, "Season"), chosen_year))
  #       # Make sure the year has rendered before the week is searched. Without this, the DOM will mix weeks.
  #       # - The webelement targeted here is the first game. If that webelement fully loads, then the year selected has rendered.
  #       # wait.until(EC.presence_of_element_located((By.XPATH, "/html/body/div[3]/main/div/div/div/div/div/div/div[2]/div/div[3]"))) # NFL_Scraper 1.0
  #       # wait.until(EC.presence_of_element_located((By.XPATH, "/html/body/div[4]/main/div/div/div/div[2]/div/div/div[2]/div/div[4]"))) # NFL_Scraper 1.1
  #       # wait.until(EC.presence_of_element_located((By.XPATH, "/html/body/div[4]/main/div/div/div/div[2]/div/div/div[2]/div/div[3]"))) # NFL_Scraper 1.11
  #       wait.until(EC.presence_of_element_located((By.XPATH, "/html/body/div[3]/main/div/div/div/div[2]/div/div/div[2]/div/div[3]"))) # NFL_Scraper 1.12
  #       wait.until(dropdown_search_and_select((By.ID, "Week"), chosen_week))

  #       # grabbing webelement containing text of which week the page is on
  #       week_check = wait.until(
  #         # EC.presence_of_element_located((By.XPATH, "/html/body/div[3]/main/div/div/div/div/div/div/div/div/div/div")) # NFL_Scraper 1.0
  #         # EC.presence_of_element_located((By.XPATH, "/html/body/div[4]/main/div/div/div/div[2]/div/div/div/div/div/div")) # NFL_Scraper 1.1
  #         EC.presence_of_element_located((By.XPATH, "/html/body/div[3]/main/div/div/div/div[2]/div/div/div/div/div/div")) # NFL_Scraper 1.12
  #       )

  #       # double check to be sure that the users "chosen_week" matches the page
  #       if(" ".join(week_check.text.split()[2::]) == chosen_week):
  #         # After the correct page has been selected (for a fact), this next step is to make sure the DOM renders completely before moving on.
  #         # wait.until(EC.presence_of_element_located((By.XPATH, "/html/body/div[4]/main/div/div/div/div[2]/div/div/div[2]/div/div[3]"))) # NFL_Scraper 1.11
  #         wait.until(EC.presence_of_element_located((By.XPATH, "/html/body/div[3]/main/div/div/div/div[2]/div/div/div[2]/div/div[3]"))) # NFL_Scraper 1.12
  #         return
  #       else:
  #         return self.select_year_and_week(self.driver, chosen_year, chosen_week, max_attempts - 1)

  #     # If dropdowns have not been found yet, will run method over again.
  #     except StaleElementReferenceException:
  #       if(max_attempts > 0):
  #           print("SEARCHING, attempting {} more times (select year and week)".format(max_attempts))
  #           return self.select_year_and_week(self.driver, chosen_year, chosen_week, max_attempts - 1)
  #       else:
  #           return print("Driver unable to find available options. Try again.")
  #     except NoSuchElementException:
  #       return print("This year/week is not an option./nSee if season and year are available using the method 'display_seasons_and_weeks()'")


  # Version 2 (updated 11/25/2025)
  # NFL main site
  def _open_nfl_website(self):
    self.driver.get("https://www.nfl.com/")

  # NFL scores page
  def _open_nfl_scores_page(self):
    self.driver.get("https://www.nfl.com/scores/")

  """
  PURPOSE:
    - Opens the 'scores' page to a specified season and week.
  INPUT PARAMETERS:
      chosen_year - String - Users choice of year (Season) that they would like to grab game data from
      chosen_week - String - Users choice of week that they would like to grab data from
     max_attempts -  int   - The maximum amount of errors allowed to occur when searching webelements before quitting.
  RETURN:
    - A state of the website open to the desired season and week.
  """
  def select_year_and_week(self, chosen_year, chosen_week, max_attempts=5):
      # Check to see if driver is on scores page. If not, will open scores page.
      if(self.driver.current_url != "https://www.nfl.com/scores/"):
          self._open_nfl_scores_page()

      wait = WebDriverWait(self.driver, 20)

      try:
        wait.until(dropdown_search_and_select((By.ID, "season-select"), chosen_year))
        # Make sure the year has rendered before the week is searched. Without this, the DOM will mix weeks.
        # - The webelement targeted here is the first game. If that webelement fully loads, then the year selected has rendered.
        wait.until(EC.presence_of_element_located((By.XPATH, "html/body/div[2]/main/div/div/div/section/div[2]/div/div/div/div/div/div[1]/ul[1]/li[1]")))

        # Select week
        # - Searches through available weeks within season and opens chosen week page
        carousel_week_select = wait.until(EC.presence_of_element_located((By.XPATH, "/html/body/div[2]/main/div/div/div/section/div/nav/ul")))
        week_options = carousel_week_select.find_elements(By.TAG_NAME, 'li')
        for week in week_options:
          week_option = wait.until(child_element_to_be_present(week, (By.XPATH, "./div/a/dl/dd[1]"))).text
          if week_option == chosen_week:
            chosen_week_url_webelement = wait.until(child_element_to_be_present(week, (By.XPATH, "./div/a")))
            chosen_week_url = chosen_week_url_webelement.get_attribute("href")
            self.driver.get(chosen_week_url)
            break

        # grabbing webelement containing text of which week the page is on
        week_check = wait.until(
          EC.presence_of_element_located((By.XPATH, "/html/body/div[2]/main/div/div/div/section/div[2]/div[2]/div"))
        )

        # double check to be sure that the users "chosen_week" matches the page
        if(week_check.text == chosen_week):
          # After the correct page has been selected (for a fact), this next step is to make sure the DOM renders completely before moving on.
          wait.until(EC.presence_of_element_located((By.XPATH, "html/body/div[2]/main/div/div/div/section/div[2]/div/div/div/div/div/div[1]/ul[1]/li[1]")))
          return
        else:
          return self.select_year_and_week(self.driver, chosen_year, chosen_week, max_attempts - 1)

      # If dropdowns have not been found yet, will run method over again.
      except StaleElementReferenceException:
        if(max_attempts > 0):
            print("SEARCHING, attempting {} more times (select year and week)".format(max_attempts))
            return self.select_year_and_week(self.driver, chosen_year, chosen_week, max_attempts - 1)
        else:
            return print("Driver unable to find available options. Try again.")
      except NoSuchElementException:
        return print("This year/week is not an option./nSee if season and year are available using the method 'display_seasons_and_weeks()'")


  ###########################################################################################################################
  ###########################################################################################################################
  ##                                                                                                                       ##
  ##                                       METHODS TO DISPLAY AVAILABLE OPTIONS                                            ##
  ##                                                                                                                       ##
  ###########################################################################################################################
  ###########################################################################################################################

  # # Version 1
  # """
  # PURPOSE:
  #   - Display all available NFL seasons and weeks to grab data from.
  # INPUT PARAMETERS:
  #   max_attempts - int - maximum number of attempts to find webelements
  # RETURN:
  #     df_season_week_opions - dataframe - contains seasons and weeks available to gather data from.
  # NOTES:
  #   - Not all options in 'season' dropdown is actually avaiable
  #   - 'Weeks' dropdown is different for almost every season
  # """
  # def display_seasons_and_weeks(self, max_attempts = 5):

  #   # Check to make sure driver is on nfl scores page.
  #   if(self.driver.current_url != "https://www.nfl.com/scores/"):
  #     self._open_nfl_scores_page()

  #   # Return dataframe that will contain seasons and weeks available
  #   df_season_week_options = pd.DataFrame(columns=["Season", "Weeks"])

  #   wait = WebDriverWait(self.driver, 20)

  #   try:
  #     # All available elements within 'season' dropdown placed into list.
  #     season_webelement_options = wait.until(get_dropdown_options((By.CSS_SELECTOR, "#Season")))

  #     # Finding 'Weeks' schedule for each season
  #     for i in season_webelement_options:
  #       try:
  #         wait.until(dropdown_search_and_select((By.ID, "Season"), i))
  #         weeks_webelement_options = wait.until(get_dropdown_options((By.CSS_SELECTOR, "#Week")))
  #         season_and_weeks = [i, weeks_webelement_options]
  #         df_season_week_options.loc[len(df_season_week_options)] = season_and_weeks
  #       except TimeoutException: # This might be a mistake. if there is a TimeoutException I think it would end up returning a list while missing a season or week.
  #          continue
  #     return df_season_week_options
    
  #   # Error handling while searching for dropdowns. Will run method completely over again.
  #   except StaleElementReferenceException: 
  #     if(max_attempts > 0):
  #       print("SEARCHING, attempting {} more times".format(max_attempts))
  #       return self.display_seasons_and_weeks(max_attempts-1)
  #     else:
  #         return print("Driver unable to find available options. Try again.")
  
  # Version 2 (updated 11/25/2025)
  """
  PURPOSE:
    - Display all available NFL seasons and weeks to grab data from.
  INPUT PARAMETERS:
    max_attempts - int - maximum number of attempts to find webelements
  RETURN:
      df_season_week_opions - dataframe - contains seasons and weeks available to gather data from.
  NOTES:
    - Not all options in 'season' dropdown is actually avaiable
    - 'Weeks' dropdown is different for almost every season
  """
  def display_seasons_and_weeks(self, max_attempts = 5):

    # Check to make sure driver is on nfl scores page.
    if(self.driver.current_url != "https://www.nfl.com/scores/"):
      self._open_nfl_scores_page()

    # Return dataframe that will contain seasons and weeks available
    df_season_week_options = pd.DataFrame(columns=["Season", "Weeks"])

    wait = WebDriverWait(self.driver, 20)

    try:
      # All available elements within 'season' dropdown placed into list.
      season_webelement_options = wait.until(get_dropdown_options((By.ID, "season-select")))

      # Finding 'Weeks' schedule for each season
      for season in season_webelement_options:
        try:
          # Selecting Season
          wait.until(dropdown_search_and_select((By.ID, "season-select"), season))
          # Identifying weeks in season
          list_of_weeks = wait.until(EC.presence_of_element_located((By.XPATH, "/html/body/div[2]/main/div/div/div/section/div/nav/ul")))
          list_week_elements = list_of_weeks.find_elements(By.TAG_NAME, 'li')
          weeks_in_season = [
            wait.until(child_element_to_be_present(week, (By.XPATH, "./div/a/dl/dd[1]"))).text 
            for week in list_week_elements
            ]
          season_and_weeks = [season, weeks_in_season]
          df_season_week_options.loc[len(df_season_week_options)] = season_and_weeks
        except TimeoutException: # This might be a mistake. if there is a TimeoutException I think it would end up returning a list while missing a season or week.
          continue
      return df_season_week_options
        
    # Error handling while searching for dropdowns. Will run method completely over again.
    except StaleElementReferenceException: 
      if(max_attempts > 0):
        print("SEARCHING, attempting {} more times".format(max_attempts))
        return self.display_seasons_and_weeks(max_attempts-1)
      else:
          return print("Driver unable to find available options. Try again.")


  ###########################################################################################################################
  ###########################################################################################################################
  ##                                                                                                                       ##
  ##                                         METHODS TO GRAB AVAILABLE DATA                                                ##
  ##                                                                                                                       ##
  ###########################################################################################################################
  ###########################################################################################################################

  # Outdated Version
  # """
  # PURPOSE:
  #   - Get all game webelements in a specified week and season.
  #     - Not meant to be called but to be used as a helper method for 'get_parsed_game_week_webelements()'
  # INPUT PARAMETERS:
  #    chosen_year - string - user chooses a season which happens to be all in years
  #    chosen_week - string - user chooses a week within a given season
  #   max_attempts -  int   - number of errors allowed when finding webelements
  # RETURN:
  #   - All webelements for games in specified week and season
  # """
  # def get_game_week_webelements(self, chosen_year, chosen_week, max_attempts=5):

  #   self.select_year_and_week(chosen_year, chosen_week)

  #   wait = WebDriverWait(self.driver, 5)

  #   # webelement that shares a classname with all webelements that contain desired data (Titles/Scores/Byes/Upcoming).
  #   # - Should be webelement container stating which week the page is on (e.g. 'Games - Week 2')
  #   shared_classname_webelement = wait.until(
  #       # /html/body/div[4]/main/div/div/div/div[2]/div/div/div
  #       # EC.presence_of_element_located((By.XPATH, "/html/body/div[3]/main/div/div/div/div/div/div/div")) # NFL_Scraper 1.0
  #       # EC.presence_of_element_located((By.XPATH, "/html/body/div[4]/main/div/div/div/div[2]/div/div/div")) # NFL_Scraper 1.1
  #       EC.presence_of_element_located((By.XPATH, "/html/body/div[3]/main/div/div/div/div[2]/div/div/div")) # NFL_Scraper 1.12
  #   )

  #   # the shared classname for all desired webelements
  #   scores_shared_classname = shared_classname_webelement.get_attribute("class")

  #   # Different weeks have different amounts of games displaying. (each week as a different amount of desired webelements displaying).
  #   num_score_elements = 19 # Week 1 - Week 17 
  #   if chosen_week in ["Hall Of Fame", "Pro Bowl", "Super Bowl"]:
  #       num_score_elements = 4
  #   elif chosen_week in ["Conference Championships"]:
  #       num_score_elements = 5
  #   # elif chosen_week in ["Divisional Playoffs", "Wild Card Weekend"]:
  #   elif chosen_week in ["Divisional Playoffs", "Wild Card"]: # NFL_Scraper 1.12
  #       num_score_elements = 7

  #   # A measure to ensure that all games (webelements) were captured
  #   # NOTE: an issue that I have been running into is that the scraper will grab all webelements that 
  #   #       are currently displaying in the DOM, but that does not necessarily mean that all of the
  #   #       webelements are displaying at that time. This is the method that I came up with to combat 
  #   #       that issue.
  #   try:
  #       # If same number of webelements are grabbed 5 times in a row, then that is likely the amount of game webelements available for that week
  #       total = 0
  #       array = [np.nan]
  #       while( total % array[0] != 0):
  #         total = 0
  #         array = []
  #         for i in range(0,5,1):
  #           game_webelements = wait.until(enough_elements_present((By.CLASS_NAME, scores_shared_classname), num_score_elements))
  #           total += len(game_webelements)
  #           array.append(len(game_webelements))

  #       checked_game_webelements = game_webelements

  #   except TimeoutException:
  #       if (max_attempts > 0):
  #         print("SEARCHING, attempting {} more times (get game week data)".format(max_attempts))
  #         return self.get_game_week_webelements(chosen_year, chosen_week, max_attempts - 1)
  #       else:
  #           return print("Unable to get game week data.")

  #   # The first 3-4 elements to all score pages are titles and adds that are not wanted.
  #   if (checked_game_webelements[1].text.lower() == "final"):
  #      return checked_game_webelements[3::]
  #   elif(checked_game_webelements[1].text.lower() == "upcoming"):
  #      return checked_game_webelements[4::]
  #   else:
  #      return print("{} {} has not been accounted for yet. Look under 'get_game_week_webelements' and try to fix this".format(chosen_year, chosen_week))

  # Version 2 (updated 11/25/2025)
  """
  PURPOSE:
    - Get all game webelements in a specified week and season.
      - Not meant to be called but to be used as a helper method for 'get_parsed_game_week_webelements()'
  INPUT PARAMETERS:
     chosen_year - string - user chooses a season which happens to be all in years
     chosen_week - string - user chooses a week within a given season
    max_attempts -  int   - number of errors allowed when finding webelements
  RETURN:
    - All webelements for games in specified week and season
  """
  def get_game_week_webelements(self, chosen_year, chosen_week, max_attempts=5):

    self.select_year_and_week(chosen_year, chosen_week)

    wait = WebDriverWait(self.driver, 5)

    # Parent webelement that has all game outcomes (Scores/Byes/Upcoming)
    parent_webelement_games = wait.until(
      EC.presence_of_element_located((By.XPATH, "/html/body/div[2]/main/div/div/div/section/div[2]/div/div/div/div/div"))
    )

    # This block of code doubles as:
    # 1. Grabbing all webelements that contain game data
    # 2. A measure to ensure that all games (webelements) were captured
    # NOTE: an issue that I have been running into is that the scraper will grab all webelements that 
    #       are currently displaying in the DOM, but that does not necessarily mean that all of the
    #       webelements are displaying at that time. This is the method that I came up with to combat 
    #       that issue.
    try:
        # If same number of webelements are grabbed 5 times in a row, then that is likely the amount of game webelements available for that week
        total = 0
        array = [np.nan]
        while( total % array[0] != 0 ):
          total = 0
          array = []
          for i in range(0,5,1):
            # Games are separated into different sections based on the date of when the game took place or if the team is on bye.
            # - Each grouping of games are within div tags
            game_webelements = wait.until(enough_child_elements_present(parent_webelement_games, (By.XPATH, './div'), 1))
            total += len(game_webelements)
            array.append(len(game_webelements))
        # Final Answer (A list that has all game webelements)
        checked_game_webelements = game_webelements
    except TimeoutException:
        if (max_attempts > 0):
          print("SEARCHING, attempting {} more times (get game week data)".format(max_attempts))
          return self.get_game_week_webelements(chosen_year, chosen_week, max_attempts - 1)
        else:
            return print("Unable to get game week data.")
        
    # Taking out adds
    game_webelements = []
    for game_day in checked_game_webelements:
      # tags that have attributes are adds. They are not webelements that have game data in them.
      has_attributes = self.driver.execute_script("return arguments[0].attributes.length > 0;", game_day)
      if has_attributes:
        continue
      else:
        self.driver.execute_script("arguments[0].style.border='3px solid blue'", game_day)
        game_webelements.append(game_day)

    return game_webelements


  #############################################################################
  #                                                                           #
  #          METHODS THAT EXTRACT SCORING DATA FROM GAME WEBELEMENTS          #
  #                                                                           #
  #############################################################################

  # - I need to create a new version of this.
  #   - Each grouping of games are separated by dates(?) (e.g. 'Thursday Night Football, December 4th',
  #                                                            'Thursday, December 16th',
  #                                                            'Sunday, November 16th, International Game',
  #                                                            'Teams on Bye')
  #                                                            - I dont exactly know how to categorize this.
  #                                                            - Game status?

  # Version 1
  # """
  # PURPOSE:
  #   - Parse out different types of game webelements 
  #     (games played, upcoming games, bye weeks, cancelled games)
  # INPUT PARAMETERS:
  #    chosen_year - string - user chooses a season which happens to be all in years
  #    chosen_week - string - user chooses a week within a given season
  # RETURN:
  #   - list of parsed game webelements -> [games_played, games_bye, games_cancelled, games_upcoming]
  # """
  # def get_parsed_game_week_webelements(self, chosen_year, chosen_week):

  #   wait = WebDriverWait(self.driver, 2)

  #   game_week_webelements = self.get_game_week_webelements(chosen_year, chosen_week)

  #   # Lists to return
  #   games_played = []
  #   games_bye = []
  #   games_cancelled = []
  #   games_upcoming = []

  #   for i in game_week_webelements:
  #       try:
  #           # locator1 = (By.XPATH, "./div/div/button/div") 
  #           # - Locator for webelements that contain (cancelled games, games played, upcoming games)
  #           # locator2 = (By.XPATH, ".//button/div[1]")
  #           # - Locator for webelements that are bye weeks
  #           game = wait.until(one_or_the_other_child(i, (By.XPATH, "./div/div/button/div"), (By.XPATH, ".//button/div[1]")))

  #           if game[1] == 1:
  #             status_and_date = wait.until(child_element_to_be_present(game[0], (By.XPATH, "./div[1]")))
  #             game_data = status_and_date.text.split()
  #             # The only status games that I have come across are
  #             # 1. Cancelled game
  #             # 2. Final outcome
  #             # 3. Upcoming games
  #             if game_data.count('CANCELLED') >= 1:
  #               games_cancelled.append(i)
  #             elif game_data.count('FINAL') >= 1:
  #               games_played.append(i)
  #             else:
  #               games_upcoming.append(i)
  #           else:
  #             games_bye.append(i)    
            
  #       except:
  #         continue
 
  #   # print("{} {} has {} played_games, {} byes, {} cancelled games, {} upcoming games".format(chosen_year, 
  #   #                                                                                          chosen_week, 
  #   #                                                                                          len(games_played), 
  #   #                                                                                          len(games_bye), 
  #   #                                                                                          len(games_cancelled), 
  #   #                                                                                          len(games_upcoming)))

  #   return [games_played, games_bye, games_cancelled, games_upcoming]

  # Version 2 (updated 12/03/2025)
  """
  PURPOSE:
    - Organize game week webelements by description followed by games that follow
  INPUT PARAMETERS:
     chosen_year - string - user chooses a season which happens to be all in years
     chosen_week - string - user chooses a week within a given season
  RETURN:
    - list of organized game week webelements
      [[game_week_description, [games within game week description]], 
       [game_week_description, [games within game week description]],
        .... ]
  """
  def get_parsed_game_week_webelements(self, chosen_year, chosen_week):

    wait = WebDriverWait(self.driver, 2)

    game_week_webelements = self.get_game_week_webelements(chosen_year, chosen_week)

    # 'game_week_webelements' will give me a list webelements containing groupings of games.
    # These webelements will have:
    # 1. A description with something like "Thursday Night Football, December 4th" or "Sunday, December 7th"
    # 2. A list of webelements containing games that fall under that description

    # Will create a list of list elements. 
    # each list element within the list will look like: 
    # [games_description, [webelement of each game]]
    game_groupings = []

    for game_grouping in game_week_webelements:

      # Will eventually have to account for game groupings that are descriptionless
      game_grouping_description = wait.until(child_element_to_be_present(game_grouping, (By.XPATH, "./div[1]")))

      # games_description
      game_group_description = game_grouping_description.text

      # [webelement of each game]
      if "Bye" in game_group_description:
        teams_on_bye = wait.until(enough_child_elements_present(game_grouping, (By.XPATH, './div[2]/div/div'), 1))
        game_groupings.append([game_group_description, teams_on_bye])
      else:
        grouping_games = wait.until(enough_child_elements_present(game_grouping, (By.XPATH, './ul/li'), 1))
        game_groupings.append([game_group_description, grouping_games])

    return game_groupings

  # Version 1 (Outdated)
  # """
  # PURPOSE:
  #   - Return outcomes of all games within a specified week (e.g. Final scores of a game played)
  # INPUT PARAMETERS:
  #   chosen_year - string - user chooses a season which happens to be all in years
  #   chosen_week - string - user chooses a week within a given season
  # RETURN:
  #   df_week_scores - Dataframe - contains all data for outcomes of each game webelement
  # """
  # def get_game_week_scores(self, chosen_year, chosen_week):

  #   parsed_game_webelements = self.get_parsed_game_week_webelements(chosen_year, chosen_week)

  #   games_played = parsed_game_webelements[0]
  #   games_bye = parsed_game_webelements[1]
  #   games_cancelled = parsed_game_webelements[2]
  #   games_upcoming = parsed_game_webelements[3]

  #   # return dataframe
  #   df_week_scores = pd.DataFrame(columns=["Season", "Week", "GameStatus", "Day", "Date", 
  #                                   "AwayTeam", "AwayRecord", "AwayScore", "AwayWin",
  #                                   "HomeTeam", "HomeRecord", "HomeScore", "HomeWin",
  #                                   "AwaySeeding", "HomeSeeding", "PostSeason"])
    
  #   """
  #   PURPOSE:
  #     - Handle "game status" data from game webelement (e.i. game type / game day / game date)
  #   INPUTE PARAMETERS:
  #     sad_webelement - webelement - status and date of individual game
  #          game_type - list name  - collection of game type webelemenets (e.g. list of games played within the week)
  #   RETURN:
  #     A collection of status and date data of the individual game (e.g. ['FINAL', 'SUN', '02/07'])
  #   """
  #   def get_game_status_and_date(sad_webelement, game_type):

  #     sad_data = sad_webelement.text.split()
  #     sad_data.remove("-")

  #     if game_type == games_played:
  #       return sad_data
  #     if game_type == games_cancelled:
  #      return ['CANCELLED', 'CANCELLED', 'CANCELLED']
  #     sad_data.insert(0, 'UPCOMING')
  #     return sad_data[:3:1]

  #   """
  #   PURPOSE: 
  #     - Handle "scores" data from game webelement (e.i. game played / game cancelled / bye week)
  #   INPUT PARAMETERS:
  #     scores_webelement - webelement - contains scores data of game
  #   RETURN:
  #     organized_game_data - list - contains organized data that breaks down the game contained in webelement.
  #   NOTE:
  #     - This method will fail if some games have been played and some have not been played yet. 
  #       - (e.g. Thursday game has finished but none of the games on Sunday have been played yet.)
  #   """
  #   def get_score_data(scores_webelement):

  #     # text data within webelement.
  #     scores_data = scores_webelement.text.split()
      
  #     # Variables to be filled with 'scores_data' and returned in a list
  #     away_team_name = None
  #     home_team_name = None
  #     away_record = np.nan
  #     home_record = np.nan
  #     away_score = 0
  #     home_score = 0
  #     away_win = 0
  #     home_win = 0
  #     away_seeding = np.nan
  #     home_seeding = np.nan
  #     is_postseason = 0

  #     clean_scores_data = [] # list for filtered and cleaned 'scores_data'
  #     multi_word_team_name = [] # Used for the rare case of a team having multiple strings within their name.

  #     # Filter for 'scores_data'.
  #     # Cycle through 'scores_data' and merge side by side strings to fit in a single element within a list.
  #     while(len(scores_data) != 0): 
  #       if scores_data[0][0].isupper():
  #         multi_word_team_name.append(scores_data[0])
  #         scores_data.pop(0)
  #         continue
  #       else:
  #         if len(multi_word_team_name) > 0:
  #           clean_scores_data.append(" ".join(multi_word_team_name))
  #           multi_word_team_name.clear()
  #         clean_scores_data.append(scores_data[0])
  #         scores_data.pop(0)
  #         continue

  #     # Data is symmetrical. Split evenly between away and home team
  #     data_split = int(len(clean_scores_data)/2)
  #     away_team = clean_scores_data[:data_split:]
  #     home_team = clean_scores_data[data_split::]

  #     # Postseason check 
  #     if(away_team[0].isnumeric()):
  #       is_postseason = 1
  #       away_seeding = away_team[0]
  #       home_seeding = home_team[0]
  #       away_team.pop(0)
  #       home_team.pop(0)

  #     # Team Names
  #     away_team_name = away_team[0]
  #     home_team_name = home_team[0]
  #     away_team.pop(0)
  #     home_team.pop(0)

  #     # Game scores AND team records (special cases will have one or the other)
  #     while(len(away_team) > 0):
  #       if(away_team[0].isnumeric()):
  #         away_score = away_team[0]
  #         home_score = home_team[0]
  #       else:
  #         away_record = away_team[0]
  #         home_record = home_team[0]
  #       away_team.pop(0)
  #       home_team.pop(0)

  #     # Team win check
  #     if(int(away_score) > int(home_score)):
  #       away_win = 1
  #       home_win = 0
  #     elif(int(away_score) < int(home_score)):
  #       away_win = 0
  #       home_win = 1
      
  #     oganized_game_data = [away_team_name, away_record, away_score, away_win,
  #                           home_team_name, home_record, home_score, home_win,
  #                           away_seeding, home_seeding, is_postseason]
      
  #     return oganized_game_data
    
  #   # Loop that goes through each game webelement of a specified game week
  #   for i in [games_played, games_upcoming, games_bye, games_cancelled]:
  #     if i == games_bye:
  #       for j in i:
  #         individual_game_data = []
  #         game = j.find_element(By.XPATH, ".//button/div[1]")
  #         self.driver.execute_script("arguments[0].style.border='3px solid blue'", game)
  #         individual_game_data += [np.nan] * 7
  #         game_team_data = game.text.split() # ['Name', 'Record']
  #         individual_game_data.insert(0, chosen_year)
  #         individual_game_data.insert(1, chosen_week)
  #         individual_game_data.insert(2, "BYE")
  #         individual_game_data.insert(3, None)
  #         individual_game_data.insert(4, None)
  #         individual_game_data.insert(5, game_team_data[0])
  #         individual_game_data.insert(6, game_team_data[1][1:len(game_team_data[1]) - 1]) # "(#-#)" -> "#-#"
  #         individual_game_data.insert(9, None)
  #         individual_game_data.append(0) # Placevalue for Postseason column. Postseason weeks do not have bye weeks displayed.
  #         df_week_scores.loc[len(df_week_scores)] = individual_game_data
  #     else:
  #       for j in i:
  #         individual_game_data = []
  #         game = j.find_element(By.XPATH, "./div/div/button/div")
  #         status_and_date_webelement = game.find_element(By.XPATH, "./div[1]")
  #         self.driver.execute_script("arguments[0].style.border='3px solid purple'", status_and_date_webelement)
  #         individual_game_data.extend(get_game_status_and_date(status_and_date_webelement, i))
  #         score_webelement = game.find_element(By.XPATH, "./div[2]/div")
  #         self.driver.execute_script("arguments[0].style.border='3px solid red'", score_webelement)
  #         individual_game_data.extend(get_score_data(score_webelement))
  #         individual_game_data.insert(0, chosen_week)
  #         individual_game_data.insert(0, chosen_year)
  #         df_week_scores.loc[len(df_week_scores)] = individual_game_data
      
  #   return df_week_scores

  # Version 2 (updated 12/04/2025)
  """
  PURPOSE:
    - Return outcomes of all games within a specified week (e.g. Final scores of a game played)
  INPUT PARAMETERS:
    chosen_year - string - user chooses a season which happens to be all in years
    chosen_week - string - user chooses a week within a given season
  RETURN:
    df_week_scores - Dataframe - contains all data for outcomes of each game webelement
  """
  def get_game_week_scores(self, chosen_year, chosen_week):

    grouped_games_by_week = self.get_parsed_game_week_webelements(chosen_year, chosen_week)

    for group in grouped_games_by_week:
      grouped_games_description = group[0]
      grouped_games = group[1]
      # Bye week
      if "Bye" in grouped_games_description:
        continue
        # for game in grouped_games:
      # Regular games
      else:
        for game in grouped_games:

          # game description
          print(grouped_games_description)

          # game status
          game_status = game.find_element(By.XPATH, "./div/div[2]/div/div/div")
          print(game_status.text)

          # away team
          away_team = game.find_element(By.XPATH, "./div/div[1]/div[1]/div[1]/div/div[2]/div[2]")
          self.driver.execute_script("arguments[0].style.border='3px solid blue'", away_team)
          away_name = away_team.find_element(By.XPATH, "./span[3]")
          away_score = away_team.find_element(By.XPATH, "./div/div/span")
          print(away_name.text)
          print(away_score.text)

          # home team
          home_team = game.find_element(By.XPATH, "./div/div[1]/div[1]/div[2]/div/div[2]/div[2]")
          self.driver.execute_script("arguments[0].style.border='3px solid red'", home_team)
          home_name = home_team.find_element(By.XPATH, "./span[3]")
          home_score = home_team.find_element(By.XPATH, "./div/div/span")
          print(home_name.text)
          print(home_score.text)

      

    # As far as I see, there are 3 different types of game grouping description:
    # 1. regular games:
    #    - Sunday, December 7th
    # 2. Bye weeks:
    #    - Teams on Bye
    # 3. Games that haven't been determined yet:
    #    - Won't have a title description

    # PLAN:
    # 1. I will check groupings descriptions for (1. bye weeks 2. games that haven't been determined yet)
    #    - These titles are consistent and do not change.
    #      - Look for "Bye" in title for bye weeks
    #      - If there is nothing, then it hasn't been determined yet.
    # 2. Clean regular games as (else)
    #    - I will clean and scrape necessities.
    #      - I am not going to grab things that can be figured out using feature engineering.
    #        - Examples:
    #          1. team record
    #          2. who won
      
    return 



# # Outdated version (Website update in August 2025)
# ##################################################################################
# #                                                                                #
# #          METHODS THAT EXTRACT PLAY BY PLAY DATA FROM GAME WEBELEMENTS          #
# #                                                                                #
# ##################################################################################


#   """
#   PURPOSE:
#     - Extract each play that happened in each game within a specified season and week
#   INPUT PARAMETERS:
#     chosen_year - string - user chooses a season which happens to be all in years
#     chosen_week - string - user chooses a week within a given season
#   RETURN:
#     df_week_plays - Dataframe - contains all data for outcomes of each game webelement
#   """
#   def get_game_week_play_by_play(self, chosen_year, chosen_week):

#     wait = WebDriverWait(self.driver, 20)

#     df_week_plays = pd.DataFrame(columns=['Season', 'Week', 'Day', 'Date', 'AwayTeam', 'HomeTeam', 
#                                           'Quarter', 
#                                           'DriveNumber', 'TeamWithPossession', 'IsScoringDrive',
#                                           'PlayNumberInDrive', 'IsScoringPlay', 'PlayOutcome', 'PlayDescription', 'PlayStart'])

#     """
#     PURPOSE:
#       - A double check to see if all child webelements have been found within a parent webelement
#     INPUT PARAMETERS:
#        parent_webelement - webelement - contains a webelement encapsulating either every quarter of a game or every drive within a quarter
#                  locator -   tuple    - A shared path from the parent webelement to the child webelements
#       num_elements_check -    int     - The least amount of child elements expected to be found
#          accuracy_number -    int     - the amount of times the method has to find the same number of child webelements consecutively
#     RETURN:
#              webelements -    list    - All specified child webelements under parent webelement
#     """
#     def num_child_webelements_check(parent_webelement, locator, num_elements_check, accuracy_number):
#       total = 0
#       array = [np.nan]
#       while( total % array[0] != 0 ):
#         total = 0
#         array = []
#         for i in range(0, accuracy_number,1):
#           webelements = wait.until(enough_child_elements_present(parent_webelement, (locator), num_elements_check))
#           total += len(webelements)
#           array.append(len(webelements))
#       return webelements
    
#     # get_parsed_game_week_webelements[0] -> returns all webelements of games that were played during the specified week
#     game_week_webelements = self.get_parsed_game_week_webelements(chosen_year, chosen_week)[0] 

#     for i in range(len(game_week_webelements)):

#       # This is necessary because these webelements seem to change when you move forward and backward through pages
#       game = self.get_parsed_game_week_webelements(chosen_year,chosen_week)[0][i]

#       try:
          
#           # ['Year', 'Week']
#           game_info = [chosen_year, chosen_week]

#           # Locating game button to 
#           # 1. Use as parent element to grab "game_info"
#           # 2. Click to get to "play_by_play_data"
#           game_button_webelement = wait.until(child_element_to_be_present(game, (By.XPATH, "./div/div/button")))

#           self.driver.execute_script("arguments[0].style.border='3px solid red'", game_button_webelement)

#           # ['Day', 'Date']
#           game_date_webelement = wait.until(child_element_to_be_present(game_button_webelement, (By.XPATH, "./div/div[1]")))
#           self.driver.execute_script("arguments[0].style.border='3px solid red'", game_date_webelement)
#           game_date = game_date_webelement.text.split()
#           game_info.extend(game_date[2::])

#           # ['Away Team', 'Home Team']
#           game_team_scores_webelement = wait.until(child_element_to_be_present(game_button_webelement, (By.XPATH, "./div/div[2]")))
#           self.driver.execute_script("arguments[0].style.border='3px solid red'", game_team_scores_webelement)
#           game_team_scores_data = game_team_scores_webelement.text.split()

#           team_names_data = [] # list for team names ['Away Team', 'Home Team']
#           multi_word_team_name = [] # Used for the rare case of a team having multiple strings within their name.
#           # Loop will receive list somewhat like:
#           # ['AwayTeam', 'AwayRecord', 'AwayScore', 'HomeTeam', 'HomeRecord', 'HomeScore']
#           # Rarely loop will receive list like:
#           # ['AwayTeam First half of name', 'AwayTeam Second half of name', 'AwayRecord', 'AwayScore', 'HomeTeam', 'HomeRecord', 'HomeScore']
#           # Either way we want to get list to be like:
#           # ['Away Team', 'Home Team']
#           while(len(game_team_scores_data) != 0):
#             if (game_team_scores_data[0].count("-") > 0 or game_team_scores_data[0].isdigit()):
#               if len(multi_word_team_name) > 0:
#                   team_names_data.append(" ".join(multi_word_team_name))
#                   multi_word_team_name.clear()
#               game_team_scores_data.pop(0)
#               continue
#             else:
#               multi_word_team_name.append(game_team_scores_data[0])
#               game_team_scores_data.pop(0)
#               continue
            
#           # game_details = ['Year', 'Week', 'Day', 'Date', 'Away Team', 'Home Team']]
#           game_info.extend(team_names_data)

#           # Scroll into view and click using JavaScript
#           self.driver.execute_script("arguments[0].scrollIntoView(); arguments[0].click();", game_button_webelement)




#           # UPDATE for newly updated website.
#           # for 'All Drives' is now a button
#           # xpath = html/body/div/main/div[2]/div/div/section[2]/div/div[2]/div/div/div/section/div


#           # Wrapper webelement containing every quarter played
#           game_parent_webelement = wait.until(EC.presence_of_element_located((By.ID, "all-drives-panel")))

#           every_quarter_in_game = num_child_webelements_check(game_parent_webelement, (By.XPATH, "./div"), 1, 5)
          
#           # Loop through every quarter of the game
#           for quarter in every_quarter_in_game:

#             # Data up to the quarter of the game
#             quarter_data = game_info.copy()

#             self.driver.execute_script("arguments[0].style.border='3px solid red'", quarter)

#             quarter_number = wait.until(child_element_to_be_present(quarter, (By.XPATH, "./div")))
#             self.driver.execute_script("arguments[0].style.border='3px solid red'", quarter_number)

#             # ['Quarter #']
#             quarter_number = quarter_number.text
#             quarter_data.extend([quarter_number])

#             every_drive_in_quarter = num_child_webelements_check(quarter, (By.XPATH, "./div"), 1, 5)

#             # Loop through every drive of the quarter
#             drives = [] # Keep count of how many drives in quarter
#             for drive in every_drive_in_quarter[1::]:
#               drives.append(drive)
              
#               # Data up until the drive of the quarter
#               drive_data = quarter_data.copy()
#               is_scoring_drive = 0

#               self.driver.execute_script("arguments[0].style.border='3px solid red'", drive)

#               drive_parent_webelement = wait.until(child_element_to_be_present(drive, (By.XPATH, "./div/div/div[2]/div/div")))

#               drive_child_webelements = num_child_webelements_check(drive_parent_webelement, (By.XPATH, "./*"), 1, 5)

#               # All non scoring drives will only have 1 webelement.
#               if (len(drive_child_webelements) > 1):
#                 is_scoring_drive = 1

#               drive_button = drive_child_webelements[0]

#               # ['Team with possession']
#               try:
#                 team_with_possession_webelement = wait.until(child_element_to_be_present(drive_button, (By.XPATH, "./div/div/div/div/div/img")))
#                 self.driver.execute_script("arguments[0].style.border='3px solid red'", team_with_possession_webelement)
#                 team_with_possession_webelement_src = team_with_possession_webelement.get_attribute('src')
#                 team_with_possession = team_with_possession_webelement_src[team_with_possession_webelement_src.rindex("/") + 1::]
#               except:
#                 team_with_possession = None

#               self.driver.execute_script("arguments[0].scrollIntoView(); arguments[0].click();", drive_button)

#               # ['Drive # in Quarter', 'Team that has possession during drive', 'is it a scoring drive']
#               drive_data.extend([len(drives), team_with_possession, is_scoring_drive])

#               # Scoring drives have more than 1 'div' webelement
#               if (is_scoring_drive):
#                 drive_plays = wait.until(child_element_to_be_present(drive, (By.XPATH, "./div/div/div[2]/div/div/div[2]")))
#               else:
#                 drive_plays = wait.until(child_element_to_be_present(drive, (By.XPATH, "./div/div/div[2]/div/div/div")))

              
#               # I need to clean this up because this is ugly. <<<<<<<<<<<<<
#               # I guess create a check here to see if there are actually plays within the drive.
#               try:
#                 wait.until(child_element_to_be_present(drive_plays, (By.XPATH, "./div")))
#                 every_play_in_drive = num_child_webelements_check(drive_plays, (By.XPATH, "./div"), 0, 5)
#               except:
#                 every_play_in_drive = []
#                 continue

#               # Loop through every play of the drive
#               plays = [] # Keep count of how many plays in drive
#               for play in every_play_in_drive:
#                 plays.append(play)
                
#                 play_data = drive_data.copy()
#                 is_scoring_play = 0
                
#                 self.driver.execute_script("arguments[0].style.border='3px solid red'", play)
                
#                 # ['is it a scoring play']
#                 if(is_scoring_drive and len(plays) == len(every_play_in_drive)):
#                   is_scoring_play = 1
                
#                 play_outcome_webelement = wait.until(child_element_to_be_present(play, (By.XPATH, "./div/div/div/div/div/div/div[1]/div")))
#                 play_outcome = play_outcome_webelement.text
                
#                 play_description = wait.until(child_element_to_be_present(play, (By.XPATH, "./div/div/div/div/div/div/div[2]")))
#                 play_description = play_description.text

#                 play_start = wait.until(child_element_to_be_present(play, (By.XPATH, "./div/div/div/div/div/div/div[3]")))
#                 play_start = play_start.text

#                 # ['Play number in drive', 'is scoring play', 'play_outcome', 'play_description', 'play_start']
#                 play_data.extend([len(plays), is_scoring_play, play_outcome, play_description, play_start])

#                 df_week_plays.loc[len(df_week_plays)] = play_data

#                 print(play_data)

#       except NoSuchElementException:
#         print("No Such Element")
    
#     return df_week_plays





# # Version 2 (For updated website) (August 2025)
# ##################################################################################
# #                                                                                #
# #          METHODS THAT EXTRACT PLAY BY PLAY DATA FROM GAME WEBELEMENTS          #
# #                                                                                #
# ##################################################################################


#   """
#   PURPOSE:
#     - Extract each play that happened in each game within a specified season and week
#   INPUT PARAMETERS:
#     chosen_year - string - user chooses a season which happens to be all in years
#     chosen_week - string - user chooses a week within a given season
#   RETURN:
#     df_week_plays - Dataframe - contains all data for outcomes of each game webelement
#   """
#   def get_game_week_play_by_play(self, chosen_year, chosen_week):

#     wait = WebDriverWait(self.driver, 20)

#     # Return Dataframe
#     df_week_plays = pd.DataFrame(columns=['Season', 'Week', 'Day', 'Date', 'AwayTeam', 'HomeTeam', 
#                                           'Quarter', 
#                                           'DriveNumber', 'TeamWithPossession', 'IsScoringDrive',
#                                           'PlayNumberInDrive', 'IsScoringPlay', 'PlayOutcome', 'PlayStart', 'PlayTimeFormation', 'PlayDescription'])

#     """
#     PURPOSE:
#       - A double check to see if all child webelements have been found within a parent webelement
#     INPUT PARAMETERS:
#        parent_webelement - webelement - contains a webelement encapsulating either every quarter of a game or every drive within a quarter
#                  locator -   tuple    - A shared path from the parent webelement to the child webelements
#       num_elements_check -    int     - The least amount of child elements expected to be found
#          accuracy_number -    int     - the amount of times the method has to find the same number of child webelements consecutively
#     RETURN:
#              webelements -    list    - All specified child webelements under parent webelement
#     """
#     def num_child_webelements_check(parent_webelement, locator, num_elements_check, accuracy_number):
#       total = 0
#       array = [np.nan]
#       while( total % array[0] != 0 ):
#         total = 0
#         array = []
#         for i in range(0, accuracy_number,1):
#           webelements = wait.until(enough_child_elements_present(parent_webelement, (locator), num_elements_check))
#           total += len(webelements)
#           array.append(len(webelements))
#       return webelements
    
#     # get_parsed_game_week_webelements[0] -> returns all webelements of games that were played during the specified week
#     game_week_webelements = self.get_parsed_game_week_webelements(chosen_year, chosen_week)[0]



#     ###########################
#     # LOOP THROUGH EVERY GAME #
#     ###########################
#     for i in range(len(game_week_webelements)):

#       # This is necessary because these webelements seem to change when you move forward and backward through pages
#       game = self.get_parsed_game_week_webelements(chosen_year,chosen_week)[0][i]

#       try:
          
#           # ['Year', 'Week']
#           game_info = [chosen_year, chosen_week]

#           # Locating game button to 
#           # 1. Use as parent element to grab "game_info"
#           # 2. Click to get to "play_by_play_data"
#           game_button_webelement = wait.until(child_element_to_be_present(game, (By.XPATH, "./div/div/button")))

#           self.driver.execute_script("arguments[0].style.border='3px solid red'", game_button_webelement)

#           # ['Day', 'Date']
#           game_date_webelement = wait.until(child_element_to_be_present(game_button_webelement, (By.XPATH, "./div/div[1]")))
#           self.driver.execute_script("arguments[0].style.border='3px solid red'", game_date_webelement)
#           game_date = game_date_webelement.text.split()
#           game_info.extend(game_date[2::])

#           # ['Away Team', 'Home Team']
#           game_team_scores_webelement = wait.until(child_element_to_be_present(game_button_webelement, (By.XPATH, "./div/div[2]")))
#           self.driver.execute_script("arguments[0].style.border='3px solid red'", game_team_scores_webelement)
#           game_team_scores_data = game_team_scores_webelement.text.split()

#           team_names_data = [] # list for team names ['Away Team', 'Home Team']
#           multi_word_team_name = [] # Used for the rare case of a team having multiple strings within their name.
#           # Loop will receive list somewhat like:
#           # ['AwayTeam', 'AwayRecord', 'AwayScore', 'HomeTeam', 'HomeRecord', 'HomeScore']
#           # Rarely loop will receive list like:
#           # ['AwayTeam First half of name', 'AwayTeam Second half of name', 'AwayRecord', 'AwayScore', 'HomeTeam', 'HomeRecord', 'HomeScore']
#           # Either way we want to get list to be like:
#           # ['Away Team', 'Home Team']
#           while(len(game_team_scores_data) != 0):
#             if (game_team_scores_data[0].count("-") > 0 or game_team_scores_data[0].isdigit()):
#               if len(multi_word_team_name) > 0:
#                   team_names_data.append(" ".join(multi_word_team_name))
#                   multi_word_team_name.clear()
#               game_team_scores_data.pop(0)
#               continue
#             else:
#               multi_word_team_name.append(game_team_scores_data[0])
#               game_team_scores_data.pop(0)
#               continue
            
#           # game_details = ['Year', 'Week', 'Day', 'Date', 'Away Team', 'Home Team']]
#           game_info.extend(team_names_data)

#           # Scroll into view and click using JavaScript
#           self.driver.execute_script("arguments[0].scrollIntoView(); arguments[0].click();", game_button_webelement)

#           # UPDATE for newly updated website (August 2025)



#           # Need to figure out orientation of webpage.
#           # - Although all games have the similar page setup, some game pages are oriented different than others.
#           orientation_webelement = wait.until(
#             EC.presence_of_element_located((By.XPATH, "/html/body/div/main/div[2]/div/div/section[2]/div/div/button[1]"))
#           )
#           print(orientation_webelement.get_attribute("id"))

#           # Wrapper webelement containing all plays, separated by quarters and drives
#           game_parent_webelement = wait.until(
#             EC.presence_of_element_located((By.XPATH, "/html/body/div/main/div[2]/div/div/section[2]/div/div[2]/div/div/div/section/div"))
#           )
#           self.driver.execute_script("arguments[0].style.border='3px solid red'", game_parent_webelement)



#           # I need to create 2 separate methods of mining for plays.
#           # - One method is a regular method of grabbing plays
#           # - Two method is a reversed method of grabbing plays



#           # Button webelement that changes the state of the wrapper webelement to display all drives within game
#           all_drives_button_webelement = wait.until(
#             child_element_to_be_present(game_parent_webelement, (By.XPATH, "./div/div/button[2]"))
#           )
#           # self.driver.execute_script("arguments[0].scrollIntoView(); arguments[0].click();", all_drives_button_webelement)

#           if orientation_webelement.get_attribute("id") == 'live':
#             # print('YES')
#             self.driver.execute_script("arguments[0].scrollIntoView()", all_drives_button_webelement)
#           else:
#             # print('NO')
#             self.driver.execute_script("arguments[0].scrollIntoView(); arguments[0].click();", all_drives_button_webelement)






#           # Highlights the dropdown menu that changes the state of the wrapper webelement to display a specified quarter of the game.
#           quarter_dropdown_menu_webelement = wait.until(
#             child_element_to_be_present(game_parent_webelement, (By.XPATH, "./div/div[2]/div/div/select"))
#           )
#           self.driver.execute_script("arguments[0].style.border='3px solid red'", quarter_dropdown_menu_webelement)

#           # Creates list containing all available options of quarters within the game
#           list_quarter_dropdown_menu_options = wait.until(
#             get_dropdown_options((By.CSS_SELECTOR, 'select[aria-label="Quarter"]'))
#           )

#           ######################################
#           # LOOP THROUGH EVERY QUARTER IN GAME #
#           ######################################
#           for quarter in list_quarter_dropdown_menu_options:

#             # Select quarter of the game ato display all drives
#             wait.until(dropdown_search_and_select((By.CSS_SELECTOR, 'select[aria-label="Quarter"]'), quarter))

#             # Data up to the quarter of the game
#             quarter_data = game_info.copy()

#             # ['Quarter #']
#             quarter_data.extend([quarter])

#             every_drive_in_quarter = num_child_webelements_check(game_parent_webelement, (By.XPATH, "./div/div/div/div[2]/div"), 1, 5)

#             #######################################
#             # LOOP THROUGH EVERY DRIVE IN QUARTER #
#             #######################################
#             drive_count_in_quarter = 0
#             for drive in every_drive_in_quarter:
              
#               # Data collected up until the drive of the quarter
#               drive_data = quarter_data.copy()

#               drive_count_in_quarter += 1
#               is_scoring_drive = 0

#               self.driver.execute_script("arguments[0].style.border='3px solid red'", drive)

#               # Grabbing drive outcome to see if it is a scoring drive
#               drive_outcome_webelement = wait.until(
#                 child_element_to_be_present(drive, (By.XPATH, "./button/div/div"))
#               )
#               self.driver.execute_script("arguments[0].style.border='3px solid red'", drive_outcome_webelement)
              
#               # if (drive_outcome_webelement.text == 'Touchdown'):
#               #   is_scoring_drive = 1
#               if drive_outcome_webelement.text in ("Field Goal", "Touchdown"):
#                 is_scoring_drive = 1

#               # ['Team with possession']
#               team_with_possession_image_webelement = wait.until(
#                 child_element_to_be_present(drive_outcome_webelement, (By.XPATH, "./img"))
#               )
#               self.driver.execute_script("arguments[0].style.border='3px solid red'", team_with_possession_image_webelement)
#               team_with_possession_image_alt = team_with_possession_image_webelement.get_attribute('alt')

#               # ['Drive # in Quarter', 'Team that has possession during drive', 'is it a scoring drive']
#               print(drive_count_in_quarter)
#               drive_data.extend([drive_count_in_quarter, team_with_possession_image_alt, is_scoring_drive])

#               # Open drive to display all plays
#               drive_button_webelement = wait.until(
#                 child_element_to_be_present(drive, (By.XPATH, "./button"))
#               )
#               self.driver.execute_script("arguments[0].scrollIntoView(); arguments[0].click();", drive_button_webelement)

#               # highlight container for all plays
#               plays_container_webelement = wait.until(
#                 child_element_to_be_present(drive, (By.XPATH, "./div"))
#               )
#               self.driver.execute_script("arguments[0].style.border='3px solid red'", plays_container_webelement)
              
#               # Check to see if plays were found in drive webelement.
#               # - Sometimes no plays within drives are posted. This does not mean that they did not happen, it means
#               #   that they have not been posted.
#               try:
#                 wait.until(child_element_to_be_present(plays_container_webelement, (By.XPATH, "./div")))
#                 every_play_in_drive = num_child_webelements_check(plays_container_webelement, (By.XPATH, "./div"), 0, 5)
#               except:
#                 every_play_in_drive = []
#                 continue

#               ####################################
#               # LOOP THROUGH EVERY PLAY IN DRIVE #
#               ####################################
#               play_count_in_drive = 0
#               for play in every_play_in_drive:

#                 # Data collected up to drive data
#                 play_data = drive_data.copy()

#                 play_count_in_drive += 1
#                 is_scoring_play = 0

#                 self.driver.execute_script("arguments[0].style.border='3px solid red'", play)

#                 play_outcome_and_start_webelements = num_child_webelements_check(play, (By.XPATH, "./div[1]/div"), 0, 5)
#                 texts = [child.text for child in play_outcome_and_start_webelements if child.text.strip()]

#                 # This is where it is buggy. Will break down occasionally

#                 play_outcome = texts[0]
#                 if play_outcome in ("Field Goal", "Touchdown", "Extra Point"):
#                   is_scoring_play = 1

#                 if len(texts) == 2:
#                   play_start = texts[1]
#                 else:
#                   play_start = ''

#                 play_formation_and_description_webelements =  num_child_webelements_check(play, (By.XPATH, "./div[2]/span"), 0, 5)
#                 texts = [child.text for child in play_formation_and_description_webelements if child.text.strip()]

#                 play_time_and_formation = texts[0]
#                 play_description = texts[1]

#                 # ['Play number in drive', 'is scoring play', 'play_outcome', 'play_start', 'play_time_and_formation', 'play_description']
#                 play_data.extend([play_count_in_drive, is_scoring_play, play_outcome, play_start, play_time_and_formation, play_description])

#                 # ADD INDIVIDUAL PLAY TO DATAFRAME OF PLAYS FOR THE WEEK
#                 df_week_plays.loc[len(df_week_plays)] = play_data

#                 print(play_data)

#       except NoSuchElementException:
#         print("No Such Element")
    
#     return df_week_plays





# Version 3 (For updated website) (August 2025) (& Error catching)
##################################################################################
#                                                                                #
#          METHODS THAT EXTRACT PLAY BY PLAY DATA FROM GAME WEBELEMENTS          #
#                                                                                #
##################################################################################


  """
  PURPOSE:
    - Extract each play that happened in each game within a specified season and week
  INPUT PARAMETERS:
    chosen_year - string - user chooses a season which happens to be all in years
    chosen_week - string - user chooses a week within a given season
  RETURN:
    df_week_plays - Dataframe - contains all data for outcomes of each game webelement
  """
  def get_game_week_play_by_play(self, chosen_year, chosen_week):

    wait = WebDriverWait(self.driver, 20)

    # Return Dataframe
    df_week_plays = pd.DataFrame(columns=['Season', 'Week', 'Day', 'Date', 'AwayTeam', 'HomeTeam', 
                                          'Quarter', 
                                          'DriveNumber', 'TeamWithPossession', 'IsScoringDrive',
                                          'PlayNumberInDrive', 'IsScoringPlay', 'PlayOutcome', 'PlayStart', 'PlayTimeFormation', 'PlayDescription'])

    """
    PURPOSE:
      - A double check to see if all child webelements have been found within a parent webelement
    INPUT PARAMETERS:
       parent_webelement - webelement - contains a webelement encapsulating either every quarter of a game or every drive within a quarter
                 locator -   tuple    - A shared path from the parent webelement to the child webelements
      num_elements_check -    int     - The least amount of child elements expected to be found
         accuracy_number -    int     - the amount of times the method has to find the same number of child webelements consecutively
    RETURN:
             webelements -    list    - All specified child webelements under parent webelement
    """
    def num_child_webelements_check(parent_webelement, locator, num_elements_check, accuracy_number):
      total = 0
      array = [np.nan]
      while( total % array[0] != 0 ):
        total = 0
        array = []
        for i in range(0, accuracy_number,1):
          webelements = wait.until(enough_child_elements_present(parent_webelement, (locator), num_elements_check))
          total += len(webelements)
          array.append(len(webelements))
      return webelements
    



    def clean_game(game_info, game_webelement):

      df_game_plays = pd.DataFrame(columns=['Season', 'Week', 'Day', 'Date', 'AwayTeam', 'HomeTeam', 
                                            'Quarter', 
                                            'DriveNumber', 'TeamWithPossession', 'IsScoringDrive',
                                            'PlayNumberInDrive', 'IsScoringPlay', 'PlayOutcome', 'PlayStart', 'PlayTimeFormation', 'PlayDescription'])

      # UPDATE for newly updated website (August 2025)



      # Need to figure out orientation of webpage.
      # - Although all games have the similar page setup, some game pages are oriented different than others.
      orientation_webelement = wait.until(
        EC.presence_of_element_located((By.XPATH, "/html/body/div/main/div[2]/div/div/section[2]/div/div/button[1]"))
      )
      print(orientation_webelement.get_attribute("id"))

      # Wrapper webelement containing all plays, separated by quarters and drives
      game_parent_webelement = wait.until(
        EC.presence_of_element_located((By.XPATH, "/html/body/div/main/div[2]/div/div/section[2]/div/div[2]/div/div/div/section/div"))
      )
      self.driver.execute_script("arguments[0].style.border='3px solid red'", game_parent_webelement)



      # I need to create 2 separate methods of mining for plays.
      # - One method is a regular method of grabbing plays
      # - Two method is a reversed method of grabbing plays



      # Button webelement that changes the state of the wrapper webelement to display all drives within game
      all_drives_button_webelement = wait.until(
        child_element_to_be_present(game_parent_webelement, (By.XPATH, "./div/div/button[2]"))
      )
      # self.driver.execute_script("arguments[0].scrollIntoView(); arguments[0].click();", all_drives_button_webelement)

      if orientation_webelement.get_attribute("id") == 'live':
        # print('YES')
        self.driver.execute_script("arguments[0].scrollIntoView()", all_drives_button_webelement)
      else:
        # print('NO')
        self.driver.execute_script("arguments[0].scrollIntoView(); arguments[0].click();", all_drives_button_webelement)






      # Highlights the dropdown menu that changes the state of the wrapper webelement to display a specified quarter of the game.
      quarter_dropdown_menu_webelement = wait.until(
        child_element_to_be_present(game_parent_webelement, (By.XPATH, "./div/div[2]/div/div/select"))
      )
      self.driver.execute_script("arguments[0].style.border='3px solid red'", quarter_dropdown_menu_webelement)

      # Creates list containing all available options of quarters within the game
      list_quarter_dropdown_menu_options = wait.until(
        get_dropdown_options((By.CSS_SELECTOR, 'select[aria-label="Quarter"]'))
      )

      ######################################
      # LOOP THROUGH EVERY QUARTER IN GAME #
      ######################################
      for quarter in list_quarter_dropdown_menu_options:

        # Select quarter of the game ato display all drives
        wait.until(dropdown_search_and_select((By.CSS_SELECTOR, 'select[aria-label="Quarter"]'), quarter))

        # Data up to the quarter of the game
        quarter_data = game_info.copy()

        # ['Quarter #']
        quarter_data.extend([quarter])

        every_drive_in_quarter = num_child_webelements_check(game_parent_webelement, (By.XPATH, "./div/div/div/div[2]/div"), 1, 5)

        #######################################
        # LOOP THROUGH EVERY DRIVE IN QUARTER #
        #######################################
        drive_count_in_quarter = 0
        for drive in every_drive_in_quarter:
          
          # Data collected up until the drive of the quarter
          drive_data = quarter_data.copy()

          drive_count_in_quarter += 1
          is_scoring_drive = 0

          self.driver.execute_script("arguments[0].style.border='3px solid red'", drive)

          # Grabbing drive outcome to see if it is a scoring drive
          drive_outcome_webelement = wait.until(
            child_element_to_be_present(drive, (By.XPATH, "./button/div/div"))
          )
          self.driver.execute_script("arguments[0].style.border='3px solid red'", drive_outcome_webelement)
          
          # if (drive_outcome_webelement.text == 'Touchdown'):
          #   is_scoring_drive = 1
          if drive_outcome_webelement.text in ("Field Goal", "Touchdown"):
            is_scoring_drive = 1

          # ['Team with possession']
          team_with_possession_image_webelement = wait.until(
            child_element_to_be_present(drive_outcome_webelement, (By.XPATH, "./img"))
          )
          self.driver.execute_script("arguments[0].style.border='3px solid red'", team_with_possession_image_webelement)
          team_with_possession_image_alt = team_with_possession_image_webelement.get_attribute('alt')

          # ['Drive # in Quarter', 'Team that has possession during drive', 'is it a scoring drive']
          print(drive_count_in_quarter)
          drive_data.extend([drive_count_in_quarter, team_with_possession_image_alt, is_scoring_drive])

          # Open drive to display all plays
          drive_button_webelement = wait.until(
            child_element_to_be_present(drive, (By.XPATH, "./button"))
          )
          self.driver.execute_script("arguments[0].scrollIntoView(); arguments[0].click();", drive_button_webelement)

          # highlight container for all plays
          plays_container_webelement = wait.until(
            # child_element_to_be_present(drive, (By.XPATH, "./div"))
            child_element_to_be_present(drive, (By.XPATH, "./ul"))
          )
          self.driver.execute_script("arguments[0].style.border='3px solid red'", plays_container_webelement)
          
          # Check to see if plays were found in drive webelement.
          # - Sometimes no plays within drives are posted. This does not mean that they did not happen, it means
          #   that they have not been posted.
          try:
            # wait.until(child_element_to_be_present(plays_container_webelement, (By.XPATH, "./div")))
            wait.until(child_element_to_be_present(plays_container_webelement, (By.XPATH, "./li")))
            # every_play_in_drive = num_child_webelements_check(plays_container_webelement, (By.XPATH, "./div"), 0, 5)
            every_play_in_drive = num_child_webelements_check(plays_container_webelement, (By.XPATH, "./li"), 0, 5)
          except:
            every_play_in_drive = []
            continue

          ####################################
          # LOOP THROUGH EVERY PLAY IN DRIVE #
          ####################################
          play_count_in_drive = 0
          for play in every_play_in_drive:

            # Data collected up to drive data
            play_data = drive_data.copy()

            play_count_in_drive += 1
            is_scoring_play = 0

            self.driver.execute_script("arguments[0].style.border='3px solid red'", play)

            play_outcome_and_start_webelements = num_child_webelements_check(play, (By.XPATH, "./div[1]/div"), 0, 5)
            texts = [child.text for child in play_outcome_and_start_webelements if child.text.strip()]

            # This is where it is buggy. Will break down occasionally

            play_outcome = texts[0]
            if play_outcome in ("Field Goal", "Touchdown", "Extra Point"):
              is_scoring_play = 1

            if len(texts) == 2:
              play_start = texts[1]
            else:
              play_start = ''

            play_formation_and_description_webelements =  num_child_webelements_check(play, (By.XPATH, "./div[2]/span"), 0, 5)
            texts = [child.text for child in play_formation_and_description_webelements if child.text.strip()]

            play_time_and_formation = texts[0]
            play_description = texts[1]

            # ['Play number in drive', 'is scoring play', 'play_outcome', 'play_start', 'play_time_and_formation', 'play_description']
            play_data.extend([play_count_in_drive, is_scoring_play, play_outcome, play_start, play_time_and_formation, play_description])

            # ADD INDIVIDUAL PLAY TO DATAFRAME OF PLAYS FOR THE WEEK
            df_game_plays.loc[len(df_game_plays)] = play_data

            print(play_data)

      return df_game_plays
    


    # get_parsed_game_week_webelements[0] -> returns all webelements of games that were played during the specified week
    game_week_webelements = self.get_parsed_game_week_webelements(chosen_year, chosen_week)[0]

    ###########################
    # LOOP THROUGH EVERY GAME #
    ###########################
    for i in range(len(game_week_webelements)):

      # This is necessary because these webelements seem to change when you move forward and backward through pages
      game = self.get_parsed_game_week_webelements(chosen_year,chosen_week)[0][i]

      try:

        # ['Year', 'Week']
        game_info = [chosen_year, chosen_week]

        # Locating game button to 
        # 1. Use as parent element to grab "game_info"
        # 2. Click to get to "play_by_play_data"
        game_button_webelement = wait.until(child_element_to_be_present(game, (By.XPATH, "./div/div/button")))

        self.driver.execute_script("arguments[0].style.border='3px solid red'", game_button_webelement)

        # ['Day', 'Date']
        game_date_webelement = wait.until(child_element_to_be_present(game_button_webelement, (By.XPATH, "./div/div[1]")))
        self.driver.execute_script("arguments[0].style.border='3px solid red'", game_date_webelement)
        game_date = game_date_webelement.text.split()
        game_info.extend(game_date[2::])

        # ['Away Team', 'Home Team']
        game_team_scores_webelement = wait.until(child_element_to_be_present(game_button_webelement, (By.XPATH, "./div/div[2]")))
        self.driver.execute_script("arguments[0].style.border='3px solid red'", game_team_scores_webelement)
        game_team_scores_data = game_team_scores_webelement.text.split()

        team_names_data = [] # list for team names ['Away Team', 'Home Team']
        multi_word_team_name = [] # Used for the rare case of a team having multiple strings within their name.
        # Loop will receive list somewhat like:
        # ['AwayTeam', 'AwayRecord', 'AwayScore', 'HomeTeam', 'HomeRecord', 'HomeScore']
        # Rarely loop will receive list like:
        # ['AwayTeam First half of name', 'AwayTeam Second half of name', 'AwayRecord', 'AwayScore', 'HomeTeam', 'HomeRecord', 'HomeScore']
        # Either way we want to get list to be like:
        # ['Away Team', 'Home Team']
        while(len(game_team_scores_data) != 0):
          if (game_team_scores_data[0].count("-") > 0 or game_team_scores_data[0].isdigit()):
            if len(multi_word_team_name) > 0:
                team_names_data.append(" ".join(multi_word_team_name))
                multi_word_team_name.clear()
            game_team_scores_data.pop(0)
            continue
          else:
            multi_word_team_name.append(game_team_scores_data[0])
            game_team_scores_data.pop(0)
            continue
          
        # game_details = ['Year', 'Week', 'Day', 'Date', 'Away Team', 'Home Team']]
        game_info.extend(team_names_data)

        # Scroll into view and click using JavaScript
        self.driver.execute_script("arguments[0].scrollIntoView(); arguments[0].click();", game_button_webelement)


        max_retries = 3
        attempt = 0
        while attempt < max_retries:
          try:
            
            df_plays_in_single_game = clean_game(game_info, game)

            df_week_plays = pd.concat([df_week_plays, df_plays_in_single_game], ignore_index=True)

            break

          except Exception as e:
            print(f"Attempt {attempt + 1} failed: {e}")
            attempt += 1


      except NoSuchElementException:
        print("No Such Element")

    return df_week_plays