# Group 5 Spotify application backend

## Installation

### If the virtual environment doesn't exist, create it
```
$ python -m venv venv
```

### Activate the virtual environment 
```
$ source venv/bin/activate      // Unix
$ .\venv\Scripts\activate.bat   // Windows
```

### Install the required packages
```
$ pip install wheel
$ pip install -r requirements.txt
```

### Populate .env file

```
DB_DIALECT="mysql"
DB_DRIVER="pymysql"
DB_PORT="3306"
DB_HOST="127.0.0.1"
DB_USER=(your db user's name here)
DB_PASS=(your db password here)
DB_NAME=""

#deployment key
FLASK_SECRET_KEY=(random generate one when deploying to production)

#cache timeout in seconds
FLASK_CACHE_TIMEOUT=1800
FLASK_CACHE_DIR=(the directory you want to store the cache files in)

# the amount of cached items to be held at one time
FLASK_CACHE_TRESHOLD=100

#spotify API credentials
SPOTIPY_CLIENT_ID=
SPOTIPY_CLIENT_SECRET=

SPOTIPY_REDIRECT_URI="http://127.0.0.1:8000/redir"
SPOTIPY_AUTH_BASE_URL="https://accounts.spotify.com/"
SPOTIPY_BASE_URL="https://api.spotify.com/v1/"
```

### Set flask variables

```
$ export FLASK_APP=app.py   // Unix
$ set FLASK_APP=app.py      // Windows
```

### Database setup
```
$ flask db upgrade
```
See https://flask-migrate.readthedocs.io/en/latest/ for more info.
### Run 
```
$ flask run
```


### Message code -> message dictionary
| code | message | 
| ----- | ----- |
| ERR_LOCATION_SAVE_500 | Something went wrong when adding a song to the location | 
| ERR_LOCATION_404 | Location not found | 
| ERR_SONG_SPOTIFY_ID_500 | Invalid song id | 
| ERR_SONG_LOCATION_SAVE_500 | Something went wrong when adding a song to the location | 
| SONG_ALREADY_ADDED | Song is already in the songs of the location | 
| SONG_ADD_SUCCESS | Song added successfully | 