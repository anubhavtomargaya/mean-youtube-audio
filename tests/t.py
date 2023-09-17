from pytube import Youtube as yt
url = 'https://www.youtube.com/watch?v=J4nvbKBuEBU'
# 
def get_meta(url):
    v= yt(url)
    print(v)
    
get_meta(url)

##this was used to test audio playing in raspi