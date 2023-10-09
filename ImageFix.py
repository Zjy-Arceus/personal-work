from PIL import Image
import os

path = "./chingmu.png"
im = Image.open(path)
   
out = im.resize((100, 80), Image.ANTIALIAS)       
dir, suffix = os.path.splitext(path)
outfile = '{}-out{}'.format(dir, suffix)
out.save(outfile)