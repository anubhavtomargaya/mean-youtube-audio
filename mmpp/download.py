from pytube import YouTube
import mutagen
#update cipher.py according to 
#  https://github.com/pytube/pytube/issues/1201
# var_regex = re.compile(r"^\$*\w+\W")
# from fastapi.logger import logger as lg
from pydantic import BaseModel
import os,subprocess
import logging
import subprocess
import datetime

lg = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)


class MetaInfo(BaseModel):
    history_ts:int=None
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

class Mp4Description(BaseModel):
    time:int
    id:str
    views:int
    length:float

class MediaFile(BaseModel):
    title:str
    description:Mp4Description
    comment:str
    
def vdo_info(yt:YouTube):
    # print(yt.__dict__)
    m = MetaInfo(id=yt.video_id, title=yt.title,length=yt.length,views=yt.views,yt_thmb=yt.thumbnail_url)
    # print(m.dict())
    return m
# import time
import calendar

def update_tags(media_file,m:MetaInfo):
    dttm_now = datetime.datetime.utcnow()
    ux_ts = calendar.timegm(dttm_now.utctimetuple())
    print(ux_ts)
 
    with open(media_file, 'r+b') as file:
        media_file = mutagen.File(file, easy=True)
        # lg.info('before:', media_file, end='\n\n')
        media_file['title'] = m.title
        media_file['comment'] = m.yt_thmb
        media_file['description'] = f'{ux_ts}/{m.id}/{m.views}/{m.length}' #remember this
        media_file['album'] = 'xxx'
        media_file['artist'] = 'jesus'
        media_file.save(file)
        # lg.info('after:', media_file.pprint(), end='\n\n')
        # lg.info(type(media_file), type(media_file.tags), end='\n\n')
        return True
    
def get_mp4_meta(file_):

    with open(file_, 'r+b') as file:
        media_file = mutagen.File(file, easy=True)
        try:
            desc = media_file['description'][0].split('/')
            if len(desc)>3:
                lg.info('>')
                history_ts_,id_,views_,length_ = media_file['description'][0].split('/')
                history_ts_= int(float(history_ts_))
            elif len(desc)==3:
                lg.info('=')
                id_,views_,length_ = media_file['description'][0].split('/')
                history_ts_=0
                
            else:
                lg.info('nno')
                lg.exception(media_file.__repr__)
                return False
            
            # lg.info('stuff %s %s %s',history_ts_,views_,id_)
            ttl_ =media_file['title'][0]
            thmb_=  media_file['comment'][0]
            lg.info('stuff %s %s',ttl_,thmb_)
            m=MetaInfo(history_ts=history_ts_, id=id_,title=ttl_,length=length_,views=views_,yt_thmb=thmb_)
            return m
        
        except Exception as e:
            id_,views_,length_,thmb_='hi',0,100,'url'
            lg.exception('GetMetaException: %s',e.__class__)
            return False
def list_():
    files = os.listdir(os.curdir)
    media = [x if '.mp4' in x else None  for x in files]
    print(files)
    print(media)
    res = {"media":[]}
    for i in media:
        if i is not None:
            # print(i)
            # print(type(i))
            res['media'].append(i)

        else: 
            pass
    return res['media']
# import numpy as np
import random
def download(url,play:bool=True,autoplay:bool=True)-> Records:
    yt = YouTube(url)
    st = datetime.datetime.utcnow()
    lg.info('downloading file.....')
    video = yt.streams.filter(only_audio=True).first()
    #catch errors here
    out_file = video.download(output_path=".") #get full path of downloaded file as output
    file_ = out_file.split('/')[-1] #used for playing the file from vlc CLI later
    lg.info('downloaded file.....')
    lg.info('out_file: %s',out_file)
    et = datetime.datetime.utcnow()
    lg.info('downloading meta.....')
    m = vdo_info(yt)
    # title = m.title
    lg.info("m: %s",m)
    lg.info("url: %s",url)
    lg.info("url: %s")
    ts = et-st
    lg.info("ts: %s",ts.total_seconds())
    returning = Records(time=datetime.datetime.utcnow(),input_link=url,user='self',downloaded_in_s=ts.total_seconds(),meta=m)
    
    ##comit to db

    if not play:
        try:
            r = update_tags(file_,m)
            if r:
                return returning
            
        except Exception as e:
            return "Exception: updatetags"

    
    else:
       
        base_cmd = ["vlc",file_]
        if not autoplay:
            cmd = base_cmd
        else:
            files=list_()


            # print('files',files)
            # f_list = list(filter(lambda item: item is not None, files))

            # print('flist',files)
            up_next = random.shuffle(files)
            print('up',files)
            cmd = base_cmd + files + ['--play-and-exit']
            print(cmd)

        r = update_tags(file_,m)

        pid = run_cmd(cmd)
        lg.info('songs played pid: %s',pid)
        # f = subprocess.Popen(cmd)
        returning.pid=pid
        lg.info('songs played pid: %s',returning.pid)
        lg.info('typetype: %s',type(returning))

        return returning

# url = 'https://www.youtube.com/watch?v=J4nvbKBuEBU'
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
    lg.info(pid)
    lg.info(type(f))
    # print(f.__dict__)
    return pid

print('hi')
print(list())
# file = 'TOPIA TWINS (Official Audio).mp4'
# print(get_mp4_meta(file_=file))
# with open(file,'r+b') as f:
#     media_file = mutagen.File(file, easy=True)
#     # id_ = media_file['description'].split('/')[0]
#     print((media_file['description'][0].split('/')[0]))
#     print(type(media_file['description']))
#     # print(id_)
# m=MetaInfo(id='xnd38cJ',title=file,length=230,views=12143,yt_thmb="abcd.com/sas/")
# # print(update_tags(file,m))
# m = vdo_info(url)
# print(m.dict())
# title='TOPIA TWINS (Official Audio).mp3'
# cmd = ["vlc",title]
# url = 'https://www.youtube.com/watch?v=Hm1YFszJWbQ'
# print(download(url))
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
# ur = 'https://www.youtube.com/watch?v=6EEW-9NDM5k'
# meta_url  = f'https://youtube.com/oembed?url={ur}&format=json'
# yt = YouTube(ur)
# print(yt)
# print(type(yt))
# print(yt.__dict__)
# print(yt._vid_info)
# import requests

# r = requests.get(meta_url)
# print(r.json())
