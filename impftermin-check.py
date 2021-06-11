import os
import time
import traceback
from datetime import datetime as dt
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import boto3
from emoji import emojize

BASE_URL = "https://www.impfportal-niedersachsen.de/portal/#/appointment/public"

ELEMENT_IDS = {
    "privacy": "mat-checkbox-1",
    "dob": "mat-input-2",
    "occupational-indication": "mat-radio-2",
    "zip-code": "mat-input-0"
}

NEXT_BTN_XPATH = (
    "/html/body/my-app/div/div[3]/mat-sidenav-container"
    "/mat-sidenav-content/appointment-public-view/div/form/div[2]/div/button[2]"
)

UNDERSTOOD_BTN_XPATH = ("/html/body/div[4]/div[2]/div/mat-dialog-container"
                        "/confirm-dialog/mat-dialog-content/div/button")

VAC_CENTER_DIV_XPATH = ("/html/body/my-app/div/div[3]/mat-sidenav-container"
                        "/mat-sidenav-content/appointment-public-view/div"
                        "/form/div[1]/div/div[1]/div[5]")

DOB = "25.09.1996"
ZIP_CODE = "31319"

TOPIC_ARN = "arn:aws:sns:eu-central-1:545087848908:ImpfterminCheck"

chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--window-size=1920x1080")

executable_path = os.getcwd() + "/chromedriver"
driver = webdriver.Chrome(options=chrome_options,
                          executable_path=executable_path)
wait = WebDriverWait(driver, 10, poll_frequency=1)

sns = boto3.client("sns")

while True:
    try:
        driver.get(BASE_URL)

        wait.until(EC.element_to_be_clickable(
            (By.ID, ELEMENT_IDS["privacy"]))).click()
        wait.until(EC.element_to_be_clickable(
            (By.XPATH, NEXT_BTN_XPATH))).click()

        wait.until(EC.element_to_be_clickable(
            (By.XPATH, NEXT_BTN_XPATH))).click()

        wait.until(EC.element_to_be_clickable(
            (By.ID, ELEMENT_IDS["dob"]))).send_keys(DOB)
        wait.until(EC.element_to_be_clickable(
            (By.XPATH, NEXT_BTN_XPATH))).click()

        wait.until(EC.element_to_be_clickable(
            (By.ID, ELEMENT_IDS["zip-code"]))).send_keys(ZIP_CODE + Keys.ENTER)
        wait.until(EC.element_to_be_clickable(
            (By.ID, ELEMENT_IDS["zip-code"])))
        vac_center_div = wait.until(
            EC.presence_of_element_located((By.XPATH, VAC_CENTER_DIV_XPATH)))

        if "cancel" in vac_center_div.text:
            time.sleep(1)
        else:
            msg = ("Beeilung, im Impfzentrum Hannover sind gerade freie "
                   "Termine verfügbar! "
                   ":rotating_light::syringe::adhesive_bandage:")
            sns.publish(TopicArn=TOPIC_ARN,
                        Message=emojize(msg, use_aliases=True),
                        Subject="Impftermine verfügbar")
            print(f"{'*'*30}\n* {dt.now()} * {msg}\n{'*'*30}")
            driver.save_screenshot("capture.png")
            time.sleep(10 * 60)

    except Exception:
        traceback.print_exc()

    except KeyboardInterrupt:
        print(" has been pressed, exiting...")
        break

driver.quit()