from time import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from urllib3.util import parse_url

from dnevnik.auth_providers.code_based_provider import CodeBasedProvider
from ..base_auth_provider import BaseAuthProvider


class SeleniumAuthorization(BaseAuthProvider):
    auth_token: str = None

    def __init__(self, login, password, executable_path='chromedriver'):
        self.login = login
        self.password = password
        self.executable_path = executable_path
        self.callback_provider = None

    def proceed_authorization(self):
        start_time = time()
        options = webdriver.ChromeOptions()
        options.add_argument("--disable-blink-features=AutomationControlled")
        self.driver = webdriver.Chrome(options=options, executable_path=self.executable_path)

        self.driver.get("https://school.mos.ru")
        login_button = self.find_element(
            (By.XPATH, '//*[@id="root"]/div[1]/div[1]/main/section/div/div[1]/div[3]/div/div[1]/div[2]/div'))
        login_button.click()

        login_input = self.find_element((By.ID, "login"))
        password_input = self.find_element((By.ID, "password"))
        submit_button = self.find_element((By.ID, "bind"))

        login_input.send_keys(self.login)
        password_input.send_keys(self.password)
        submit_button.click()
        self.driver.execute_cdp_cmd('Network.setBlockedURLs', {"urls": ["https://school.mos.ru"]})
        self.driver.execute_cdp_cmd('Network.enable', {})
        while parse_url(self.driver.current_url).host != "school.mos.ru":
            pass
        callback_code = parse_url(self.driver.current_url).query[5:]

        self.driver.close()

        self.login_provider = CodeBasedProvider(callback_code)
        self.login_provider.proceed_authorization()
        self.auth_token = self.login_provider.auth_token
        self.profile_id = self.login_provider.profile_id

    def refresh_token(self):
        self.login_provider.refresh_token()

    def find_element(self, locator, time=10):
        return WebDriverWait(self.driver, time).until(EC.presence_of_element_located(locator),
                                                      message=f"Can't find element by locator {locator}")
