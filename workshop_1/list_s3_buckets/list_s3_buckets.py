import logging
import boto3
from botocore.exceptions import ClientError

print('\nStarting list_s3_buckets.ipynb ...')

# We would normally set these via config file or env vars
# Hard coding these to keep the demo simple
# profile_name = 'default'
region_name = 'us-west-2'

# print('get_s3_client: profile_name=%s, region_name=%s' % (profile_name, region_name))
print('get_s3_client: region_name=%s' % (region_name))

# session = boto3.Session(profile_name=profile_name)
session = boto3.Session()
s3 = session.client('s3',
    region_name=region_name)

s3_bucket_names = []

if s3 is None:
    print('get_s3_bucket_names: Failed to get s3 client.')

try:
    response = s3.list_buckets()
    print('DEBUG: get_s3_bucket_names: s3.list_buckets() response: %s' % (response))
    if 'Buckets' in response:
        for bucket in response['Buckets']:
            s3_bucket_names.append(bucket['Name'])
    
except ClientError as e:
    logging.error("get_s3_bucket_names: unexpected error: ")
    logging.exception(e)

num_s3_bucket_names = len(s3_bucket_names)

print("s3_bucket_names: ")
print(s3_bucket_names)
print("Total # of S3 Buckets: %d" % num_s3_bucket_names)

print('\n... Thaaat\'s all, Folks!')
