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
        self.driver.find_element(By.CSS_SELECTOR, "label:nth-child(4)").click()
        self.driver.find_element(By.CSS_SELECTOR, ".compute-button").click()

        try:
            WebDriverWait(self.driver, 2).until(
                lambda d: len(d.find_elements(By.CSS_SELECTOR, ".result-display")) > 0
            )
            results = self.driver.find_elements(By.CSS_SELECTOR, ".result-display")

            if len(results) >  0:
                assert False, "Errore nella risposta del server."
        except TimeoutException:
            assert True, "System returned the correct results"