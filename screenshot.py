import os
from subprocess import Popen, PIPE, call
import math
for file in os.listdir("/mnt/c/Users/Isiah/Videos/Community/Community.S01.Season.1.720p.5.1Ch.Web-DL.ReEnc-DeeJayAhmed"):
    if file.endswith(".mkv"):
        full_path = "/mnt/c/Users/Isiah/Videos/Community/Community.S01.Season.1.720p.5.1Ch.Web-DL.ReEnc-DeeJayAhmed/" + file 
        caption_file = "/mnt/c/Users/Isiah/Videos/Community/Community.S01.Season.1.720p.5.1Ch.Web-DL.ReEnc-DeeJayAhmed/" + file[:-3] + "srt"
        process = Popen('ffprobe -i ' + full_path + ' -show_entries format=duration -v quiet -of csv="p=0"', stdout=PIPE, stderr=PIPE, shell=True)
        stdout, stderr = process.communicate()
        stdout = math.floor(float(stdout))
        number_secs = stdout // 10
        for x in range(0, int(number_secs)):
            seek_time = x*15
            seek_time = str(seek_time)
            call("ffmpeg " "-ss " + seek_time + " -copyts -i " + full_path + " -vf subtitles=" + caption_file + " -q:v 3 -vframes 1 "+ file[10:16] +"_"+ str(x) + ".jpg", shell=True)
        