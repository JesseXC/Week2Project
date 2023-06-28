import unittest
from project import trendingVideos

class TestProject(unittest.TestCase):

    def setup(self):
        self.testFunc = trendingVideos()