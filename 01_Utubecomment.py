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
url = "https://www.youtube.com/results?search_query=final+fantsy"

# use a chrome core. https://chromedriver.chromium.org/downloads
bot = webdriver.Chrome(executable_path="assets/chromedriver.exe") # if you are a mac user, please use "assets/chromedriver"
bot.get(url)

f = open("assets/ffyoutube.csv", "a", encoding="utf-8")
f.write('Title, Duration, Views, Uploader, Status, Details, Cover-image \n')
start = datetime.datetime.now()
time_limit = 60
texts = []

# Read the Xpath tutorial if you are not familiar with XPath.
# "//" operator indicates Selects nodes in the document from the current node that match the selection no matter where they are.
while len(bot.find_elements_by_xpath('//class[contains(text(), "Searches related to")]')) != 1:
    time.sleep(5)
    bot.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    soup = BeautifulSoup(bot.page_source, 'html5lib')
    videos = soup.find_all('ytd-video-renderer')[-20:] # only process the newly-acquired videos.
    if int((datetime.datetime.now() - start).seconds) >= time_limit: # if longer than a minute, then stop scrolling.
        break
    for video in videos:
        try:
            video_name = video.find(id="video-title").text
            video_name = video_name.replace('\n', ' ').replace('\r', '')
            video_duration = video.find("span", class_="style-scope ytd-thumbnail-overlay-time-status-renderer").text
            video_duration = video_duration.replace('\n', ' ').replace('\r', '')
            video_data = video.find('span', class_='style-scope ytd-video-meta-block').contents
            video_views = video_data[0]
            video_publisher = video.find("a", class_='yt-simple-endpoint style-scope yt-formatted-string').text
            text = video.find("yt-formatted-string", id="description-text").text
            is_video_new = video.find("span", class_="style-scope ytd-badge-supported-renderer").text
            video_cover = video.find_all('img', {'class': 'style-scope yt-img-shadow'})[0].attrs["src"]
            regex = re.compile(r'[\n\r\t]')
            text = regex.sub(" ", text)
            record = '%s, %s, %s, %s, %s, %s, %s \n' % (video_name, video_duration, video_views, video_publisher, is_video_new, text, video_cover)
            print(record)
            f.write(record)
            texts.append(text)
        except:
            pass
f.close()
bot.close()
print("finished")

if __name__ == "__main__":
    pass
