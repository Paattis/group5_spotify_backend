"""Summary

Attributes:
    AUTH_BASE_URL (TYPE): Description
    BASE_URL (TYPE): Description
    CLIENT_ID (TYPE): Description
    CLIENT_SECRET (TYPE): Description
    REDIRECT_URI (TYPE): Description
"""
import requests
import base64
import os
import json
import pprint
from datetime import datetime, timedelta
from db.models import AccessToken
from db import db
from sqlalchemy.orm import Session
from sqlalchemy import desc

from spotipy import CacheHandler

SPOTIPY_CLIENT_ID = os.getenv('SPOTIPY_CLIENT_ID')
SPOTIPY_CLIENT_SECRET= os.getenv('SPOTIPY_CLIENT_SECRET')
SPOTIPY_REDIRECT_URI = os.getenv('SPOTIPY_REDIRECT_URI')
SPOTIPY_AUTH_BASE_URL = os.getenv('SPOTIPY_AUTH_BASE_URL')
SPOTIPY_BASE_URL = os.getenv('SPOTIPY_BASE_URL')


class DatabaseTokenCacheHandler(CacheHandler):
  """a Cache Handler for the SpotiPy library that uses a database to store access tokens so we don't 
  need to fetch a new one every time.

  Attributes:
      access_token (string): the latest access_token for the API
      lastTokenUpdate (datetime): the datetime when the token was last updated
      tokenExpireTime (datetime): the datetime when the token will/has expire(d)
  """


  def save_token_to_cache(self, token_info):
    pass

  def get_access_token(self, as_dict=True):
    return self.get_cached_token(as_dict)

  def get_cached_token(self, as_dict=True):
    """Checks if we have a currently valid access token in the database and return that one.
      If one isn't found, get a new one from Spotify's API. Overrides the "get_cached_token" method from CacheHandler
    Returns:
        string||dict: the access token for the Spotify API
    """

    # find tokens that are still valid for the next 2 minutes
    token = AccessToken.query.filter(
      AccessToken.expire_time>datetime.now()+timedelta(seconds=120)
    ).order_by(desc(AccessToken.id)).first()

    if token:
      print("exp time", token.expire_time)
      print("now", datetime.now())
      print("Not expired" if token.expire_time > datetime.now() else "expired")

      # calculate a new expire time in seconds for the existing token
      expire_seconds = int((token.expire_time - datetime.now()).total_seconds())
      token_data = {'access_token': token.access_token, 'expires_in': expire_seconds, 'token_type': 'bearer'}
      print('Returning data from db', token_data)

    else:
      # if a valid token doesn't exist, fetch a new one from the Spotify API
      token_data = self.fetch_token()


    return token_data if as_dict else token_data['access_token']

  def fetch_token(self):
    """
      Fetches a new token from the Spotify API and returns the response
    """
    requestCode = base64.b64encode(f'{SPOTIPY_CLIENT_ID}:{SPOTIPY_CLIENT_SECRET}'.encode('utf-8'))

    headers = {
      'Authorization': 'Basic '+requestCode.decode('utf-8'),
      'Content-Type': 'application/x-www-form-urlencoded'
    }


    r = requests.post(os.path.join(SPOTIPY_AUTH_BASE_URL, 'api/token'), headers=headers, data={'grant_type': 'client_credentials'})
    data = r.json()

    access_token = data['access_token']
    token_expire_time = datetime.now() + timedelta(seconds=data['expires_in'])


    # finally save the token
    newToken = AccessToken(access_token=access_token, expire_time=token_expire_time)
    db.session.add(newToken)
    db.session.commit()
    print('Returning token', data)
    return data