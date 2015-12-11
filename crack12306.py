#!/usr/bin/python
#encoding=utf-8


from PIL import Image, ImageDraw
from PIL import ImageFilter
import urllib
import urllib2
import re
import json
import tempfile
import os
import ssl
import urllib2
import simplejson
import re



if hasattr(ssl, '_create_unverified_context'):
    ssl._create_default_https_context = ssl._create_unverified_context


UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.89 Safari/537.36"

# pic_url = "https://kyfw.12306.cn/otn/passcodeNew/getPassCodeNew?module=login&rand=sjrand&0.21191171556711197"
pic_url = "http://pic3.zhimg.com/76754b27584233c2287986dc0577854a_b.jpg"


def get_img():
    resp = urllib.urlopen(pic_url)
    raw = resp.read()
    tmp_jpg = tempfile.NamedTemporaryFile(prefix="fuck12306_").name + ".jpg"
    with open(tmp_jpg, 'wb') as fp:
        fp.write(raw)

    im = Image.open(tmp_jpg)
    try:
        os.remove(tmp_jpg)
    except OSError:
        pass
    return im


def get_sub_img(im, x, y):
    assert 0 <= x <= 3
    assert 0 <= y <= 2
    #WITH = HEIGHT = 68
    left = 4 + (67 + 5) * x
    top = 41 + (67 + 5) * y
    right = left + 67
    bottom = top + 67

    return im.crop((left, top, right, bottom))


#通过百度上传图片
def baidu_stu_lookup(im):
    url = "http://stu.baidu.com/n/image?fr=html5&needRawImageUrl=true&id=WU_FILE_0&name=233.png&type=image%2Fpng&lastModifiedDate=Mon+Mar+16+2015+20%3A49%3A11+GMT%2B0800+(CST)&size="
    tmp_jpg = tempfile.NamedTemporaryFile(prefix="fuck12306_").name + ".png"
    im.save(tmp_jpg)
    raw = open(tmp_jpg, 'rb').read()
    try:
        os.remove(tmp_jpg)
    except OSError:
        pass
    url = url + str(len(raw))
    req = urllib2.Request(url, raw, {'Content-Type':'image/png', 'User-Agent':UA})
    resp = urllib2.urlopen(req)

    resp_url = resp.read()      # return a pure url

    print resp_url

#百度的图片搜索，结果很不理想，要么就猜出是啥，要么就啥也不显示，google还能显示类似的结果，还能进一步提取
    url = "http://stu.baidu.com/n/searchpc?queryImageUrl=" + urllib.quote(resp_url)

    req = urllib2.Request(url, headers={'User-Agent':UA})
    resp = urllib2.urlopen(req)
    #resp = google_image_search(resp_url)


    html = resp.read()

    result = open('result', 'w+')
    result.write(html)
    result.close()

    return baidu_stu_html_extract(html)

#通过google用图片搜索，需配置https代理，返回的是一堆js代码，需要进一步处理，未完成
def google_image_search(image_url):
    print "google_image_search start-----"
    #这个API过时关闭了，找过custom的api，只有用text搜索的定制
    #google_url = ('https://ajax.googleapis.com/ajax/services/search/images?' +
    #               'v=1.0&q=helloyang&start=4&userip=120.24.63.97')
    #这个地址用浏览器可以生效，在windows下用selenium可以进一步操作一下，不过用selenium了，还有必要搞这个网址吗...
    google_url = 'https://www.google.com/searchbyimage?hl=en&site=search&sa=X&image_url='+image_url
    request = urllib2.Request(google_url)
    response = urllib2.urlopen(request)

    return response

def baidu_stu_html_extract(html):
    #pattern = re.compile(r'<script type="text/javascript">(.*?)</script>', re.DOTALL | re.MULTILINE)
    pattern = re.compile(r"keywords:'(.*?)'")
    matches = pattern.findall(html)
    print matches
    if not matches:
        return '[UNKNOWN]'
    json_str = matches[0]

    json_str = json_str.replace('\\x22', '"').replace('\\\\', '\\')

    #print json_str

    #关键字原先是keyword，现在变成text了
    result = [item['text'] for item in json.loads(json_str)]
    print result

    return '|'.join(result) if result else '[UNKNOWN]'


def ocr_question_extract(im):
    # git@github.com:madmaze/pytesseract.git
    global pytesseract
    try:
        import pytesseract
    except:
        print "[ERROR] pytesseract not installed"
        return
    im = im.crop((130, 2, 180, 21))
    #im = pre_ocr_processing(im)
    # im.show()
    return pytesseract.image_to_string(im, lang='chi_sim').strip()


#这段预处理没什么用
def pre_ocr_processing(im):
    im = im.convert("RGB")
    width, height = im.size

    white = im.filter(ImageFilter.BLUR).filter(ImageFilter.MaxFilter(23))
    grey = im.convert('L')
    impix = im.load()
    whitepix = white.load()
    greypix = grey.load()

    for y in range(height):
        for x in range(width):
            greypix[x,y] = min(255, max(255 + impix[x,y][0] - whitepix[x,y][0],
                                        255 + impix[x,y][1] - whitepix[x,y][1],
                                        255 + impix[x,y][2] - whitepix[x,y][2]))

    new_im = grey.copy()
    binarize(new_im, 150)
    return new_im


#这段预处理没什么用
def binarize(im, thresh=120):
    assert 0 < thresh < 255
    assert im.mode == 'L'
    w, h = im.size
    for y in xrange(0, h):
        for x in xrange(0, w):
            if im.getpixel((x,y)) < thresh:
                im.putpixel((x,y), 0)
            else:
                im.putpixel((x,y), 255)

#二值判断,如果确认是噪声,用改点的上面一个点的灰度进行替换
#该函数也可以改成RGB判断的,具体看需求如何
def getPixel(image,x,y,G,N):
    L = image.getpixel((x,y))
    if L > G:
        L = True
    else:
        L = False

    nearDots = 0
    if L == (image.getpixel((x - 1,y - 1)) > G):
        nearDots += 1
    if L == (image.getpixel((x - 1,y)) > G):
        nearDots += 1
    if L == (image.getpixel((x - 1,y + 1)) > G):
        nearDots += 1
    if L == (image.getpixel((x,y - 1)) > G):
        nearDots += 1
    if L == (image.getpixel((x,y + 1)) > G):
        nearDots += 1
    if L == (image.getpixel((x + 1,y - 1)) > G):
        nearDots += 1
    if L == (image.getpixel((x + 1,y)) > G):
        nearDots += 1
    if L == (image.getpixel((x + 1,y + 1)) > G):
        nearDots += 1

    if nearDots < N:
        return image.getpixel((x,y-1))
    else:
        return None

# 降噪
# 根据一个点A的RGB值，与周围的8个点的RBG值比较，设定一个值N（0 <N <8），当A的RGB值与周围8个点的RGB相等数小于N时，此点为噪点
# G: Integer 图像二值化阀值
# N: Integer 降噪率 0 <N <8
# Z: Integer 降噪次数
# 输出
#  0：降噪成功
#  1：降噪失败
def clearNoise(image,G,N,Z):
    draw = ImageDraw.Draw(image)

    for i in xrange(0,Z):
        for x in xrange(1,image.size[0] - 1):
            for y in xrange(1,image.size[1] - 1):
                color = getPixel(image,x,y,G,N)
                if color != None:
                    draw.point((x,y),color)

def main():
    #im = get_img()
    im = Image.open("./screenshots/pic1.jpg")
    #print baidu_stu_lookup(im)
    print 'OCR Question:', ocr_question_extract(im)
    for y in xrange(2):
        for x in xrange(4):
            im2 = get_sub_img(im, x, y)
            clearNoise(im2, 50, 4, 4)
            #im3 = im2.filter(ImageFilter.SHARPEN)
            #clearNoise(im3, 50, 4, 4)
            result = baidu_stu_lookup(im2)
            print (y,x), result

def test():
    pattern = re.compile(r'rg-header _kk _wI.*_Icb _kk _wI')
    result = open('result','r+')
    content = result.read()
    result.close()
    match_results = pattern.match(content)
    print match_results


if __name__ == '__main__':
    main()

