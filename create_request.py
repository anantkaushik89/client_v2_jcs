#!/usr/bin/env python
import os
import sys
import datetime
import auth_handler
import httplib
import requests
import hashlib
import urllib
from oslo_serialization import jsonutils
params, headers = {}, {}
method = 'GET'
path, port, auth_path = '', '', ''
body, host, protocol = '', '', ''

def add_params(string):
    length = len(string)
    parts = string.split('&')
    for p in parts:
        (key, val) = p.split('=')
        params[key] = val

def fetch_token_from_iam(req_obj, headers, auth_handler_obj):
    iam_endpoint = os.environ.get('JCS_IAM_ENDPOINT')
    if iam_endpoint is None:
        print('No JCS IAM endpoint found. Exiting with Error')
        raise KeyError
    cred_dict = {}
    cred_dict['access'] = req_obj.params['JCSAccessKeyId']
    cred_dict['signature'] = urllib.unquote(req_obj.params['Signature'])
    cred_dict['host'] = auth_handler_obj.host
    cred_dict['verb'] = req_obj.method
    cred_dict['path'] = req_obj.path
    req_obj.params.pop('Signature')
    cred_dict['params'] = req_obj.params
    cred_dict['headers'] = headers
    cred_dict['body_hash'] = hashlib.sha256(req_obj.body).hexdigest()
    cred_dict['action_resource_list'] = []
    creds = {'ec2Credentials': cred_dict}
    data = jsonutils.dumps(creds)
    print data, headers
    response = requests.request('POST', iam_endpoint,
                     verify=False, data=data, headers=headers)
    print response
    if response.status_code:
        return response.text
    return response.json()


def requestify(request, get_token):
    [initial, rest] = request.split('?')
    parts = initial.split('/')
    protocol, host_port = parts[0][ : -1], parts[2]
    path = '/'
    if (':' not in host_port):
        host = host_port
        port = 443
    else:
       [host, port] = host_port.split(':')
    auth_path = path
    add_params(rest)
    headers['User-Agent'] = 'curl/7.35.0'
    headers['Content-Type'] = 'application/json'
    headers['Accept-Encoding'] = 'identity'
    req_obj = auth_handler.HTTPRequest(method, protocol, host, port, path, auth_path,
                         params, headers, body)
    auth_handler_obj = auth_handler.V2Handler(host)
    req_obj = auth_handler_obj.add_auth(req_obj)
    if get_token:
        return fetch_token_from_iam(req_obj, headers, auth_handler_obj)
    request_string = 'curl -X ' + req_obj.method
    request_string += ' -H \"Accept-Encoding: identity\"'
    request_string += ' -H \"User-Agent: ' + headers['User-Agent'] + '\"'
    request_string += ' -H \"Content-Type: ' + headers['Content-Type'] + '\"'
    request_string += ' \"' + initial + '?'
    for keys in req_obj.params:
        request_string += keys + '=' + req_obj.params[keys] + '&'
    request_string = request_string[ : -1]
    request_string += '\"'
    return request_string

def main():
    req = sys.argv[1]
    get_token = False
    if len(sys.argv) == 3 and sys.argv[2] == 'get-token':
        get_token = True
    chngd_req = requestify(req, get_token)
    print chngd_req
    #os.system(chngd_req)

main()
