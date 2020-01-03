#!/usr/bin/python3

from config import Config
import argparse
import os
import json
from bs4 import BeautifulSoup
import requests

viewedClassifieds = []
loadedClassifieds = []

def sendSlack(new_oglas):
    url = 'https://slack.com/api/chat.postMessage'
    params = {
        "channel": "CB9J59V5H",
        "text": new_oglas,
        "username": Config.slackBotName
    }
    headers = {
        "Authorization": Config.slackAuth,
        "Content-Type": "application/json"
    }
    print(new_oglas)
    # requests.post(url, data=json.dumps(params), headers=headers)


def parseOglasnikPage(link):
    classifiedList = []
    response = requests.get(link)

    soup = BeautifulSoup(response.content, 'lxml')

    for clasified in soup.findAll('a', attrs={ 'class':'classified-box'}):
        titles = clasified.findAll('h3', attrs={ 'class':'classified-title'})
        # print(clasified.contents)
        # titleElement = BeautifulSoup(clasified.contents)

        if (len(titles) < 1):
            continue

        # classifiedTitle = titles[0].get_text()
        classifiedLink = clasified.get('href')
        # print(classifiedTitle)
        if classifiedLink not in viewedClassifieds:
            classifiedList.append(classifiedLink)

    return classifiedList

def parseNjuskaloPage(link):
    classifiedList = []
    response = requests.get(link, headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:71.0) Gecko/20100101 Firefox/71.0'})

    soup = BeautifulSoup(response.content, 'lxml')
    for classified in soup.findAll('li', attrs = {'class': 'EntityList-item--Regular'}):
        link = classified.findAll('a', attrs = {'class': 'link'})

        if len(link) < 1:
            continue

        classifiedLink = 'https://www.njuskalo.hr' + link[0].get('href')

        if classifiedLink not in viewedClassifieds:
            classifiedList.append(classifiedLink)      

    return classifiedList


parser = argparse.ArgumentParser()
parser.add_argument("--db", help="full path to DB file eg. /opt/classifieds/viewedClassifieds.db")
args = parser.parse_args()

if os.path.isfile(args.db):
    file = open(args.db, 'r+')
    viewedClassifieds = json.load(file)
    file.close()



for link in Config.oglasnikList:
    loadedClassifieds += parseOglasnikPage(link)

for link in Config.njuskaloList:
    loadedClassifieds += parseNjuskaloPage(link)

# print(loadedClassifieds)

for classified in loadedClassifieds:
    sendSlack(classified)

viewedClassifieds += loadedClassifieds

file = open(args.db, 'w+')
json.dump(viewedClassifieds, file)
file.close()