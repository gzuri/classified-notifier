#!/usr/bin/python3

from config import Config
import json
import requests
import os


class Utils:

    def sendToSlack(message):
        url = 'https://slack.com/api/chat.postMessage'
        params = {
            "channel": "CB9J59V5H",
            "text": message,
            "username": "Classifields!"
        }
        headers = {
            "Authorization": Config.slackAuth,
            "Content-Type": "application/json"
        }
        response = requests.post(url, data=json.dumps(params), headers=headers)

