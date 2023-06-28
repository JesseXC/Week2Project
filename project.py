import requests
import os
from pyyoutube import Api
import random
import pandas as pd
import sqlalchemy as db
import wikipediaapi
import translators as ts ts.google

class TrendingVideos:

    def __init__(self, api_key):
        self.api = Api(api_key=f"{api_key}")
        self.chartedVideos = []
        self.engine = db.create_engine('sqlite:///youtube_most_popular.db')
        self.wiki = wikipediaapi.Wikipedia('en')
    
    def store_wiki_info(self, channel_name):
        page = self.wiki.page(f'{channel_name}')
        if page.exists():
            wiki_data = {
                'title': page.title,
                'summary': page.summary
            }
            df = pd.DataFrame([wiki_data])
            df.to_sql('wiki_information', con=self.engine, if_exists='replace', index=False)
        else:
            print("Wiki page does not exist!")

    def display_wiki_info(self, channel_name):
        with self.engine.connect() as connection:
            query_result = connection.execute(db.text(f"SELECT * FROM wiki_information WHERE title = '{channel_name}'")).fetchall()
            df = pd.DataFrame(query_result, columns=['title', 'summary'])
            print(df)

    def get_channel_statistics(self, channel_id):
        info = self.api.get_channel_info(channel_id=f"{channel_id}")
        return info.items[0].to_dict()
    
    def get_video_information(self, video_object):
        info = {}
        info["title"] = video_object.snippet.localized.title
        info["channel"] = video_object.snippet.channelTitle	
        info["description"] = video_object.snippet.localized.description
        info["viewCount"] = video_object.statistics.viewCount
        return info
    
    def display_chart(self, videos):
        for i, video in enumerate(videos):
            info = self.get_video_information(video)
            print(f"{i+1}. Title: {info['title']}\n   Channel: {info['channel']}\n   Description: {info['description']}\n   ViewCount: {info['viewCount']}\n")

    def store_video_information(self):
        video_data = []
        for video in self.chartedVideos:
            info = self.get_video_information(video)
            video_data.append(info)
        df = pd.DataFrame(video_data)
        df.to_sql('video_information', con=self.engine, if_exists='replace', index=False)
        with self.engine.connect() as connection:
            query_result = connection.execute(db.text("SELECT * FROM video_information;")).fetchall()
            print(pd.DataFrame(query_result))
    
    def get_most_popular(self, num_videos):
        response = self.api.get_i18n_regions(parts=['snippet']).items
        regions = []
        for region in response:
            regions.append(region.snippet.gl)
        random_regions = random.choices(regions, k=num_videos)
        for region in random_regions:
            video_by_chart = self.api.get_videos_by_chart(chart="mostPopular", region_code=region, count=1)
            self.chartedVideos.append(video_by_chart.items[0])
        return self.chartedVideos

api_key = "AIzaSyBYoF9cK-a35nyziWfaxA8a3VZVXIG1ib4"
trending = TrendingVideos(api_key)

while True:
     num_videos = int(input("How many random videos from around the world would you like? (Enter a number, 0 to exit): "))
    if num_videos == 0:
        print("Exiting the program...")
        break
    videos = trending.get_most_popular(num_videos)
    trending.display_chart(videos)
    print()
    show_wiki_info = input("Would you like to see the Wikipedia page for any of the channels? Enter the corresponding video number or 'N' to skip: ")
    if show_wiki_info.lower() == 'n':
        continue
    video_number = int(show_wiki_info) - 1
    if video_number < 0 or video_number >= len(videos):
        print("Invalid video number")
        continue
    channel_title = videos[video_number].snippet.channelTitle
    trending.store_wiki_info(channel_title)
    trending.display_wiki_info(channel_title)
