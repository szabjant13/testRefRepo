import os
import time
import logging
from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.common import ElementNotInteractableException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options


class TarrAutomation:
    def __init__(self):
        """
        Initializes the basic things.
        """
        os.environ['PATH'] += r"C:/cd"
        options = Options()
        options.add_experimental_option('detach', True)
        self.driver = webdriver.Chrome(options=options)
        self.driver.maximize_window()

    def login(self, username, password):
        """
        Log in to the website using the provided username and password.
        """
        login_url = 'https://tarr.hu/ugyfelkapu/bejelentkezes'
        self.driver.get(login_url)

        try:
            username_field = self.driver.find_element(By.NAME, 'username')
            password_field = self.driver.find_element(By.NAME, 'password')
            login_button = self.driver.find_element(By.XPATH, "//button[@class='btn btn--primary' and text()='Belépés']")
            username_field.send_keys(username)
            password_field.send_keys(password)
            login_button.click()
        except (NoSuchElementException, ElementNotInteractableException) as e:
            logging.error(f"Error during login: {str(e)}")

    def check_out_personal_info(self):
        """
        Clicks on the 'Személyes adatok' link to check out personal information.
        """
        try:
            personal_data_link = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.LINK_TEXT, 'Személyes adatok'))
            )
            personal_data_link.click()
            logging.info("Successfully clicked on 'Személyes adatok' link")
        except NoSuchElementException as e:
            logging.error(f"Error during 'Személyes adatok' link click: {str(e)}")

    def set_new_contact_data(self, email, phone_number):
        """
        Searches the given fields, and sets new contact data for the customer
        """
        try:
            email_field = self.driver.find_element(By.NAME, 'email')
            phone_number_field = self.driver.find_element(By.NAME, 'phoneNumber')
            modify_button = self.driver.find_element(By.XPATH,
                                                     "//button[@class='btn btn--primary' and text()='Módosítom']")

            email_field.send_keys(email)
            phone_number_field.send_keys(phone_number)
        except NoSuchElementException:
            logging.error("Error: One or more required elements not found on the page.")

        try:
            modify_button.click()
        except ElementNotInteractableException:
            logging.error("Error: The button is not interectable.")

    def logout(self):
        """
        Logs out from the account
        """
        try:
            element = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.CLASS_NAME, "profile"))
            )
            element.click()
            logging.info("Successfully clicked on 'Profile' link")
        except NoSuchElementException as e:
            logging.error("Error:", str(e))

        try:
            logout_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.CLASS_NAME, "btn--primary"))
            )
            logout_button.click()
        except ElementNotInteractableException as e:
            logging.info("Error:", str(e))

    def close_browser(self):
        """
        After the given time, it closes the Browser.
        """
        time.sleep(3)
        self.driver.quit()


if __name__ == "__main__":
    automation = TarrAutomation()
    automation.login('testuser', 'testPassword')
    automation.check_out_personal_info()
    automation.set_new_contact_data('teszt@teszt.hu', '0674123456')
    automation.logout()
    automation.close_browser()
