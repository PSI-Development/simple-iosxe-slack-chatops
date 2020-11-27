# simple-iosxe-slack-chatops
Some functions that could be hosted in server-less infrastructure e.g Google Cloud Function for managing Cisco IOS-XE using Slack

## How it Works
This repo give sample how to do simple chatops (network operation using chat/messaging platform) using Slack as messaging platform and Google Cloud Function as serverless infrastructure

showprocesscpu.py --> host it in google cloud function, it will receive call from Slack's slash command (please refer to slack documentation on how to setup slash command i.e. https://api.slack.com/interactivity/slash-commands). It will give immediate respond to slash command issuer and publish pubsub message for further processing (slack requires slash command to be replied within 3 seconds)

taskhandler.py --> it will be called using pubsub after showprocesscpu is called. This function will extract slash command instruction and do necessary resconf call to ios xe device, do some message formatting and send back to slack's channel
