import sqlite3
import logging

import datetime
import pandas as pd

logger = logging.getLogger()

def daily_product(db_dir):
    '''
    '''

    # Set connection
    conn = None
    try:
        conn = sqlite3.connect(db_dir)
    except Exception as e:
        logger.exception('Error connecting to database')

    # Retrieve data from today and yesterday
    sql_query = pd.read_sql_query(f'''SELECT * FROM productdata WHERE timestamp = date('now', '-1 days') OR timestamp = date('now')''', conn)
    df = pd.DataFrame(sql_query, columns = ['name', 'category', 'format', 'price', 'timestamp']).drop_duplicates()

    # Separate date into yesterday and today
    today = (datetime.datetime.now()).date()
    yesterday = (datetime.datetime.now() - datetime.timedelta(1)).date()
    
    groups = df.groupby('timestamp')
    df_today = groups.get_group(f'{today}')
    df_yesterday = groups.get_group(f'{yesterday}')

    #  Calculate price difference and sort
    merge = pd.merge(df_today, df_yesterday, on=['name', 'format', 'category'], how='outer')
    merge['difference'] = merge[['price_x', 'price_y']].pct_change(axis=1)['price_y']*100
    merge.dropna(inplace=True)
    merge.drop(merge.loc[merge['difference'] == 0].index, inplace=True)
    merge.sort_values(by='difference', ascending = False, inplace=True)
    merge.drop_duplicates()

    # extract top 5 price changes in both directions
    df_top = merge.head(5)
    df_bot = merge.tail(5)

    # convert to dictionary
    top = df_top.to_dict('records')
    bottom = df_bot.to_dict('records')
    
    return top, bottom


def weekly_product(db_dir):
    # Set connection
    conn = None
    try:
        conn = sqlite3.connect(db_dir)
    except Exception as e:
        logger.exception('Error connecting to database')

    # Retrieve data from today and yesterday
    sql_query = pd.read_sql_query(f'''SELECT * FROM productdata WHERE timestamp = date('now', '-7 days') OR timestamp = date('now')''', conn)
    df = pd.DataFrame(sql_query, columns = ['name', 'category', 'format', 'price', 'timestamp']).drop_duplicates()

    # Separate date into yesterday and today
    today = (datetime.datetime.now()).date()
    yesterday = (datetime.datetime.now() - datetime.timedelta(7)).date()
    
    groups = df.groupby('timestamp')
    df_today = groups.get_group(f'{today}')
    df_yesterday = groups.get_group(f'{yesterday}')

    #  Calculate price difference and sort
    merge = pd.merge(df_today, df_yesterday, on=['name', 'format', 'category'], how='outer')
    merge['difference'] = merge[['price_x', 'price_y']].pct_change(axis=1)['price_y']*100
    merge.dropna(inplace=True)
    merge.drop(merge.loc[merge['difference'] == 0].index, inplace=True)
    merge.sort_values(by='difference', ascending = False, inplace=True)
    merge.drop_duplicates()

    # extract top 5 price changes in both directions
    df_top = merge.head(5)
    df_bot = merge.tail(5)[::-1]

    # convert to dictionary
    top = df_top.to_dict('records')
    bottom = df_bot.to_dict('records')
    
    return top, bottom


def daily_category(db_dir):
    
    conn = None
    try:
        conn = sqlite3.connect(db_dir)
    except Exception as e:
        logger.exception('Error connecting to database')

    # Retrieve data from today and yesterday
    sql_query = pd.read_sql_query(f'''SELECT * FROM productdata WHERE timestamp = date('now', '-1 days') OR timestamp = date('now')''', conn)
    df = pd.DataFrame(sql_query, columns = ['name', 'category', 'format', 'price', 'timestamp']).drop_duplicates()

    # Separate date into yesterday and today
    today = (datetime.datetime.now()).date()
    yesterday = (datetime.datetime.now() - datetime.timedelta(1)).date()

    # SEPARATE BY TIME
    groups = df.groupby('timestamp')
    df_today = groups.get_group(f'{today}')
    df_yesterday = groups.get_group(f'{yesterday}')

    df_today = df_today.groupby(by='category')['price'].mean().reset_index()
    df_yesterday = df_yesterday.groupby(by='category')['price'].mean().reset_index()

    merge = pd.merge(df_today, df_yesterday, on='category', how='outer').dropna()
    merge['difference'] = merge[['price_x', 'price_y']].pct_change(axis=1)['price_y']*100
    merge.sort_values('difference', ascending=False, inplace=True)
    merge.drop_duplicates()

    df_top = merge.head(5)
    df_bot = merge.tail(5)[::-1]

    top = df_top.to_dict('records')
    bottom = df_bot.to_dict('records')

    return top, bottom

def weekly_category(db_dir):
    
    conn = None
    try:
        conn = sqlite3.connect(db_dir)
    except Exception as e:
        logger.exception('Error connecting to database')

    # Retrieve data from today and yesterday
    sql_query = pd.read_sql_query(f'''SELECT * FROM productdata WHERE timestamp = date('now', '-7 days') OR timestamp = date('now')''', conn)
    df = pd.DataFrame(sql_query, columns = ['name', 'category', 'format', 'price', 'timestamp']).drop_duplicates()

    # Separate date into yesterday and today
    today = (datetime.datetime.now()).date()
    yesterday = (datetime.datetime.now() - datetime.timedelta(7)).date()

    # SEPARATE BY TIME
    groups = df.groupby('timestamp')
    df_today = groups.get_group(f'{today}')
    df_yesterday = groups.get_group(f'{yesterday}')

    df_today = df_today.groupby(by='category')['price'].mean().reset_index()
    df_yesterday = df_yesterday.groupby(by='category')['price'].mean().reset_index()

    merge = pd.merge(df_today, df_yesterday, on='category', how='outer').dropna()
    merge['difference'] = merge[['price_x', 'price_y']].pct_change(axis=1)['price_y']*100
    merge.sort_values('difference', ascending=False, inplace=True)
    merge.drop_duplicates()

    df_top = merge.head(5)
    df_bot = merge.tail(5)[::-1]

    top = df_top.to_dict('records')
    bottom = df_bot.to_dict('records')

    return top, bottom