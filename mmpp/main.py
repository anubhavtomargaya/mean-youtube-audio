from fastapi import FastAPI,HTTPException,Response
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from fastapi.logger import logger as lg
from starlette import status
import mutagen
import uvicorn
import logging
lg.setLevel(logging.DEBUG)
from enum import Enum
import os,subprocess
from  config import settings
from download import download,kill_by_pid,kill_all_vlc,get_mp4_meta,MetaInfo,Records,update_tags
# from kill import kill_by_pid
active_pid = settings.ACTIVE_PID

origins = [
    "http://192.168.0.102:3000",
    "http://192.168.1.5:3000",
    "http://10.5.40.167:8086",
    "https://localhost.redbus.com",
    "http://localhost:3001",
    "http://localhost:3000",
    "http://localhost:8086",
]
import alsaaudio
mixer = alsaaudio.Mixer()
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class DownloadRequest(BaseModel):
    url : str
    play:bool=True
    
class KillRequest(BaseModel):
    pid :str=None
    all:bool=False
    
class PlayRequest(BaseModel):
    uri : str=None
    surprise:bool=False
    
class MixerRequest(BaseModel):
    volume : str='DOWN'
    step_size:int=10
    mute:bool=False

class PlayResponse(BaseModel):
    meta:MetaInfo=None
    pid:int =None
    exception: str = None

# from enum import Enum
# class VisualiserType(str, Enum):
#     spectrometer = "spectrometer"
#     goom = "goom"


class SpectrometerVisualiser(BaseModel):
    radius:int
    color:int
    amp:int
    spear:int
    peakWd:int
    peakHt:int

## added / route in shome branch to show bunch of stats and current home status
##use this to build "how many users at home" and "whats happening in home" by intercepting the home network using pi


@app.get("/ydl/api/v1/now")
def now_playing():
    if settings.ACTIVE_PID!=0:
        dttm_now = datetime.datetime.utcnow()
        ux_ts = calendar.timegm(dttm_now.utctimetuple())
        lg.warn('NOW/%s/%s/%s/%s/%s','CHECK','user',int(float(ux_ts)),settings.ACTIVE_TITLE,settings.ACTIVE_PID)
        if not settings.ACTIVE_TITLE=='STREAM':
            f = f'{settings.ACTIVE_TITLE}.mp4'
            m = get_mp4_meta(f) #MetaInfo
            b = {   "meta": m,"pid": settings.ACTIVE_PID }
    
            # r = {"pid":settings.ACTIVE_PID ,"meta":m.d }
            return b
        else:
            b = {   "meta":settings.ACTIVE_TITLE ,"pid": settings.ACTIVE_PID }
            return b
    else:
        return "NOTHING"

@app.post("/ydl/api/v1/download") #play by url 
def trigger_download(input:DownloadRequest)->Records: 

    lg.error('input: %s',input.url)
    try:
        url = input.url
        if settings.ACTIVE_PID !=0:
            dttm_now = datetime.datetime.utcnow()
            ux_ts = calendar.timegm(dttm_now.utctimetuple())
            lg.warn('SKIPPLAY/%s/%s/%s/%s/%s',url,'user',int(float(ux_ts)),settings.ACTIVE_TITLE,settings.ACTIVE_PID)
            try:
                r = kill_all_vlc()
                if r:
                    settings.ACTIVE_PID=0
                    pass
            except Exception as e:
                return False
        
        try:
            resp = download(url,play=input.play)
            dttm_now = datetime.datetime.utcnow()
            ux_ts = calendar.timegm(dttm_now.utctimetuple())
            # download_resp = f
            settings.ACTIVE_PID =resp.pid
            settings.ACTIVE_TITLE =resp.meta.title
            lg.info('respose" %s',resp.dict())
            ts_id = f"""{str(resp.meta.id)+ " - " + str(resp.downloaded_in_s)}"""
            lg.warn('DOWNLOAD/%s/%s/%s/%s/%s',ts_id ,'user',int(float(ux_ts)),settings.ACTIVE_TITLE,settings.ACTIVE_PID)
            return resp
 
            
        except Exception as e:
            lg.exception(e)
            return {"exception1":e.__class__}
         
    except Exception as e:
        return {"exception":e}
import time ,calendar,datetime
@app.post("/ydl/api/v1/play")
def play_by_out_file(input:PlayRequest,autoplay:bool=True,visualiser:bool=True): 
    ## here autoplay takes you to internet radio
    
    radio_stream = 'http://www.radioparadise.com/m3u/aac-128.m3u'
    visualiser_spec = ['--audio-visual' ,'visual',
                        '--effect-list', 'spectrometer' , 
                        '--spect-radius=100', '--spect-peak-width=40' ,
                        '--spect-peak-height=10' ,'--spect-separ=100' ,
                        '--spect-sections=2' , '--spect-amp=10' ,'--spect-color=100' ]
                        
    if input.uri:
        lg.info('uri')
        
        base_cmd = ["vlc",input.uri]
        curr_playing_title = input.uri.split('.')[0]
        
        m = get_mp4_meta(input.uri)

        if not m:
            lg.warn('m not received')

        if not autoplay:
            try:
                cmd = base_cmd
            except Exception as e:
                lg.exception(e)
        else:
            #always play radio after a play by default,
            # optionally can add a justonce bool to have last version behaviour
            cmd = base_cmd+[radio_stream]
            # return "Exceptopm get mp4 meta"
        
    elif input.surprise:
        lg.info('surprise')
        curr_playing_title = 'STREAM' #find the title from radio
        m= MetaInfo()
        cmd = ["vlc",radio_stream]
        dttm_now = datetime.datetime.utcnow()
        ux_ts = calendar.timegm(dttm_now.utctimetuple())
        lg.warn('RADIO/%s/%s/%s/%s/%s','STREAM','user',int(float(ux_ts)),settings.ACTIVE_TITLE,settings.ACTIVE_PID)

    lg.info("active pid %s",settings.ACTIVE_PID)
    
    #async

    if settings.ACTIVE_PID !=0:
        dttm_now = datetime.datetime.utcnow()
        ux_ts = calendar.timegm(dttm_now.utctimetuple())
        lg.warn('SKIPPLAY/%s/%s/%s/%s/%s',curr_playing_title,'user',int(float(ux_ts)),settings.ACTIVE_TITLE,settings.ACTIVE_PID)
        try:
            r = kill_all_vlc()
            (settings.ACTIVE_PID )
            if r:
                settings.ACTIVE_PID=0
        except Exception as e:
            return False
    else:
        pass
    try:

        if not visualiser:
            lg.debug('no visual')
            lg.debug('cmd %s',cmd)
            f = subprocess.Popen(cmd)
        else:
            cmd = cmd + visualiser_spec
            f = subprocess.Popen(cmd)
        settings.ACTIVE_PID = f.pid
        
        settings.ACTIVE_TITLE = curr_playing_title
        lg.info('m %s',m.dict())
        lg.info('m _%s',m.history_ts)
        dttm_now = datetime.datetime.utcnow()
        ux_ts = calendar.timegm(dttm_now.utctimetuple())
        lg.warn('PLAY/%s/%s/%s/%s/%s',m.id,'user',int(float(ux_ts)),settings.ACTIVE_TITLE,settings.ACTIVE_PID)
        return PlayResponse(meta=m,pid=f.pid)
    except Exception as e:
        return f"PlayerException {e.__class__}"



@app.get("/ydl/api/v1/kill")
def kill(req:KillRequest=None):
    try:
        
        r = kill_all_vlc()
        if r:
            dttm_now = datetime.datetime.utcnow()
            ux_ts = calendar.timegm(dttm_now.utctimetuple())
            lg.warn('KILL/%s/%s/%s/%s/%s','N','user',int(float(ux_ts)),settings.ACTIVE_TITLE,settings.ACTIVE_PID)
            
            settings.ACTIVE_PID=0
            settings.ACTIVE_TITLE='null'
            return True

    except Exception as e:
        return False
    # if req.all:
    #     return kill_all_vlc
    
    # if req.pid:
    #     pid = req.pid
    #     res = kill_by_pid(pid)
    #     settings.ACTIVE_PID = 0
    #     return res
    # else:

    #     return kill_all_vlc()


@app.post("/ydl/api/v1/mixer")
def control_mixer(req:MixerRequest):
    lg.info(req.__dict__)
    value = mixer.getvolume()[0]
    dttm_now = datetime.datetime.utcnow()
    ux_ts = calendar.timegm(dttm_now.utctimetuple())
    if req.volume=='UP':
        value = value+req.step_size
        lg.warn('VOLUMEUP/%s/%s/%s/%s/%s',value,'user',int(float(ux_ts)),settings.ACTIVE_TITLE,settings.ACTIVE_PID)
    elif req.volume=='DOWN':
        lg.warn('VOLUMEDOWN/%s/%s/%s/%s/%s',value,'user',int(float(ux_ts)),settings.ACTIVE_TITLE,settings.ACTIVE_PID)
        value = value-req.step_size
    else:
        lg.exception('Invalid Command')
        return False
    if value > 100:
        value = 100

    if req.mute:
        lg.warn('VOLUMEMUTE/%s/%s/%s/%s/%s',value,'user',int(float(ux_ts)),settings.ACTIVE_TITLE,settings.ACTIVE_PID)
        value = 0
       
    mixer.setvolume(value)
    value = mixer.getvolume()[0]
    return value

    


@app.get("/ydl/api/v1/list")
def list():
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
    # res = os.listdir(os.curdir)
    dttm_now = datetime.datetime.utcnow()
    ux_ts = calendar.timegm(dttm_now.utctimetuple())
    lg.warn('LIST/%s/%s/%s/%s/%s',len(res['media']),'user',int(float(ux_ts)),settings.ACTIVE_TITLE,settings.ACTIVE_PID)
    return res
    