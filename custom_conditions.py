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
        except (StaleElementReferenceException, NoSuchElementException):
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
        - This custom wait will only return true if the dropdown element is found and its options have been returned
INPUT PARAMETERS:
                    locator -  tuple  - How to find an element on a webpage. typically formatted
                                        as (By.'locator strategy', 'identifier').
RETURN:
    - list of dropdown options
"""
class get_dropdown_options(object):

    def __init__(self, locator):
        self.locator = locator

    def __call__(self, driver):
        try:
            element = driver.find_element(*self.locator)
            dropdown_webelement = Select(element)
            return [option.text for option in dropdown_webelement.options]
        except (StaleElementReferenceException, NoSuchElementException):
            return False        

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
    

    ###########################################################################################################################
    ###########################################################################################################################
    ##                                                                                                                       ##
    ##                                         METHODS FOR CHILD ELEMENTS                                                    ##
    ##                                                                                                                       ##
    ###########################################################################################################################
    ###########################################################################################################################

# These methods might be redundant

"""
PURPOSE:
    - Return true if child webelement has been found under a given parent webelement
INPUT PARAMETERS:
    parent_webelement - webelement - parent element to desired child webelement
        child_locator -    tuple   - How to find child element on a webpage relative to parent_webelement,
                                        typically formatted as (By.'locator strategy', 'identifier').
RETURN:
    - Child element if it has been found. If not, will return 'False'
"""
class child_element_to_be_present:
    def __init__(self, parent_webelement, child_locator):
        self.parent_webelement = parent_webelement
        self.child_locator = child_locator

    def __call__(self, driver):
        try:
            return self.parent_webelement.find_element(*self.child_locator)
        except (StaleElementReferenceException, NoSuchElementException):
            return False    

"""
PURPOSE
    - Will only pass if a specified amount (or more) of like child Webelements are found.
INPUT PARAMETERS:
     parent_webelement - webelement - parent element to desired child webelements
               locator -   tuple    - How to find an element on a webpage. typically formatted
                                      as (By.'locator strategy', 'identifier').
    num_elements_check -    int     - Desired number of like Webelements that need to be found 
                                      in the DOM order to pass.
RETURN:
    elements -  list   - List of all elements found with given locator at that time.
                                  - The reason why I say "at that time" is because not all 
                                    elements might have been found. 
                                    (e.g. there are 100 like elements and this method is searching
                                          for 5 or more. Anywhere from 5-100 might return.)
       False - boolean - If specified like Webelements or more are not found.
"""
class enough_child_elements_present(object):

    def __init__(self, parent_webelement, locator, num_elements_check):
        self.parent_webelement = parent_webelement
        self.locator = locator
        self.num_elements_check = num_elements_check
    
    def __call__(self, driver):
        try:
            elements = self.parent_webelement.find_elements(*self.locator)
            if len(elements) >= self.num_elements_check:
                return elements
            else:
                return False
        except (StaleElementReferenceException, NoSuchElementException):
            return False


"""
PURPOSE
    - A webelement can either be one of 2 different things.
        - This was needed while going through a list of like webelements. Depending on which
          webelement the scraper was observing, there were different parts of the webelement that needed to be checked.
INPUT PARAMETERS:
     parent_webelement  - webelement - parent element to desired child webelements
               locator1 -   tuple    - How to find an element on a webpage. typically formatted
                                       as (By.'locator strategy', 'identifier').
               locator2 -   tuple    - How to find an element on a webpage. typically formatted
                                       as (By.'locator strategy', 'identifier').
RETURN:
    - List that contains webelement that has been found and an indication of which webelement was found
    - Will return False if neither webelement was found.
NEXT ITERATION:
    - Can probably make this more flexable by creating a list of locators instead of limiting it to 2
"""
class one_or_the_other(object):

    def __init__(self, parent_webelement, locator1, locator2):
        self.parent_webelement = parent_webelement
        self.locator1 = locator1
        self.locator2 = locator2

    def __call__(self, driver):
        try:
            return [self.parent_webelement.find_element(*self.locator1), 1]
        except:
            try:
                return [self.parent_webelement.find_element(*self.locator2), 2]
            except:
                return False