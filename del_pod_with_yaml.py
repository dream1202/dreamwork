import argparse
import yaml
import time
import kubernetes.client
from kubernetes.client.rest import ApiException
from pprint import pprint
from kubernetes import config

config.load_kube_config()
parser = argparse.ArgumentParser()
parser.add_argument('-f', action='store', dest='yamlfile')
options = parser.parse_args()
f=open(options.yamlfile)
y=yaml.load(f)
def Dict_get(list, objkey):
    tmp=list
    for dict in tmp:
        for k,v in dict.items():
            if k==objkey:
                return v
name=Dict_get(y['spec']['containers'],'name')
# create an instance of the API class
api_instance = kubernetes.client.CoreV1Api()
namespace = 'default' # str | object name and auth scope, such as for teams and projects
body=kubernetes.client.V1DeleteOptions()
pretty = 'true' # str | If 'true', then the output is pretty printed. (optional)
grace_period_seconds=56

try:
    api_response = api_instance.delete_namespaced_pod(name, namespace, body, pretty=pretty, grace_period_seconds=grace_period_seconds)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling CoreV1Api->create_namespaced_pod: %s\n" % e)
