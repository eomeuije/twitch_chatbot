import requests
from dateutil.parser import parse
import time
import datetime
import argparse
import os
import traceback
from google.googledrive import Upload



client_id = ''
client_secret = ''
clip_authorization = ''

class Clip(object):
  def __init__(self, username):
    self.username = username
    url = 'https://id.twitch.tv/oauth2/token'

    header_content_type = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    data = {
        'client_id': client_id,
        'client_secret': client_secret,
        'grant_type': 'client_credentials'
    }
    response = requests.post(url, headers=header_content_type, data=data)
    self.token_json = response.json()

  def create_clip(self):
    
    url = 'https://api.twitch.tv/helix/users?login=' + self.username
    header = {
        'Client-Id': client_id,
        'Authorization': 'Bearer ' + self.token_json['access_token']
    }
    response = requests.get(url, headers=header)
    broadcast_json = response.json()

    try:
        url = 'https://api.twitch.tv/helix/streams?user_id=' + broadcast_json['data'][0]['id']
        header = {
            'Client-Id': client_id,
            'Authorization': 'Bearer ' + self.token_json['access_token']
        }
        response = requests.get(url, headers=header)
        started_at = response.json()['data'][0]['started_at']
        started_at = time.mktime(parse(started_at).timetuple())
        now = time.time()
        time_diff = 0 * 60 * 60
        t = datetime.datetime.utcfromtimestamp(now - started_at - time_diff)
        self.stream_time = f' {t.hour}시{t.minute}분{t.second}초'
    except:
        self.stream_time = ''
        traceback.print_exc()

    url = 'https://api.twitch.tv/helix/clips?broadcaster_id=' + broadcast_json['data'][0]['id']
    header = {
        'Client-Id': client_id,
        'Authorization': 'Bearer ' + clip_authorization
    }
    response = requests.post(url, headers=header).json()
    for i in range(15):
        if ('data' in response) and (len(response['data']) > 0):
           break
        print('Create Clip Retry...After 5sec')
        time.sleep(1)
        response = requests.post(url, headers=header).json()

    return response

  def download_clip(self, clip_id: str, clip_url: str, title: str):
    header = {
        'Client-Id': client_id,
        'Authorization': 'Bearer ' + self.token_json['access_token']
    }
    response = requests.get(clip_url, headers=header)

    url = 'https://api.twitch.tv/helix/clips?id=' + clip_id
    header = {
        'Client-Id': client_id,
        'Authorization': 'Bearer ' + self.token_json['access_token']
    }
    response = requests.get(url, headers=header).json()
    for i in range(15):
        if ('data' in response) and (len(response['data']) > 0):
           break
        time.sleep(1)
        response = requests.get(url, headers=header).json()
        
    thumbnail_url: str = response['data'][0]['thumbnail_url']
    if not title:
      title: str = response['data'][0]['title']


    url = thumbnail_url.replace('-preview-480x272.jpg', '.mp4')
    header = {
        'Client-Id': client_id,
        'Authorization': 'Bearer ' + self.token_json['access_token']
    }
    response = requests.get(url, headers=header)

    clip_dir = os.path.join(os.path.dirname(__file__), 'clips', self.username + '_clips/')
    if not os.path.exists(clip_dir):
        os.mkdir(clip_dir)
    clip_file_name = os.path.join(clip_dir, title)
    uniq = 1
    while os.path.exists(clip_file_name):
        clip_file_name = os.path.join(clip_dir, title + '_' + str(uniq))
        uniq += 1
    clip_file_name += self.stream_time + '.mp4'
    with open(clip_file_name, "wb") as f_out:
        f_out.write(response.content)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Twitch Clip Creater And Downloader")
    parser.add_argument("-u", "--username", required=True)
    parser.add_argument("-t", "--title")
    parser.add_argument("-m", "--mode", default="download")
    # parser.add_argument("--logging-telegram", action="store_true")
    args = parser.parse_args()
    clip = Clip(args.username)
    clip_json = clip.create_clip()
    print(clip_json)
    clip_edit_url: str = clip_json['data'][0]['edit_url']
    clip_id: str = clip_json['data'][0]['id']
    clip_url = clip_edit_url.replace('/edit', '')
    clip.download_clip(clip_id, clip_url, args.title)
    
    uploader = Upload()
    uploader.upload(args.username + '_clips')