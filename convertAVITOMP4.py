
#pip install imageio
#pip install imageio-ffmpeg

import imageio
import os, sys

class TargetFormat(object):
    GIF = ".gif"
    MP4 = ".mp4"
    AVI = ".avi"

def convertFile(inputpath, filename, targetFormat):
    outputpath = inputpath+filename+targetFormat
    inputpath = inputpath+filename+".avi"
    
    print("converting\r\n\t{0}\r\nto\r\n\t{1}".format(inputpath, outputpath))

    reader = imageio.get_reader(inputpath)
    fps = reader.get_meta_data()['fps']

    writer = imageio.get_writer(outputpath, fps=fps)
    for i,im in enumerate(reader):
        writer.append_data(im)
    writer.close()
    print("Done.")

print(os.getcwd())

#url = "D:\TelegramBOT\\"
#convertFile(url,"outpy", TargetFormat.GIF)
