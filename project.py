import requests
import os
from pyyoutube import Api
import random

#KEY = os.environ.get('PROJECT_KEY')

class trendingVideos:

    def __init__(self,api_key):
        self.api = Api(api_key=f"{api_key}")
        self.chartedVideos = []

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
        for i in range(len(self.chartedVideos)):
            info = self.get_video_information(self.chartedVideos[i])
            print(f"{str(i+1)}. Title: {info['title']}\n Channel: {info['channel']}\n Description: {info['description']}\n ViewCount: {info['viewCount']}")
        return
    # def get_subscribers(self,channel_id):
    #     #[index]['subscriberCount'])
    
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
    
test = trendingVideos('AIzaSyBYoF9cK-a35nyziWfaxA8a3VZVXIG1ib4')
test.get_most_popular()
test.dispalyChart()
