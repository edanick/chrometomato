#region imports
from selenium import webdriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pathlib import Path
from enum import Enum
import yaml, time
from typing import Union, List, Type
#endregion

class sm(Enum):
    CLASS = By.CLASS_NAME
    ID = By.ID
    NAME = By.NAME
    CSS_SELECTOR = By.CSS_SELECTOR
    XPATH = By.XPATH

class Chrome():

    def __init__(self, options: Union[str, List[str]], cookies: str, cookies_domain: str, default_url: str = 'about:blank', driver: Type[webdriver.Chrome] = webdriver.Chrome):

        _options = Options()

        if isinstance(options, list) and all(type(i) == str for i in options):
            [_options.add_argument(option) for option in options]
        else:
            
            options_file = Path(options + ('' if options.endswith('.yaml') else '.yaml'))

            if options_file.exists:
                pass
            else:
                raise FileExistsError(f"{options_file.name} doesn't exist")

            chrome_args = yaml.safe_load(options_file.read_text())
            chrome_args['options'].append(f'user-agent={chrome_args["user_agent"]}')

            [_options.add_argument(option) for option in chrome_args['options']]


        self.__prevent_closing = True
        self.__driver = driver(options=_options)

        if default_url != 'about:blank': self.__driver.get('about:blank')

        self.__driver.get(default_url)

        cookies_file = Path(cookies)
        if cookies_file.exists():

            for cookie in cookies_file.read_text().split(';'):
                if '=' in cookie:
                    name, value = cookie.strip().split('=', 1)
                    self.__driver.add_cookie({
                        'name': name,
                        'value': value,
                        'domain': cookies_domain,
                        'path': '/'
                    })

            self.__driver.refresh()

    @property
    def title(self) -> str:
        '''
        :returns: Returns the current title of the document
        '''
        return self.__driver.title

    def get(self, url : str) -> None:
        '''
        Navigate to a url

        :param str url: The url to navigate to 
        '''
        self.__driver.get(url)

    def find_element(self, sm : sm, value : str, timeout : int = 10) -> WebElement:
        '''
        Find a web element by a specific selection method
        
        :param sm sm: Selection method
        :param str value: A value of an id / class / name / css selector / xpath
        :param int timeout: Timeout to wait for the element to be found until an error is being thrown if the element is not found
        :returns: Returns a web element 
        '''
        return WebDriverWait(self.__driver, timeout).until(EC.presence_of_element_located((sm.value, value))) if \
            timeout > 0 else self.__driver.find_element(sm.value, value)
    
    def element_exists(self, sm : sm, value : str, timeout : int = 10) -> bool:
        '''
        Determine if an element exists in the page or not
        
        :param sm sm: Selection method
        :param str value: A value of an id / class / name / css selector / xpath
        :param int timeout: Timeout to wait for the element to be found until an error is being thrown if the element is not found
        :returns: Returns true or false base on the element existence
        '''
        try:
            WebDriverWait(self.__driver, timeout).until(EC.presence_of_element_located((sm.value, value))) if \
            timeout > 0 else self.__driver.find_element(sm.value, value)
            return True
        except:
            return False

    def find_elements(self, sm : sm, value : str, timeout : int = 10):
        '''
        Find an array of web element by a specific selection method
        
        :param sm sm: Selection method
        :param str value: A value of an id / class / name / css selector / xpath
        :param int timeout: Timeout to wait for the element to be found until an error is being thrown if the elements are not found
        :returns: Returns an array of web elements
        '''
        return WebDriverWait(self.__driver, timeout).until(EC.presence_of_all_elements_located((sm.value, value))) if \
            timeout > 0 else self.__driver.find_elements(sm.value, value)

    def click_element(self, sm : sm, value : str, timeout : int = 10) -> None:
        '''
        Find a web element by a specific selection method and click it
        
        :param sm sm: Selection method
        :param str value: A value of an id / class / name / css selector / xpath
        :param int timeout: Timeout to wait for the element to be found and clicked until an error is being thrown if the element is not found
        '''
        element = self.find_element(sm, value, timeout)
        if element: element.click()

    def scroll_element(self, sm : sm, value : str, timeout : int = 10) -> None:
        '''
        Find a web element by a specific selection method and scroll it until the end
        
        :param sm sm: Selection method
        :param str value: A value of an id / class / name / css selector / xpath
        :param int timeout: Timeout to wait for the element to be found and start scrolling until an error is being thrown if the element is not found
        '''
        element = WebDriverWait(self.__driver, timeout).until(EC.presence_of_element_located((sm.value, value)))

        while True:
            self.__driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", element)
            
            last_scroll_top = self.__driver.execute_script("return arguments[0].scrollTop", element)
            
            time.sleep(1.5)
            
            is_at_bottom = self.__driver.execute_script(
                "return (arguments[0].scrollTop + arguments[0].clientHeight) >= arguments[0].scrollHeight - 1", 
                element
            )
            
            new_scroll_top = self.__driver.execute_script("return arguments[0].scrollTop", element)

            if is_at_bottom and new_scroll_top == last_scroll_top:
                break

    def wait(self, seconds : float) -> None:
        '''
        Wait before executing a command
        :param float seconds: Time in seconds to wait before the driver executes a command
        '''
        self.__driver.implicitly_wait(seconds)

    def run(self, process, interval = 10):
        '''
        Loop your function until you forcefully exit your main code or call the quit method
        
        :param function process: Infinite loop function that you want to run
        :param second interval: Tickrate in seconds for the time to sleep between calls of your loop function 
        '''
        while self.__prevent_closing:
            process()
            time.sleep(interval)

    def stays(self) -> None:
        '''
        Prevent chrome from closing
        '''
        while self.__prevent_closing:
            time.sleep(10)

    def quit(self) -> None:
        '''
        Close the web browser and stops running your loop function
        '''
        self.__driver.quit()