from time import sleep
from selenium import webdriver

class SeleniumAuth:
    auth_token_value: str = None

    def __init__(self, login, password, executable_path):
        self.login = login
        self.password = password
        self.executable_path = executable_path

    @property
    def auth_token(self):
        if not self.auth_token_value:
            self.auth_token_value = self.obtain_token()
        return self.auth_token_value

    def obtain_token(self):
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
        auth_token = driver.get_cookie("auth_token_value")
        while not auth_token:
            auth_token = driver.get_cookie("auth_token_value")
            sleep(0.5)
        return auth_token["value"]
