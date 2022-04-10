import sys
import pkgutil
print("LIST OF MODULES")
#sys.path.insert(0, '/home/leevi/git/group5_spotify_backend/venv/lib/python3.6/site-packages/')

#import flask
#sys.path.insert(0, '/home/leevi/git/group5_spotify_backend/')
sys.path.insert(0, '/home/leevi/git')
print("PATH", sys.path)

mlist = list(pkgutil.iter_modules())

for m in mlist:
        print(m)
from group5_spotify_backend import app as application
#import app as application
