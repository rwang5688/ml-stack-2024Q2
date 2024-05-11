import boto3
from botocore.exceptions import ClientError
import json
import logging
import os

import config


def get_s3_client():
    print('get_s3_client: profile_name=%s, region_name=%s' % (config.profile_name, config.region_name))

    p_name = None
    if (config.profile_name != ''):
        p_name = config.profile_name
    session = boto3.Session(profile_name=p_name)
    s3 = session.client('s3', region_name=config.region_name)
    return s3
    

def get_s3_object_keys_by_prefix(source_bucket_name, source_dataset_prefix):
    s3 = get_s3_client()
    if s3 is None:
        print('get_s3_object_keys_by_prefix: Failed to get s3 client.')
        return []

    s3_object_keys = []        
    try:
        response = s3.list_objects_v2(Bucket=source_bucket_name, Prefix=source_dataset_prefix)
        for object in response['Contents']:
            s3_object_keys.append(object['Key'])

    except ClientError as e:
        logging.error("get_dcm_object_keys_by_prefix: unexpected error: ")
        logging.exception(e)
        return []

    return s3_object_keys


def download_s3_objects(source_bucket_name, source_object_keys):
    s3 = get_s3_client()
    if s3 is None:
        print('download_s3_object: Failed to get s3 client.')
        return False
        
    # foreach source object key, download source object
    n_source_objects = 0
    n_succeeded = 0
    n_failed = 0
    for source_object_key in source_object_keys:
        print("==")
        
        # parse source_object_prefix and source_object_name from dcm
        dcm_object_path = dcm_object_key.split("/")
        dcm_object_path_len = len(dcm_object_path)
        print("[DEBUG] dcm_object_path: %s" % (dcm_object_path))
        print("[DEBUG] dcm_object_path has %d elements." % (dcm_object_path_len))

        source_bucket_name = config.dcm_bucket_name
        # source_object_prefix:
        #    handle boundary conditions of 0 and 1 element
        #    can use join for 2 or more elements
        if dcm_object_path_len == 1:
            source_object_prefix = "/"
        elif dcm_object_path_len == 2:
            source_object_prefix = dcm_object_path[0] + "/"
        else:
            source_object_prefix = "/".join(dcm_object_path[0:-1]) + "/"
        source_object_name = dcm_object_path[-1]
        print("[DEBUG] source_bucket_name: %s" % (source_bucket_name))
        print("[DEBUG] source_object_prefix: %s" % (source_object_prefix))
        print("[DEBUG] source_object_name: %s" % (source_object_name))

        if not source_object_name:
            print("[DEBUG] source_object_name is empty. Skip.")
        else:
            n_dcm_objects += 1

    print("download-s3-objects: Processed %d DCM objects." % (n_dcm_objects))
    print("download-s3-objects: %d succeeded; %d failed." % (n_succeeded, n_failed))
    
    
    tmp_source_object_name = '/tmp/'+source_object_name
    try:
        # download the DCM image from S3 as a local file
        with open(tmp_source_object_name, 'wb') as data:
            source_object_key = source_object_prefix + source_object_name
            s3.download_fileobj(source_bucket_name, source_object_key, data)
    except ClientError as e:
        logging.error("convert_dicom_image_from_s3_object: unexpected error: ")
        logging.exception(e)
        return None
