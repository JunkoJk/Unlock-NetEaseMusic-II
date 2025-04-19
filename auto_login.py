# coding: utf-8

import os
import time
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from retrying import retry

# Configure logging
logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(asctime)s %(message)s')

@retry(wait_random_min=5000, wait_random_max=10000, stop_max_attempt_number=3)
def enter_iframe(browser):
    logging.info("Enter login iframe")
    time.sleep(5)  # 给 iframe 额外时间加载
    try:
        iframe = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, "//*[starts-with(@id,'x-URS-iframe')]")
        ))
        browser.switch_to.frame(iframe)
        logging.info("Switched to login iframe")
    except Exception as e:
        logging.error(f"Failed to enter iframe: {e}")
        browser.save_screenshot("debug_iframe.png")  # 记录截图
        raise
    return browser

@retry(wait_random_min=1000, wait_random_max=3000, stop_max_attempt_number=5)
def extension_login():
    chrome_options = webdriver.ChromeOptions()

    logging.info("Load Chrome extension NetEaseMusicWorldPlus")
    chrome_options.add_extension('NetEaseMusicWorldPlus.crx')

    logging.info("Initializing Chrome WebDriver")
    try:
        service = Service(ChromeDriverManager().install())  # Auto-download correct chromedriver
        browser = webdriver.Chrome(service=service, options=chrome_options)
    except Exception as e:
        logging.error(f"Failed to initialize ChromeDriver: {e}")
        return

    # Set global implicit wait
    browser.implicitly_wait(20)

    browser.get('https://music.163.com')

    # Inject Cookie to skip login
    logging.info("Injecting Cookie to skip login")
    browser.add_cookie({"name": "MUSIC_U", "value": "00AF043779243202F8664EF89313E8A2E1C199C3105999C1F9D33EF4502915C9D6F0AF56C73A9F4988E81DFD06170A016250702D277501ABA943B096EC1B2FD68FD044007F1616F9256C30790DE54EF7D2AA0DA9107F1F147E88144A19672C6E2CB65F3FBB1D178CBE329DC00EBF68EC9B53263B935D64896FCCB22DBE242C92447D1BA1BD7B419016EC4071DCC273E70DC95702CD7E118D6F0B8B5E1994B4459D7255D3B0E93B1D08D98F79CAA026E5447B66F64B4198D51D8570F65542FED21C925CCC03DBA2A020BC461CA0174A528FFC6A2C3179D84DC247FA789A8FFCA10F56C6482BCE7CB377E3B397272ED6B76E8AB0E07E1B9870547EE5CCFDACF29DA73C6C49788D2C2A9A8AEE18AE7FAE9902EC7AAF806F23D73E4B25C60AA5EFA602B53688EDA037C4A29794B14418317FA2C6BAD624B0C8F4F8EE2262C99492D376A57B52DEDDF97D15E8BCAD40C36A804269BC9704905B3F8B35D67B8D001BE9E7"})
    browser.refresh()
    time.sleep(5)  # Wait for the page to refresh
    logging.info("Cookie login successful")

    # Confirm login is successful
    logging.info("Unlock finished")

    time.sleep(10)
    browser.quit()


if __name__ == '__main__':
    try:
        extension_login()
    except Exception as e:
        logging.error(f"Failed to execute login script: {e}")
