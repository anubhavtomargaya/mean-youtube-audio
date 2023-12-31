from pytube import YouTube
import mutagen
#update cipher.py according to 
#  https://github.com/pytube/pytube/issues/1201
# var_regex = re.compile(r"^\$*\w+\W")
from fastapi.logger import logger as lg
from pydantic import BaseModel
import os,subprocess
import logging
import subprocess
import datetime

# lg = logging.getLogger(__name__)
# logging.basicConfig(level=logging.DEBUG)


class MetaInfo(BaseModel):
    id:str =None
    title:str=None
    length:int=None
    views:int=None
    yt_thmb:str=None

class Records(BaseModel):
    time:datetime.datetime
    input_link:str
    user:str=None
    downloaded_in_s:float=False
    pid:int=None
    meta:MetaInfo=None


def vdo_info(yt:YouTube):
    # print(yt.__dict__)
    m = MetaInfo(id=yt.video_id, title=yt.title,length=yt.length,views=yt.views,yt_thmb=yt.thumbnail_url)
    # print(m.dict())
    return m

def download(url,play:bool=True):
    yt = YouTube(url)
    st = datetime.datetime.utcnow()
    lg.info('downloading file.....')
    video = yt.streams.filter(only_audio=True).first()
    lg.info('downloading file.....')
    out_file = video.download(output_path=".")
    lg.info('downloading file.....')
    lg.info('out_file: %s',out_file)
    et = datetime.datetime.utcnow()
    lg.info('downloading meta.....')
    m = vdo_info(yt)
    title = m.title
    lg.info("m: %s",m)
    lg.info("url: %s",url)
    lg.info("url: %s")
    ts = et-st
    lg.info("ts: %s",ts.total_seconds())
    returning = Records(time=datetime.datetime.utcnow(),input_link=url,user='self',downloaded_in_s=ts.total_seconds(),meta=m)
    lg.info("returning: %s",returning)
    if not play:
        return returning
    
    else:
        cmd = ["vlc",title]
        pid = run_cmd(cmd)
        lg.info('songs played pid: %s',pid)
        # f = subprocess.Popen(cmd)
        returning.pid=pid
        lg.info('songs played pid: %s',returning.pid)
        lg.info('typetype: %s',type(returning))
        # pid = f.pid
        return returning

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

file = 'TOPIA TWINS (Official Audio).mp4'


       

def update_tags(media_file,m:MetaInfo):
    with open('new.mp4', 'r+b') as file:
        media_file = mutagen.File(file, easy=True)
        print('before:', media_file.pprint(), end='\n\n')
        media_file['title'] = m.title
        media_file['album'] = 'xxx'
        media_file['artist'] = 'jesus'
        media_file['comment'] = m.yt_thmb
        media_file['description'] = f'{m.id}/{m.views}/{m.length}'
        media_file.save(file)
        print('after:', media_file.pprint(), end='\n\n')
        print(type(media_file), type(media_file.tags), end='\n\n')
# m=MetaInfo(id='xnd38cJ',title=file,length=230,views=12143,yt_thmb="abcd.com/sas/")
# print(update_tags(file,m))

# m = vdo_info(url)
# print(m.dict())
# title='TOPIA TWINS (Official Audio).mp3'
# cmd = ["vlc",title]
# url = 'https://www.youtube.com/watch?v=Hm1YFszJWbQ'
# print(download(url))
# print('hi')
# outfile = download(url)
# print(outfile.split('/')[-1])
# run_cmd()
# run_cmd(cmd)
# base, ext = os.path.splitext(out_file)
# new_file = base + '.mp3'
# os.rename(out_file, new_file)

# files = os.listdir(os.curdir)
# media = [x if '.mp4' in x else None  for x in files]
# print(files)
# print(media)
# res = {"media":[]}
# for i in media:
#     if i:
#         res['media'].append(i)
#     else: 
#         pass
# print(res)