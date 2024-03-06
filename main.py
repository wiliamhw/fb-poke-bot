from selenium import webdriver
from selenium.webdriver.common.by import By
from dotenv import load_dotenv
import os
import time
import pickle

load_dotenv()
browser = webdriver.Chrome()
cookie_file = "cookies.pkl"

def login_to_facebook ():
    if os.path.exists("cookies.pkl"):
        cookies = pickle.load(open("cookies.pkl", "rb"))
        for cookie in cookies:
            browser.add_cookie(cookie)
        return
    browser.get("https://m.facebook.com/login")
    browser.find_element(By.NAME, "email").send_keys(os.environ.get("EMAIL"))
    browser.find_element(By.NAME, "pass").send_keys(os.environ.get("PASSWORD"))
    browser.find_element(By.NAME,"login").click()
    pickle.dump(browser.get_cookies(), open("cookies.pkl", "wb"))

login_to_facebook();
time.sleep(300)
browser.quit()