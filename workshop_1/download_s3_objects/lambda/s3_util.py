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
        logging.error("get_source_object_keys_by_prefix: Unexpected error: ")
        logging.exception(e)
        return s3_object_keys
        
    return s3_object_keys
    
    
def create_target_object_prefix_path(target_object_prefix):
    # initialize parent path to target path root
    parent_path = config.target_path_root
    
    # if target directories already exist, we are done
    target_object_prefix_path = os.path.join(parent_path, target_object_prefix)
    if os.path.exists(target_object_prefix_path):
        print("[DEBUG] create_target_object_prefix_path: %s exists." % (target_object_prefix_path))
        # success
        return target_object_prefix_path
        
    # target_object_prefix_path needs to create one or more directories
    try: 
        os.makedirs(target_object_prefix_path, exist_ok = True) 
        print("[DEBUG] create_target_object_prefix_path: %s created." % (target_object_prefix_path))
    except OSError as e:
        logging.error("create_target_object_prefix_path: Unexpected error: ")
        logging.exception(e)
    
    return target_object_prefix_path
    
    
def download_s3_object(source_bucket_name, source_object_prefix, source_object_name):
    s3 = get_s3_client()
    if s3 is None:
        print('download_s3_object: Failed to get s3 client.')
        # failure
        return False
    
    # make sure all the directories have been created along target_object_prefix_path    
    target_object_prefix_path = create_target_object_prefix_path(source_object_prefix)
    
    # download s3 source object as a local target file
    target_file_name = target_object_prefix_path + "/" + source_object_name
    try:
        print("[DEBUG] download_s3_object: Open and write to target_file_name: %s" % (target_file_name))
        with open(target_file_name, 'wb') as target_file:
            source_object_key = source_object_prefix + "/" + source_object_name
            s3.download_fileobj(source_bucket_name, source_object_key, target_file)
        target_file.close()
        print("[DEBUG] download_s3_object: Close target_file_name: %s" % (target_file_name))
        
    except ClientError as e:
        logging.error("download_s3_object: Unexpected error: ")
        logging.exception(e)
        # failure
        return False
    
    # success
    return True
    
        
def download_s3_objects(source_bucket_name, source_object_keys):
    # foreach source object key, download source object
    n_source_objects = 0
    n_success = 0
    n_failure = 0
    for source_object_key in source_object_keys:
        print("==")
        print("[DEBUG] download_s3_objects: Downloading source_object_key: %s" % (source_object_key))
        
        # parse source object key into an array of source object path elements
        source_object_path_elements = source_object_key.split("/")
        n_source_object_path_elements = len(source_object_path_elements)
        print("[DEBUG] download_s3_objects: source_object_path_elements: %s" % (source_object_path_elements))
        print("[DEBUG] download_s3_objects: source_object_path_elements has %d elements." % (n_source_object_path_elements))
        
        # set input to download_s3_object
        source_bucket_name = config.source_bucket_name
        # source_object_prefix:
        #   handle boundary conditions of:
        #       1 element: bucket-level object name
        #       2 elements: bucket-level prefix + object name
        #   str.join() can handle 2 or more prefix levels
        source_object_prefix = ""
        if n_source_object_path_elements == 1:
            source_object_prefix = ""
        elif n_source_object_path_elements == 2:
            source_object_prefix = source_object_path_elements[0]
        else:
            source_object_prefix = "/".join(source_object_path_elements[0:-1])
        source_object_name = source_object_path_elements[-1]
        print("[DEBUG] download_s3_objects: source_bucket_name: %s" % (source_bucket_name))
        print("[DEBUG] download_s3_objects: source_object_prefix: %s" % (source_object_prefix))
        print("[DEBUG] download_s3_objects: source_object_name: %s" % (source_object_name))
        
        if not source_object_name:
            print("[DEBUG] download_s3_objects: source_object_name is empty. Skip.")
        else:
            n_source_objects += 1
            success = download_s3_object(source_bucket_name, source_object_prefix, source_object_name)
            if success:
                n_success += 1
            else:
                n_failure += 1
            
    print("download_s3_objects: Processed %d source objects." % (n_source_objects))
    print("download_s3_objects: %d succeeded; %d failed." % (n_success, n_failure))
    
    