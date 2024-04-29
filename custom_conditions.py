from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import NoSuchElementException

# For METHODS FOR DROPDOWN MENUS
from selenium.webdriver.support.ui import Select
 

##############################################################
# EVERY OBJECT IN THIS MODULE IS A CUSTOM "CONDITION OBJECT" #
# FOR Selenium WebDriverWait METHOD 'until()'.               #
##############################################################


    ###########################################################################################################################
    ###########################################################################################################################
    ##                                                                                                                       ##
    ##                                   METHODS FOR ELEMENTS WITH LIKE IDENTIFIERS                                          ##
    ##                                                                                                                       ##
    ###########################################################################################################################
    ###########################################################################################################################


"""
PURPOSE
    - Will only pass if a specified amount (or more) of like Webelements are found.
INPUT PARAMETERS:
               locator -  tuple  - How to find an element on a webpage. typically formatted
                                   as (By.'locator strategy', 'identifier').
    num_elements_check -   int   - Desired number of like Webelements that need to be found 
                                   in the DOM order to pass.
RETURN:
    elements -  list   - List of all elements found with given locator at that time.
                                  - The reason why I say "at that time" is because not all 
                                    elements might have been found. 
                                    (e.g. there are 100 like elements and this method is searching
                                          for 5 or more. Anywhere from 5-100 might return.)
       False - boolean - If specified like Webelements or more are not found.
"""
class enough_elements_present(object):

    def __init__(self, locator, num_elements_check):
        self.locator = locator
        self.num_elements_check = num_elements_check
    
    def __call__(self, driver):
        try:
            elements = driver.find_elements(*self.locator)
            if len(elements) >= self.num_elements_check:
                return elements
            else:
                return False
        except [StaleElementReferenceException, NoSuchElementException]:
            return False


    ###########################################################################################################################
    ###########################################################################################################################
    ##                                                                                                                       ##
    ##                                         METHODS FOR DROPDOWN MENUS                                                    ##
    ##                                                                                                                       ##
    ###########################################################################################################################
    ###########################################################################################################################


"""
PURPOSE:
    - An attempt to adjust to dynamic dropdown webelements.
        - This custom wait will only return true if the dropdown element is found and if the desired selected option has been selected
INPUT PARAMETERS:
                    locator -  tuple  - How to find an element on a webpage. typically formatted
                                        as (By.'locator strategy', 'identifier').
    dropdown_desired_option - string  - dropdown option that user would like to be selected
RETURN:
    - State in which the dropdown option has been selected for specified dropdown webelement.
"""
class dropdown_search_and_select(object):

    def __init__(self, locator, dropdown_desired_option):
        self.locator = locator
        self.dropdown_desired_option = dropdown_desired_option

    def __call__(self, driver):
        try:
            element = driver.find_element(*self.locator)
            select_option = Select(element)
            select_option.select_by_visible_text(self.dropdown_desired_option)
            return select_option.first_selected_option.text == self.dropdown_desired_option
        except (StaleElementReferenceException, NoSuchElementException):
            return False
    
