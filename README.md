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