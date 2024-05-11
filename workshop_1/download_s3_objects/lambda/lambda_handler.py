import argparse
from datetime import datetime
import json
import logging
from pprint import pformat

import config
import s3_util


LOGGER = logging.getLogger(__name__)
logging.getLogger().setLevel(logging.INFO)


def get_event_vars(event):
    # AWS parameters
    config.profile_name = event["profile_name"]
    config.region_name = event["region_name"]

    # Data locations
    config.source_bucket_name = event["source_bucket_name"]
    config.source_dataset_prefix = event["source_dataset_prefix"]
    config.target_path_root = event['target_path_root']
    
    # DEBUG
    print("get_event_vars:")
    print("profile_name: %s" % (config.profile_name))
    print("region_name: %s" % (config.region_name))
    print("source_bucket_name: %s" % (config.source_bucket_name))
    print("source_dataset_prefix: %s" % (config.source_dataset_prefix))
    print("target_path_root: %s" % (config.target_path_root))
    

def lambda_handler(event, context):
    # print start datetime
    now = datetime.now()
    print("Start dateime: %s" % (now))

    # start
    print('\nStarting lambda_handler.lambda_handler ...')
    LOGGER.info("%s", pformat({"Context" : context, "Request": event}))

    # get event variables
    get_event_vars(event)

    # get list of source object keys based on source dataset prefix
    source_bucket_name = config.source_bucket_name
    source_dataset_prefix = config.source_dataset_prefix
    source_object_keys = s3_util.get_s3_object_keys_by_prefix(source_bucket_name, source_dataset_prefix)
    print("[DEBUG] download_s3_objects: source_object_keys: %s" % (source_object_keys))
    
    # download files
    s3_util.download_s3_objects(source_bucket_name, source_object_keys)
    
    # end
    print('\n... Thaaat\'s all, Folks!')
    
    # print end datetime
    now = datetime.now()
    print("End dateime: %s" % (now))
    
    
if __name__ == '__main__':
    # read arguments
    ap = argparse.ArgumentParser()
    ap.add_argument("-t", "--task-spec", required=True, help="Task specification.")
    args = vars(ap.parse_args())
    print("download_s3_objects: args = %s" % (args))

    # load json file
    task_spec_file_name = args['task_spec']
    f = open(task_spec_file_name)
    event = json.load(f)
    f.close()
    print("download_s3_objects: task_spec = %s" % (event))

    # create test context
    context = {}

    # Execute test
    lambda_handler(event, context)

