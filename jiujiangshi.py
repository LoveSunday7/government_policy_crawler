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

    while True:
        count = check_ok(driver,"/html/body/div[1]/div/div[1]/div[4]/div[1]/span")

        # 检查是否无查询结果
        if count == 0:
            try:
                info = driver.find_element(By.XPATH,"/html/body/div[1]/div/div[1]/div[6]/div[1]/div[4]/div[1]")
                if '抱歉' in info:
                    print("[search]: 该关键词无搜索结果，跳过该关键词")
                    break
            except:
                print("[driver]: 检测到页面非正常加载完成，暂停1s重试")
                sleep(1)
                continue
        break

    news_count = 0
    
    while True:
        card_length = len(driver.find_elements(By.XPATH, "/html/body/div[1]/div/div[1]/div[6]/div[1]/div[2]/div"))
        for i in range(card_length):
            try:
                if driver.find_element(By.XPATH, f"/html/body/div[1]/div/div[1]/div[6]/div[1]/div[2]/div[{i+1}]").get_attribute("class") == "jcse-result-box":
                    print("[robot]: 检测到非新闻，跳过")
                    continue
            except:
                pass

            try:
                link = driver.find_element(By.XPATH,f"/html/body/div[1]/div/div[1]/div[6]/div[1]/div[2]/div[{i+1}]/a[1]").get_attribute("href")
            except:
                print("[robot]: 该新闻结构异常执行跳过")
                continue
            publisher = driver.find_element(By.XPATH,f"/html/body/div[1]/div/div[1]/div[6]/div[1]/div[2]/div[{i+1}]/a[2]").text
            
            # 下载页面
            print(f"[parser]: 正在下载{link}的新闻")
            try:
                link = link.replace("http://","https://")
                respose = requests.get(link)
            except:
                print(f"[robot]: 下载{link}失败，跳过")
                continue
            print(f"[robot]: 下载{link}成功")

            with open(f"./test/{publisher}.html", "wb") as f:
                f.write(respose.content)



        # 换页操作代码
        # 检查是否为最后一页
        try:
            lab_count = len(driver.find_elements(By.XPATH,"/html/body/div[1]/div/div[1]/div[6]/div[1]/div[5]/div/a"))
            value = driver.find_element(By.XPATH,f"/html/body/div[1]/div/div[1]/div[6]/div[1]/div[5]/div/a[{lab_count}]").get_attribute("class")
            if value == 'next lose':
                print("[WebDriver]: 该关键词数据爬取完毕，切换关键词继续爬取")
                continue
        except:
            print("[WebDriver]: 该关键词数据爬取完毕，切换关键词继续爬取")
            continue

        # 点击下一页
        try:
            print("[WebDriver]: 点击下一页，并等待页面加载")
            lab_count = len(driver.find_elements(By.XPATH,"/html/body/div[1]/div/div[1]/div[6]/div[1]/div[5]/div/a"))
            driver.find_element(By.XPATH,f"/html/body/div[1]/div/div[1]/div[6]/div[1]/div[5]/div/a[{lab_count}]").click()                
            sleep(1)
        except:
            print("[WebDriver]: 该关键词数据爬取完毕，切换关键词继续爬取")
            continue

print("[WebDriver]: 退出浏览器")
driver.quit()
print("[WebDriver]: 成功退出浏览器")
print("[log]: 程序结束")

# 尚未完成