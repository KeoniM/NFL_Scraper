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
        # Make sure the year is rendered before the week is searched. Without this, the DOM will mix weeks.
        wait.until(EC.presence_of_element_located((By.XPATH, "/html/body/div[3]/main/div/div/div/div/div/div/div[2]/div/div[3]")))
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
    - All webelements for games in specified week and season
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
          return self.get_game_week_webelements(chosen_year, chosen_week, max_attempts - 1)
        else:
            return print("Unable to get game week data.")

    # The first 3-4 elements to all score pages are titles and adds that are not wanted.
    if (checked_game_webelements[1].text.lower() == "final"):
       return checked_game_webelements[3::]
    elif(checked_game_webelements[1].text.lower() == "upcoming"):
       return checked_game_webelements[4::]
    else:
       return print("{} {} has not been accounted for yet. Look under 'get_game_week_webelements' and try to fix this".format(chosen_year, chosen_week))


  #############################################################################
  #                                                                           #
  #          METHODS THAT EXTRACT SCORING DATA FROM GAME WEBELEMENTS          #
  #                                                                           #
  #############################################################################
  
  """
  PURPOSE:
    - Parse out different types of game webelements 
      (games played, upcoming games, bye weeks, cancelled games)
  INPUT PARAMETERS:
     chosen_year - string - user chooses a season which happens to be all in years
     chosen_week - string - user chooses a week within a given season
  RETURN:
    - list of parsed game webelements -> [games_played, games_bye, games_cancelled, games_upcoming]
  """
  def get_parsed_game_week_webelements(self, chosen_year, chosen_week):

    game_week_webelements = self.get_game_week_webelements(chosen_year, chosen_week)

    # Lists to return
    games_played = []
    games_bye = []
    games_cancelled = []
    games_upcoming = []

    for i in game_week_webelements:
        try:
            # The closest parent element to all wanted data for game.
            game = i.find_element(By.XPATH, "./div/div/button/div")
            status_and_date = game.find_element(By.XPATH, "./div[1]")

            game_data = status_and_date.text.split()

            # The only status games that I have come across are
            # 1. Cancelled game
            # 2. Final outcome
            # 3. Upcoming games
            if game_data.count('CANCELLED') >= 1:
               games_cancelled.append(i)
            elif game_data.count('FINAL') >= 1:
               games_played.append(i)
            else:
               games_upcoming.append(i)

        except NoSuchElementException:
            # score welement not found because the webelement is a bye week
            try:
                # A check to see if the bye week is there, if not then it is a webelement that is not wanted.
                i.find_element(By.XPATH, ".//button/div[1]")
                games_bye.append(i)
                continue
            except NoSuchElementException:
                continue
 
    # print("{} {} has {} played_games, {} byes, {} cancelled games, {} upcoming games".format(chosen_year, 
    #                                                                                          chosen_week, 
    #                                                                                          len(games_played), 
    #                                                                                          len(games_bye), 
    #                                                                                          len(games_cancelled), 
    #                                                                                          len(games_upcoming)))

    return [games_played, games_bye, games_cancelled, games_upcoming]

  """
  PURPOSE:
    - Return outcomes of all games within a specified week (e.g. Final scores of a game played)
  INPUT PARAMETERS:
     chosen_year - string - user chooses a season which happens to be all in years
     chosen_week - string - user chooses a week within a given season
  RETURN:
    - df_week_scores - Dataframe - contains all data for outcomes of each game webelement
  """
  def get_game_week_scores(self, chosen_year, chosen_week):

    parsed_game_webelements = self.get_parsed_game_week_webelements(chosen_year, chosen_week)

    games_played = parsed_game_webelements[0]
    games_bye = parsed_game_webelements[1]
    games_cancelled = parsed_game_webelements[2]
    games_upcoming = parsed_game_webelements[3]

    # return dataframe
    df_week_scores = pd.DataFrame(columns=["Season", "Week", "GameStatus", "Day", "Date", 
                                    "AwayTeam", "AwayRecord", "AwayScore", "AwayWin",
                                    "HomeTeam", "HomeRecord", "HomeScore", "HomeWin",
                                    "AwaySeeding", "HomeSeeding", "PostSeason?"])
    
    """
    PURPOSE:
      - Handle "game status" data from game webelement (e.i. game type / game day / game date)
    INPUTE PARAMETERS:
      sad_webelement - webelement - status and date of individual game
           game_type - list name  - collection of game type webelemenets (e.g. list of games played within the week)
    RETURN:
      A collection of status and date data of the individual game (e.g. ['FINAL', 'SUN', '02/07'])
    """
    def get_game_status_and_date(sad_webelement, game_type):

      sad_data = sad_webelement.text.split()
      sad_data.remove("-")

      if game_type == games_played:
        return sad_data
      if game_type == games_cancelled:
       return ['CANCELLED', 'CANCELLED', 'CANCELLED']
      sad_data.insert(0, 'UPCOMING')
      return sad_data[:3:1]

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
    
    # Loop that goes through each game webelement of a specified game week
    for i in [games_played, games_upcoming, games_bye, games_cancelled]:
      if i == games_bye:
        for j in i:
          individual_game_data = []
          game = j.find_element(By.XPATH, ".//button/div[1]")
          self.driver.execute_script("arguments[0].style.border='3px solid blue'", game)
          individual_game_data += [np.nan] * 7
          game_team_data = game.text.split() # ['Name', 'Record']
          individual_game_data.insert(0, chosen_year)
          individual_game_data.insert(1, chosen_week)
          individual_game_data.insert(2, "BYE")
          individual_game_data.insert(3, None)
          individual_game_data.insert(4, None)
          individual_game_data.insert(5, game_team_data[0])
          individual_game_data.insert(6, game_team_data[1][1:len(game_team_data[1]) - 1]) # "(#-#)" -> "#-#"
          individual_game_data.insert(9, None)
          individual_game_data.append(0) # Placevalue for Postseason column. Postseason weeks do not have bye weeks displayed.
          df_week_scores.loc[len(df_week_scores)] = individual_game_data
      else:
        for j in i:
          individual_game_data = []
          game = j.find_element(By.XPATH, "./div/div/button/div")
          status_and_date_webelement = game.find_element(By.XPATH, "./div[1]")
          self.driver.execute_script("arguments[0].style.border='3px solid purple'", status_and_date_webelement)
          individual_game_data.extend(get_game_status_and_date(status_and_date_webelement, i))
          score_webelement = game.find_element(By.XPATH, "./div[2]/div")
          self.driver.execute_script("arguments[0].style.border='3px solid red'", score_webelement)
          individual_game_data.extend(get_score_data(score_webelement))
          individual_game_data.insert(0, chosen_week)
          individual_game_data.insert(0, chosen_year)
          df_week_scores.loc[len(df_week_scores)] = individual_game_data
      
    return df_week_scores


















# vvvvvvvvvvvvvvvvvvvvvvvvvvvvv METHOD INCOMPLETE vvvvvvvvvvvvvvvvvvvvvvvvvvvvv #

##################################################################################
#                                                                                #
#          METHODS THAT EXTRACT PLAY BY PLAY DATA FROM GAME WEBELEMENTS          #
#                                                                                #
##################################################################################


  def get_game_week_play_by_play(self, chosen_year, chosen_week):

    wait = WebDriverWait(self.driver, 20)

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
    
    # get_parsed_game_week_webelements[0] -> returns all webelements of games that were played during the specified week
    game_week_webelements = self.get_parsed_game_week_webelements(chosen_year, chosen_week)[0] 

    for i in range(len(game_week_webelements)):

      # Need to do this because when we enter a game and come back to the start page with all games the webelement 
      # to get to enter the next game is not exactly the same as it was even though it is in the same position.
      game = self.get_parsed_game_week_webelements(chosen_year,chosen_week)[0][i]

      try:
          
          # ['Year', 'Week']
          game_details = [chosen_year, chosen_week]

          # Locating game button to 
          # 1. Use as parent element to grab "game_details"
          # 2. Click to get to "play_by_play_data"
          game_button_webelement = wait.until(
            child_element_to_be_present(game, (By.XPATH, "./div/div/button"))
          ) 

          self.driver.execute_script("arguments[0].style.border='3px solid red'", game_button_webelement)

          # ['Day', 'Date']
          game_date_webelement = game_button_webelement.find_element(By.XPATH, "./div/div[1]")
          self.driver.execute_script("arguments[0].style.border='3px solid red'", game_date_webelement)
          game_date = game_date_webelement.text.split()
          game_details.extend(game_date[2::])

          # ['Away Team', 'Home Team']
          game_team_scores_webelement = game_button_webelement.find_element(By.XPATH, "./div/div[2]")
          self.driver.execute_script("arguments[0].style.border='3px solid red'", game_team_scores_webelement)
          game_team_scores_data = game_team_scores_webelement.text.split()

          team_names_data = [] # list for team names ['Away Team', 'Home Team']
          multi_word_team_name = [] # Used for the rare case of a team having multiple strings within their name.
          # Filter for 'game_team_scores_data'.
          # Cycle through 'game_team_scores_data' and merge side by side strings to fit in a single element within a list.
          while(len(game_team_scores_data) != 0): 
            if game_team_scores_data[0][0].isupper():
              multi_word_team_name.append(game_team_scores_data[0])
              game_team_scores_data.pop(0)
              continue
            else:
              if len(multi_word_team_name) > 0:
                team_names_data.append(" ".join(multi_word_team_name))
                multi_word_team_name.clear()
              game_team_scores_data.pop(0)
              continue

          # game_details = ['Year', 'Week', 'Day', 'Date', 'Away Team', 'Home Team']]
          game_details.extend(team_names_data)
          print(game_details)

          # Scroll into view and click using JavaScript
          self.driver.execute_script("arguments[0].scrollIntoView(); arguments[0].click();", game_button_webelement)

          # Wrapper webelement containing every quarter played
          game_parent_webelement = wait.until(
            EC.presence_of_element_located((By.ID, "all-drives-panel"))
          )

          every_quarter_in_game = num_child_webelements_check(game_parent_webelement, (By.XPATH, "./div"), 1, 5)
          
          # Loop through every quarter of the game
          for quarter in every_quarter_in_game:
            self.driver.execute_script("arguments[0].style.border='3px solid red'", quarter)
            # self.driver.execute_script("arguments[0].scrollIntoView();", quarter)
            quarter_number = quarter.find_element(By.XPATH, "./div")
            self.driver.execute_script("arguments[0].style.border='3px solid red'", quarter_number)
            # ['Quarter #']
            quarter_number = quarter_number.text

            every_drive_in_quarter = num_child_webelements_check(quarter, (By.XPATH, "./div"), 1, 5)

            # Loop through every drive of the quarter
            drives = []
            for drive in every_drive_in_quarter[1::]:

              # I need to somehow figure out who has possession each drive
              # 	https://static.www.nfl.com/f_png,q_85,h_90,w_90,c_fill,f_auto/league/api/clubs/logos/CIN
              #	  https://static.www.nfl.com/f_auto,q_85/league/api/clubs/logos/CIN

              #   https://static.www.nfl.com/f_auto,q_85/league/api/clubs/logos/HOU
              #   




              
              drive_data = game_details.copy()
              is_scoring_drive = 0

              self.driver.execute_script("arguments[0].style.border='3px solid red'", drive)
              drives.append(drive)

              drive_parent_webelement = drive.find_element(By.XPATH, "./div/div/div[2]/div/div")

              drive_child_webelements = num_child_webelements_check(drive_parent_webelement, (By.XPATH, "./*"), 1, 5)

              # All non scoring drives will only have 1 webelement.
              if (len(drive_child_webelements) > 1):
                is_scoring_drive = 1

              # ['Quarter #', 'Drive # in Quarter', 'is it a scoring drive']
              drive_data.extend([quarter_number, len(drives), is_scoring_drive])

              drive_button = drive_child_webelements[0]

              self.driver.execute_script("arguments[0].scrollIntoView(); arguments[0].click();", drive_button)

              # Scoring drives have more than 1 'div' webelement
              if (is_scoring_drive):
                drive_plays = drive.find_element(By.XPATH, "./div/div/div[2]/div/div/div[2]")
              else:
                drive_plays = drive.find_element(By.XPATH, "./div/div/div[2]/div/div/div")

              self.driver.execute_script("arguments[0].style.border='3px solid red'", drive_plays)

              every_play_in_drive = num_child_webelements_check(drive_plays, (By.XPATH, "./div"), 1, 5)

              plays = []
              for play in every_play_in_drive:
                
                play_data = drive_data.copy()
                is_scoring_play = 0
                
                self.driver.execute_script("arguments[0].style.border='3px solid red'", play)
                plays.append(play)

                # ['Play # in drive']
                play_data.extend([len(plays)])

                # ['is it a scoring play']
                if(is_scoring_drive and len(plays) == len(every_play_in_drive)):
                  is_scoring_play = 1
                play_data.extend([is_scoring_play])
                
                play_outcome_webelement = play.find_element(By.XPATH, "./div/div/div/div/div/div/div[1]/div")
                play_outcome = play_outcome_webelement.text
                play_data.append(play_outcome)
                
                play_description = play.find_element(By.XPATH, "./div/div/div/div/div/div/div[2]")
                play_description = play_description.text
                play_data.append(play_description)

                play_start = play.find_element(By.XPATH, "./div/div/div/div/div/div/div[3]")
                play_start = play_start.text
                play_data.append(play_start)

                print(play_data)

      except NoSuchElementException:
        print("No Such Element")
    
    return