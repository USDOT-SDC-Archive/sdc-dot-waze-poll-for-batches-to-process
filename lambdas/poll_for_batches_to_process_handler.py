import boto3
import json
import os
from common.logger_utility import LoggerUtility

sns = boto3.client('sns', region_name='us-east-1')


class SqsHandler:

    def publish_message_to_sns(self, message):
        """
        Publishes a message to Amazon's Simple Notification Service
        :param message: dict
        """

        sns.publish(
            TargetArn=os.environ['BATCH_NOTIFICATION_SNS'],
            Message=json.dumps({'default': json.dumps(message)}),
            MessageStructure='json'
        )

    def poll_for_batches(self, event):
        """
        gets the messages from the data persistence queue to start the persistence in Redshift
        :param event: a dictionary, or a list of a dictionary, that contains information on a batch
        :return:
        """
        try:
            sqs = boto3.resource('sqs', region_name='us-east-1')
            is_historical = event["is_historical"] == "true"
            persist_sqs = os.environ["persistence_sqs"]
            if is_historical:
                persist_sqs = os.environ["persistence_historical_sqs"]
                
            queue = sqs.get_queue_by_name(QueueName=persist_sqs)
            data = dict()
            data["is_historical"] = str(is_historical).lower()

            # if no batch id assigned, gather BatchId, queueUrl, and receiptHandle from the messages in the queue.
            if 'BatchId' not in event:
                for message in queue.receive_messages():
                    json_body = json.loads(message.body)
                    data["BatchId"] = json_body["BatchId"]
                    data["queueUrl"] = message.queue_url
                    data["receiptHandle"] = message.receipt_handle
                    LoggerUtility.log_info("Batch {} retrieved for processing".format(json_body["BatchId"]))
                    break

            # Otherwise, only assign the BatchId from the event.
            else:
                data["BatchId"] = event['BatchId']

            if 'BatchId' in data:
                self.publish_message_to_sns({"BatchId": data["BatchId"], "Status": "Persistence process started"})
            return data
        except Exception as e:
            LoggerUtility.log_error("Error polling for batches")
            raise e
    
    def get_batches(self, event):
        """
        Executes poll_for_batches
        :param event: a dictionary, or a list of a dictionary, that contains information on a batch
        :return:
        """
        return self.poll_for_batches(event)
