import requests
import base64,time

with open(r"/Users/mac/Downloads/data_ttt/aaa/蚝前_1561785262.png", "rb") as f:
    img_bytes = f.read()

bs64_img = base64.b64encode(img_bytes).decode()
# 提交图片参数必须为base64 格式

while True:
    t1 = int(time.time()*1000)
    site_key = 'a3234814f9ed118d0bc94b4a3f3df3b3'
    jsondata = {'site_key': site_key}
    result = requests.post('http://bababy.vicp.cc:7790/api/', json=jsondata).json()
    t2 = int(time.time() * 1000)
    print(t2-t1)
    print(result)
