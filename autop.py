#!/usr/bin/env python3
from plurk_oauth import PlurkAPI

from datetime import datetime, timezone, timedelta
from dateutil.parser import parse as parse_date
import json
import os
import sys

config_file = os.path.join(os.path.dirname(__file__), 'config.json')

oauth_key = oauth_secret = None # must have
oauth_token = oauth_token_secret = None # optional
globals().update(json.load(open(config_file, 'r')))

plurk = PlurkAPI(oauth_key, oauth_secret, oauth_token, oauth_token_secret)
if not oauth_token or not oauth_token_secret:
    plurk.authorize()
    globals().update(plurk._oauth.oauth_token)
    json.dump({ key: val for key, val in globals().items() if key.startswith('oauth_') }, open(config_file, 'w'))
    print('[+] token saved')

def get_last_post():
    posts = plurk.callAPI('/APP/Timeline/getPlurks', {'limit': 1, 'filter': 'my'})
    return posts['plurks'][0]

def get_last_post_time():
    return parse_date(get_last_post()['posted'])

now = datetime.now(timezone.utc)
last_time = get_last_post_time()
diff = now - last_time
print('[*] last time = %s, time diff = %s' % (last_time, diff))

if diff <= timedelta(hours=12):
    print('[*] quit, less than 12 hours')
else:
    r = []
    for unit, time_delta in [ ('天', timedelta(days=1)), ('小時', timedelta(hours=1)), ('分', timedelta(minutes=1)), ('秒', timedelta(seconds=1)) ]:
        d = diff // time_delta
        diff -= d * time_delta
        if d: r.append('%d%s' % (d, unit))
    time = ''.join(r)
    r = plurk.callAPI('/APP/Timeline/plurkAdd', {'content': '我已經有%s忘了發噗啦！ [emo5]\nhttps://github.com/Inndy/AutoP (from AutoP)' % time, 'qualifier': 'feels'})
    if r:
        print('[+] plurk posted')
    else:
        print('[-] post failed')
