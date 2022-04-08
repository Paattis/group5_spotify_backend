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
