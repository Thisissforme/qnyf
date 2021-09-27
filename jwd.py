# __author:Chou
# data:2021/9/25
#获取经纬度
import requests
import pandas as pd
import json
import random
headers1={
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36 Edg/90.0.818.56"
}
headers2={
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.101 Safari/537.36"
}
headers=[headers1,headers2]
# print(headers)
def loc(location):
    base_url="https://apis.map.qq.com/jsapi?qt=geoc&addr="
    data=requests.get(base_url+location,headers=random.choice(headers))
    # print(type(data))
    inf=data.json()
    jwd_x=inf['detail']['pointx']
    jwd_y=inf['detail']['pointy']
    JWD=jwd_y+','+jwd_x
    return JWD

# print(loc("河南省周口市"))