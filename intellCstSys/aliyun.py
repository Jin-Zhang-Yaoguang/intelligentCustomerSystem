# -*- coding: utf-8 -*-
import sys
from typing import List
from alibabacloud_chatbot20171011.client import Client as Chatbot20171011Client
from alibabacloud_tea_openapi import models as open_api_models
from alibabacloud_chatbot20171011 import models as chatbot_20171011_models


class ChatRobot:
    def __init__(self, access_key_id, access_key_secret, instance_id):
        self.access_key_id = access_key_id
        self.access_key_secret = access_key_secret
        self.instance_id = instance_id

    def create_client(self):
        config = open_api_models.Config(
            access_key_id=self.access_key_id,
            access_key_secret=self.access_key_secret
        )
        config.endpoint = 'chatbot.cn-shanghai.aliyuncs.com'
        client = Chatbot20171011Client(config)
        return client

    def create_chat(self, client, utterance):
        chat_request = chatbot_20171011_models.ChatRequest(
            instance_id=self.instance_id,
            utterance=utterance
        )
        response = client.chat(chat_request)
        return response.body


def one_chat(question):
    chatRobot = ChatRobot(AK, SK, 'chatbot-cn-aMuUnVBYfa')
    client = chatRobot.create_client()
    response = chatRobot.create_chat(client, question)
    response = eval(str(response))
    type = response['Messages'][0]['Type']
    content = ''
    if type == 'Text':
        content = response['Messages'][0]['Text']['Content']
    elif type == 'Knowledge':
        content = response['Messages'][0]['Knowledge']['Content']
    if content == '':
        content = '这个问题我回答不了，我会尽快学习的~'
    return content
