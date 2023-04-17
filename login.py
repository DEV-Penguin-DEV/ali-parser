import time
from selenium.webdriver.common.by import By


# DELAYS
DELAY_ONLOAD = 9
DELAY_ONLOAD_SPEED = 4
DELAY_ONLOAD_AUTH = 20
DELAY_ONLOAD_DOWNLOAD_ALI_INSIDER = 15
DELAY_ONCLICK = 5
DELAY_TIK = 2


# LOGIN (SETTING)
EMAIL_INPUT_ID = 'fm-login-id'
PASSWORD_INPUT_ID = 'fm-login-password'
EMAIL = 'kostiklysenko5@gmail.com'
PASSWORD = 'qazwsx'
NEXT_BUTTON_CLASS = 'login-submit'


def login(driver, link):
    driver.get(link)

    time.sleep(DELAY_ONLOAD_SPEED)  # Задержка для ожидания загрузки страницы

    emailInputElement = driver.find_element(By.ID, EMAIL_INPUT_ID)
    emailInputElement.send_keys(EMAIL)
    passwordInputElement = driver.find_element(By.ID, PASSWORD_INPUT_ID)
    passwordInputElement.send_keys(PASSWORD)
    nextButton = driver.find_element(By.CLASS_NAME, NEXT_BUTTON_CLASS)
    nextButton.click()

    time.sleep(DELAY_ONLOAD_AUTH)
