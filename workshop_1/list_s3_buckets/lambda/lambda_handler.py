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
    
    # DEBUG
    print("get_event_vars:")
    print("profile_name: %s" % (config.profile_name))
    print("region_name: %s" % (config.region_name))
    

def lambda_handler(event, context):
    # print start datetime
    now = datetime.now()
    print("Start dateime: %s" % (now))

    # start
    print('\nStarting lambda_handler.lambda_handler ...')
    LOGGER.info("%s", pformat({"Context" : context, "Request": event}))

    # get event variables
    get_event_vars(event)
    
    # get s3 bucket names
    s3_bucket_names = s3_util.get_s3_bucket_names()
    num_s3_bucket_names = len(s3_bucket_names)
    
    print("S3 Bucket Names: ")
    print(s3_bucket_names)
    print("Total # of S3 Buckets: %d" % (num_s3_bucket_names))
    
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
    print("list_s3_buckets: args = %s" % (args))

    # load json file
    task_spec_file_name = args['task_spec']
    f = open(task_spec_file_name)
    event = json.load(f)
    f.close()
    print("list_s3_buckets: task_spec = %s" % (event))

    # create test context
    context = {}

    # Execute test
    lambda_handler(event, context)
    
    