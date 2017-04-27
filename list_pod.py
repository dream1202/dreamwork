from kubernetes import client, config
from pprint import pprint
config.load_kube_config()
v1 = client.CoreV1Api()
print("Listing pods with their information:")
ret = v1.list_pod_for_all_namespaces(watch=False)
print("%-10s\t%-37s\t%-10s\t%-10s\t%-30s\t%-10s" % ("NAMESPACE","NAME","IP","STATUS","NODENAME","AGE"))
for i in ret.items:
	print("%-10s\t%-37s\t%-10s\t%-10s\t%-30s\t%-10s" % (i.metadata.namespace, i.metadata.name, i.status.pod_ip, i.status.phase, i.spec.node_name, i.status.start_time))

