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
    

def get_dcm_object_keys_by_prefix(source_bucket_name, source_dataset_prefix):
    s3 = get_s3_client()
    if s3 is None:
        print('get_dcm_object_keys_by_prefix: Failed to get s3 client.')
        return []

    dcm_object_keys = []        
    try:
        response = s3.list_objects_v2(Bucket=source_bucket_name, Prefix=source_dataset_prefix)
        for object in response['Contents']:
            dcm_object_keys.append(object['Key'])

    except ClientError as e:
        logging.error("get_dcm_object_keys_by_prefix: unexpected error: ")
        logging.exception(e)
        return []

    return dcm_object_keys

