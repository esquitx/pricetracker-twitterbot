import tweepy


import os
import logging
import time
import schedule
from dotenv import load_dotenv

from processing import weekly_product,daily_product, weekly_category
from tweets import tweet_product, tweet_category


# ENVIRONMENT VARIABLES
logger = logging.getLogger()

def initiate_client(env_dir = '.env'):
    
    load_dotenv(env_dir)

    # ----- SECRETS ----------

    ACCESS_TOKEN = os.getenv('ACCESS_TOKEN')
    ACCESS_SECRET = os.getenv('ACCESS_SECRET')

    API_KEY = os.getenv('API_KEY')
    API_SECRET = os.getenv('API_SECRET')

    OAUTH_TOKEN = os.getenv('OAUTH_TOKEN')
    OAUTH_TOKEN_SECRET = os.getenv('OAUTH_TOKEN_SECRET')

    BEARER_TOKEN = os.getenv('BEARER_TOKEN')

    # --------------------------

    # ------ DATABASE -----------
    DB_DIR = os.getenv('DB_DIR')


    # CLIENT
    client = tweepy.Client(bearer_token=BEARER_TOKEN, access_token=OAUTH_TOKEN, access_token_secret=OAUTH_TOKEN_SECRET, consumer_key=API_KEY, consumer_secret=API_SECRET)

    # Report progress
    print("Client created successfully")

    return client, DB_DIR


def daily_tweet(client, db_dir):
    
    # FETCH DATA FOR PRODUCTS
    top, bottom = daily_product(db_dir)

    # TWEET BOTTOM
    tweet_product(client, products=bottom, top=False)

    time.sleep(90)

    # TWEET TOP
    tweet_product(client, products=top, top=True)

    print('Successfully tweeted daily information')


def weekly_tweet(client,db_dir):

    # ------------
    # WEEKLY CATEGORY
    # -------------

    # FETCH DATA FOR CATEGORIES
    top_cat, bottom_cat = weekly_category(db_dir)

    # TWEET CATEGORY DATA
    tweet_category(client, categories=bottom_cat, top=False)
    time.sleep(90)
    tweet_category(client, categories=top_cat, top=True)

    time.sleep(120)

    # ---------------
    # WEEKLY PRODUCT
    # ---------------

    # FETCHDATA FOR PRODUCTS
    top_prod, bot_prod = weekly_product(db_dir)

    # TWEET DATA
    tweet_product(client, products=bot_prod, top=False, daily=False)
    time.sleep(90)
    tweet_product(client, products=top_prod, top=True, daily=False)

    print('Successfuly tweeted weekly information')

if __name__ == '__main__':
    
    # Connect to twitter client
    client, DB_DIR = initiate_client()

    schedule.every().day.at("12:00").do(daily_tweet, client=client, db_dir=DB_DIR)
    schedule.every().sunday.at("18:00").do(weekly_tweet, client=client, db_dir=DB_DIR)

    while True:
        print("Checking for new jobs to run...")
        schedule.run_pending()
        print("Run completed. Going to sleep")
        time.sleep(120)
        print("----------------")



    