# Description and Architecture
This repo give sample how to do simple network chatops (network operation/monitoring using chat/messaging platform). Environment used are Slack as messaging platform, Google Cloud Functions as serverless infrastructure and IOS-XE as managed device.

This function developed to be run on serverless architecture that provides HTTP/HTTPS endpoint to be called by external system to be used for daily network operation on chat platform e.g Slack. Please refer to below architecture:
![Image of Environment](https://user-images.githubusercontent.com/9415402/100731219-b026b000-33fd-11eb-9ae9-0f550323115b.png)

# How to Setup

## Step 1
-Put Slack Verification Token into parameter in *config.json*. You can disobey the other parameters in the file.

-**Rename *showprocesscpu.py* to *main.py*** as GCF's function will execute "main.py" for each created function. function showprocesscpu is the main receiving endpoint from Slack. It parses slack command and response url to be processed further. It will give immediate respond to slash command issuer and publish pubsub message for further processing (slack requires slash command to be replied within 3 seconds)

-make a zip file containing 3 files: 
main.py 
config.json 
requirements.txt 

## Step 2
-Next step is to create function on Google Gloud Function (GCF). You need to create function with following parameters:
Trigger Type: HTTP
Authentication: Allow Unauthenticated Invocation
Runtime: Python 3.7
Entry Point: pubsub_handler

-Upload the zip file prepared in Step 1.

-Note "Trigger URL" generated to be configured later on Slack's slash command configuration (https://api.slack.com/interactivity/slash-commands)

For detailed explanation on creating GCF Function please refer to: https://cloud.google.com/functions/docs/quickstart-python


## Step 3
-Rename *taskhandler.py* to *main.py* and put to a zip file
function taskhandler will be called using pubsub after function showprocesscpu is called. This function will extract slash command instruction and do necessary resconf call to ios xe device, do some message formatting and send back to slack's channel

## Step 4
-Create another function on GCF. It is different with previous function as it will be triggered by pubsub using specific topic, not a HTTP request. You need to create the function with following parameters:
Trigger Type: Cloud Pub/Sub
Topic: yourprojectid/taskhandler (create using CREATE A TOPIC option)
Runtime: Python 3.7
Entry Point: hello_pubsub

-Upload zip file prepared in step 3

## Step 5
-Prepare Slack App and Slash Command in Slack environment. When configuring slash command put the Trigger URL gotten from Step 2 as webhook URL
For reference please refer to Slack documentation: https://api.slack.com/interactivity/slash-commands

# Output Example

When it's all setup, we can access network resource information using Slack Channel.

Issuing Slack Slash Command in channel:
![Image of Command](https://user-images.githubusercontent.com/9415402/100743118-6db99f00-340e-11eb-8bb2-6091650b738a.png)

Result returned in Slack's channel:
![Image of Result](https://user-images.githubusercontent.com/9415402/100743296-b6715800-340e-11eb-943d-72d257a80d2f.png)
