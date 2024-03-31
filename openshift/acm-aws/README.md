# acm-aws

```
mkdir acm-aws/files
```

```
oc get secret/pull-secret -n openshift-config --template='{{index .data ".dockerconfigjson" | base64decode}}' > acm-aws/files/pull-secret.json
```

```
ssh-keygen -t rsa -N '' -f ~/.ssh/id_rsa ; cat .ssh/id_rsa > acm-aws/files/ssh_private_key ; cat .ssh/id_rsa.pub > acm-aws/files/ssh_public_key
```

```
export OCP_VERSION=<>
```

```
helm install ocp-${OCP_VERSION} acm-aws/ --set ocpVersion=${OCP_VERSION} --set clusterReplicas=<> --set accessKey=<> --set secretAccessKey=<> --set region=<> --set baseDomain=<>
```

```
oc get managedcluster
```

```
export CLUSTER_NAME=<>
```

```
export CLUSTER_URL=<>
```

```
curl \
-X GET \
-H "Authorization: Bearer `oc whoami -t`" \
"https://api.${CLUSTER_URL}:6443/apis/cluster.open-cluster-management.io/v1/managedclusters/${CLUSTER_NAME}" > cluster.json ;\
sed -i -e '/resourceVersion/d' -e '/uid/d' cluster.json
```

```
curl \
-X DELETE \
-H "Authorization: Bearer `oc whoami -t`" \
"https://api.${CLUSTER_URL}:6443/apis/cluster.open-cluster-management.io/v1/managedclusters/${CLUSTER_NAME}"
```

```
curl \
-X POST \
-d @cluster.json \
-H "Authorization: Bearer `oc whoami -t`" \
-H 'Accept: application/json' \
-H 'Content-Type: application/json' \
"https://api.${CLUSTER_URL}:6443/apis/cluster.open-cluster-management.io/v1/managedclusters"
```

