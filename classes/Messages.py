from types import SimpleNamespace

class Messages(object):

  """Simple class to store messages
  
  Attributes:
      code_message (dict): a mapping of the messages and their message codes
  """
  
  code_message = {
    'ERR_LOCATION_SAVE_500':'Something went wrong when saving location to the database',
    'ERR_LOCATION_404':'Location not found',
    'ERR_LOCATION_404':'Location not found',
    'ERR_SONG_SPOTIFY_ID_500':'Invalid song id',
    'ERR_SONG_LOCATION_SAVE_500':'Something went wrong when adding a song to the location',
    'SONG_ALREADY_ADDED':'Song is already in the songs of the location',
    'ERR_LOCATION_SAVE_500':'Something went wrong when adding a song to the location',
    'SONG_ADD_SUCCESS':'Song added successfully',
  }

  # assign the messages as class variables for easier access (e.g. Messages.ERR_LOCATION_404)
  # also assign the codes as strings for easy access (e.g. Messages.codes.ERR_LOCATION_404)
  for code, message in code_message.items():
    vars()[code] = message

  vars()['codes'] = SimpleNamespace(**{k:k for k in code_message.keys()})

