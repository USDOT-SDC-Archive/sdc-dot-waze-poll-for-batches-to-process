from lambdas.poll_for_batches_to_process_handler import *
from common.logger_utility import *
from common.constants import *

def lambda_handler(event, context):
    LoggerUtility.set_level()
    get_batches_handle_event = SqsHandler()
    return get_batches_handle_event.get_batches(event)