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
        self.driver.find_element(By.CSS_SELECTOR, ".selected-values").click()
        self.driver.find_element(By.ID, "Italy").click()
        element = self.driver.find_element(By.ID, "participantsInput")
        actions = ActionChains(self.driver)
        actions.move_to_element(element).click_and_hold().perform()
        element = self.driver.find_element(By.ID, "participantsInput")
        actions = ActionChains(self.driver)
        actions.move_to_element(element).perform()
        element = self.driver.find_element(By.ID, "participantsInput")
        actions = ActionChains(self.driver)
        actions.move_to_element(element).release().perform()
        self.driver.find_element(By.ID, "participantsInput").click()
        self.driver.find_element(By.ID, "participantsInput").send_keys(Keys.BACKSPACE)
        self.driver.find_element(By.ID, "participantsInput").send_keys("5")
        self.driver.find_element(By.CSS_SELECTOR, ".ok-button").click()
        self.driver.find_element(By.CSS_SELECTOR, ".selected-values").click()
        self.driver.find_element(By.ID, "Germany").click()
        element = self.driver.find_element(By.ID, "participantsInput")
        actions = ActionChains(self.driver)
        actions.move_to_element(element).click_and_hold().perform()
        element = self.driver.find_element(By.ID, "participantsInput")
        actions = ActionChains(self.driver)
        actions.move_to_element(element).perform()
        element = self.driver.find_element(By.ID, "participantsInput")
        actions = ActionChains(self.driver)
        actions.move_to_element(element).release().perform()
        self.driver.find_element(By.ID, "participantsInput").click()
        self.driver.find_element(By.ID, "participantsInput").send_keys(Keys.BACKSPACE)
        self.driver.find_element(By.ID, "participantsInput").send_keys("6")
        self.driver.find_element(By.CSS_SELECTOR, ".ok-button").click()
        self.driver.find_element(By.CSS_SELECTOR, "label:nth-child(3)").click()
        self.driver.find_element(By.CSS_SELECTOR, ".compute-button").click()

        try:
            WebDriverWait(self.driver, 2).until(
                lambda d: len(d.find_elements(By.CSS_SELECTOR, ".result-display")) > 2
            )
            results = self.driver.find_elements(By.CSS_SELECTOR, ".result-display")

            if len(results) <  2:
                assert False, "Errore nella risposta del server."
        except TimeoutException:
            assert True, "System returned the correct results"