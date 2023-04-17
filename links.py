import json

import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from login import login

# DELAYS
DELAY_ONLOAD = 5
DELAY_ONLOAD_SPEED = 3
DELAY_TIK = 1

categoryLink = 'https://ds.aliexpress.com/dscenter/productfind/category_list.htm'
categories = []


class Category:
    def __init__(self, categoryName):
        self.categoryName = categoryName
        self.links = []


def getLinks(driver):
    login(driver, categoryLink)

    time.sleep(DELAY_TIK)
    categoryResponse = driver.find_element(By.TAG_NAME, 'pre').text

    my_json = json.loads(categoryResponse)
    for category in my_json["data"]:
        categoryObject = Category(category["name"])
        for i in range(30):
            categoryObject.links.append(
                f'https://ds.aliexpress.com/dscenter/productfind/search.htm?searchText=&categoryId={category["id"]}&shipFrom=&requireCouponCode=n&freeShipping=n&overseasWarehouse=n&requireVideo=n&sort=DEFAULT&specialOffer=&minPrice=&maxPrice=&pageSize=100&pageNum={i + 1}')

        categories.append(categoryObject)

    return categories
