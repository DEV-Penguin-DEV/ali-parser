import json
from selenium import webdriver
from links import getLinks
from colorama import init, Back
import requests
import os

# Инициализация библиотеки
init()


headers = {
    'authority': 'ds.aliexpress.com',
    'scheme': 'https',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
    'cookie': 'ali_apache_id=33.1.223.138.1680770622798.638836.7; e_id=pt20; cna=QXS1HG5pIVUCAbLF2ZlNlM3h; acs_usuc_t=acs_rt=eb173648d7d54af9949be545e96ee7cc&x_csrf=15yf6bn94w12a; xlly_s=1; havana_tgc=eyJwYXRpYWxUZ2MiOnsiYWNjSW5mb3MiOnsxMzp7ImFjY2Vzc1R5cGUiOjEsIm1lbWJlcklkIjoxNTc2NTMwNDUyMDMzLCJ0Z3RJZCI6IjZ3WEloaUVoUmM2ODc5UzlDU2t3MndRIn19fX0; _hvn_login=13; x_router_us_f=x_alimid=4520032409; xman_us_t=x_lid=ch2923864409jjcae&sign=y&rmb_pp=kostiklysenko5@gmail.com&x_user=JskOVbQInmfSeu45c5CDIt2CYByt0hfYl6OHhcUUzg4=&ctoken=3accbkmx0zxh&l_source=aliexpress; sgcookie=E100Fbu6ft3sOaMRYcCLZErv8hllj4FDFom01Zydq8eUDAk19B2fg44YdrAK5gXw+n+ED4KZMo7Yba0LLPDBDz9KhtA6jLwW8+PqcTMK+r8/4tg=; aep_common_f=v/1GpQS/Oqg1MYZvUwIhim/PJ3DNTsqh7Jkr7InShAflMaqa2Y+7CQ==; xman_f=JaDQHodYYTUYy3ROEDV96tuqpG14nRWd/ewyg4UgxfU0RlvFvYwi6ejb0owZR6mklAMVcwIkcDENMUl4MDlkteI4wB2H/cDcV5ZRJntWBzT5yydxdhZpI9B13UgbwopeSBO1K2sn0poEvI61t3PClUf5NPLl4ebUyKCJLpg4zkIwHAuGj9Z0uhnDnaMYuRnvZnUqgQ3hO6PsuKSjPXFSU+HSqfgasoE/Wytag8T5wqE7FMt9+FF1b8wHxwcayFx6wpOxE7ud6qXwEGCKZCy9RW25TmU7HOrinTMxdWW50UStUKuL5nCzcVESigUo8WP0lhtK/L2zLIQ8igkTR5X2Bag18Vfst5EUFpSkligRvCDlBL5G4uZEuWRwzWx18dRPI9K6dGisro82GiC9M8f8Jy8kqF8MyEqt2pqyF9lRIa8HyZs6edhmgg==; x-hng=lang=en-US; _gid=GA1.2.311867750.1681194906; _gcl_au=1.1.1210172044.1681194907; ali_apache_tracktmp=W_signed=Y; _ym_uid=1681194909329750107; _ym_d=1681194909; _fbp=fb.1.1681194910154.2091630742; traffic_se_co=%7B%7D; af_ss_a=1; af_ss_b=1; ae-msite-city=; ae-msite-province=; aep_usuc_f=site=glo&c_tp=CHF&x_alimid=4520032409&ups_d=1|1|1|1&isb=y&ups_u_t=1696746930479&region=CH&b_locale=en_US&ae_u_p_s=2; intl_locale=en_US; ali_apache_track=mt=1|ms=|mid=ch2923864409jjcae; aeu_cid=d0fe9dc1130744e1b63d4ce934a9fcfe-1681240350591-07065-_ePNSNV; _m_h5_tk=b92209f2bed7c12974165b498832b7b6_1681242963209; _m_h5_tk_enc=031b562a424aea084512b92d51202b33; xman_us_f=x_locale=en_US&x_l=0&x_user=CH|kostiklysenko5|user|ifm|4520032409&x_lid=ch2923864409jjcae&x_c_chg=0&x_c_synced=0&x_as_i=%7B%22aeuCID%22%3A%22d0fe9dc1130744e1b63d4ce934a9fcfe-1681240350591-07065-_ePNSNV%22%2C%22af%22%3A%221320704%22%2C%22affiliateKey%22%3A%22_ePNSNV%22%2C%22channel%22%3A%22AFFILIATE%22%2C%22cv%22%3A%221%22%2C%22isCookieCache%22%3A%22N%22%2C%22ms%22%3A%221%22%2C%22pid%22%3A%22177275576%22%2C%22tagtime%22%3A1681240350591%7D&acs_rt=ff09b9035f874aa99563608d55332e92; cto_bundle=T_Q3ll9zbGVQaGFacXBZQXp0WXNpaHluM3pXbG95eCUyRjN4UXRWRXhlaEFMWGtobXB6SHlRdTVOaGwlMkJSbkpjVyUyRmdvdWU5WGFwdDkzRzVGZzVjRTEwM2d0T0RTN0VZMmglMkZIaG1qVHo4a1hJV294UUFlJTJGYzdYZG5Tc0VKbTNIcUFOVXJpaVdsa3JpU2pFSkNYRGltTVclMkZNT0RkY0ElM0QlM0Q; intl_common_forever=GB9qLbvh08f+d3MOsuvK6uu14e2NjnL3n7FTz3iznstiOLH8RE/LYQ==; aep_history=keywords%5E%0Akeywords%09%0A%0Aproduct_selloffer%5E%0Aproduct_selloffer%094001148163894%094000387045984%091005003338667739%091005005048285738%091005004279719268%091005004378803837%091005005054989620%091005004546160959; _ga=GA1.1.1905676086.1681194906; RT="z=1&dm=aliexpress.com&si=2ec0dde9-023e-4534-8e07-ab6724b0fc0b&ss=lgcn3ghr&sl=0&tt=0&rl=1&ul=431ot&hd=431q8"; _ga_VED1YSGNC7=GS1.1.1681247209.6.1.1681247210.0.0.0; l=fBMZx9XnNx5vvfWtKO5Courza779rCAX1sPzaNbMiIEGC6YdAfpI1LxQ2-7b4FtRRWXlwtTW4mDFErptLF3_WyD_vN0j4WZoITZ6Bemgl7SF.; tfstk=c-mcB_Noq71BRjxtNjZXYA_Swy8ca3-QMy4o4LhAIUT739gL3sV5zwuuOsPJE3b1.; isg=BK-vU-VsFxCxRxTkPgdiAExEPsW5VAN2w5WDNcE4AZ64EMQSwSZyxHKKlhguaNvu; JSESSIONID=A819B6DFDB047E618381AC89EBF66E08; xman_t=848ZhPdcyYQb8a0az9DwEeu9FVIlVW/Oq85GVas6/RriS0AoHFdWsv967D+ZfwsClB+kF10613oozolaY2BsSQQtNx00fOzEiy76boPb/iGkuAaLIcReg3yq+zp2NIhui822oKk4wSjyg05vVidZb99mhe86Det2s64EBOW80sotCBdlAFVXbNidI0M9nmWhChjtkqU8nf2OOFMatQYuOXVGP0D1sU3CaRLNHDbXgx0/HtpAtqB3NJvgKZlgcZUNSibVRKwvFi4sjRtI79vF3NFTbag+P0y2yfXuZuJ3RGDt0QBScuDf3ExxAnXvV6UQEoj/1Fx70OdSjarFU1x8nLm7Mkqi4Xqh0BaYSfhflZaYNfuNqENYly4ocHPUcqG9Np7UasZiFwF5g3B4LovP1PUrfWRahOre6tlYAn1NuRe3XxDiBc32LmYVUCfPP5I2BQIXXulewpb8pk4aDcODO0mJU3kpdT56vAh2I+XUiTIyvBrcg7LzBjr4eUjDE3pqLn+ALnudZV+R0pzibqOdKMbjKlT3v+KQhy1SiHKpxGzhrgLaNFkiAMGYvLeYLMYzpngiVAvxWMD4hjyLA+H9E9X29BMRqhDX1N6ruX4M0GPJNP1dUg7JUU3+N0GjJLAMDRmwP74a+0A5pylzIn8WWQZzotrJxbgs5h078lBKgA36rAZHMRdF4pTS+Nm47dKnVDZzrHf46Qq+En16bLkMugAm/RAlzEVCClrZ7dgPVCpnBC76nyag4L5S/u0PQ6sE',
    'pragma': 'no-cache',
    'sec-ch-ua': '"Google Chrome";v="111", "Not(A:Brand";v="8", "Chromium";v="111"',
    'sec-ch-ua-platform': 'Android',
    'sec-fetch-dest': 'navigate',
    'sec-fetch-site': 'none',
    'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Mobile Safari/537.36'
}


class CategoryJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, CategoryJSON):
            return obj.__dict__
        return json.JSONEncoder.default(self, obj)


# DELAYS
DELAY_ONLOAD = 5
DELAY_ONLOAD_SPEED = 2
DELAY_TIK = 1

# SORTINGS
MIN_RATING = 4.5
MIN_SOLDS = 300
DELIVERY_LIMIT = 37

driver = webdriver.Chrome()

categoryLinks = getLinks(driver)


class CategoryJSON:
    def __init__(self, categoryName):
        self.categoryName = categoryName
        self.JSONs = []


categoriesJSON = []

for category in (categoryLinks):
    print(category)
    print(Back.RED + category.categoryName + Back.RESET)
    categoryObject = CategoryJSON(category.categoryName)
    pageNumber = 1
    for link in category.links:
        response = requests.get(link, headers=headers)
        try:
            resJSON = response.json()
        except:
            print("Ошибка декодирования JSON")
        print(Back.RED + link + Back.RESET)

        if (len(resJSON["data"]["results"]) > 0):
            for product in (resJSON["data"]["results"]):
                if (
                    product["orders"] >= MIN_SOLDS
                    and
                    float(product["score"]) >= MIN_RATING if (
                        product["score"] != '' and product["score"] != '-') else 0 >= MIN_RATING
                ):
                    del product["discount"]
                    del product["discountMinPriceFormat"]
                    del product["freeShipping"]
                    del product["itemId"]
                    del product["sellerId"]
                    del product["originMinPriceFormat"]
                    categoryObject.JSONs.append(product)
        else:
            print(Back.YELLOW + f'Меньше {pageNumber} страниц' + Back.RESET)

        pageNumber += 1
    categoryObject.productsCount = len(categoryObject.JSONs)
    categoriesJSON.append(categoryObject)


productsCount = 0
os.mkdir('jsons')
for category in (categoriesJSON):
    productsCount += category.productsCount
    json_data = json.dumps(category, cls=CategoryJSONEncoder, indent=4)

    with open(f'jsons/products-{category.categoryName}.json', "w") as outfile:
        outfile.write(json_data)

print(productsCount)
