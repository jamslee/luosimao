from Crypto.Cipher import AES
from PIL import Image
import base64, json,random,time,hashlib,ssl,requests
import io,config,re
from yolo import *
def strGetlen(strn,strx,strend):
    sint = strn.find(strx)
    strn = strn[sint + len(strx):]
    if strend=="":
        return strn
    eint = strn.find(strend)
    return  strn[:eint]

def get_image(res,s):
    getImg = 'https://captcha.luosimao.com/api/frame?s=' + s + '&i=_6qms5tqki&l=zh-cn'
    rep = res.get(getImg,verify=False,headers = config.Headers).text
    aa = eval(strGetlen(rep, 'l: ', '}'))
    imgUrl = strGetlen(rep, 'p:[\'', '\'')
    all_path = []
    ssl._create_default_https_context = ssl._create_unverified_context
    image = res.get(imgUrl,verify=False,headers = config.Headers).content

    # 读取图片并打开
    tmpIm = io.BytesIO(image)
    im = Image.open(tmpIm)
    for i in aa:
        xx = int(i[0])
        yy = int(i[1])
        box = (xx, yy, xx + 20, yy + 80)
        new_im = im.crop(box)
        all_path.append(new_im)
    # 图片压缩后的大小
    width_i = 20
    height_i = 80
    # 每行每列显示图片数量
    line_max = 15
    row_max = 2
    # 参数初始化
    num = 0
    toImage = Image.new('RGBA', (width_i * line_max, height_i * row_max))
    for i in range(0, row_max):
        yy = i * 80
        xx = 0
        for j in range(0, line_max):
            pic_fole_head = all_path[num]
            tmppic = pic_fole_head.resize((width_i, height_i))
            loc = (int(xx), int(yy))
            # print("第" + str(num) + "存放位置" + str(loc))
            toImage.paste(tmppic, loc)
            xx = xx + 20
            num = num + 1
    return [toImage,getImg]

def pad(data):
    length = 16 - (len(data) % 16)
    return data + (chr(length) * length).encode()
def unpad(data):
    return data[:-(data[-1] if type(data[-1]) == int else ord(data[-1]))]
def encrypt(content, key,iv):
    key = key.encode()
    key_iv = iv.encode()
    aes = AES.new(key, AES.MODE_CBC, key_iv)
    return base64.b64encode(aes.encrypt(pad(content.encode()))).decode()
# 解密
def decrypt(content, keyx,iv):
    key = keyx.encode()
    encrypted = base64.b64decode(content)
    key_iv = iv.encode()
    aes = AES.new(key, AES.MODE_CBC, key_iv)
    return unpad(aes.decrypt(encrypted))

def getToken(res,site_key):
    geturl = 'https://captcha.luosimao.com/api/widget?k=' + site_key + '&l=zh-cn&s=normal&i=_6qms5tqki'
    res = res.get(geturl,verify=False,headers = config.Headers).text
    data_token = strGetlen(res, 'data-token="', '"')
    return data_token

def getData(res,data_token,site_key):
    strurl = 'https://captcha.luosimao.com/api/request?k=' + site_key + '&l=zh-cn'
    pix = ':'.join([str(random.randint(600, 1080)), str(random.randint(480, 960))])
    bg = config.Headers['User-Agent'] + '||' + data_token + '||' + pix + '||win32||webkit'
    dt1 = str(int(time.time() * 1000))
    dt2 = str(int(time.time() * 1000) + random.randint(1000, 9999))
    b_str = '166,18:' + dt1 + '||164,27:' + dt2
    bg = encrypt(bg, config.aes_configs['AES_KEY'], config.aes_configs['AES_IV'])
    b_str = encrypt(b_str,  config.aes_configs['AES_KEY'],  config.aes_configs['AES_IV'])
    postData = 'bg=' + bg + '&b=' + b_str
    rep = res.post(strurl,verify=False,data=postData,headers = config.Headers).json()
    return rep

def get_Verify(res,rep_key,loc,h_str,getImg):
    v_str = encrypt(loc, rep_key, config.aes_configs['AES_IV'])
    user_verify = 'https://captcha.luosimao.com/api/user_verify'
    v_str = v_str.replace('+', '-').replace('/', '_').replace('=', '')
    postData = 'h=' + h_str + '&v=' + v_str + '&s=' + hashlib.md5(loc.encode()).hexdigest()
    config.Headers['Referer'] = getImg
    rep = res.post(user_verify,verify=False,data=postData,headers = config.Headers).json()
    return rep


def wordtotype(types):
    result = []
    all_type = types.split(',')
    for ty in all_type:
        if ty in config.dict_type:
            result.append(config.dict_type[ty])
    return result

def run(yolo,site_key):
    res = requests.Session()
    try:
        data_token = getToken(res,site_key)
        rep = getData(res, data_token,site_key)
        h_str = rep['h']
        ans = rep['w']
        ans_list = re.findall(r'<i>(.*?)</i>', ans)[0]
        result_l = wordtotype(ans_list)
        rep_key = rep['i']
        rep_s = rep['s']
        im, getImg = get_image(res,rep_s)

        r_image = yolo.detect_image(im, str(round(time.time() * 1000)) + '.png')
        back_loc = []
        for ii in range(len(result_l)):
            for y in r_image[1]:
                if result_l[ii] == y['class']:
                    back_loc.append(','.join(y['loc']))
        r_image[0].show()
        if len(back_loc) < 1:
            return {'code':'img error'}
        # print(back_loc)
        loction = '#'.join(back_loc)
        rep = get_Verify(res, rep_key,loction, h_str, getImg)
    except:
        rep = {'code':'400'}
    return rep

if __name__ == '__main__':
    yolo = YOLO()
    bbb = run(yolo,'e7b4d20489b69bab25771f9236e2c4be')
    print(bbb)