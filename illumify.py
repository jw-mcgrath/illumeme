from PIL import Image, ImageDraw
import random
class Illumify:
    def __init__(self, filename):
        self.illumitati_img = Image.open('illuminati.png','r')
        self.pic = Image.open(filename,'r')
        #self.illumitati_img.convert("RGBA")
        #self.transparency(self.illumitati_img)
        #self.pic.convert("RGBA")
        self.filename = filename
    def generate(self):
        height, width = self.pic.size
        ill_height, ill_width = self.illumitati_img.size
        self.illumitati_img = self.illumitati_img.resize((ill_height/12,ill_width/12))
        pos = (random.randrange(height/5)+ill_height/18, random.randrange(width/5)+ill_width/18)
        self.pic.paste(self.illumitati_img,pos, self.illumitati_img) 
        self.pic.save(self.filename.split('.')[0] + "illum."+ self.filename.split('.')[1])
    def transparency(self, image):
        datas = image.getdata()
        newData = []
        for item in datas:
            if item[0] == 0 and item[1] == 0 and item[2] == 0:
                newData.append((1,1,1,0))
            else:
                newData.append(item)
        image.putdata(newData)
