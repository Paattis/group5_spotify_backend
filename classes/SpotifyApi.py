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


SPOTIFY_CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
SPOTIFY_CLIENT_SECRET= os.getenv("SPOTIFY_CLIENT_SECRET")
SPOTIFY_REDIRECT_URI = os.getenv("SPOTIFY_REDIRECT_URI")
SPOTIFY_AUTH_BASE_URL = os.getenv("SPOTIFY_AUTH_BASE_URL")
SPOTIFY_BASE_URL = os.getenv("SPOTIFY_BASE_URL")


class SpotifyApi(object):
  """docstring for SpotifyApi
  
  Attributes:
      access_token (string): the latest access_token for the API
      lastTokenUpdate (datetime): the datetime when the token was last updated
      tokenExpireTime (datetime): the datetime when the token will/has expire(d)
  """
  def __init__(self):
    self.access_token = None
    self.lastTokenUpdate = None
    self.tokenExpireTime = None


  def getAccessToken(self):
    token = AccessToken.query.filter(
      AccessToken.expire_time>datetime.now()+timedelta(seconds=60)
    ).first()
    if token:
      self.access_token = token.access_token
      self.tokenExpireTime = token.expire_time

    print("Tokens found", token)
    print(SPOTIFY_AUTH_BASE_URL)
    """Checks if the current access token is valid/we have one
       gets a new access token if necessary
    Returns:
        string: the access token for the Spotify API
    """
    if not self.access_token or (datetime.now() >= self.tokenExpireTime):
      requestCode = base64.b64encode(f'{SPOTIFY_CLIENT_ID}:{SPOTIFY_CLIENT_SECRET}'.encode("utf-8"))

      headers = {
        "Authorization": "Basic "+requestCode.decode("utf-8"),
        "Content-Type": "application/x-www-form-urlencoded"
      }
      pp = pprint.PrettyPrinter(indent=4)
      print(headers)
      r = requests.post(os.path.join(SPOTIFY_AUTH_BASE_URL, "api/token"), headers=headers, data={"grant_type": "client_credentials"})
      data = r.json()

      self.access_token = data["access_token"]
      self.tokenExpireTime = datetime.now() + timedelta(seconds=data["expires_in"])

      newToken = AccessToken(access_token=self.access_token, expire_time=self.tokenExpireTime)
      db.session.add(newToken)
      db.session.commit()
      return self.access_token

    return self.access_token


  @property
  def accessToken(self):
    """a convenience property
    
    Returns:
        string: the access token
    """
    return self.getAccessToken()

  
  """API endpoints"""
  def searchArtists(self, artistName):
    """Searches the Spotify API for artists with
    the given name
    
    Args:
        artistName (string): Description
    
    Returns:
        List<Dictionary>: the representation of the search results 
    """
    try: 
      resp = requests.get(
        BASE_URL+"search",
        params={
          "q": artistName,
          "type": ["artist"],
        },
        headers={
          "Authorization": "Bearer {}".format(self.accessToken)
        }  
      )
      return resp.json()
    except Exception as e:
      print("API ERROR", e)
      return None

  def getArtistTopTracks(self, artistId):
    """Gets the top tracks for the artist with the corresponding id  
       
    Args:
        artistId (string): the Spotify artist id for the artist
    
    Returns:
        List<Dictionary>: the list of the tracks
    """
    try:
      resp = requests.get(
        BASE_URL+"artists/{}/top-tracks".format(artistId),
        params={
          "market":"FI"
        },
        headers={
          "Authorization": "Bearer {}".format(self.accessToken)
        }  
      )
      print("resp",resp)
      return resp.json()

    except Exception as e:
      print("API ERROR", e)
      return None
