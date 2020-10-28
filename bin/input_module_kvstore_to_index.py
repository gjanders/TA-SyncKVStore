
# encoding = utf-8

import os
import sys
import time
import datetime
import requests
from requests.auth import HTTPBasicAuth

'''
    IMPORTANT
    Edit only the validate_input and collect_events functions.
    Do not edit any other part in this file.
    This file is generated only once when creating the modular input.
'''
'''
# For advanced users, if you want to create single instance mod input, uncomment this method.
def use_single_instance_mode():
    return True
'''

def validate_input(helper, definition):
    """Implement your own validation logic to validate the input stanza configurations"""
    # This example accesses the modular input variable
    # u_splunk_server = definition.parameters.get('u_splunk_server', None)
    # u_source_app = definition.parameters.get('u_source_app', None)
    # u_source_collection = definition.parameters.get('u_source_collection', None)
    # global_account = definition.parameters.get('global_account', None)
    pass

def collect_events(helper, ew):
    """Implement your data collection logic here

    # The following examples get the arguments of this input.
    # Note, for single instance mod input, args will be returned as a dict.
    # For multi instance mod input, args will be returned as a single value.
    opt_u_splunk_server = helper.get_arg('u_splunk_server')
    opt_u_source_app = helper.get_arg('u_source_app')
    opt_u_source_collection = helper.get_arg('u_source_collection')
    opt_global_account = helper.get_arg('global_account')
    # In single instance mode, to get arguments of a particular input, use
    opt_u_splunk_server = helper.get_arg('u_splunk_server', stanza_name)
    opt_u_source_app = helper.get_arg('u_source_app', stanza_name)
    opt_u_source_collection = helper.get_arg('u_source_collection', stanza_name)
    opt_global_account = helper.get_arg('global_account', stanza_name)

    # get input type
    helper.get_input_type()

    # The following examples get input stanzas.
    # get all detailed input stanzas
    helper.get_input_stanza()
    # get specific input stanza with stanza name
    helper.get_input_stanza(stanza_name)
    # get all stanza names
    helper.get_input_stanza_names()

    # The following examples get options from setup page configuration.
    # get the loglevel from the setup page
    loglevel = helper.get_log_level()
    # get proxy setting configuration
    proxy_settings = helper.get_proxy()
    # get account credentials as dictionary
    account = helper.get_user_credential_by_username("username")
    account = helper.get_user_credential_by_id("account id")
    # get global variable configuration
    global_userdefined_global_var = helper.get_global_setting("userdefined_global_var")

    # The following examples show usage of logging related helper functions.
    # write to the log for this modular input using configured global log level or INFO as default
    helper.log("log message")
    # write to the log using specified log level
    helper.log_debug("log message")
    helper.log_info("log message")
    helper.log_warning("log message")
    helper.log_error("log message")
    helper.log_critical("log message")
    # set the log level for this modular input
    # (log_level can be "debug", "info", "warning", "error" or "critical", case insensitive)
    helper.set_log_level(log_level)

    # The following examples send rest requests to some endpoint.
    response = helper.send_http_request(url, method, parameters=None, payload=None,
                                        headers=None, cookies=None, verify=True, cert=None,
                                        timeout=None, use_proxy=True)
    # get the response headers
    r_headers = response.headers
    # get the response body as text
    r_text = response.text
    # get response body as json. If the body text is not a json string, raise a ValueError
    r_json = response.json()
    # get response cookies
    r_cookies = response.cookies
    # get redirect history
    historical_responses = response.history
    # get response status code
    r_status = response.status_code
    # check the response status, if the status is not sucessful, raise requests.HTTPError
    response.raise_for_status()

    # The following examples show usage of check pointing related helper functions.
    # save checkpoint
    helper.save_check_point(key, state)
    # delete checkpoint
    helper.delete_check_point(key)
    # get checkpoint
    state = helper.get_check_point(key)

    # To create a splunk event
    helper.new_event(data, time=None, host=None, index=None, source=None, sourcetype=None, done=True, unbroken=True)
    """

    '''
    # The following example writes a random number as an event. (Multi Instance Mode)
    # Use this code template by default.
    import random
    data = str(random.randint(0,100))
    event = helper.new_event(source=helper.get_input_type(), index=helper.get_output_index(), sourcetype=helper.get_sourcetype(), data=data)
    ew.write_event(event)
    '''

    '''
    # The following example writes a random number as an event for each input config. (Single Instance Mode)
    # For advanced users, if you want to create single instance mod input, please use this code template.
    # Also, you need to uncomment use_single_instance_mode() above.
    import random
    input_type = helper.get_input_type()
    for stanza_name in helper.get_input_stanza_names():
        data = str(random.randint(0,100))
        event = helper.new_event(source=input_type, index=helper.get_output_index(stanza_name), sourcetype=helper.get_sourcetype(stanza_name), data=data)
        ew.write_event(event)
    '''
    try:
        import splunklib.client as splunkClient
        import json
        import six.moves.urllib.request, six.moves.urllib.parse, six.moves.urllib.error
    except Exception as err_message:
        helper.log_error("{}".format(err_message))
        return 1


    helper.log_info("Modular Input pullkvtoindex started.")

    u_session_key = helper.context_meta.get('session_key')

    u_splunkserver = helper.get_arg('u_splunk_server')
    helper.log_info("u_splunkserver={}".format(u_splunkserver))

    u_srcappname = helper.get_arg("u_source_app")
    helper.log_info("u_destappname={}".format(u_srcappname))

    u_srccollection = helper.get_arg("u_source_collection")
    helper.log_info("u_destcollection={}".format(u_srccollection))

    user_account = helper.get_arg('global_account')

    srcSplunkService = splunkClient.connect(host=u_splunkserver, port=8089, username=user_account.get('username'), password=user_account.get('password'),owner='nobody',app=u_srcappname)

    srcKVStoreTable = srcSplunkService.kvstore[u_srccollection].data.query()

    for entry in srcKVStoreTable:
        dataToIndex = {}
        orig_key = entry.pop('_key')
        dataToIndex = {k:entry.get(k) for k,v in list(entry.items()) if not k.startswith('_')}
        dataToIndex['key'] = orig_key
        event = helper.new_event(source=helper.get_input_type(), index=helper.get_output_index(), sourcetype=helper.get_sourcetype(), data=json.dumps(dataToIndex))

        try:
            ew.write_event(event)
        except Exception as e:
            raise e

    # if the source kvstore is > 10K rows, then we limit=0 doesn't always get you all the rows, it goes until some
    # unknown limit and then obtaining more involves extra queries, but we don't know the size of the kvstore/collection
    src_kvstore_length = len(srcKVStoreTable)
    helper.log_debug("KV Store received {0} rows".format(src_kvstore_length))

    kvstore_limit = 10000
    if src_kvstore_length > kvstore_limit:
        # TODO find a nicer way to do this, ask the introspection stats how big the kvstore is
        auth = HTTPBasicAuth(username, password)
        url = "https://" + u_splunkserver + ":8089/services/server/introspection/kvstore/collectionstats?output_mode=json&f=data"
        res = requests.get(url, auth=auth, verify=False)
        if (res.status_code != requests.codes.ok):
            helper.log_error("HTTP status code={0} on URL={1} with username={2} result text={3}".format(res.status_code, url, username, res.text))
        json_res = json.loads(res.text)
        if 'entry' in json_res and len(json_res['entry'])>0:
            entry = json_res['entry'][0]
            if 'content' in entry and 'data' in entry['content']:
                json_data = entry['content']['data']
                for a_data in json_data:
                    # for some reason this is a giant string of text, oh well
                    start = a_data.find(u_srcappname + "." + u_srccollection)
                    if start != -1:
                        slice_start = a_data.find("count", start)
                        slice_end = a_data.find(",", slice_start+9)
                        found_count = int(a_data[slice_start+7:slice_end])
                        helper.log_info("kvstore has {0} total rows, received {1} rows from the first query with limit=0".format(found_count, src_kvstore_length))
                        break

        # if we have not seen all the rows from the collection we have to keep querying
        if src_kvstore_length < found_count:
            skip_number = src_kvstore_length
            while skip_number < found_count:
                helper.log_info("kvstore exceeded the code-configured limit of {0}, running a query to remote kvstore and skipping {1} rows".format(kvstore_limit, skip_number))
                # we could loop just the query portion and do a large post at the end but tha might consume a lot of memory
                # so per-loop we submit to the destination kvstore and re-query the source if required
                # TODO repeated code below, could move this into a function
                kvstore_result = srcSplunkService.kvstore[u_srccollection].data.query(limit=0,skip=skip_number)
                postList = []
                helper.log_debug("KV Store received {0} rows".format(len(kvstore_result)))
                for entry in kvstore_result:
                    dataToIndex = {}
                    orig_key = entry.pop('_key')
                    dataToIndex = {k:entry.get(k) for k,v in list(entry.items()) if not k.startswith('_')}
                    dataToIndex['key'] = orig_key
                    event = helper.new_event(source=helper.get_input_type(), index=helper.get_output_index(), sourcetype=helper.get_sourcetype(), data=json.dumps(dataToIndex))

                    try:
                        ew.write_event(event)
                    except Exception as e:
                        raise e
                skip_number = skip_number + len(kvstore_result)

    helper.log_info("Modular Input pullkvtoindex completed.")

