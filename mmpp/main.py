from fastapi import FastAPI,HTTPException,Response
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from fastapi.logger import logger as lg
from starlette import status
import uvicorn

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
    
@app.get("/ydl/api/v1/now")
def now_playing():
    if settings.ACTIVE_PID!=0:
        f = f'{settings.ACTIVE_TITLE}.mp4'
        m = get_mp4_meta(f)
        b = {   "meta": m,"pid": settings.ACTIVE_PID }
 
        # r = {"pid":settings.ACTIVE_PID ,"meta":m.d }
        return b
    else:
        return "NOTHING"

@app.post("/ydl/api/v1/download") #play by url 
def trigger_download(input:DownloadRequest)->Records: 

    lg.error('input: %s',input.url)
    try:
        url = input.url
        if settings.ACTIVE_PID !=0:
            try:
                r = kill_all_vlc()
                if r:
                    settings.ACTIVE_PID=0
                    pass
            except Exception as e:
                return False
        
        try:
            resp = download(url,play=input.play)
            # download_resp = 
            settings.ACTIVE_PID =resp.pid
            settings.ACTIVE_TITLE =resp.meta.title
            lg.info('respose" %s',resp.dict())
            return resp
 
            
        except Exception as e:
            lg.exception(e)
            return {"exception1":e.__class__}
         
    except Exception as e:
        return {"exception":e}
    
@app.post("/ydl/api/v1/play")
def play_by_out_file(input:PlayRequest,autoplay:bool=True,visualiser:bool=False): 
    ## here autoplay takes you to internet radio
    
    radio_stream = 'http://www.radioparadise.com/m3u/aac-128.m3u'
    visualiser_spec = ['--audio-visual' ,'visual',
                        '--effect-list', 'spectrometer' , 
                        '--spect-radius=100', '--spect-peak-width=40' ,
                        '--spect-peak-height=10' ,'--spect-separ=100' ,
                        '--spect-sections=2' , '--spect-amp=10' ,'--spect-color=100' ]
    if input.uri:
    
        base_cmd = ["vlc",input.uri]
        if not autoplay:
            try:
                cmd = base_cmd
                m = get_mp4_meta(input.uri)
                curr_playing_title = input.uri
            except Exception as e:
                lg.exception(e)
        else:
            #always play radio after a play by default,
            # optionally can add a justonce bool to have last version behaviour
            cmd = base_cmd+[radio_stream]
            # return "Exceptopm get mp4 meta"
        
    elif input.surprise:
        curr_playing_title = 'A SURPRISE' #find the title from radio
        m= MetaInfo()
        cmd = ["cvlc",radio_stream]

    lg.info("active pid %s",settings.ACTIVE_PID)
    
    #async

    if settings.ACTIVE_PID !=0:
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
            f = subprocess.Popen(cmd)
        else:
            cmd = cmd + visualiser_spec
            f = subprocess.Popen(cmd)
        settings.ACTIVE_PID = f.pid
        
        settings.ACTIVE_TITLE = curr_playing_title
        return PlayResponse(meta=m,pid=f.pid)
    except Exception as e:
        return f"PlayerException {e.__class__}"



@app.get("/ydl/api/v1/kill")
def kill(req:KillRequest=None):
    try:
        
        r = kill_all_vlc()
        if r:
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
 
    if req.volume=='UP':
        value = value+req.step_size
    elif req.volume=='DOWN':
        value = value-req.step_size
    else:
        lg.exception('Invalid Command')
        return False
    if value > 100:
        value = 100

    if req.mute:
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
    return res
    