import requests
import os
from pyyoutube import Api
import random
import pandas as pd
import sqlalchemy as db

#KEY = os.environ.get('PROJECT_KEY')

class trendingVideos:

    def __init__(self,api_key):
        self.api = Api(api_key=f"{api_key}")
        self.chartedVideos = []
        self.engine = db.create_engine('sqlite:///youtube_most_popular.db')
    
    def get_channel_statistics(self,channel_id):
        info = self.api.get_channel_info(channel_id=f"{channel_id}")
        return info.items[0].to_dict()
    
    def get_channle_description(self,channel_id):
        diciontary  = self.get_channel_statistics()
        return dictionary['snippet']['description']
    
    def get_video_information(self,video_object):
        info = {}
        info["title"] = video_object.snippet.localized.title
        info["channel"] = video_object.snippet.channelTitle	
        info["description"] = video_object.snippet.localized.description
        info["viewCount"] = video_object.statistics.viewCount
        return info
    
    def dispalyChart(self):
        with self.engine.connect() as connection:
            query_result = connection.execute(db.text("SELECT * FROM video_information;")).fetchall()
            df = pd.DataFrame(query_result, columns=['title', 'channel', 'description', 'viewCount'])
            for i in range(len(df)):
                print(f"{i+1}. Title: {df.loc[i, 'title']}\n Channel: {df.loc[i, 'channel']}\n Description: {df.loc[i, 'description']}\n ViewCount: {df.loc[i, 'viewCount']}")
        return

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
    
    def get_most_popular(self):
        response = self.api.get_i18n_regions(parts=['snippet']).items
        regions = []
        for region in response:
            regions.append(region.snippet.gl)
        random_regions = random.choices(regions, k=10)
        for region in random_regions:
            video_by_chart = self.api.get_videos_by_chart(chart="mostPopular", region_code = region, count=1)
            self.chartedVideos.append(video_by_chart.items[0])
        return video_by_chart.items

    
test = trendingVideos('')
test.get_most_popular()
test.store_video_information()
test.dispalyChart()
