import argparse
from datetime import datetime
import json
import logging
from pprint import pformat

import config
import lambda_util
import s3_util


LOGGER = logging.getLogger(__name__)
logging.getLogger().setLevel(logging.INFO)


def get_event_vars(event):
    # AWS parameters
    config.profile_name = event['profile_name']
    config.region_name = event['region_name']

    # Data locations
    config.dcm_bucket_name = event['dcm_bucket_name']
    config.dcm_dataset_prefix = event['dcm_dataset_prefix']
    config.png_bucket_name = event['png_bucket_name']
    config.de_id_png_bucket_name = event['de_id_png_bucket_name']
    
    # Pipeline parameters
    config.dpi = event['dpi']
    config.phi_detection_threshold = event['phi_detection_threshold']
    config.redacted_box_color = event['redacted_box_color']

    # DEBUG
    print("get_event_vars:")
    print("profile_name: %s" % (config.profile_name))
    print("region_name: %s" % (config.region_name))
    print("dcm_bucket_name: %s" % (config.dcm_bucket_name))
    print("dcm_dataset_prefix: %s" % (config.dcm_dataset_prefix))
    print("png_bucket_name: %s" % (config.png_bucket_name))
    print("de_id_png_bucket_name: %s" % (config.de_id_png_bucket_name))
    print("dpi: %s" % (config.dpi))
    print("phi_detection_threshold: %s" % (config.phi_detection_threshold))
    print("redacted_box_color: %s" % (config.redacted_box_color))


def lambda_handler(event, context):
    # print start datetime
    now = datetime.now()
    print("Start dateime: %s" % (now))

    # start
    print('\nStarting submit_mip_de_identify_task.lambda_handler ...')
    LOGGER.info("%s", pformat({"Context" : context, "Request": event}))

    # get event variables
    get_event_vars(event)

    # get list of ddcm_object_keys based on dcm dataset prefix
    source_bucket_name = config.dcm_bucket_name
    source_dataset_prefix = config.dcm_dataset_prefix
    dcm_object_keys = s3_util.get_dcm_object_keys_by_prefix(source_bucket_name, source_dataset_prefix)
    print("[DEBUG] dcm_object_keys: %s" % (dcm_object_keys))

    # foreach dcm object, async invoke de-identify-png Lambda function
    n_dcm_objects = 0
    n_succeeded = 0
    n_failed = 0
    for dcm_object_key in dcm_object_keys:
        print("==")

        # get source_object_prefix and source_object_name from dcm
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
            success = lambda_util.dcm_to_png_async(source_bucket_name, source_object_prefix, source_object_name)
            n_dcm_objects += 1
            if success:
                n_succeeded += 1
                print("Async invoke succeeded for DCM object #%d: %s." % \
                    (n_dcm_objects, source_object_prefix+source_object_name))
            else:
                n_failed += 1
                print("Async invoke failed for DCM object #%d: %s." % \
                    (n_dcm_objects, source_object_prefix+source_object_name))
        
        print("==")

    print("mip-submit-task: Processed %d DCM objects." % (n_dcm_objects))
    print("mip-submit-task: %d succeeded; %d failed." % (n_succeeded, n_failed))
    
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
    print("mip-submit-task: args = %s" % (args))

    # load json file
    task_spec_file_name = args['task_spec']
    f = open(task_spec_file_name)
    event = json.load(f)
    f.close()
    print("mip-submit-task: task_spec = %s" % (event))

    # create test context
    context = {}

    # Execute test
    lambda_handler(event, context)

