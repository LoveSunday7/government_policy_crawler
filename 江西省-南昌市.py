import requests

data = {
    "siteCode" : "3601000057",
    "tab" : "all",
    "qt" : "农业",
    "keyPlace" : "0",
    "sort" : "relevance",
    "fileType" : None,
    "timeOption" : "0",
    "locationCode" : "360000000000",
    "page" : 1,
    "pageSize" : 20,
    "ie" : "d5b83295-309f-49f8-a610-636c395f0d71"
}

response = requests.post("https://api.so-gov.cn/query/s",data=data)

with open("data.json","w",encoding="utf-8") as f:
    f.write(response.text)