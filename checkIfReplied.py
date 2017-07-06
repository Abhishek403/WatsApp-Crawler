import csv
import os
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

CONTACT_NAME = 'Name'
NAME = 'Actual Name'
MESSAGE = 'Message'
CONTENT_PATH = 'ContentPath'
PHONE = 'Phone 1 - Value'
MESSAGE_STATUS = 'Message Status'
REPLIES = 'replies'
headers = {NAME, PHONE, MESSAGE_STATUS, REPLIES}

driver = None
input_file_path = raw_input('Enter input file path: ')
sleepTime = raw_input('Enter interval in seconds: ')
outFilePath = raw_input('Enter output file path: ')
tempFilePath = outFilePath + '.tmp'
contact_data_list = []


def web_driver_load():
    global driver
    driver = webdriver.Chrome()


def web_driver_quit():
    driver.quit()


def whatsapp_login():
    driver.get('https://web.whatsapp.com/')
    wait(10)


def openFriendChat(name):
    web_obj = driver.find_element_by_xpath("//input[@class='input input-search']")
    web_obj.send_keys(name)
    web_obj.send_keys(Keys.RETURN)


def wait(web_opening_time=3):
    time.sleep(web_opening_time)


def load_contacts_from_csv():
    with open(input_file_path, 'rb') as csvFile:
        reader = csv.DictReader(csvFile, delimiter=',')
        for t in reader:
            if t[MESSAGE_STATUS]:
                d = dict()
                d[CONTACT_NAME] = t[CONTACT_NAME]
                d[PHONE] = t[PHONE]
                d[NAME] = t[NAME]
                contact_data_list.append(d)
                # contacts.append("Himanshu Gupta")
                # contactNameMap["Himanshu Gupta"] = "Himanshu Gupta"


def write_headers(file_name):
    with open(file_name, 'w+') as out_file:
        writer = csv.DictWriter(out_file,  delimiter=',', fieldnames=headers)
        writer.writeheader()


def write_data(file_name, row):
    with open(file_name, 'a+') as out_file:
        writer = csv.DictWriter(out_file, delimiter=',', fieldnames=headers)
        writer.writerow(row)


def write_to_csv(contact_data, message_status, replies):
    replies_str = ""
    i = len(replies) - 1
    while i >= 0:
        replies_str = replies_str + replies[i] + ' |'
        i = i - 1
    with open(outFilePath, 'r+') as out_file:
        reader = csv.DictReader(out_file, delimiter=',')
        for r in reader:
            if contact_data[PHONE] == r[PHONE]:
                old_replies = r[REPLIES]
                replies_str = old_replies + ' ' + replies_str
        new_row = dict()
        new_row[NAME] = contact_data[NAME]
        new_row[PHONE] = contact_data[PHONE]
        new_row[MESSAGE_STATUS] = message_status
        new_row[REPLIES] = replies_str
        write_data(tempFilePath, new_row)


def fetch_replies():
    web_objs = driver.find_elements_by_xpath("//div[@class='msg' or @class='msg msg-continuation']/div")
    i = len(web_objs) - 1
    r = []
    if i < 0 or 'message-out' in web_objs[i].get_attribute('class'):
        return r
    while i >= 0:
        web_obj = web_objs[i]
        if ('message-out' in str(web_obj.get_attribute('class'))):
            return r
        t1 = web_obj.find_elements_by_xpath(".//span[@class='emojitext selectable-text']")
        if len(t1) != 0:
            reply = str(t1[0].text)
            r.append(reply)
        i = i - 1


def check_message_status():
    web_obj = driver.find_elements_by_xpath("//div[@class='msg' or @class='msg msg-continuation']/div")[-1]
    class_name = str(web_obj.find_element_by_xpath(".//span[contains(@class, 'icon')]").get_attribute('class'))
    if 'icon icon-msg-dblcheck' == class_name:
        return 'RECEIVED_NOT_SEEN'
    if 'icon icon-msg-dblcheck-ack' == class_name:
        return 'RECEIVED_SEEN'
    return 'NOT_RECEIVED'


if __name__ == "__main__":
    load_contacts_from_csv()
    web_driver_load()
    whatsapp_login()
    wait(5)
    changed = False
    write_headers(tempFilePath)
    while len(contact_data_list) > 0:
        for contact_data in contact_data_list:
            openFriendChat(contact_data[CONTACT_NAME])
            wait(1)
            replies = fetch_replies()
            if len(replies) > 0:
                write_to_csv(contact_data, 'RECEIVED_SEEN', replies)
                changed = True
            else:
                wait(1)
                write_to_csv(contact_data, check_message_status(), [])
                changed = True
        if changed:
            os.remove(outFilePath)
            os.rename(tempFilePath, outFilePath)
        wait(sleepTime)
    wait()
    web_driver_quit()
