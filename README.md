# mean-youtube-audio

## startup

```bash 
> cd mean-youtube-audio/mmpp
> source .venv/bin/activate
> screen -S "api" uvicorn main:app --reload --log-config loggconf.ini --host 0.0.0.0

```

## docs
localhost:8000/docs --> swagger
localhost:8000/redoc --> redoc

## files
downloads files to the current dir.
lists and plays files from the same dir.
each file is saved after attaching the meta info in it's schema. 
For this update_tags() handles the file manipulation using mutagen library.
audio controls of the device are accessed using alsaaudio which interacts with the soundcard. in case of raspberry pi this needs to be changed.
radio is implemented using a stream url, currently no way to find what song is playing on radio.
now playling endpoint shows the info from active session.