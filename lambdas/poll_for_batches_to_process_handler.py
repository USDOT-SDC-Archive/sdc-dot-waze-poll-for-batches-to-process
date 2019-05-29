import boto3
import json
import os
from common.logger_utility import *
from common.constants import *

sns = boto3.client('sns', region_name='us-east-1')
class SqsHandler:

    def publish_message_to_sns(self, message):
        response = sns.publish(
            TargetArn=os.environ['BATCH_NOTIFICATION_SNS'],
            Message=json.dumps({'default': json.dumps(message)}),
            MessageStructure='json'
        )

    def poll_for_batches(self,event, context):
        try:
            sqs = boto3.resource('sqs', region_name='us-east-1')
            is_historical = event["is_historical"] == "true"
            persist_sqs = os.environ["persistence_sqs"]
            if(is_historical):
                persist_sqs = os.environ["persistence_historical_sqs"]
                
            queue = sqs.get_queue_by_name(QueueName=persist_sqs)
            data = dict()
            data["is_historical"] = str(is_historical).lower()
            if 'BatchId' not in event:
                for message in queue.receive_messages():
                    jsonBody = json.loads(message.body)
                    data["BatchId"]=jsonBody["BatchId"]
                    data["queueUrl"]=message.queue_url
                    data["receiptHandle"]=message.receipt_handle
                    LoggerUtility.logInfo("Batch {} retrieved for processing".format(jsonBody["BatchId"]))
                    break
            else:
                data["BatchId"] = event['BatchId']

            if 'BatchId' in data:
                self.publish_message_to_sns({"BatchId": data["BatchId"], "Status": "Persistence process started"})
            return data
        except Exception as e:
            LoggerUtility.logError("Error polling for batches")
            raise e
    
    def get_batches(self, event, context):
        return self.poll_for_batches(event, context)
        
