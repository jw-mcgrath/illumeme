import requests
import json
import random
count = 30
def getVapor():
    payload = {"count":count}
    headers = {"user-agent":"Bot by /u/joshmcgrath"}
    res = requests.get('http://www.reddit.com/r/vaporwaveart/hot/.json',params=payload, headers = headers)
    resobj = json.loads(res.text)
    res_len = len(resobj["data"]["children"])
    pic_url =  resobj["data"]["children"][random.randrange(res_len - 1)]["data"]["preview"]["images"][0]["source"]["url"]
    pic = requests.get(pic_url)
    f = open('picture','w')
    f.write(pic.content)

getVapor()
