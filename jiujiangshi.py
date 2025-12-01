from selenium.webdriver.common.by import By
from utils.InitSpider import *
from utils.Tools import *
from utils import settings
import requests

from time import sleep  

# 浏览器
url = settings.GOV_LINKS['九江市农业农村局']
Page = search_keywords_by_url(driver,url) # 返回迭代器

for key_class in Page :
    
    news_count = 0
    card_length = len(driver.find_elements(By.XPATH, "/html/body/div[1]/div/div[1]/div[6]/div[1]/div[2]/div"))
    
    for i in range(card_length):
        print("[driver]: 检测到非新闻，跳过一条信息")

        if driver.find_element(By.XPATH, f"/html/body/div[1]/div/div[1]/div[6]/div[1]/div[2]/div[{i+1}]/div[1]/div[1]/a").get_attribute("class") == "jcse-result-box":
            continue

        

