from selenium.webdriver.common.by import By
from utils.InitSpider import *
from utils.Tools import *
from utils import settings
import requests

from time import sleep  

url = settings.GOV_LINKS['吉安市农业农村局']
# 吉安市禁止直接跳转到搜索页面，需要从主页面点击进去
driver.get(url)
driver.find_element(By.XPATH,"//*[@id=\"search\"]").click()
check_ok(driver,"/html/body/div[2]/div/p/span[1]")
SearchBox = driver.find_element(By.XPATH, "//*[@id=\"keyword\"]")
Page = search_keywords(SearchBox) # 返回迭代器

for page in Page:
    check_ok(driver,"/html/body/div[2]/div/p/span[1]",time=2)
    card_count = len(driver.find_element(By.XPATH,"/html/body/div[3]/div/div/div[1]/div/div[1]/div[4]/ul"))
    count = 0
    for i in range(card_count):
        title = driver.find_element(By.XPATH,f"/html/body/div[3]/div/div/div[1]/div/div[1]/div[4]/ul[{i+1}]/li[1]/a").get_attribute("title")
        data = driver.find_element(By.XPATH,f"/html/body/div[3]/div/div/div[1]/div/div[1]/div[4]/ul[{i+1}]/li[4]/span").text.replace("发布日期：","")
        content = driver.find_element(By.XPATH,f"/html/body/div[3]/div/div/div[1]/div/div[1]/div[4]/ul[{i+1}]/li[3]").text
        link = driver.find_element(By.XPATH,f"/html/body/div[3]/div/div/div[1]/div/div[1]/div[4]/ul[{i+1}]/li[1]/a").get_attribute("href")

        # 下载页面
        response = requests.get(link)
        with open(f"./testforjian/{count}.html", "wb") as file:

            file.write(response.content)



