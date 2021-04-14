import random

from PIL import Image, ImageDraw, ImageFont
import requests
from lxml import etree
import base64
from flask import Flask
import demjson
import os
import traceback
app = Flask(__name__)


def url_encode(url):
    return str(base64.urlsafe_b64encode(str(url).encode()).decode())


def url_decode(url):
    return base64.urlsafe_b64decode(url.encode('utf-8')).decode()


def process_img(ori_img, p_img, title, s_x, s_y, width, height, c_x, c_y, f_size, color):
    p_img = p_img.resize((width, height))
    ori_img.paste(p_img, (s_x, s_y))
    text_size = f_size
    draw = ImageDraw.Draw(ori_img)
    font_style = ImageFont.truetype("pingfangSS.TTF", text_size, encoding="utf-8")
    # 绘制文本
    draw.text((c_x, c_y), title, color, font=font_style)
    return ori_img


def qndxx_list():
    url = "http://news.cyol.com/gb/channels/vrGlAKDl/index.html"
    x_path = "/html/body/div/div/ul/li/h3"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chro"
                                "me/89.0.4389.90 Safari/537.36 Edg/89.0.774.54"}
    dom = requests.get(url, headers=headers).content.decode('utf-8')
    dom_tree = etree.HTML(dom)
    links = dom_tree.xpath(x_path)
    print(links)
    l_list = []
    for item in links:
        print(item)
        l_list.append({
            'title': item.xpath('a/text()')[0],
            'url': url_encode(item.xpath('a/@href')[0])
        })
    return l_list


def query_pic(b64url):
    try:
        s = url_decode(b64url)
        final_pic = ""
        url = s[0:len(s)-len(s.split('/')[-1])-1] + "/images/end.jpg"
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chro"
                                "me/89.0.4389.90 Safari/537.36 Edg/89.0.774.54"}
        pic = requests.get(url, headers=headers).content
        try:
            os.mkdir(f"./qndxx/{b64url}")
        except:
            pass
        file = open(f"./qndxx/{b64url}/ori.jpg", 'wb')
        file.write(pic)
        img = Image.open(f'./qndxx/{b64url}/ori.jpg')
        html = requests.get(s).content.decode()
        x_path = "/html/head/title/text()"
        title = etree.HTML(html).xpath(x_path)[0]
        for root, dirs, files in os.walk('./frame'):
            # root 表示当前正在访问的文件夹路径
            # dirs 表示该文件夹下的子目录名list
            # files 表示该文件夹下的文件list
            # 遍历文件
            for f in files:
                path = os.path.join(root, f)
                if f[-5:len(f)] == '.json':
                    d_json = demjson.decode_file(path)
                    p_path = f"./frame/{d_json['id']}.jpg"
                    if os.path.exists(f"./qndxx/{b64url}/{d_json['id']}.jpg"):
                        continue
                    pri_img = Image.open(f"./qndxx/{b64url}/ori.jpg")
                    ori_img = Image.open(p_path)
                    result = process_img(ori_img, pri_img, title, d_json['start_x']
                                         , d_json['start_y'], d_json['width'],
                                         d_json['height'], d_json['c_x'], d_json['c_y'],
                                         d_json['f_size'], d_json['color'])
                    result.save(f"./qndxx/{b64url}/{d_json['id']}.jpg")
        for root, dirs, files in os.walk('./frame'):
            all = 10
            pic = open(f"./qndxx/{b64url}/{random.randint(1,all-1)}.jpg", 'rb')
            base64_data = base64.b64encode(pic.read())  # 使用base64进行加密
            final_pic = base64_data
            pic.close()
    except Exception as e:
        return {
            'code': -1,
            'msg': f"""str(Exception):\t {str(Exception)}<br>
str(e):\t\t {str(e)}<br>
repr(e):\t {repr(e)}<br>
e.message:\t {e}<br>
traceback.print_exc():{traceback.print_exc()}<br>
traceback.format_exc():{traceback.format_exc()}<br>"""}
    return {
        'code': 0,
        'pic': f"data:image/png;base64,{final_pic.decode()}"
    }


@app.route('/')
def forbid():
    return '<h1>403 Forbidden</h1>', 403


@app.route('/smw/qndxx')
def qn():
    text = """<!DOCTYPE html>
    <html xmlns="http://www.w3.org/1999/xhtml" lang="zh-cn">
    <style>
        body{
            text-align: center;
        }
    </style>
    <head>
        <title>青年大学习生成器</title>
    </head>
    <body>
        <h1>青年大学习生成器</h1>
        <h2>点击相应链接即可生成，仅提供最近几期</h2>
        <p>Made By 不做评论</p>"""
    q_list = qndxx_list()
    for item in q_list:
        text += f'<p><a href="./qnxx/{item["url"]}"> {item["title"]} </a></p>'
    text += "<br>------------<br>El Psy Congroo.<br></body></html>"
    return text


@app.route('/smw/qnxx/<url>')
def qnxx(url):
    result = query_pic(url)
    if result['code'] != 0:
        return f"""<h1>502 Error<h1>
        <h2>请与管理员联系！</h2>
        <h3>错误信息：</h3>
        {result['msg']}""", 502
    return """<!DOCTYPE html>
    <html xmlns="http://www.w3.org/1999/xhtml" lang="zh-cn">
    <style>
        body{
            text-align: center;
        }
    </style>
    <head>
        <title>青年大学习生成器</title>
    </head>
    <body>
        <h1>长按保存</h1>
        <img src="%s" alt="image"></img>
    </body>""" % result['pic']


if __name__ == '__main__':
    app.run(host="0.0.0.0")