from imports import *

date_today = ""
date_today_dash_format = ""
day_today = ""
time_now = ""

def get_date_today():
    global date_today
    global day_today
    global date_today_dash_format

    date_today = datetime.datetime.today()
    day_today = date_today.strftime('%d').lstrip('0')
    date_today_dash_format = date_today.strftime('%Y-%m-%d')
    date_today = date_today.strftime('%Y/%m/%d')

def get_time_now():
    global time_now

    time_now = datetime.datetime.today()
    time_now = time_now.strftime('%H:%M')