from PIL import Image, ImageOps
import requests
import json
import random
import cv2
def build(filename = None):
    if filename is None:
        spook = Illumify(getVapor())
        filename = spook.getFilename()
        spooky_x, spooky_y = spook.generate()
    else:
        spooky_x, spooky_y = Illumify(filename)
    dst = copy = img = cv2.imread(filename, cv2.IMREAD_COLOR) 
    orig_h, orig_w = img.shape[:2]
    cv2.imwrite("image005."+filename.split(".")[1],dst)
    h_o,w_o = copy.shape[:2]
    step_h = h_o/5
    step_w = w_o/5
    for i in range(1,5):
        h = h_o - step_h*i
        w = w_o - step_w*i
        crop_image = img[spooky_x:spooky_x+h, spooky_y:spooky_y+h]
        dst = cv2.resize(crop_image,(orig_w,orig_h))
        cv2.imwrite("image00" + str(i) +"."+filename.split(".")[1],dst)

 
count = 30
def getVapor():
    print random
    payload = {"count":count}
    headers = {"user-agent":"Bot by /u/joshmcgrath"}
    res = requests.get('http://www.reddit.com/r/vaporwaveart/hot/.json',params=payload, headers = headers)
    resobj = json.loads(res.text)
    res_len = len(resobj["data"]["children"])
    pic_url =  resobj["data"]["children"][random.randrange(res_len - 1)]["data"]["preview"]["images"][0]["source"]["url"]
    pic = requests.get(pic_url)
    img_type = pic.headers['Content-Type'].split('/')[1]
    f = open('picture.'+img_type,'w')
    f.write(pic.content)
    return 'picture.'+img_type

class Illumify:
    def __init__(self, filename):
        self.illumitati_img = Image.open('illuminati.png','r')
        self.pic = Image.open(filename,'r')
        self.filename = filename
    def generate(self):
        height, width = self.pic.size
        ill_height, ill_width = self.illumitati_img.size
        self.illumitati_img = self.illumitati_img.resize((ill_height/12,ill_width/12))
        pos = (random.randrange(height/5)+ill_height/18, random.randrange(width/5)+ill_width/18)
        self.pic.paste(self.illumitati_img,pos, self.illumitati_img) 
        self.pic.save(self.filename.split('.')[0] + "illum."+ self.filename.split('.')[1])
        return pos
    def getFilename(self):
        return self.filename.split('.')[0] + "illum."+ self.filename.split('.')[1]
build()
