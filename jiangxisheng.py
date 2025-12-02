from selenium.webdriver.common.by import By
from utils.InitSpider import *
from utils.Tools import *
from utils import settings
import requests

from time import sleep  

# 打开网页
driver.get(settings.GOV_LINKS['江西省农业农村厅'])
SearchBox = driver.find_element(By.XPATH, "//*[@id=\"allSearchWord\"]")
Page = search_keywords(SearchBox) # 返回迭代器

for key_class in Page:
    count = check_ok(driver,"/html/body/div[2]/div[2]/div[3]/div[1]/div[1]/p/span")
    parse_count = 0

    if count == 0:
        print("[search]: 搜索结果为0,跳过该关键词")
        continue
    
    while True:
        link_dict = {}
        length = len(driver.find_elements(By.XPATH, "//*[@id=\"wordGuideList\"]/div"))

        for i in range(length):
            
            print(f"[parser]: 正在解析第{parse_count+1}条信息")
            # 获取页面标题
            url = driver.find_element(By.XPATH, f"/html/body/div[2]/div[2]/div[3]/div[21]/div[{i+1}]/div[1]/a").get_attribute("href")
            try:
                response = requests.get(url,timeout=3)
                if response.status_code!= 200:
                    parse_count += 1
                    print(f"[parser]: 第{parse_count+1}条信息响应超时,跳过")
            except:
                parse_count += 1
                print(f"[parser]: 第{parse_count+1}条信息获取失败,跳过")
                continue
            response.encoding = response.apparent_encoding
            infomation = parse_html(response.text)

            # 检查是否有附件
            attachment_links = {}
            try:
                attachment_links[
                        driver.find_element(By.XPATH, f"/html/body/div[2]/div[2]/div[3]/div[21]/div[{i+1}]/div[2]/div/div/a").text
                    ] = driver.find_element(By.XPATH, f"/html/body/div[2]/div[2]/div[3]/div[21]/div[{i+1}]/div[2]/div/div/a").get_attribute("href")
            except:
                pass

            card = Information(
                title=infomation['title'],
                publisher=infomation['content_source'],
                time=infomation['pub_date'],
                content=infomation['content'],
                attachment_links=attachment_links,
                file_class=key_class
            )

            if len(attachment_links) > 0:
                print(f"[parser]: 检测到附件,开始下载")
                card.download_attachment()
                print(f"[parser]: 下载完成")
            card.write_to_file()

            print(f"[parser]: 写入文件完成")
            print(f"[parser]: 第{parse_count+1}条信息解析完成")
            parse_count += 1
        if parse_count <= count:
            print("[WebDriver]: 点击下一页") 
            k = len(driver.find_elements(By.XPATH, "/html/body/div[2]/div[2]/div[3]/div[25]/ul[2]/li"))
            while True:
                try:
                    driver.find_element(By.XPATH, f"/html/body/div[2]/div[2]/div[3]/div[25]/ul[2]/li[{k}]/a").click()
                    break
                except:
                    print("[WebDriver]: 点击下一页失败，等待1s后重试")
                    sleep(1)
            count = check_ok(driver)
        else:
            print("[WebDriver]: 切换关键词")
            break

print("[WebDriver]: 退出浏览器")
driver.quit()
print("[WebDriver]: 成功退出浏览器")
print("[log]: 程序结束")


