import os
import time
from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.common import ElementNotInteractableException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options


class TarrAutomation:
    def __init__(self):
        os.environ['PATH'] += r"C:/cd"
        options = Options()
        options.add_experimental_option('detach', True)
        self.driver = webdriver.Chrome(options=options)
        self.driver.maximize_window()

    def login(self, username, password):
        login_url = 'https://tarr.hu/ugyfelkapu/bejelentkezes'
        self.driver.get(login_url)

        username_field = self.driver.find_element(By.NAME, 'username')
        password_field = self.driver.find_element(By.NAME, 'password')
        login_button = self.driver.find_element(By.XPATH, "//button[@class='btn btn--primary' and text()='Belépés']")

        username_field.send_keys(username)
        password_field.send_keys(password)
        login_button.click()

    def check_out_personal_info(self):
        try:
            personal_data_link = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.LINK_TEXT, 'Személyes adatok'))
            )
            personal_data_link.click()
            print("Successfully clicked on 'Személyes adatok' link")
        except NoSuchElementException as e:
            print("Error:", str(e))

    def logout(self):
        try:
            element = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.CLASS_NAME, "profile"))
            )
            element.click()
        except NoSuchElementException as e:
            print("Error:", str(e))

        try:
            logout_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.CLASS_NAME, "btn--primary"))
            )
            logout_button.click()
        except ElementNotInteractableException as e:
            print("Error:", str(e))

    def close_browser(self):
        time.sleep(3)
        self.driver.quit()


if __name__ == "__main__":
    automation = TarrAutomation()
    automation.login('szabjant13', 'Szabjanqwe0123.')
    automation.check_out_personal_info()
    automation.logout()
    automation.close_browser()
