import tweepy
import logging
import textwrap

logger = logging.getLogger()


SIREN = '\N{police cars revolving light}'
SPEAKER = '\U0001F4E3'
FINGER_DOWN = '\N{white down pointing backhand index}'

FIRST = '🥇'
SECOND = '🥈'
THIRD = '🥉'
FOURTH = '4️⃣'
FIFTH = '5️⃣'

EMOJIREF = [FIRST, SECOND, THIRD, FOURTH, FIFTH]

TOP = '\N{top with upwards arrow above}'

UP = '\U0001F4C8'
DOWN = '\U0001F4C9'

PCKG = '\N{package}'
EURO = '\U0001F4B6'
ARROW = '→'
NEW = '\U0001F195'

# TODO Update for api v2
# def like_mentions(client, last_check):

#     logger.info('Retrieving mentions...')
    
#     new_check = last_check
#     for tweet in tweepy.Cursor(client.mentions_timeline, since_id=last_check).items():
        
#         # Update last checked tweet
#         new_check = max(tweet.id, new_check)

#         if not tweet.favorited:
#             try:
#                 tweet.favorite()
#             except Exception as e:
#                 logger.exception("Error encountered when liking tweet", exc_info=True)

#     return new_check


def tweet_product(client, products, top=True, daily=True):
    
    if top: 
        tweet_type = 'subidas'
    else: 
        tweet_type = 'bajadas'

    if daily: 
        periodic = 'HOY'
    else: 
        periodic = 'ESTA SEMANA'

    opener_body  = f'{SPEAKER} ¡TENEMOS DATOS PARA {periodic}! {SPEAKER}\n\n{TOP} Estas son las TOP 5 {tweet_type} {TOP}\n\n {FINGER_DOWN}{FINGER_DOWN}{FINGER_DOWN}'
    opener = client.create_tweet(text=opener_body)

    first_body = format_product_tweet(0, product=products[0], top=top)
    first = client.create_tweet(text=first_body, in_reply_to_tweet_id=opener.data['id'])

    second_body = format_product_tweet(1, product=products[1], top=top)
    second = client.create_tweet(text=second_body, in_reply_to_tweet_id=first.data['id'])

    third_body = format_product_tweet(2, product=products[2], top=top)
    third = client.create_tweet(text=third_body, in_reply_to_tweet_id=second.data['id'])

    fourth_body = format_product_tweet(3, product=products[3], top=top)
    fourth = client.create_tweet(text=fourth_body, in_reply_to_tweet_id=third.data['id'])

    fifth_body = format_product_tweet(4, product=products[4], top=top )
    fifth = client.create_tweet(text=fifth_body, in_reply_to_tweet_id=fourth.data['id'])

    return 'Success!'
    
def format_product_tweet(position, product, top):

    if top:
        PERCENT = UP
    else: 
        PERCENT = DOWN
    
    rank = EMOJIREF[position]
    name = textwrap.shorten(product['name'], width=36, placeholder=' ...')
    format = textwrap.shorten(product['format'], width=25, placeholder=' ...')
    old_price = str(round(product['price_x'], 2)) + ' €'
    new_price = str(round(product['price_y'], 2)) + ' €'
    percent = round(product['difference'])

    body = f'{rank} {name} \n{PCKG} {format} \n{EURO} {old_price} {ARROW} {new_price} \n{PERCENT} {percent}%'

    return body


def tweet_category(client, categories, top=True):

    if top:
        tweet_type = 'subidas'
    else: 
        tweet_type = 'bajadas'

    opener_body  = f'{SPEAKER} ¡TENEMOS DATOS DE CATEGORIAS! {SPEAKER} \n\n{TOP} Estas son las TOP 5 {tweet_type} {TOP}\n\n {FINGER_DOWN}{FINGER_DOWN}{FINGER_DOWN}'
    opener = client.create_tweet(text=opener_body)

    first_body = format_category_tweet(0, category=categories[0], top=top)
    first = client.create_tweet(text=first_body, in_reply_to_tweet_id=opener.data['id'])

    second_body = format_category_tweet(1, category=categories[1], top=top)
    second = client.create_tweet(text=second_body, in_reply_to_tweet_id=first.data['id'])

    third_body = format_category_tweet(2, category=categories[2], top=top)
    third = client.create_tweet(text=third_body, in_reply_to_tweet_id=second.data['id'])

    fourth_body = format_category_tweet(3, category=categories[3], top=top)
    fourth = client.create_tweet(text=fourth_body, in_reply_to_tweet_id=third.data['id'])

    fifth_body = format_category_tweet(4, category=categories[4], top=top)
    fifth = client.create_tweet(text=fifth_body, in_reply_to_tweet_id=fourth.data['id'])

    return 'Success!'

def format_category_tweet(position, category, top):
    
    if top:
        PERCENT = UP
    else: 
        PERCENT = DOWN


    rank = EMOJIREF[position]
    name = textwrap.shorten(category['category'], width=36, placeholder=' ...')
    old_price = str(round(category['price_x'], 2)) + ' €'
    new_price = str(round(category['price_y'], 2)) + ' €'
    percent = str(round(category['difference']))

    body = f'{rank} {name} \n{EURO} {old_price} {ARROW} {new_price} \n{PERCENT} {percent}%' 

    return body