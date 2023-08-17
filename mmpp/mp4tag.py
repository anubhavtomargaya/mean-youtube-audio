import shutil
## https://gist.github.com/lemon24/ebd0b8fa9b223be1948cddc279ea7970
import mutagen

shutil.copy('SICKO MODE.mp4', 'new.mp4')

# mutagen.File knows how to open any file (works with both MP4 and MP4):
#
# https://mutagen.readthedocs.io/en/latest/user/gettingstarted.html    
# https://mutagen.readthedocs.io/en/latest/api/base.html#mutagen.File
from datetime import datetime
import time
import calendar
with open('YehAllah.mp4', 'r+b') as file:
    media_file = mutagen.File(file, easy=True)
    print('before:', media_file.pprint(), end='\n\n')
    # print(media_file['date'])
    # print(media_file['tracknumber'])
    # print(media_file['tracknumber'])
    # print(time.time()*1000)
    # print(datetime.utcnow())
    # print(time.time().__str__())
    dttm_now = datetime.utcnow()
    ux_ts = calendar.timegm(dttm_now.utctimetuple())
    print(ux_ts)

    # print(time.mktime(dttm_now.utctimetuple()))
    # media_file.tracknumber =1
    # media_file['album'] = 'my album'
    # media_file['artist'] = 'my artist'
    media_file.save(file)
    print('after:', media_file.pprint(), end='\n\n')
    print(type(media_file), type(media_file.tags), end='\n\n')
print()
# Alternatively, you can use the explicit file type classes, e.g.
#
#   with open('new.mp4', 'r+b') as file:
#       media_file = mutagen.easymp4.EasyMP4(file)
# 
# https://mutagen.readthedocs.io/en/latest/api/mp4.html#mutagen.easymp4.EasyMP4
# https://mutagen.readthedocs.io/en/latest/api/mp3.html#mutagen.mp3.EasyMP3

# To see the tags you can set, you need to look at their corresponding tags:
#
# https://mutagen.readthedocs.io/en/latest/api/id3.html#mutagen.easyid3.EasyID3
# https://mutagen.readthedocs.io/en/latest/api/mp4.html#mutagen.easymp4.EasyMP4Tags

from mutagen.easymp4 import EasyMP4Tags
from mutagen.easyid3 import EasyID3

print('mp3 tags:', *sorted(EasyID3.Set.keys()), end='\n\n')
print('mp4 tags:', *sorted(EasyMP4Tags.Set.keys()), end='\n\n')
a = 1.23242
print(int(a))