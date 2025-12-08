# 我他妈直接爬接口
import requests
import json
from math import ceil
from utils.settings import *
from utils.Tools import Information

url = "https://nyj.xinyu.gov.cn/u/search/list/28ad8169f137457eb09f517bffac37f9"
base_url = "https://nyj.xinyu.gov.cn"

data = {
    'keywords': '{}',
    'currentPage': '{}',
    'number': '{}'
}

data["number"] = 15

# response = requests.post(url, data=json.dumps(data))
# print(response.status_code)
# with open('./xinyushi.json', 'w', encoding='utf-8') as f:
#     f.write(response.content)

if __name__ == '__main__':
    for key1 in KEY_MAP:
        for key2 in KEY_MAP[key1]:
            for key3 in KEY_MAP[key1][key2]:
                # URL Decode
                data["keywords"] = key3
                data["currentPage"] = 1
                max_page = 1

                count = 0

                print(f"[robot]: 正在爬取关键词{key1}->{key2}->{key3}的新闻")
                while True:
                    response = requests.post(url, data=data)


                    list_data = json.loads(response.content)
                    if list_data["data"]["page"]["allRow"] == 0:
                        print(f"[robot]: 关键词{key1}->{key2}->{key3}的新闻无搜索结果")
                        break
                    max_page = ceil(list_data["data"]["page"]["allRow"] / 15)

                    print(f"[robot]: 正在爬取{data["currentPage"]}/{max_page}页数据")

                    # 详情页获取
                    for card in list_data["data"]["page"]["list"]:
                        print(f"[robot]: 正在爬取{card['TITLE']}",end="\r",flush=True)
                        title = card["TITLE"]
                        date = card["PUBLISHED_TIME_FORMATED"]
                        detail_url = base_url + card["URL_COMP"]
                        print(detail_url)
                        response = requests.get(detail_url)
                        
                        count+=1
                        with open(f"./test/{count}.html","wb") as f:
                            
                            f.write(response.content)





                        # info = Information(
                        #     title=title,
                        #     time=date,
                        #     file_class=f"./农业分类目录/{key1}/{key2}/{key3}"
                        # )

                        print(f"[robot]: 正在爬取{card['TITLE']}---[完成]")

                    print(f"[robot]: 爬取{data["currentPage"]}/{max_page}页数据结束")
                    data["currentPage"] += 1
                    if data["currentPage"] > max_page:
                        print(f"[robot]: 关键词{key1}->{key2}->{key3}的新闻爬取结束")
                        break

                print(f"[robot]: 正在爬取关键词{key1}->{key2}->{key3}的新闻结束")