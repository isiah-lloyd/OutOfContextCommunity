import boto3
import random
import requests
from requests_oauthlib import OAuth1Session
import os
import logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)
SEASONS = {"S01": 25, "S02": 24, "S03": 22, "S04": 13, "S05": 13, "S06": 13}
CLIENT_KEY = os.environ['TWITTER_CLIENT_KEY']
CLIENT_TOKEN_SECRET = os.environ['TWITTER_TOKEN_SECRET']
ACCESS_TOKEN = os.environ['TWITTER_ACCESS_TOKEN']
ACCESS_TOKEN_SECRET = os.environ['TWITTER_ACCESS_TOKEN_SECRET']
s3 = boto3.client('s3')
def getFile():
    season_choice = random.choice(list(SEASONS))
    episode_choice = str(random.randint(1, SEASONS[season_choice]))
    episode_choice = episode_choice.rjust(2, '0')
    prefix = season_choice + "E" + episode_choice
    keys = []
    try:
        response = s3.list_objects_v2(
            Bucket='occ-pictures',
            Prefix=prefix,
        )
    except boto3.ClientError as e:
        logger.error("Received error while trying to list objects: %s", e, exc_info=True)   
    for x in response['Contents']:
         keys.append(x['Key'])
    if not keys:
        getFiles()      #If there isn't a certain episode or season left
    else:
        key_selected = random.choice(keys)
        try:
            s3.download_file('occ-pictures', key_selected, '/tmp/temp.jpg')
        except ClientError as e:
            logger.error("Received error while trying to download file: %s", e, exc_info=True)
        logger.info("Downloaded: %s", str(key_selected))
        return key_selected
def tweet(key):
    twitter = OAuth1Session(CLIENT_KEY,
        client_secret= CLIENT_TOKEN_SECRET,
        resource_owner_key= ACCESS_TOKEN,
        resource_owner_secret= ACCESS_TOKEN_SECRET)
    try:
        media_post = twitter.post("https://upload.twitter.com/1.1/media/upload.json", files={'media': open('/tmp/temp.jpg', 'rb')})
    except requests.exceptions.RequestException as e:
        logger.error("Error while posting media to twitter: %s", e)
    id = media_post.json()["media_id_string"]
    try:
        post = twitter.post("https://api.twitter.com/1.1/statuses/update.json", data={"status": "#Community #andamovie","media_ids": id, "trim_user": 'true'}).json()
    except requests.exceptions.RequestException as e:
        logger.error("Error while posting status to twitter: %s", e)
    logger.info("Posted status to twitter at %s", post['created_at'])
def main(event, context):
    tweet(getFile())