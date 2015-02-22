#!/usr/bin/env python


import twitter
import requests
import smtplib
from email.mime.text import MIMEText
import os
import ConfigParser


config = ConfigParser.ConfigParser()
config.read('.config.cfg')

alert_txt_file = config.get('config', 'alert_txt_file')
dump_txt_file = config.get('config', 'dump_txt_file')
email_to = config.get('config', 'email_to')
email_from = config.get('config', 'email_from')
email_subject = config.get('config', 'email_subject')
smtp_server = config.get('config', 'smtp_server')
search_string = config.get('config', 'search_string')
twitter_user = config.get('config', 'twitter_user')
consumer_key = config.get('config', 'consumer_key')
consumer_secret = config.get('config', 'consumer_secret')
access_token_key = config.get('config', 'access_token_key')
access_token_secret = config.get('config', 'access_token_secret')

class Dumpmon(object):

    def __init__(self):
        self.status = []
        self.links = []
        self.twitter_user = twitter_user
        self.api = twitter.Api(consumer_key=consumer_key,
                               consumer_secret=consumer_secret,
                               access_token_key=access_token_key,
                               access_token_secret=access_token_secret)

    def get_tweets(self):
        return self.api.GetUserTimeline(screen_name=self.twitter_user)

    def get_links(self):
        for s in self.get_tweets():
            self.links.append(s.text.split(" ")[0])


def get_link_output(link):
    r = requests.get(link)
    return r.text


def remove_old_dump_and_alert_txts():
    if os.path.isfile(dump_txt_file):
        os.remove(dump_txt_file)
    if os.path.isfile(alert_txt_file):
        os.remove(alert_txt_file)


def scrape_info_from_links():
    f = open(dump_txt_file, 'w+')
    for link in tweets.links:
        if link.startswith('http'):
            f.write(get_link_output(link).encode('utf-8'))
    f.close()


def search_for_text():
    alert = open(alert_txt_file, 'w+')
    with open(dump_txt_file) as final:
        for line in final:
            if search_string in line:
                alert.write(line.strip())
    alert.close()


def send_alert_email():
    alert = open(alert_txt_file, 'r')
    msg = MIMEText(alert.read())
    alert.close()
    msg['Subject'] = email_subject
    msg['From'] = email_from
    msg['To'] = email_to
    s = smtplib.SMTP(smtp_server)
    s.sendmail(email_from, email_to, msg.as_string())
    s.quit()


if __name__ == '__main__':
    try:
        tweets = Dumpmon()
        tweets.get_links()
        remove_old_dump_and_alert_txts()
        scrape_info_from_links()
        search_for_text()
        if os.stat(alert_txt_file).st_size > 0:
            send_alert_email()
    except Exception, e:
        print e
