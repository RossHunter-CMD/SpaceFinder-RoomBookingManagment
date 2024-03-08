import unittest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time
import os
from dotenv import load_dotenv
 
load_dotenv()

LoginUsername = os.environ.get("STUDENT_EXAMPLE_LOGIN_USERNAME")
LoginPassword = os.environ.get("STUDENT_EXAMPLE_LOGIN_PASSWORD")

localSiteURL = "http://localhost:4200/"
testPage = "reportbug"

dashboardButtonXPath = "//button[text()='Dashboard']"
searchButtonXPath = "//button[text()='Search']"
bookARoomButtonXPath = "//button[text()='Book a Room']"
myBookingButtonXPath = "//button[text()='My Bookings']"
reportBugButtonXPath = "//button[text()='Report Bug']"
aboutUsButtonXPath = "//button[text()='About Us']"
contactUsButtonXPath = "//button[text()='Contact Us']"
logoutButtonXPath = "//button[text()='Logout']"

loginUsernameFieldXPath = "//*[@id='inputUsername']"
loginPasswordFieldXPath = "//*[@id='inputPassword']"
loginButtonSubmitXPath = "//*[@id='submitbutton']"

# Securely login into the website, and navigate to the dashboard
def login(driver):
        
        # Navigate to the Login Page
        driver.get(localSiteURL)

        # Locate login Username Field
        loginUsernameField = driver.find_element(By.XPATH, loginUsernameFieldXPath)

        # Send Username to Username Field
        loginUsernameField.send_keys(LoginUsername)

        # Locate Login Password Field
        loginPasswordField = driver.find_element(By.XPATH, loginPasswordFieldXPath)

        # Send Password to Password Field
        loginPasswordField.send_keys(LoginPassword)

        # Locate Login Button
        LoginButton = driver.find_element(By.XPATH, loginButtonSubmitXPath)

        # Click Login Submit BUtton
        ActionChains(driver).click(LoginButton).perform()

        # Wait 2 seconds
        time.sleep(2)

        return driver



# Dashboard Button Nav Bar Test
class Dashboard_Button_Function(unittest.TestCase):
    def test_Dashboard_Button_Function(self):

        # Creating Instance of Driver
        self.driver = webdriver.Chrome()
        driver = self.driver 

        # Login to Website
        login(self.driver)
        
        # Load Test Page
        driver.get("{0}{1}".format(localSiteURL,testPage))

        # Wait 2 seconds
        time.sleep(2)

        element = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, dashboardButtonXPath)))

        # Finding SearchButton Web Element
        searchButton = driver.find_element(By.XPATH, dashboardButtonXPath)

        # Clicking Relevant Button
        ActionChains(driver).click(searchButton).perform()

        # Wait 2 seconds
        time.sleep(2)

        # Asserting URL has changed to expected URL
        self.assertIn("{0}{1}".format(localSiteURL, "dashboard"), driver.current_url)

        # Closing Driver
        self.driver.close()

# Search Button Nav Bar Test
class Search_Button_Function(unittest.TestCase):
    def test_Search_Button_Function(self):

        # Creating Instance of Driver
        self.driver = webdriver.Chrome()
        driver = self.driver 

         # Login to Website
        login(self.driver)
        
        # Load Test Page
        driver.get("{0}{1}".format(localSiteURL,testPage))

        # Wait 2 seconds
        time.sleep(2)

        element = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, dashboardButtonXPath)))

        # Finding SearchButton Web Element
        searchButton = driver.find_element(By.XPATH, searchButtonXPath)

        # Clicking Relevant Button
        ActionChains(driver).click(searchButton).perform()

        # Wait 2 seconds
        time.sleep(2)

        # Asserting URL has changed to expected URL
        self.assertIn("{0}{1}".format(localSiteURL, "search"), driver.current_url)

        # Closing Driver
        self.driver.close()

# Book a Room Button Nav Bar Test
class BookRoom_Button_Function(unittest.TestCase):
    def test_BookRoom_Button_Function(self):

        # Creating Instance of Driver
        self.driver = webdriver.Chrome()
        driver = self.driver 

        # Login to Website
        login(self.driver)
        
        # Load Test Page
        driver.get("{0}{1}".format(localSiteURL,testPage))

        # Wait 2 seconds
        time.sleep(2)

        element = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, dashboardButtonXPath)))

        # Finding SearchButton Web Element
        searchButton = driver.find_element(By.XPATH, bookARoomButtonXPath)

        # Clicking Relevant Button
        ActionChains(driver).click(searchButton).perform()

        # Wait 2 seconds
        time.sleep(2)

        # Asserting URL has changed to expected URL
        self.assertIn("{0}{1}".format(localSiteURL, "bookroom"), driver.current_url)

        # Closing Driver
        self.driver.close()

# My Bookings Button Nav Bar Test
class My_Bookings_Button_Function(unittest.TestCase):
    def test_My_Bookings_Button_Function(self):

        # Creating Instance of Driver
        self.driver = webdriver.Chrome()
        driver = self.driver 

        # Login to Website
        login(self.driver)
        
        # Load Test Page
        driver.get("{0}{1}".format(localSiteURL,testPage))

        # Wait 2 seconds
        time.sleep(2)

        element = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, dashboardButtonXPath)))

        # Finding SearchButton Web Element
        searchButton = driver.find_element(By.XPATH, myBookingButtonXPath)

        # Clicking Relevant Button
        ActionChains(driver).click(searchButton).perform()

        # Wait 2 seconds
        time.sleep(2)

        # Asserting URL has changed to expected URL
        self.assertIn("{0}{1}".format(localSiteURL, "mybookings"), driver.current_url)

        # Closing Driver
        self.driver.close()

# Report A Bug Button Nav Bar Test
class Report_A_Bug_Button_Function(unittest.TestCase):
    def test_Report_A_Bug_Button_Function(self):

        # Creating Instance of Driver
        self.driver = webdriver.Chrome()
        driver = self.driver 

        # Login to Website
        login(self.driver)
        
        # Load Test Page
        driver.get("{0}{1}".format(localSiteURL,testPage))

        # Wait 2 seconds
        time.sleep(2)

        element = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, dashboardButtonXPath)))

        # Finding SearchButton Web Element
        searchButton = driver.find_element(By.XPATH, reportBugButtonXPath)

        # Clicking Relevant Button
        ActionChains(driver).click(searchButton).perform()

        # Wait 2 seconds
        time.sleep(2)

        # Asserting URL has changed to expected URL
        self.assertIn("{0}{1}".format(localSiteURL, "reportbug"), driver.current_url)

        # Closing Driver
        self.driver.close()

# About Us Button Nav Bar Test
class About_Us_Button_Function(unittest.TestCase):
    def test_About_Us_Button_Function(self):

        # Creating Instance of Driver
        self.driver = webdriver.Chrome()
        driver = self.driver 

         # Login to Website
        login(self.driver)
        
        # Load Test Page
        driver.get("{0}{1}".format(localSiteURL,testPage))

        # Wait 2 seconds
        time.sleep(2)

        element = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, dashboardButtonXPath)))

        # Finding SearchButton Web Element
        searchButton = driver.find_element(By.XPATH, aboutUsButtonXPath)

        # Clicking Relevant Button
        ActionChains(driver).click(searchButton).perform()

        # Wait 2 seconds
        time.sleep(2)

        # Asserting URL has changed to expected URL
        self.assertIn("{0}{1}".format(localSiteURL, "aboutus"), driver.current_url)

        # Closing Driver
        self.driver.close()

# Contact Us Button Nav Bar Test
class Contact_Us_Button_Function(unittest.TestCase):
    def test_Contact_Us_Button_Function(self):

        # Creating Instance of Driver
        self.driver = webdriver.Chrome()
        driver = self.driver 

         # Login to Website
        login(self.driver)
        
        # Load Test Page
        driver.get("{0}{1}".format(localSiteURL,testPage))

        # Wait 2 seconds
        time.sleep(2)

        element = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, dashboardButtonXPath)))

        # Finding SearchButton Web Element
        searchButton = driver.find_element(By.XPATH, contactUsButtonXPath)

        # Clicking Relevant Button
        ActionChains(driver).click(searchButton).perform()

        # Wait 2 seconds
        time.sleep(2)

        # Asserting URL has changed to expected URL
        self.assertIn("{0}{1}".format(localSiteURL, "contactus"), driver.current_url)

        # Closing Driver
        self.driver.close()

# Logout Button Nav Bar Test
class Log_out_Button_Function(unittest.TestCase):
    def test_Log_Out_Button_Function(self):

        # Creating Instance of Driver
        self.driver = webdriver.Chrome()
        driver = self.driver 

        # Login to Website
        login(self.driver)
        
        # Load Test Page
        driver.get("{0}{1}".format(localSiteURL,testPage))

        # Wait 2 seconds
        time.sleep(2)

        element = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, dashboardButtonXPath)))

        # Finding SearchButton Web Element
        searchButton = driver.find_element(By.XPATH, logoutButtonXPath)

        # Clicking Relevant Button
        ActionChains(driver).click(searchButton).perform()

        # Wait 2 seconds
        time.sleep(2)

        # Asserting URL has changed to expected URL
        self.assertIn("{0}{1}".format(localSiteURL, ""), driver.current_url)

        # Closing Driver
        self.driver.close()
 

if __name__ == "__main__":
    unittest.main()