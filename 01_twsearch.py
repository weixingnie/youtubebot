# created on Dec 24, 2020
# @author:          Bo Zhao
# @email:           zhaobo@uw.edu
# @website:         https://hgis.uw.edu
# @organization:    Department of Geography, University of Washington, Seattle
# @description:     Search tweets of a specific topic using a web crawler

from selenium import webdriver
from bs4 import BeautifulSoup
import time, datetime, json, re


# url = "https://twitter.com/search?l=&q=near%3A%22houston%22%20within%3A15mi%20since%3A2017-08-24%20until%3A2017-08-31&src=typd&lang=en"  #crawlling all the tweets posted near Houston during the Hurricane Harvey attacked period.
url = "https://twitter.com/search?f=tweets&vertical=news&q=wuhan&src=typd&lang=en"

# use a chrome core. https://chromedriver.chromium.org/downloads
bot = webdriver.Chrome(executable_path="assets/chromedriver") # if you are a mac user, please use "assets/chromedriver"
bot.get(url)

f = open("assets/tweets.csv", "a", encoding="utf-8")
f.write('user_name, screen_name, created_at, time_integer, reply_num, retweet_num, favorite_num, content \n')
start = datetime.datetime.now()
time_limit = 60
texts = []

# Read the Xpath tutorial if you are not familiar with XPath.
# "//" operator indicates Selects nodes in the document from the current node that match the selection no matter where they are.
while len(bot.find_elements_by_xpath('//div[contains(text(), "Back to top ↑")]')) != 1:
    time.sleep(5)
    bot.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    soup = BeautifulSoup(bot.page_source, 'html.parser')
    tweets = soup.find_all('article')[-20:] # only process the newly-acquired tweets.
    if int((datetime.datetime.now() - start).seconds) >= time_limit: # if longer than a minute, then stop scrolling.
        break
    for tweet in tweets:
        try:
            user_name = tweet.find('span', dir="ltr").text
            screen_name = tweet.find('span', class_='css-901oao css-16my406 r-1qd0xha r-ad9z0x r-bcqeeo r-qvutc0').text
            text = tweet.find('div', lang='en').text
            created_at = tweet.find("time").text
            time_integer = tweet.find("time").attrs['datetime']
            reply_retweets = tweet.find('div', class_='css-1dbjc4n r-18u37iz r-1wtj0ep r-156q2ks r-1mdbhws').contents
            reply_num = reply_retweets[0].text
            retweet_num = reply_retweets[1].text
            favorite_num = reply_retweets[2].text
            inst_url = ""
            if "www.instagram.com" in text:
                inst_url = tweet.p.a.attrs["title"]
            regex = re.compile(r'[\n\r\t]')
            text = regex.sub(" ", text)
            record = '%s, %s, %s, %s, %s, %s, %s, %s \n' % (user_name, screen_name, created_at, time_integer, reply_num, retweet_num, favorite_num, text)
            print(record)
            if (text not in texts):
                f.write(record)
            texts.append(text)
        except:
            pass
f.close()
bot.close()
print("finished")

if __name__ == "__main__":
    pass
