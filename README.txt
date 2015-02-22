------------------
dumpmon-scraper.py
------------------

This is a simple script that will open the last 20 links from the @Dumpmon
(https://twitter.com/dumpmon) twitter account, dig through the info, and send an
email alert to you based on a keyword you define. 


------------------
Prerequisites
------------------

You'll need to create a new Twitter app at https://apps.twitter.com in order to
get the keys and tokens necessary to scrape the info. 
    1. Click "Create New App" and fill out the info
    2. After the app is created, look at the "Keys and Access Tokens" tab to
       find the info necessary to run this script
    3. Update the variables in the config.cfg file with the tokens for twitter
       and your search details

    NOTE: There is an ".example_config.cfg" file for you - remove the "example_"
          from the filename before executing (but leave the '.')

Also check that you have the prerequisites by running 'check-prereq.py'


------------------
Running
------------------

./dumpmon-scraper.py

Simple enough :) I have it cron'd, but it can be run adhoc as well
