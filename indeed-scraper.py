import os
import requests
import time
import re
from selenium import webdriver
from bs4 import BeautifulSoup

def create_data_files():

    if not os.path.isfile("crawled.txt"):
        write_file("crawled.txt", cur_crawled)
    else:
        read_crawled()

def write_file(file_name, text):

    f = open(file_name, 'w')
    for cur_text in text:
        f.write(cur_text + "\n")
    f.close()

def read_crawled():

    global cur_crawled
    cur_crawled = []

    with open("crawled.txt", 'r') as file:
        line = file.readline()
        while line:
            cur_crawled.append(line.strip())
            line = file.readline()

def set_up_queue():

    starts = [0, 10, 20, 30, 40, 50]
    global cur_queue

    for start in starts:

        result = requests.get("https://www.indeed.com/jobs?q=Software+Engineer&l=San+Francisco,+CA&explvl=entry_level&sort=date&start=" + str(start))
        soup = BeautifulSoup(result.content, 'html.parser')

        mydivs = soup.find_all("div", class_="title")
        for divs in mydivs:
            for link in divs.find_all('a', href=True):
                cur_queue.append('indeed.com' + link.get('href'))


cur_crawled = []
cur_queue = []

create_data_files()
set_up_queue()
write_file("queue.txt", cur_queue)


