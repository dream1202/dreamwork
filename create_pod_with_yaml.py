#! /usr/bin/env python
import argparse
import yaml
import time
import kubernetes.client
from kubernetes.client.rest import ApiException
from pprint import pprint
from kubernetes import config
# Get yaml configuration
parser = argparse.ArgumentParser()
parser.add_argument('-f', action='store', dest='yamlfile')
options = parser.parse_args()
f=open(options.yamlfile)
y=yaml.load(f)
def Dict_get(list, objkey):
    tmp=list
    for dict in tmp:
        for k,v in dict.items():
            if k== objkey:
                 return v
apiversion=y['apiVersion']
kind=y['kind']
name=Dict_get(y['spec']['containers'],'name')
image=Dict_get(y['spec']['containers'],'image')
command=Dict_get(y['spec']['containers'],'command')
args=Dict_get(y['spec']['containers'],'args')
imagepullpolicy=Dict_get(y['spec']['containers'],'imagePullPolicy')
dnspolicy=y['spec']['dnsPolicy']
restartpolicy=y['spec']['restartPolicy']
termination=y['spec']['terminationGracePeriodSeconds']
#Create pod
config.load_kube_config()
api_instance = kubernetes.client.CoreV1Api()
namespace = 'default' # str | object name and auth scope, such as for teams and projects
#meta = kubernetes.client.V1ObjectMeta(name='123')
meta = kubernetes.client.V1ObjectMeta(name=name)

#container = kubernetes.client.V1Container(name='123',image='bootstrapper:5000/pineking/hyperkube-amd64:v1.6.0-alpha-2aa99',command=['/bin/bash','-c'],args=['sleep 1d'],image_pull_policy='IfNotPresent')
#myspec = kubernetes.client.V1PodSpec(containers=[container],dns_policy='ClusterFirst',restart_policy='Never',termination_grace_period_seconds=1)

container = kubernetes.client.V1Container(name=name,image=image,command=command,args=args,image_pull_policy=imagepullpolicy)
myspec = kubernetes.client.V1PodSpec(containers=[container],dns_policy=dnspolicy,restart_policy=restartpolicy,termination_grace_period_seconds=termination)
body = kubernetes.client.V1Pod(api_version=apiversion,kind=kind,metadata=meta, spec=myspec) # V1Pod |
#print body

pretty = 'true' # str | If 'true', then the output is pretty printed. (optional)

try:
    api_response = api_instance.create_namespaced_pod(namespace, body, pretty=pretty)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling CoreV1Api->create_namespaced_pod: %s\n" % e)


