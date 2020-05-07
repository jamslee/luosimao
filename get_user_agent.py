import requests
import json
from copyheaders import headers_raw_to_dict
from lxml import etree
req = requests.Session()

headers = b'''Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3
Accept-Encoding: gzip, deflate
Accept-Language: zh-CN,zh;q=0.9
Connection: keep-alive
Cookie: Hm_lvt_0fa7b8c467469bd8f2eaddd5dc1d440d=1562556685; Hm_lpvt_0fa7b8c467469bd8f2eaddd5dc1d440d=1562556740
Host: www.fynas.com
Referer: http://www.fynas.com/ua/search?d=&b=&k=&page=1
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'''

headers = headers_raw_to_dict(headers)
all_ua = []
for i in range(1,11):
    try:
        res = req.get('http://www.fynas.com/ua/search?d=&b=%E5%BE%AE%E4%BF%A1&k=&page='+str(i),headers = headers)
        print('all:{}'.format(i))
        if res.status_code == 200:
            res.encoding = res.apparent_encoding
            content = res.content
            root = etree.HTML(content)
            ua = root.xpath('//tr/td[4]/text()')
            UA = list(ua)
            UA.pop(0)
            # for u in UA:
            #     with open('user_agent.txt','a+') as f:
            #         f.writelines(u+'\n')
            all_ua.extend(UA)

        else:
            print('loss:{}'.format(i))
    except Exception as e:
        print('except:{}'.format(e))



with open('ua.py','w') as f:
    aa = json.dump(all_ua,f, ensure_ascii=False,separators=(',\n ', ': '))
