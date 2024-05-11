import boto3
from botocore.exceptions import ClientError
import json
import logging

import config


def get_s3_client():
    print('get_s3_client: profile_name=%s, region_name=%s' % (config.profile_name, config.region_name))

    p_name = None
    if (config.profile_name != ''):
        p_name = config.profile_name
    session = boto3.Session(profile_name=p_name)
    s3 = session.client('s3', region_name=config.region_name)
    return s3
    

def get_s3_bucket_names():
    s3 = get_s3_client()
    if s3 is None:
        print('get_s3_buckets: Failed to get s3 client.')
        return []
        
    s3_bucket_names = []
    try:
        response = s3.list_buckets()
        print('[DEBUG] get_s3_bucket_names: s3.list_buckets() response: %s' % (response))
        if 'Buckets' in response:
            for bucket in response['Buckets']:
                s3_bucket_names.append(bucket['Name'])
                
    except ClientError as e:
        logging.error("get_s3_bucket_names: unexpected error: ")
        logging.exception(e)
        
    return s3_bucket_names

