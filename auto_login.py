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
    browser.add_cookie({"name": "MUSIC_U", "value": "00F1EC54CA6C65DC4E3633F7236527FD6A3EFF62FE70118EDCCE9FCB95FCD2F9F4ADDE188946DCE9053D9AF292D58A98797C973D29A9515DF52168A01753CED1A6E5DC7A4488F0868490D70EB8AAD9B2E11913BE58BFE0839466A0AFCC20668C606945B6A0FB7315FE9397737FCB242FD3CC30F429833D8E98DB90BD2C4E9E643D9C5542399E5F7851F618E954660A620C04F1A54E912DB0CE05084ECCE300D117E77E46E8682539B6AD7D225AED4D8A87ED15E5DCA79AA6B19042466B1FC990127D891E02F373D2E636170F3D638D184A75FFB2986EC2075A693C4D866B2307C993AC5436A52B3B723A2CA3E60F80AC5E4F477149A63BB10E94EC9642A942BC681999E573F99E345734DD589D4E03760B477F9A67E45019390944DB0F9CF9703F19794A0D55E8C1F4E8640B88559D8F0C51C8A6A8390E3641B24E81C7FE731041670A2B1E0574A52C63CB2BFA6B45CFB5"})
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
