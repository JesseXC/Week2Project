import unittest
import os
import requests
from pyyoutube import Api
from project import TrendingVideos
#command to run the test:
#python3 -m unittest test_project.py

class TestProject(unittest.TestCase):

    def setUp(self):
        self.dummyObject = TrendingVideos(os.environ.get('PROJECT_KEY'))
        self.videoList = self.dummyObject.get_most_popular(10)

    def test_get_video_information(self):
        #I'm thinking about adding a loop here to test the 10 videos inside the list
        dataDict = self.dummyObject.get_video_information(self.videoList[0])
        self.assertEqual(dataDict["title"],self.videoList[0].snippet.localized.title)
        self.assertEqual(dataDict["channel"],self.videoList[0].snippet.channelTitle)
        self.assertEqual(dataDict["description"],self.videoList[0].snippet.localized.description)
        self.assertEqual(dataDict["viewCount"],self.videoList[0].statistics.viewCount)

    # def test_get_channel_statistics(self):
