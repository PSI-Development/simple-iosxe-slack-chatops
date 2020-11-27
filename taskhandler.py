import base64
import json
import requests
import os
    
def process_pubsub(event, context):
    """Triggered from a message on a Cloud Pub/Sub topic.
    Args:
         event (dict): Event payload.
         context (google.cloud.functions.Context): Metadata for the event.
    """
    ios_username = os.environ.get['IOS_USERNAME']
    ios_password = os.environ.get['IOS_PASSWORD']

    # Get published data, get slack's response url and do restconf call to IOS-XE NE
    pubsub_message = base64.b64decode(event['data']).decode('utf-8')
    json_payload = json.loads(pubsub_message)
    slack_url = json_payload['response_url']
    resp = requests.get(json_payload['ios_url'], auth=(ios_username, ios_password), verify=False, headers={'Accept': 'application/yang-data+json'})
    pk = next(iter(json.loads(resp.text)))
    params = json.loads(resp.text)[pk]

    # Formatting returned data from IOS-XE NE to be send to slack's channel
    msg_canvass = {
        "blocks": [
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "*" + pk.split(":")[0] + "*\n" + pk.split(":")[1] + " status per " + resp.headers["Date"]
                }
            },
            {
                "type": "divider"
            },
            
            {
                "type": "divider"
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "*Would you like me to send you periodic update of this statistic?*"
                }
            },
            {
                "type": "actions",
                "elements": [
                    {
                        "type": "button",
                        "text": {
                            "type": "plain_text",
                            "text": "YES"
                        },
                        "value": "click_me_123"
                    },
                    {
                        "type": "button",
                        "text": {
                            "type": "plain_text",
                            "text": "NO"
                        },
                        "value": "click_me_123"
                    }
                ]
            }
        ]
    }
    
    return_msg = message_interfaces(msg_canvass,params)
    send_slack_message(slack_url, return_msg)
    return pubsub_message

# Send data payload to slack channel
def send_slack_message(url, payload):
    r = requests.post(url, json=payload)
    print(r.status_code)
    print(r.reason)