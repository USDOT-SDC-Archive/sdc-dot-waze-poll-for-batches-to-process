from moto import mock_sns, mock_sqs, mock_events
import sys
import os
import time
import boto3
import pytest
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from lambdas.poll_for_batches_to_process_handler import SqsHandler


@mock_sns
def test_publish_message_to_sns():
    batchId = str(int(time.time()))
    topic_name = "dev-dot-sdc-cloudwatch-alarms-notification-topic"
    message = {"BatchId": batchId, "Status": "Manifest generation completed"}
    sns = boto3.client('sns', region_name='us-east-1')
    response = sns.create_topic(Name=topic_name)
    os.environ["BATCH_NOTIFICATION_SNS"] = response['TopicArn']
    poll_batches_to_process_obj = SqsHandler()
    poll_batches_to_process_obj.publish_message_to_sns(message)
    assert True


@mock_sqs
def test_poll_for_batches_not_historical():
    with pytest.raises(Exception):
        os.environ["persistence_sqs"] = "dev-dot-sdc-waze-data-persistence-orchestration"
        queue_event = dict()
        queue_event["is_historical"] = "false"
        queue_event["BatchId"] = str(int(time.time()))
        poll_batches_to_process_obj = SqsHandler()
        poll_batches_to_process_obj.poll_for_batches(queue_event, None)


@mock_sqs
def test_poll_for_batches_historical():
    with pytest.raises(Exception):
        os.environ["persistence_historical_sqs"] = "dev-dot-sdc-waze-data-historical-persistence-orchestration"
        queue_event = dict()
        queue_event["is_historical"] = "true"
        queue_event["BatchId"] = str(int(time.time()))
        poll_batches_to_process_obj = SqsHandler()
        poll_batches_to_process_obj.poll_for_batches(queue_event, None)


# @mock_sqs
# def test_poll_for_batches_not_historical(monkeypatch):
#     sqs = boto3.client('sqs', region_name='us-east-1')
#     response = sqs.create_queue(QueueName='dev-dot-sdc-waze-data-persistence-orchestration',
#                                 Attributes={'FifoQueue': "false", 'DelaySeconds': "5", 'MaximumMessageSize': "262144",
#                                             'MessageRetentionPeriod': "1209600", 'VisibilityTimeout': "960"})
#     queue_url = response['QueueUrl']
#
#     queue_name = queue_url[queue_url.rfind('/') + 1: len(queue_url)]
#     os.environ["persistence_sqs"] = queue_name
#     queue_event = dict()
#     queue_event["is_historical"] = "false"
#     batchId = str(int(time.time()))
#     queue_event["BatchId"] = batchId
#     poll_batches_to_process_obj = SqsHandler()
#     def mock_get_dict():
#         data = dict()
#         data["BatchId"] = batchId
#         return data
#     message = {"BatchId": batchId, "Status": "Manifest generation completed"}
#     monkeypatch.setattr('lambdas.poll_for_batches_to_process_handler.SqsHandler.poll_for_batches', mock_get_dict())
#     monkeypatch.setattr('lambdas.poll_for_batches_to_process_handler.SqsHandler.publish_message_to_sns', message)
#     poll_batches_to_process_obj.poll_for_batches(queue_event, None)
#
#     assert True


@mock_events
def test_get_batches():
    with pytest.raises(Exception):
        assert SqsHandler.get_batches(None, None) is None


