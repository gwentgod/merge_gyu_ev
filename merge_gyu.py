import os
import struct
import sys
from tqdm import tqdm

def decode():
    os.system("fixipgyu.exe def.rld")

def gyu_to_bmp():
    os.system("for /r %i in (*.gyu) do gyu2bmp.exe %i")

def delete_gyu():
    os.system("for /r %i in (*.gyu) do del %i")

if '-d' in sys.argv:
    decode()
if '-g' in sys.argv:
    gyu_to_bmp()

for files in tqdm(os.listdir("./")):
    if os.path.isdir(files):
        for file in os.listdir(files):
            file=os.path.join(files,file)

            ext=file.split(".")[-1]
            file_name=file.split(".")[0]+".bmp"
            if ext=="gyu":
                with open(file,"rb") as gyu:
                    data=gyu.read()

                    x,y=struct.unpack("<2I",data[16:24]) #得到差分尺寸
            
                    length=len(data)
                    num=length-1

                    while data[num]==0: #判断末尾有多少0
                        num=num-1
                    if length-num-1<=3: #此时不是差分
                        continue
            
                    current_num=num
                    while data[current_num]!=0:
                        current_num=current_num-1 

                    if  num+1-current_num>30: #此时不是差分
                        continue

                    location=data[current_num:num+1].decode(encoding="utf8").split(",") #得到覆盖坐标信息
            
                    base_file=os.path.join(location[0][-4:-2],location[0][-4:]+".bmp")
                    size=str(x)+"x"+str(y)+"+"+location[1]+"+"+location[2]

                    os.system("magick "+base_file+" -compose over "+file_name+" -geometry "+size+" -composite "+file_name)

if '-del' in sys.argv:
    delete_gyu()
