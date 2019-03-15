from PIL import Image, ImageDraw
import sys
import struct
import os
import math

zipdata=bytearray()
original_image=None

if (len(sys.argv) < 2):
    print("Please supply a zip file or whatever")
    exit(1)

if (len(sys.argv)==3):
    print("Combining with ", sys.argv[2])
    original_image=Image.open(sys.argv[2]) 

print("reading data...")
with open(sys.argv[1], "rb") as zipfile:
    zipdata = bytearray(zipfile.read())

DATA_LEN = len(zipdata)
PXCOUNT = int(DATA_LEN/3)+10
WIDTH= int(2*math.sqrt(PXCOUNT))
HEIGHT=int(PXCOUNT/WIDTH)+20+(0 if original_image is None else original_image.height)

im = Image.new('RGB', (WIDTH,HEIGHT))

im.save('nicememe.bmp')

print("writing data...")
with open("nicememe.bmp","rb+") as bmp:
    bmp.seek(10)
    img_offset=struct.unpack('I', bmp.read(4))
    # print('Image Offset: %s' % img_offset)
    bmp.seek(img_offset[0])
    bmp.write(zipdata)

print("creating png...")
meme = Image.open('nicememe.bmp')

if original_image is not None:
    meme.putdata(original_image.resize((WIDTH,original_image.height)).getdata())

d = ImageDraw.Draw(meme)
d.text((WIDTH/2-20, 0 if original_image is None else original_image.height+5),"SAVE AS 24-BIT BMP. UNZIP WITH ARCHIVING SOFTWARE.")

meme.save("%s.png"%sys.argv[1])

os.remove("nicememe.bmp")