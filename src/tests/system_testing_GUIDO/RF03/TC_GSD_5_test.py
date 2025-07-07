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
        self.driver.find_element(By.CSS_SELECTOR, "input").send_keys(
            "can you provide me community smells in https://github.com/gianwario/beehave after 01/01/2020?")
        self.driver.find_element(By.CSS_SELECTOR, "input").send_keys(Keys.ENTER)

        try:
            WebDriverWait(self.driver, 60).until(
                lambda d: len(d.find_elements(By.CSS_SELECTOR, ".bot-msg")) >= 2
            )
            bot_messages = self.driver.find_elements(By.CSS_SELECTOR, ".bot-msg")

            second_msg_text = bot_messages[1].text.strip().lower()

            assert "these are the community smells we were able to detect in the repository" in second_msg_text, \
                f"Messaggio inatteso: {second_msg_text}"

        except TimeoutException:
            assert False, "Timeout: i messaggi bot non sono apparsi in tempo"
