from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from LogInData import username, password
import time
import random
from selenium.common.exceptions import NoSuchElementException

class InstagramBot():
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.browser = webdriver.Chrome('/your/path/chromedriver')

    def close(self):
        self.browser.close()
        self.browser.quit()

    def login(self):
        browser = self.browser
        browser.get('https://www.instagram.com')
        time.sleep(random.randrange(3, 5))

        username_input = browser.find_element_by_name('username')
        username_input.clear()
        username_input.send_keys(username)

        time.sleep(2)

        password_input = browser.find_element_by_name('password')
        password_input.clear()
        password_input.send_keys(password)

        password_input.send_keys(Keys.ENTER)
        time.sleep(5)

    def like_it(self, hashtag):
        browser = self.browser
        browser.get(f'https://www.instagram.com/explore/tags/{hashtag}/')
        time.sleep(5)

        for i in range(1, 4):
            browser.execute_script('window.scrollTo(0, document.body.scrollHeight);')
            time.sleep(random.randrange(3, 5))

        hrefs = browser.find_elements_by_tag_name('a')
        posts_urls = [item.get_attribute('href') for item in hrefs if "/p/" in item.get_attribute('href')]

        for url in posts_urls:
            try:
                browser.get(url)
                time.sleep(3)
                like_button = browser.find_element_by_xpath(
                    '/html/body/div[1]/section/main/div/div[1]/article/div[3]/section[1]/span[1]/button').click()
                time.sleep(random.randrange(30, 40))
            except Exception as ex:
                print(ex)
                self.close()

    def el_exists(self, url):

        browser = self.browser
        try:
            browser.find_element_by_xpath(url)
            exist = True
        except NoSuchElementException:
            exist = False
        return exist

    def likes_by_url(self, userpage):

        browser = self.browser
        browser.get(userpage)
        time.sleep(3)


        not_exist = '/html/body/div[1]/section/main/div/h2'
        if self.el_exists(not_exist):
            print('url does not exist')
            self.browser.close()
        else:
            print('like it!')
            time.sleep(3)

            count = int(browser.find_element_by_xpath('/html/body/div[1]/section/main/div/header/section/ul/li[1]/span/span').text)
            iter_count = int(count / 12)
            print(iter_count)

            catched_urls = []
            for i in range(0, iter_count):
                hrefs = browser.find_elements_by_tag_name('a')
                hrefs = [item.get_attribute('href') for item in hrefs if '/p/' in item.get_attribute('href')]

                for href in hrefs:
                    catched_urls.append(href)

                browser.execute_script('window.scrollTo(0, document.body.scrollHeight);')
                time.sleep(random.randrange(2, 5))
                print(f'iteration #{i}')

            file_name = userpage.split('/')[-2]

            with open(f'{file_name}.txt', 'a') as file:
                for catched_url in catched_urls:
                    file.write(catched_url + '\n')

                set_catched_urls = set(catched_urls)
                set_catched_urls = list(set_catched_urls)

                with open(f'{file_name}_set.txt', 'a') as file:
                    for catched_url in set_catched_urls:
                        file.write(catched_url + '\n')\

                with open(f'{file_name}_set.txt') as file:
                    urls_list = file.readlines()

                    for catched_url in urls_list[0:6]:
                        try:
                            browser.get(catched_url)
                            time.sleep(2)

                            like_button = '/html/body/div[1]/section/main/div/div/article/div[3]/section[1]/span[1]/button'
                            browser.find_element_by_xpath(like_button).click()
                            time.sleep(random.randrange(80, 100))
                            time.sleep(2)

                            print(f'{catched_url} is liked!')
                        except Exception as ex:
                            print(ex)
                            self.close()

                self.close()


                self.close()


bot = InstagramBot(username, password)
bot.login()
bot.likes_by_url('https://www.instagram.com/username/')
