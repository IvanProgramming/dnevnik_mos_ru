from time import sleep, time
from ..base_auth_provider import BaseAuthProvider
from ..exceptions import CredentialsInvalidException
from selenium import webdriver
from urllib3.util import parse_url


class SeleniumAuthorization(BaseAuthProvider):
    auth_token: str = None

    def __init__(self, login, password, executable_path='chromedriver'):
        self.login = login
        self.password = password
        self.executable_path = executable_path

    def proceed_authorization(self):
        start_time = time()
        options = webdriver.ChromeOptions()
        options.add_argument("--disable-blink-features=AutomationControlled")
        driver = webdriver.Chrome(options=options, executable_path=self.executable_path)

        driver.get("https://dnevnik.mos.ru")
        login_button = driver.find_element_by_xpath("//div[2]/div/a")
        login_button.click()

        login_input = driver.find_element_by_id("login")
        password_input = driver.find_element_by_id("password")
        submit_button = driver.find_element_by_id("bind")

        login_input.send_keys(self.login)
        password_input.send_keys(self.password)
        submit_button.click()

        auth_token = driver.get_cookie("auth_token")
        while parse_url(driver.current_url).host != "dnevnik.mos.ru":
            if driver.find_element_by_css_selector('blockquote.blockquote-danger'):
                raise CredentialsInvalidException(driver.find_element_by_css_selector('blockquote.blockquote-danger'))

        while not auth_token:
            auth_token = driver.get_cookie("auth_token")
            sleep(0.01)

        self.profile_id = int(driver.get_cookie("profile_id")["value"])
        driver.close()
        execution_time = time() - start_time
        self.auth_token = auth_token['value']

    def refresh_token(self):
        self.proceed_authorization()
