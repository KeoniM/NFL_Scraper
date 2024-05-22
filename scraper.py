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

# explicit Waits
import time

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
    self.data = pd.DataFrame() # Do I really need this?

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
    - A state of the website being open to the desired season and week.
  """
  def select_year_and_week(self, chosen_year, chosen_week, max_attempts=5):
      # Check to see if driver is on scores page. If not, will open scores page.
      if(self.driver.current_url != "https://www.nfl.com/scores/"):
          self._open_nfl_scores_page()

      wait = WebDriverWait(self.driver, 20)

      try:
        wait.until(dropdown_search_and_select((By.ID, "Season"), chosen_year))
        wait.until(dropdown_search_and_select((By.ID, "Week"), chosen_week))

        # grabbing webelement containing text of which week the page is on
        week_check = wait.until(
          EC.presence_of_element_located((By.XPATH, "/html/body/div[3]/main/div/div/div/div/div/div/div/div/div/div"))
        )

        # double check to be sure that the users "chosen_week" matches the page
        if(" ".join(week_check.text.split()[2::]) == chosen_week):
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
        return print("This year/week is not an option.")


  ###########################################################################################################################
  ###########################################################################################################################
  ##                                                                                                                       ##
  ##                                       METHODS TO DISPLAY AVAILABLE OPTIONS                                            ##
  ##                                                                                                                       ##
  ###########################################################################################################################
  ###########################################################################################################################


  """
  PURPOSE:
    - Display all available NFL seasons and weeks to grab data from.
  INPUT PARAMETERS:
    max_attempts - int - maximum number of attempts to find webelements
  RETURN:
      df - dataframe - contains seasons and weeks available to gather data from.
  NOTES:
    - Not all options in 'season' dropdown is actually avaiable
    - 'Weeks' dropdown is different for almost every season
  """
  def display_seasons_and_weeks(self, max_attempts = 5):

    # Check to make sure driver is on nfl scores page.
    if(self.driver.current_url != "https://www.nfl.com/scores/"):
      self._open_nfl_scores_page()

    # Return dataframe that will contain seasons and weeks available
    df = pd.DataFrame(columns=["Season", "Weeks"])

    wait = WebDriverWait(self.driver, 10)

    try:
      # Wait until 'season' dropdown is available in the DOM and selects it.
      locate_season_webelement = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#Season")))
      select_season_webelement = Select(locate_season_webelement)

      # All available elements within 'season' dropdown placed into list.
      season_webelement_options = [option.text for option in select_season_webelement.options]

      # Finding 'Weeks' schedule for each season
      for i in season_webelement_options:
        try:
          wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#Season")))
          wait.until(dropdown_search_and_select((By.ID, "Season"), i))
          weeks_webelement = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#Week")))
          select_weeks_webelement = Select(weeks_webelement)
          weeks_webelement_options = [option.text for option in select_weeks_webelement.options]
          season_and_weeks = [i, weeks_webelement_options]
          df.loc[len(df)] = season_and_weeks
        except TimeoutException:
           continue
      return df
    
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


  """
  PURPOSE:
    - Get all game webelements in a specified week and season.
  INPUT PARAMETERS:
     chosen_year - string - user chooses a season which happens to be all in years
     chosen_week - string - user chooses a week within a given season
    max_attempts -  int   - number of errors allowed when finding webelements
  RETURN:
    - All webelements for games played in a specific week and season
  """
  def get_game_week_webelements(self, chosen_year, chosen_week, max_attempts=5):

    self.select_year_and_week(chosen_year, chosen_week)

    wait = WebDriverWait(self.driver, 5)

    # webelement that shares a classname with all webelements that contain desired data (Titles/Scores/Byes/Upcoming).
    shared_classname_webelement = wait.until(
        EC.presence_of_element_located((By.XPATH, "/html/body/div[3]/main/div/div/div/div/div/div/div"))
    )

    # the shared classname for all desired webelements
    scores_shared_classname = shared_classname_webelement.get_attribute("class")

    # Different weeks have different amounts of games displaying. (each week as a different amount of desired webelements displaying).
    num_score_elements = 19 # Week 1 - Week 17 
    if chosen_week in ["Hall Of Fame", "Pro Bowl", "Super Bowl"]:
        num_score_elements = 4
    elif chosen_week in ["Conference Championships"]:
        num_score_elements = 5
    elif chosen_week in ["Divisional Playoffs", "Wild Card Weekend"]:
        num_score_elements = 7

    # A measure to ensure that all games (webelements) were captured
    # NOTE: an issue that I have been running into is that the scraper will grab all webelements that 
    #       are currently displaying in the DOM but that does not necessarily mean that all of the
    #       webelements are displayed at that time. This is the method that I came up with to combat 
    #       that issue.
    try:
        # If same number of webelements are grabbed 5 times in a row, then that is likely the amount of game webelements available for that week
        total = 0
        array = [np.nan]
        while( total % array[0] != 0):
          total = 0
          array = []
          for i in range(0,5,1):
            game_webelements = wait.until(enough_elements_present((By.CLASS_NAME, scores_shared_classname), num_score_elements))
            total += len(game_webelements)
            array.append(len(game_webelements))

        checked_game_webelements = game_webelements

    except TimeoutException:
        if (max_attempts > 0):
          print("SEARCHING, attempting {} more times (get game week data)".format(max_attempts))
          return self.get_game_week_data(chosen_year, chosen_week, max_attempts - 1)
        else:
            return print("Unable to get game week data.")

    # The first 3 elements to all score pages are titles and adds that are not wanted.
    clean_checked_game_webelements = checked_game_webelements[3::]

    return clean_checked_game_webelements


  #####################################################################
  #                                                                   #
  #          METHODS THAT EXTRACT DATA FROM GAME WEBELEMENTS          #
  #                                                                   #
  #####################################################################  


  """
  PURPOSE:
    - Retreive all outcome data from game webelements (final scores/ bye weeks/ canceled games / upcoming games)
  INPUT PARAMETERS:
     chosen_year - string - user chooses a season which happens to be all in years
     chosen_week - string - user chooses a week within a given season
  RETURN:
    - All game outcomes for a specified week loaded into class dataframe. (scores/byes/canceled/upcoming)
  NOTE: Helper methods are located within this method to handle different game webelements.
        Decided to do this because there wont be any other method using these helper methods
        except for this method here.
  """
  def get_game_week_scores(self, chosen_year, chosen_week):

    game_week_webelements = self.get_game_week_webelements(chosen_year, chosen_week)

    # return dataframe
    df_week_scores = pd.DataFrame(columns=["Season", "Week", "GameStatus", "Day", "Date", 
                                    "AwayTeam", "AwayRecord", "AwayScore", "AwayWin",
                                    "HomeTeam", "HomeRecord", "HomeScore", "HomeWin",
                                    "AwaySeeding", "HomeSeeding", "PostSeason?"])

    """
    PURPOSE: 
      - Handle "status and date" data from game webelement 
    INPUT PARAMETERS:
      sad_webelement - webelement - contains status and date of game
    RETURN:
      sad_data - list - contains ['Game Status', 'Game Day', 'Game Date']
    """
    def get_game_status_and_date(sad_webelement):

      # text data within webelement
      sad_data = sad_webelement.text.split()

      if sad_data.count('CANCELLED') >= 1:
          return ['CANCELLED', 'CANCELLED', 'CANCELLED']

      sad_data.remove("-")

      return sad_data

    """
    PURPOSE: 
      - Handle "scores" data from game webelement (e.i. game played / game cancelled / bye week)
    INPUT PARAMETERS:
      scores_webelement - webelement - contains scores data of game
    RETURN:
      organized_game_data - list - contains organized data that breaks down the game contained in webelement.
    """
    def get_score_data(scores_webelement):

      # text data within webelement.
      scores_data = scores_webelement.text.split()
      
      # Variables to be filled with 'scores_data' and returned in a list
      away_team_name = None
      home_team_name = None
      away_record = np.nan
      home_record = np.nan
      away_score = 0
      home_score = 0
      away_win = 0
      home_win = 0
      away_seeding = np.nan
      home_seeding = np.nan
      is_postseason = 0

      clean_scores_data = [] # list for filtered and cleaned 'scores_data'
      multi_word_team_name = [] # Used for the rare case of a team having multiple strings within their name.

      # Filter for 'scores_data'.
      # Cycle through 'scores_data' and merge side by side strings to fit in a single element within a list.
      while(len(scores_data) != 0): 
        if scores_data[0][0].isupper():
          multi_word_team_name.append(scores_data[0])
          scores_data.pop(0)
          continue
        else:
          if len(multi_word_team_name) > 0:
            clean_scores_data.append(" ".join(multi_word_team_name))
            multi_word_team_name.clear()
          clean_scores_data.append(scores_data[0])
          scores_data.pop(0)
          continue

      # Data is symmetrical. Split evenly between away and home team
      data_split = int(len(clean_scores_data)/2)
      away_team = clean_scores_data[:data_split:]
      home_team = clean_scores_data[data_split::]

      # Postseason check 
      if(away_team[0].isnumeric()):
        is_postseason = 1
        away_seeding = away_team[0]
        home_seeding = home_team[0]
        away_team.pop(0)
        home_team.pop(0)

      # Team Names
      away_team_name = away_team[0]
      home_team_name = home_team[0]
      away_team.pop(0)
      home_team.pop(0)

      # Game scores AND team records (special cases will have one or the other)
      while(len(away_team) > 0):
        if(away_team[0].isnumeric()):
          away_score = away_team[0]
          home_score = home_team[0]
        else:
          away_record = away_team[0]
          home_record = home_team[0]
        away_team.pop(0)
        home_team.pop(0)

      # Team win check
      if(int(away_score) > int(home_score)):
        away_win = 1
        home_win = 0
      elif(int(away_score) < int(home_score)):
        away_win = 0
        home_win = 1
      
      oganized_game_data = [away_team_name, away_record, away_score, away_win,
                            home_team_name, home_record, home_score, home_win,
                            away_seeding, home_seeding, is_postseason]
      
      return oganized_game_data


    for i in game_week_webelements:
        try:
            # The closest parent element to all wanted data for game.
            game = i.find_element(By.XPATH, "./div/div/button/div")

            # Status and date of game broken down and organized.
            status_and_date_webelement = game.find_element(By.XPATH, "./div[1]")
            self.driver.execute_script("arguments[0].style.border='3px solid red'", status_and_date_webelement)
            sad_data = get_game_status_and_date(status_and_date_webelement)

            # score of game broken down and organized. 
            score_webelement = game.find_element(By.XPATH, "./div[2]/div")
            self.driver.execute_script("arguments[0].style.border='3px solid red'", score_webelement)
            score_data = get_score_data(score_webelement)

            # ['Season', 'Week', Status and Date Data, Score Data]
            sad_data.extend(score_data)
            sad_data.insert(0, chosen_week)
            sad_data.insert(0, chosen_year)

            df_week_scores.loc[len(df_week_scores)] = sad_data

        except NoSuchElementException:
            # score welement not found because the webelement is a bye week
            try:
                bye = i.find_element(By.XPATH, ".//button/div[1]")
                self.driver.execute_script("arguments[0].style.border='3px solid red'", bye)
                bye_week = [np.nan] * 7
                bye_data = bye.text.split() # ['Name', 'Record']
                bye_week.insert(0, chosen_year)
                bye_week.insert(1, chosen_week)
                bye_week.insert(2, "BYE")
                bye_week.insert(3, None)
                bye_week.insert(4, None)
                bye_week.insert(5, bye_data[0])
                bye_week.insert(6, bye_data[1][1:len(bye_data[1]) - 1]) # "(#-#)" -> "#-#"
                bye_week.insert(9, None)
                bye_week.append(0) # Placevalue for Postseason column. Postseason weeks do not have bye weeks displayed.
                df_week_scores.loc[len(df_week_scores)] = bye_week
                continue
            except NoSuchElementException:
                continue

    return df_week_scores