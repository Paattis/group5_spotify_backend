# Group 5 Spotify application backend

### installation/running it

* If the virtual environment doesn't exist, create it
```
$ pip install virtualenv
$ python -m virtualenv venv
```

* Activate the virtual environment 

#### Windows
```
$ .\venv\Scripts\activate.bat
```

#### Linux/MacOs/other Unix-like OS
```
$ source venv/bin/activate
```

* Install the required packages
```
$ pip install -r requirements.txt
```

* Fill the .env file

```
DB_DIALECT="mysql"
DB_DRIVER="pymysql"
DB_PORT="3306"
DB_HOST="127.0.0.1"
DB_USER=(your db user's name here)
DB_PASS=(your db password here)
```

```
* Run the app
```
$ set FLASK_APP=run.py
$ flask run -p 8000
```