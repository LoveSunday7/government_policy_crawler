import requests

data = {
    "code": "183f883089d",
    "configCode": "",
    "codes": "",
    "searchWord": "农业",
    "historySearchWords": [],
    "dataTypeId": "3",
    "orderBy": "related",
    "searchBy": "all",
    "appendixType": "",
    "granularity": "ALL",
    "beginDateTime": "",
    "endDateTime": "",
    "isSearchForced": 0,
    "filters": [],
    "pageNo": 3,
    "pageSize": 10
}

response = requests.post("https://zmhd.jiujiang.gov.cn/irs/front/search",data=data)

with open("data.json","w",encoding="utf-8") as f:
    f.write(response.text)

