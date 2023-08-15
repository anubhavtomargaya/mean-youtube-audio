
from pytube import Youtube
url0s = 'https://www.youtube.com/watch?v=J4nvbKBuEBU'
# 
def get_meta(url):
    v= Youtube(url)
    print(v)
    
get_meta(url0s)