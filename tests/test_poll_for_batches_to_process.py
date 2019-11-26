import json
import os
import sys
import time

import boto3
import pytest
from botocore.errorfactory import ClientError
from moto import mock_sqs, mock_events

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from lambdas.poll_for_batches_to_process_handler import SqsHandler
from unittest.mock import patch


os.environ['BATCH_NOTIFICATION_SNS'] = "batch_notification_sns"


class MockSNS:
    def publish(self, *args, **kwargs):
        pass


mock_client = MockSNS()


@patch('lambdas.poll_for_batches_to_process_handler.sns', mock_client)
def test_publish_message_to_sns():
    sqs_handler = SqsHandler()
    sqs_handler.publish_message_to_sns(None)


@mock_sqs
def test_poll_for_batches_not_historical():
    with pytest.raises(Exception):
        os.environ["persistence_sqs"] = "dev-dot-sdc-waze-data-persistence-orchestration"
        queue_event = dict()
        queue_event["is_historical"] = "false"
        queue_event["BatchId"] = str(int(time.time()))
        poll_batches_to_process_obj = SqsHandler()
        poll_batches_to_process_obj.poll_for_batches(queue_event)


@mock_sqs
def test_poll_for_batches_historical():
    with pytest.raises(ClientError):
        os.environ["persistence_sqs"] = "persistence_sqs"
        os.environ["persistence_historical_sqs"] = "dev-dot-sdc-waze-data-historical-persistence-orchestration"
        queue_event = dict()
        queue_event["is_historical"] = "true"
        queue_event["BatchId"] = str(int(time.time()))
        poll_batches_to_process_obj = SqsHandler()
        poll_batches_to_process_obj.poll_for_batches(queue_event)


@mock_sqs
def test_poll_for_batches_historical_status_assigned(monkeypatch):
    def mock_publish_message(*args, **kwargs):
        pass

    monkeypatch.setattr(SqsHandler, "publish_message_to_sns", mock_publish_message)
    os.environ["persistence_sqs"] = "dev-dot-sdc-curated-batches.fifo"
    sqs = boto3.resource('sqs', region_name='us-east-1')
    sqs.create_queue(QueueName=os.environ["persistence_sqs"])
    queue_event = dict()
    queue_event["is_historical"] = "false"
    queue_event["BatchId"] = str(int(time.time()))
    poll_batches_to_process_obj = SqsHandler()

    data = poll_batches_to_process_obj.poll_for_batches(queue_event)
    assert data["is_historical"] == queue_event["is_historical"].lower()


def test_poll_for_batches_batches_not_in_event(monkeypatch):
    class MockMessage:
        body = None

    class MockQueue:
        @staticmethod
        def receive_messages(*args, **kwargs):
            mock_messages = [MockMessage()]
            mock_messages[0].queue_url = "test_queue_url"
            mock_messages[0].receipt_handle = "test_receipt_handle"
            return mock_messages

    class MockSQS:
        @staticmethod
        def get_queue_by_name(*args, **kwargs):
            queue = MockQueue()
            return queue

    def mock_boto3_resource(*args, **kwargs):
        sqs = MockSQS()
        return sqs

    def mock_json_loads(*args, **kwargs):
        return {"BatchId": "test_batch_id"}

    def mock_publish_message(*args, **kwargs):
        pass

    monkeypatch.setattr(boto3, "resource", mock_boto3_resource)
    monkeypatch.setattr(json, "loads", mock_json_loads)
    monkeypatch.setattr(SqsHandler, "publish_message_to_sns", mock_publish_message)

    os.environ["persistence_sqs"] = "dev-dot-sdc-curated-batches.fifo"
    boto3.setup_default_session()
    queue_event = dict()
    queue_event["is_historical"] = "false"
    poll_batches_to_process_obj = SqsHandler()

    data = poll_batches_to_process_obj.poll_for_batches(queue_event)

    assert data["BatchId"] == "test_batch_id"
    assert data["queueUrl"] == "test_queue_url"
    assert data["receiptHandle"] == "test_receipt_handle"


@mock_events
def test_get_batches():
    with pytest.raises(TypeError):
        sqs_handler = SqsHandler()
        assert sqs_handler.get_batches(None) is None
