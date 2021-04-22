# -*- coding: utf-8 -*-
"""
Created on Thu Apr 22 15:49:35 2021

@author: logankao
"""

from flask import Flask, abort, request

# https://github.com/line/line-bot-sdk-python
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

app = Flask(__name__)

line_bot_api = LineBotApi("5zH5Jqhngz6pNsOO2buDwZb9CiEtmsjGSqLRwiSWFZJyFdhzyophyHMIOHqkAfdE5Kb6l+MnS0eWvjFzlzAO7dFXp3s8+XOG6xxkGqk6N2MX7HmLqomAm0haADWfd1YQSz37smbB0+ijYlmNPq1/TgdB04t89/1O/w1cDnyilFU=")
handler = WebhookHandler("241e28de45063bf87dd63f1b93b7f727")


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))


if __name__ == "__main__":
    app.run()