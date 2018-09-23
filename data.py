import json
from pprint import pprint
import urllib.request
import requests
from requests_oauthlib import OAuth1
from datetime import date
import datetime
import csv

url = 'https://api.twitter.com/1.1/account/verify_credentials.json'

#auth = OAuth1() - code won't work because the keys and tokens for the twitter API were taken out for security reasons

month = {'Jan':1,'Feb':2,"Mar":3,"Apr":4,"May":5,"Jun":6,"Jul":7,"Aug":8,"Sep":9,"Oct":10,"Nov":11,"Dec":12}
requests.get(url, auth=auth)

troll_words = ["media", "vote", "liberal", "cuck", "libs", "boycott","boycot", "nra", "trump", "amendment", "resist", "infidel", "flyover", "saynoto", "kgb", "maga" "noneya", "stupid"]

link_shorteners = ["goo.gl","bit.ly","tinyurl.com","awe.sm","tiny.cc","is.gd","s2r.co"]

with open('sample-dataset.json', encoding='utf-8') as f:
    data = json.load(f)

new_data = open('data-csv.csv', 'w')
csvwriter = csv.writer(new_data)
data[0]["classification"] = "normal"
print(data[0].keys())
csvwriter.writerow(data[0].keys())

for d in range(len(data)-1):
    try:
        classification = "normal"
        user_id = data[d]['user_id']
        r = requests.get('https://api.twitter.com/1.1/users/show.json?user_id=' + user_id, auth=auth)
        try:
            tweets = r.json()['statuses_count']
            date_created = r.json()['created_at']
            date_created = date_created.split()
            day0 = date(int(date_created[5]), month[date_created[1]], int(date_created[2]))
            today = datetime.date.today()
            diff = today - day0
            avg_tweets = tweets / diff.days
        except:
            classification = "bot"

        try:
            if (avg_tweets > 10):
                if diff.days < 60:
                    classification = "troll"
                else:
                    classification = "bot"
            for link_shortener in link_shorteners:
                if (data[d]["tweet_text"].lower().find(link_shortener) != -1):
                    classification = "bot"
                    break
            for troll_word in troll_words:
                if (data[d]["user_name"].find(troll_word) != -1):
                    classification = "troll"
                    break
        except:
            classification = "bot"
        data[d]["classification"] = classification
        csvwriter.writerow(data[d].values())
    except:
        print("error on " + str(d))


