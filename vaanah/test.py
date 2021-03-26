from selenium import webdriver
#from django.contrib.staticfiles.testing import StaticLiveServerTestCase

class Test(StaticLiveServerTestCase):

  def testform(self):
    selenium = webdriver.Chrome()
    