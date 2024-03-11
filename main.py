from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from dotenv import load_dotenv
from datetime import datetime
import traceback
import logging
import os
import time

# Main
def login_to_facebook(driver):
    driver.get("https://m.facebook.com/login")
    driver.find_element(By.NAME, "email").send_keys(os.environ.get("EMAIL"))
    driver.find_element(By.NAME, "pass").send_keys(os.environ.get("PASSWORD"))
    driver.find_element(By.NAME,"login").click()
    page_changed = EC.presence_of_element_located((By.NAME, 'next'))
    WebDriverWait(driver, 5).until(page_changed)

def set_logger():
    logging.basicConfig(
        filename='poke.log', level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        datefmt="%Y-%m-%d %H:%M:%S"
    )
  
def get_driver(is_headless):
    option = Options()
    option.add_argument("--disable-infobars")
    option.add_argument("--disable-extensions")
    option.add_experimental_option(
        "prefs", {"profile.default_content_setting_values.notifications": 2}
    )
    if (is_headless == 'true'):
        option.add_argument("--headless=new")
    return webdriver.Chrome(options=option)

def poke_target(driver, target_name):
    try:
        name_link = driver.find_element(By.LINK_TEXT, target_name)
        parent_container = name_link.find_element(By.XPATH, "." + ("/.." * 7))
        if (parent_container.get_attribute('aria-disabled') != None):
            return False

        poke_button = parent_container.find_element(By.XPATH, "//span[contains(text(), 'Poke Back')]")
        poke_button.click()
        logging.info("Poke " + target_name)
        
        disabled_button = EC.text_to_be_present_in_element_attribute(parent_container, 'aria-disabled', 'true')
        WebDriverWait(driver, 5).until(disabled_button)
        
        return True
    except:
        return False

def main():
    load_dotenv()
    set_logger()
    driver = get_driver(os.environ.get("IS_HEADLESS", False))
    target_names = os.environ.get("TARGET_NAMES").split(",")
    poke_delay = int(os.environ.get("POKE_DELAY_IN_SECONDS", 30))
    poke_alert_timeout = int(os.environ.get("POKE_ALERT_TIMEOUT", 300))

    try:
        login_to_facebook(driver);
        while True:
            driver.get("https://m.facebook.com/pokes/")
            for target_name in target_names:
                poke_target(driver, target_name)
                
            try:
                alert_shown = EC.presence_of_element_located((By.XPATH, "//div[@role='alert'][contains(text(), 'poked you.')]"))
                WebDriverWait(driver, poke_alert_timeout).until(alert_shown)
            except:
                None
                
            time.sleep(poke_delay)
    except KeyboardInterrupt:
        print("Keyboard interrupt")
    except:
        errorFile = open('error.log', 'a')
        errorFile.write(datetime.now().strftime("%A, %d-%m-%y %H:%M:%S") + '\n')
        errorFile.write(traceback.format_exc())
        errorFile.close()
    finally:
        driver.quit()

while True:
    try:
        main()
    except ConnectionResetError:
        time.sleep(300)
        continue