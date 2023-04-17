import requests
from colorama import init, Fore, Back, Style
import json
import os
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from openpyxl.drawing.image import Image
import datetime
import requests
from io import BytesIO
from parserSettings import DELIVERY_PRICE_CLASS, DELIVERY_LIMIT, IS_STAR_CLASS, IS_STAR_INDEX, MIN_MONTH_SOLDS, MONTH_REVENUE_ID, MONTH_REVENUE_INDEX, MONTH_SOLDS_CLASS, MONTH_SOLDS_INDEX, PRICE_CLASS, SHOP_NAME_CLASS
import math

# DELAYS
DELAY_ONLOAD = 9
DELAY_ONLOAD_SPEED = 4
DELAY_ONLOAD_AUTH = 20
DELAY_ONLOAD_DOWNLOAD_ALI_INSIDER = 15
DELAY_ONCLICK = 5
DELAY_TIK = 2


def getDeliveryPrice(deliveryLines):
    if (len(deliveryLines) == 3 or len(deliveryLines) == 5):
        if (': ' in deliveryLines[0].text):
            return float(deliveryLines[0].text.split(': ')[1].split('CHF ')[1])
        if (':' in deliveryLines[0].text):
            return float(deliveryLines[0].text.split(':')[1].split('CHF ')[1])
        return 0 if deliveryLines[0].text == 'Free Shipping ' else float(deliveryLines[0].text.split('CHF ')[1])
    return False


def getDeliveryDuraction(deliveryLines):
    if (len(deliveryLines) == 1):
        return False
    if (len(deliveryLines) == 5):
        today = datetime.date.today()
        deliveryDate = date_obj = datetime.datetime.strptime(
            deliveryLines[1].text.split('on ')[1] + ', 2023', "%b %d , %Y")
        return (deliveryDate.date() - today).days

    if ':' in deliveryLines[len(deliveryLines) - 1].text:
        minAndMaxDuraction = deliveryLines[len(
            deliveryLines) - 1].text.split(': ')[1].split(' ')[0].split('-')
        avarageDuraction = (
            int(minAndMaxDuraction[0]) + int(minAndMaxDuraction[1])) / 2
        return avarageDuraction

    if 'on' in deliveryLines[len(deliveryLines) - 1].text:
        today = datetime.date.today()
        deliveryDate = date_obj = datetime.datetime.strptime(
            deliveryLines[len(deliveryLines) - 1].text.split('on ')[1] + ', 2023', "%b %d , %Y")
        return (deliveryDate.date() - today).days

    today = datetime.date.today()
    deliveryDate = date_obj = datetime.datetime.strptime(
        deliveryLines[len(deliveryLines) - 1].text.split('by ')[1] + ', 2023', "%b %d , %Y")
    return (deliveryDate.date() - today).days


def parseProduct(driver, productObj):
    driver.get(productObj["itemUrl"])
    try:
        driver.find_element(By.CLASS_NAME, 'customs-message-wrap')
        return False
    except NoSuchElementException:
        print('alles GUT!')

    time.sleep(DELAY_ONLOAD)

    deliveryLines = driver.find_elements(
        By.CLASS_NAME, DELIVERY_PRICE_CLASS)
    if (len(deliveryLines) <= 0):
        time.sleep(10)
        deliveryLines = driver.find_elements(
            By.CLASS_NAME, DELIVERY_PRICE_CLASS)

    deliveryPrice = getDeliveryPrice(deliveryLines)

    if (deliveryPrice == False):
        return False

    delivery = getDeliveryDuraction(deliveryLines)
    if (delivery == False):
        return False

    if (delivery > DELIVERY_LIMIT):
        return False

    try:
        if len(driver.find_elements(
                By.CLASS_NAME, MONTH_SOLDS_CLASS)) - 1 < MONTH_SOLDS_INDEX:
            time.sleep(20)
            print('noooooonononoon')
        monthSolds = driver.find_elements(
            By.CLASS_NAME, MONTH_SOLDS_CLASS)[MONTH_SOLDS_INDEX].find_element(
            By.TAG_NAME, 'b').text.replace(',', '')
    except NoSuchElementException:
        time.sleep(20)
        monthSolds = driver.find_elements(
            By.CLASS_NAME, MONTH_SOLDS_CLASS)[MONTH_SOLDS_INDEX].find_element(
            By.TAG_NAME, 'b').text.replace(',', '')

    try:
        intMonthSolds = int(monthSolds)
    except ValueError:
        print(f'AAAAAAAA bullshit {monthSolds}')
        intMonthSolds = 99999

    if (intMonthSolds < MIN_MONTH_SOLDS):
        return False

    shopName = driver.find_elements(
        By.CLASS_NAME, SHOP_NAME_CLASS)[0].text

    try:
        if len(driver.find_element(
                By.ID, MONTH_REVENUE_ID).find_elements(
                By.TAG_NAME, 'div')) - 1 < MONTH_REVENUE_INDEX:
            time.sleep(15)
        monthRevenue = 0 if len(driver.find_element(
            By.ID, MONTH_REVENUE_ID).find_elements(
            By.TAG_NAME, 'div')[MONTH_REVENUE_INDEX].find_element(
            By.TAG_NAME, 'b').text.split('CHF ')) < 2 else driver.find_element(
            By.ID, MONTH_REVENUE_ID).find_elements(
            By.TAG_NAME, 'div')[MONTH_REVENUE_INDEX].find_element(
            By.TAG_NAME, 'b').text.split('CHF ')[1]
    except NoSuchElementException:
        time.sleep(15)
        monthRevenue = 0 if len(driver.find_element(
            By.ID, MONTH_REVENUE_ID).find_elements(
            By.TAG_NAME, 'div')[MONTH_REVENUE_INDEX].find_element(
            By.TAG_NAME, 'b').text.split('CHF ')) < 2 else driver.find_element(
            By.ID, MONTH_REVENUE_ID).find_elements(
            By.TAG_NAME, 'div')[MONTH_REVENUE_INDEX].find_element(
            By.TAG_NAME, 'b').text.split('CHF ')[1]

    isStar = driver.find_elements(
        By.CLASS_NAME, IS_STAR_CLASS)[IS_STAR_INDEX].find_element(
        By.TAG_NAME, 'img').get_attribute('src') != 'chrome-extension://cbcoaginjmpgjalcbfmlkpjkeldoaeio/images/icon_Xmark.png'

    print('-------')
    print(deliveryPrice)
    print(delivery)
    print(shopName)
    print()
    print(monthSolds)
    print(monthRevenue)
    print(isStar)
    print('-------')
    productObj["deliveryPrice"] = deliveryPrice
    productObj["delivery"] = delivery
    productObj["shopName"] = shopName
    productObj["monthSolds"] = monthSolds
    productObj["monthRevenue"] = monthRevenue
    productObj["isStar"] = isStar
    return productObj


print('NaN' is 'NaN')
print('NaN' == 'NaN')
print(float('NaN '))
print(math.isnan(float('NaN')))
