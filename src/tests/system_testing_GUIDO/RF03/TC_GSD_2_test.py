import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
import time

class Test:
    def setup_method(self, method):
        self.driver = webdriver.Firefox()
        self.vars = {}

    def teardown_method(self, method):
        self.driver.quit()

    def test(self):
        self.driver.get("http://localhost:3000/")
        self.driver.set_window_size(1290, 829)
        self.driver.find_element(By.ID, "1").click()
        time.sleep(3)
        self.driver.find_element(By.CSS_SELECTOR, "input").click()
        self.driver.find_element(By.CSS_SELECTOR, "input").send_keys("can you provide me community smells in https://github.com/gianwario/beehave from 31/adwa/2dw21")
        self.driver.find_element(By.CSS_SELECTOR, "input").send_keys(Keys.ENTER)

        try:
            WebDriverWait(self.driver, 5).until(
                lambda d: len(d.find_elements(By.CSS_SELECTOR, ".bot-msg")) >= 2
            )
            bot_message = self.driver.find_elements(By.CSS_SELECTOR, ".bot-msg")

            if bot_message[1].text.strip().lower() == "errore nella risposta del server.".strip().lower():
                assert True, "Errore nella risposta del server."
            else:
                assert False, "System didn't return the correct error"
        except TimeoutException:
            assert False, "System didn't return the correct error"