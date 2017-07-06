number_of_times = 2

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import csv
import os

CONTACT_NAME = 'Name'
NAME = 'Actual Name'
MESSAGE = 'Message'
CONTENT_PATH = 'ContentPath'
PHONE = 'Phone 1 - Value'
MESSAGE_STATUS = 'Message Status'

driver = None
in_file_name = raw_input('Enter the file name: ')
temp_file_name = in_file_name + ".tmp"
contacts = []
data = []
message = 'Hello, this is a dummy message, please ignore!'


#
# with open(filename, 'rb') as csvFile:
#     reader = csv.reader(csvFile, delimiter=',')
#     for t in reader:
#         d = dict()
#         d[CONTACT_NAME] = t[CONTACT_NAME]
#         d[NAME] = t[NAME]
#         d[MESSAGE] = t[MESSAGE]
#         d[CONTENT_PATH] = t[CONTENT_PATH]
#         data.append(d)


def wait(web_opening_time=3):
    time.sleep(web_opening_time)


def web_driver_load():
    global driver
    driver = webdriver.Chrome()


def web_driver_quit():
    driver.quit()


def whatsapp_login():
    driver.get('https://web.whatsapp.com/');
    wait(10)


def openFriendChat(name):
    web_obj = driver.find_element_by_xpath("//input[@class='input input-search']")
    web_obj.send_keys(name)
    web_obj.send_keys(Keys.RETURN)


def sendMessage(msg='Hi!'):
    web_obj = driver.find_element_by_xpath("//div[@contenteditable='true']")
    web_obj.send_keys(msg)
    web_obj.send_keys(Keys.RETURN)


def sendVideo(path='/Users/abhishekdas/Downloads/6.JPG.jpg'):
    wait(1)
    driver.find_elements_by_xpath("//button[@title='Attach']")[0].click()
    wait(1)
    driver.find_elements_by_xpath("//div[@class='menu-item active']/span/div/div/ul/li")[0].click()
    wait(1)
    uploadFiles(path)


def uploadFiles(path):
    driver.find_element_by_xpath("//input[@type='file']").send_keys(path)
    wait(1)
    driver.find_element_by_xpath("//div[@contenteditable='true']").send_keys(Keys.RETURN)


def update_status_when_mssg_send(filename, row, headers):
    with open(filename, 'a+') as in_file:
        writer = csv.DictWriter(in_file, delimiter=',', fieldnames=headers)
        writer.writerow(row)


def write_headers(filename, headers):
    with open(filename, 'w+') as csv_file:
        writer = csv.DictWriter(csv_file, delimiter=',', fieldnames=headers)
        writer.writeheader()


if __name__ == "__main__":
    web_driver_load()
    whatsapp_login()
    wait(1)
    with open(in_file_name, 'r+') as csvFile:
        reader = csv.DictReader(csvFile, delimiter=',')
        headers = reader.fieldnames
        write_headers(temp_file_name, headers)
        for t in reader:
            sent = False
            try:
                openFriendChat(t[CONTACT_NAME])
                wait()
                msg = t[MESSAGE]
                videoAudioPath = t[CONTENT_PATH]
                if msg:
                    msg = 'Hi ' + t[NAME] + ", " + msg
                    sendMessage(msg)
                    sent = True
                    wait()

                if videoAudioPath:
                    sendVideo(videoAudioPath)
                    sent = True
                    wait()
            except ValueError:
                sent = False
            t[MESSAGE_STATUS] = sent
            update_status_when_mssg_send(temp_file_name, t, headers)
            # for i in range(number_of_times):
            #     # sendMessage(message)
            #     sendVideo()
            #     wait()
            print("Successfully send message to contact: " + t[NAME])
    os.remove(in_file_name)
    os.rename(temp_file_name, in_file_name)
    wait()
    web_driver_quit()
