import boto3
import json
import os
from common.logger_utility import *
from common.constants import *

class SqsHandler:

    def __poll_for_batches(self,event, context):
        try:
            sqs = boto3.resource('sqs', region_name='us-east-1')

            queue = sqs.get_queue_by_name(QueueName='dev-dot-sdc-waze-data-persistence-orchestration')
            data={}
            for message in queue.receive_messages():
                jsonBody = json.loads(message.body)
                data["BatchId"]=jsonBody["BatchId"]
                data["queueUrl"]=message.queue_url
                data["receiptHandle"]=message.receipt_handle
                LoggerUtility.logInfo("Batch {} retrieved for processing".format(jsonBody["BatchId"]))
                break
            return data
        except Exception as e:
            LoggerUtility.logError("Error polling for batches")
            raise e
    
    def get_batches(self, event, context):
        return self.__poll_for_batches(event, context)
        
