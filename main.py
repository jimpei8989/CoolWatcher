from selenium import webdriver

import time, random
from argparse import ArgumentParser
from multiprocessing import Pool

import secret

class CoolWatcher():
    def __init__(self):
        options = webdriver.ChromeOptions()
        #  options.add_argument('--headless')
        options.add_argument('--mute-audio')
        self.driver = webdriver.Chrome(options = options)
        self.driver.get('https://cool.ntu.edu.tw')

        self.openTabs = set()
        self.mainTab = self.driver.current_window_handle
        self.openTabs.add(self.mainTab)

        time.sleep(0.1)

    def __del__(self):
        self.driver.quit()

    def createNewTab(self, URL = ''):
        self.driver.execute_script(f'window.open("{URL}");')
        newTab = [t for t in self.driver.window_handles if t not in self.openTabs][0]
        self.openTabs.add(newTab)
        return newTab

    def closeTab(self, tab):
        self.openTabs.remove(tab)
        self.driver.switch_to.window(tab)
        self.driver.close()

    def login(self):
        self.driver.find_element_by_id('saml').click()
        self.driver.find_element_by_id('ContentPlaceHolder1_UsernameTextBox').send_keys(secret.username)
        self.driver.find_element_by_id('ContentPlaceHolder1_PasswordTextBox').send_keys(secret.password)
        self.driver.find_element_by_id('ContentPlaceHolder1_SubmitButton').click()
        print('> Successfully login!')

    def play(self, URL):
        time.sleep(random.random() * 30)
        self.driver.get(URL)
        time.sleep(1)

        try:
            # Go into the iframe
            self.driver.switch_to.frame('tool_content')

            button = self.driver.find_element_by_class_name('vjs-big-play-button')
            button.click()
            print(f'+ Now playing {URL}')

            while True:
                time.sleep(30)
                try:
                    replayButton = self.driver.find_element_by_class_name('vjs-ended')
                    print(f'+ End playing {URL}')
                    return
                except:
                    print(f'Keep playing {URL}')
        except:
            print(f'- Fail to play {URL}')
            return

    def GetAllURLs(self, courseID):
        newTab = self.createNewTab()
        self.driver.switch_to.window(newTab)
        self.driver.get(f'https://cool.ntu.edu.tw/courses/{courseID}/modules')

        urls = list(map(lambda e : e.get_attribute('href'), self.driver.find_elements_by_class_name('item_link')))
        return urls

def PlayOne(url):
    watcher = CoolWatcher()
    watcher.login()
    watcher.play(url)
    del watcher

def main():
    args = parseArguments()
    # Retrieve all urls
    head = CoolWatcher()
    head.login()
    urls = head.GetAllURLs(args.courseId)
    del head

    with Pool(args.numWorkers) as p:
        p.map(PlayOne, urls)

def parseArguments():
    parser = ArgumentParser()
    parser.add_argument('--courseId')
    parser.add_argument('--numWorkers', type=int, default=4)
    return parser.parse_args()

if __name__ == '__main__':
    main()
