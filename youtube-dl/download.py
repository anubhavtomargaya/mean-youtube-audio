from pytube import YouTube
#update cipher.py according to 
#  https://github.com/pytube/pytube/issues/1201
# var_regex = re.compile(r"^\$*\w+\W")
from fastapi.logger import logger as lg
import os,subprocess
import logging
import subprocess

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)

def download(url,play:bool=False):
    yt = YouTube(url)
    lg.info('downloading file.....')
    video = yt.streams.filter(only_audio=True).first()
    lg.info('downloading file.....')
    out_file = video.download(output_path=".")
    lg.info('downloading file.....')
    logger.info('out_file: %s',out_file)
    title = out_file.split('/')[-1]
    if not play:
        return out_file
    else:
        cmd = ["vlc",title]
        pid = run_cmd(cmd)
        # f = subprocess.Popen(cmd)
        # logger.info(f.__dict__)
        # pid = f.pid
        return title,pid

url = 'https://www.youtube.com/watch?v=J4nvbKBuEBU'
# 

# subprocess.Popen(["rm","-r","some.file"])
def kill_by_pid(pid):
    cmd = ["kill","-9",pid]
    f = subprocess.run(cmd)
    return True

def kill_all_vlc():

    cmd = ["killall","-9",'vlc']
    f = subprocess.run(cmd)
    return True

def run_cmd(cmd:list):
    f= subprocess.Popen(cmd)
    pid =f.pid
    print(pid)
    print(type(f))
    print(f.__dict__)
    return pid

# title='TOPIA TWINS (Official Audio).mp3'
# cmd = ["vlc",title]

# print(outfile)
# outfile = download(url)
# print(outfile.split('/')[-1])
# run_cmd()
# run_cmd(cmd)
# base, ext = os.path.splitext(out_file)
# new_file = base + '.mp3'
# os.rename(out_file, new_file)

files = os.listdir(os.curdir)
media = [x if '.mp4' in x else None  for x in files]
print(files)
print(media)
res = {"media":[]}
for i in media:
    if i:
        res['media'].append(i)
    else: 
        pass
print(res)