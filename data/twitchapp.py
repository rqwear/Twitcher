import logging
from twitchAPI.twitch import Twitch
from data.config import TWITCH_ID, TWITCH_SECRET
"""
Twitchapi for checking online
add to .env
TWITCH_ID=
TWITCH_SECRET=
"""
client_id = TWITCH_ID
client_secret = TWITCH_SECRET

twitch = Twitch(client_id, client_secret)
twitch.authenticate_app([])

async def CheckUser(user): #returns true if online, false if not
    user_info = twitch.get_users(logins=[user])
    try:
        user_id = user_info['data'][0]['id']
        st_info = twitch.get_streams(user_id=user_id)
        jsondata = st_info.get('data')
        try:
            status = st_info.get('data')[0]
            live = status.get('type')
            if live == 'live':
                return True
            else:
                return False
        except:
            return False
    except Exception as e:
        logging.info(user)
        logging.exception(e)


async def name_of_stream(user): #returns name of stream if None return info_string
    user_info = twitch.get_users(logins=[user])
    try:
        user_id = user_info['data'][0]['id']
        st_info = twitch.get_streams(user_id=user_id)
        jsondata = st_info.get('data')
        try:
            status = st_info.get('data')[0]
            live = status.get('title')
            if live is not None:
                return live
            else:
                info_string = 'В эфире'
                return info_string
        except:
            info_string = 'В эфире'
            return info_string
    except Exception as e:
        logging.info(user)
        logging.exception(e)
