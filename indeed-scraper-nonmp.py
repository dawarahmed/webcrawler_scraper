import os
import requests
import time
import re
from selenium import webdriver
from bs4 import BeautifulSoup
import time
from multiprocessing import Pool


def create_data_files():

    if not os.path.isfile("crawled.txt"):
        write_file("crawled.txt", [])
        return []
    else:
        return read_crawled()

def write_file(file_name, text):

    f = open(file_name, 'w')
    for cur_text in text:
        f.write(cur_text + "\n")
    f.close()

def read_crawled():

    cur_crawled = []

    with open("crawled.txt", 'r') as file:
        line = file.readline()
        while line:
            cur_crawled.append(line.strip())
            line = file.readline()

    return cur_crawled

def set_up_queue(cur_crawled):

    starts = [0, 10, 20, 30, 40, 50]
    cur_queue = []

    for start in starts:

        result = requests.get("https://www.indeed.com/jobs?q=Software+Engineer&l=San+Francisco,+CA&explvl=entry_level&sort=date&start=" + str(start))
        soup = BeautifulSoup(result.content, 'html.parser')

        mydivs = soup.find_all("div", class_="title")
        for divs in mydivs:
            for link in divs.find_all('a', href=True):
                new_link = link.get('href')

                if not new_link in cur_crawled:
                    cur_queue.append('indeed.com' + link.get('href'))

    return cur_queue


def crawling(new_queue):

    cur_jobs = []

    for link in new_queue:

        count = requests.get('http://' + link).text.count('Java')

        if (count > 0):
            cur_jobs.append(link)

    return cur_jobs


if __name__ == '__main__':

    start_time = time.time()

    cur_crawled = create_data_files()
    cur_queue = set_up_queue(cur_crawled)

    jobs = crawling(cur_queue)

    write_file("jobs.txt", jobs)

    print("--- %s seconds ---" % (time.time() - start_time))
