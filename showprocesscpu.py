import json
import os
from google.cloud import pubsub_v1

# Load configuration data that includes Slack's token
with open('slackconfig.json', 'r') as f:
    data = f.read()
config = json.loads(data)

# When this gcf function is called, it immediately activates below pubsub handler
# Slack or other messaging need immediate synchronous respond
# while network response and post-processing need some times, thus it's handled by another aynchronous task
def pubsub_handler(request):
    project_id = os.environ['GCP_PROJECT_ID'] # specify google cloud platform project id
    topic_name = "taskhandler" # can be changed to anything
    publisher = pubsub_v1.PublisherClient()
    topic_path = publisher.topic_path(project_id, topic_name)

    if(verify_web_hook(request.form)):
        # Converting slack command data to dict and add NE url information
        req_dict = request.form.to_dict()
        # Get NE's ip address from slack command and add as "ios_url" and specify netconf resource to be acessed
        req_dict["ios_url"] = "https://" + req_dict["text"] + "/restconf/data/Cisco-IOS-XE-process-cpu-oper:cpu-usage/cpu-utilization?depth=1"
        data = json.dumps(req_dict)
        # When you publish a message, the client returns a future.
        future = publisher.publish(
            topic_path, data=data.encode("utf-8")  # data must be a bytestring.
        )
        return f'Command is well-received. Please wait for query result..'
    else:
        return f'Invalid request/credentials'
# [END functions_pubsub_handler]

# Verify incoming slack webhook
def verify_web_hook(form):
    if not form or form.get('token') != config['SLACK_VERIFICATION_TOKEN']:
        raise ValueError('Invalid request/credentials.')
    else:
        return True