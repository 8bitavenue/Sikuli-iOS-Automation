# Import python unit tests. This is needed to create test suites and test cases.
import unittest
import time
# Import sikuli Api
from org.sikuli.script import *

# This is where you store your screenshots
# Remember to take these screenshots using the Sikuli IDE
img_dir = '/Users/me/projects/visual/images/small/'

# This is where to store your test reports
reports_dir = '/Users/me/projects/visual/reports'

# Create a global Sikuli screen object
S = Screen()

# This method keeps waiting for an image to show up then clicks it. 
# It times out after 40 trials. It can highlight the image found if needed. 
# You can also set the similarity factor when searching for images.
def waitImage(image, highlight=False, time_out=40, similarity=0.99):
    counter = 0
    img_found = None
    while img_found == None and counter < time_out:
        time.sleep(0.1)
        print '..... Waiting for image [' + image + ']'
        img_found = S.exists(Pattern(image).similar(similarity), 1)
        counter+=1
        if img_found != None:
            print('***** Found image [' + image + ']')
        if highlight:
            img_found.highlight(2)
        else:
            print('????? Could not find image [' + image + ']')
    return img_found

# This method is called before your run your suite of test cases. 
# For example you can launch the app in this module if you wish. 
# In this case we are clicking the iOS app icon. Note that this makes 
# sense only if you have more than one class of test cases otherwise 
# if you have only one class then a setup class and teardwon class is 
# all what you need.
def setUpModule():
    printLine('Module Setup', False)

    # Click app icon
    R = S.exists(Pattern(img_dir + "icon.png").similar(0.99), 1)
    if R:
        print('***** Found app icon, trying to click it...')
    S.click(R)

# Any cleanup on the module level is put here
def tearDownModule():
    printLine('Module Teardown')

# This is the base test case. You can specify the details of 
# the shared setup and teardown here.
class BaseCase(unittest.TestCase):

    # This method executes before any test case runs
    @classmethod
    def setUpClass(self):

        printLine('Class Setup')

    # This method executes after all test cases finish.
    @classmethod
    def tearDownClass(self):
        printLine('Class Teardown')

    # In this case, I am assuming my iOS app has a play button 
    # and we play a video before each test case runs.
    def setUp(self):
        printLine('Setup', False)

        # Click play button
        waitImage(img_dir + "play.png")
        S.click(Pattern(img_dir + "play.png").similar(0.95))

    # After each test case we close the video
    def tearDown(self):

        printLine('Teardown')

        # Click close
        waitImage(img_dir + "close.png")
        S.click(Pattern(img_dir + "close.png").similar(0.95))

# You can skip a class of test cases or a single case by 
# un-commented the skip below. This is a class of test cases called Sanity. 
# All test cases in this class have the setup and teardown defined earlier

#@unittest.skip("Skipping")
class Sanity(BaseCase):

    # This is the first test case, it checks if the app plays a video normally.
    #@unittest.skip("Skipping")
    def test_001_VideoPlaysNormally(self):

        printLine('001 - Video Plays Normally')

        # Wait for a given frame in the video
        self.assertNotEqual(waitImage(img_dir + "frame.png", True), None)

# This is where the script starts running, it uses a test running that generates
# xml output that is compatible with Jenkins CI
if __name__ == '__main__':
import xmlrunner
unittest.main(testRunner=xmlrunner.XMLTestRunner(output=reports_dir))
