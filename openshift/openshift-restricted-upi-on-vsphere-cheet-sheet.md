#

#### THIS INSTALLATION REQUIRES YOU TO USE LOAD BALANCER
 
##### INSTALL LOAD BALANCER IN CASE YOU DONT HAVE ONE ALLREADY 

*install simple load balancer to use on linux machines*

```
yum install haproxy
```

*edit the configuration file to fits your DNS names*

```
vim /etc/haproxy/haproxy.cfg
```

  ```
  global
   log         127.0.0.1 local2
   pidfile     /var/run/haproxy.pid
   maxconn     4000
   daemon
  defaults
   mode                    http
   log                     global
   option                  dontlognull
   option http-server-close
   option                  redispatch
   retries                 3
   timeout http-request    10s
   timeout queue           1m
   timeout connect         10s
   timeout client          1m
   timeout server          1m
   timeout http-keep-alive 10s
   timeout check           10s
   maxconn                 3000
  frontend stats
   bind *:1936
   mode            http
   log             global
   maxconn 10
   stats enable
   stats hide-version
   stats refresh 30s
   stats show-node
   stats show-desc Stats for ocp4 cluster
   stats auth admin:ocp4
   stats uri /stats
  listen api-server-6443
   bind *:6443
   mode tcp
   server bootstrap bootstrap.<cluster name.domain name>:6443 check inter 1s backup
   server master0 master0.<cluster name.domain name>:6443 check inter 1s
   server master1 master1.<cluster name.domain name>:6443 check inter 1s
   server master2 master2.<cluster name.domain name>:6443 check inter 1s
  listen machine-config-server-22623
   bind *:22623
   mode tcp
   server bootstrap bootstrap.<cluster name.domain name>:22623 check inter 1s backup
   server master0 master0.<cluster name.domain name>:22623 check inter 1s
   server master1 master1.<cluster name.domain name>:22623 check inter 1s
   server master2 master2.<cluster name.domain name>:22623 check inter 1s
  listen ingress-router-443
   bind *:443
   mode tcp
   balance source
   server worker0 worker0.<cluster name.domain name>:443 check inter 1s
   server worker1 worker1.<cluster name.domain name>:443 check inter 1s
  listen ingress-router-80
   bind *:80
   mode tcp
   balance source
   server worker0 worker0.<cluster name.domain name>:80 check inter 1s
   server worker1 worker1.<cluster name.domain name>:80 check inter 1s
  ```

*start and enable the service after the config file is ready*

```
systemctl enable-now haproxy.service
```

#
 
#### INSTALL REGISTRY IN CASE YOU DONT HAVE ONE ALLREADY

##### [!] THIS REGISTRY MUST HAVE NETWORK CONNECTION WITH THE BASTION MACHINE IN THE LAN 

*Download and install a local, minimal single instance deployment of Red Hat Quay to aid bootstrapping the first disconnected cluster*

https://console.redhat.com/openshift/downloads#tool-mirror-registry

*extract the files from the tar file to your location*

```
tar -xvzf tar/mirror-registry.tar.gz -C .
```

> FILES INCLUDE THE TAR FILE -
> execution-environment.tar
> image-archive.tar
> mirror-registry

#### CREATE SELF-SIGNED CERTIFICATE FOR THE REGISTRY LOGIN 

```
mkdir ~/openssl
```

```
cd ~/openssl/
```

```
vim ca.cnf
```

  ```
  [ req ]
  distinguished_name = req_distinguished_name
  policy             = policy_anything
  x509_extensions     = v3_ca

  [ req_distinguished_name ]
  commonName                      = Common Name (eg, your name or your server hostname) ## Print this message

  [ v3_ca ]
  subjectKeyIdentifier = hash
  authorityKeyIdentifier = keyid:always,issuer
  basicConstraints = critical,CA:true
  ```

```
openssl genrsa -out ca.key 4096
```

```
openssl req -new -x509 -days 3650 -config ca.cnf -key ca.key -out ca.crt
```

```
vim server.cnf
```

* *[!] YOU **MUST** ADD YOUR SERVER FQDN AND SERVER IP UNDER [ alt_names ] CATEGORY*  

  ```
  [ req ]
  distinguished_name  = req_distinguished_name
  policy              = policy_anything
  x509_extensions     = ext
  req_extensions      = v3_req

  [ req_distinguished_name ]
  commonName                      = Common Name (eg, your name or your server hostname)

  [ ext ]
  subjectKeyIdentifier    = hash
  authorityKeyIdentifier  = keyid,issuer
  basicConstraints        = CA:FALSE
  extendedKeyUsage        = serverAuth
  keyUsage                = nonRepudiation, digitalSignature, keyEncipherment, dataEncipherment
  subjectAltName          = @alt_names

  [ v3_req ]
  basicConstraints        = CA:FALSE
  extendedKeyUsage        = serverAuth
  keyUsage                = nonRepudiation, digitalSignature, keyEncipherment, dataEncipherment
  subjectAltName          = @alt_names

  [ alt_names ]
  IP.1 = 1.1.1.1
  DNS.1 = <your.server.com>
  DNS.2 = <your>
  ```
```
openssl genrsa -out server.key 4096
```

```
openssl req -config server.cnf -new -key server.key -out server.csr
```

```
openssl x509 -req -days 365 -in server.csr -CA ca.crt -CAkey ca.key -CAcreateserial -out server.crt -extensions ext -extfile server.cnf
```

```
cp <ca certificate> /etc/pki/ca-trust/source/anchors/
```

```
update-ca-trust
```

*create directory for the mirror-registry*

```
mkdir /quay
```

*run the mirror registry installation with the server self-signed certificate*

```
./mirror-registry install --quayHostname [server fqdn] --quayRoot [registry directory] --sslCert [server certificate] --sslKey [server key]
```

* *[!] THE INSTALLATION WILL GENERATE LOGIN CREDENTIAL FOR THE MIRROR-REGISTRY, **KEEP THEM***

  *`EXAMPLE: { init, 6Ioty2XCw3H0Tk1549qpfsB7DlGRVj8g }`*
  




CONNECTED NETWORK -

https://access.redhat.com/downloads/content/290/ver=4.11/rhel---8/4.11.22/x86_64/product-software
[download oc client cli]

$ echo $PATH
[print the bianry files location on your server]

$ tar -xvzf oc-4.11.18-linux.tar.gz .
[extract the binary files]

$ install oc /usr/local/bin
[install oc client]

$ oc version
[check oc version]

$ OCP_RELEASE=[client version from the `oc version` stdout]
[create OCP_RELEASE variable with the oc version as value]

https://console.redhat.com/openshift/install/pull-secret
[download your pull-secret]

$ cat ./pull-secret.txt | jq . > /root/pull-secret.json
[convert your pull-secret file to JSON format]

## CREATE VARIABLES TO PULL THE RELEVANT IMAGES FOR THE INSTALLATION ##
$ LOCAL_REGISTRY='<local_registry_host_name>:<local_registry_host_port>'
$ LOCAL_REPOSITORY='ocp4/openshift4'
$ PRODUCT_REPO='openshift-release-dev'
$ LOCAL_SECRET_JSON='<path_to_pull_secret>'
$ RELEASE_NAME="ocp-release"
$ ARCHITECTURE=`uname -m`

$ mkdir mirror-images
[create directory for the images]

$ REMOVABLE_MEDIA_PATH='/root/mirror-images/'
[create variable to use it in the pull command, [!] the path must be absolute path]

$ oc adm release mirror -a ${LOCAL_SECRET_JSON} --from=quay.io/${PRODUCT_REPO}/${RELEASE_NAME}:${OCP_RELEASE}-${ARCHITECTURE} --to=${LOCAL_REGISTRY}/${LOCAL_REPOSITORY} --to-release-image=${LOCAL_REGISTRY}/${LOCAL_REPOSITORY}:${OCP_RELEASE}-${ARCHITECTURE} --dry-run
[dry run the pull command to generate the imageContentSources from the output, use it later in the install-config file]

        {

        imageContentSources:
        - mirrors:
          - <your.registry.server>:8443/ocp4/openshift4
          source: quay.io/openshift-release-dev/ocp-release
        - mirrors:
          - <your.registry.server>:8443/ocp4/openshift4
          source: quay.io/openshift-release-dev/ocp-v4.0-art-dev

        }

$ oc adm release mirror -a ${LOCAL_SECRET_JSON} --to-dir=${REMOVABLE_MEDIA_PATH}/mirror quay.io/${PRODUCT_REPO}/${RELEASE_NAME}:${OCP_RELEASE}-${ARCHITECTURE}
[pull the images from Red-Hat to the local directory to your local machine]





RESTRICTED NETWORK -

## COPY THE DIRECTORY WITH THE IMAGES YOU HAVE BEEN CREATED BEFORE FROM THE CONNECTED NETWORK TO YOUR LAN ##

https://access.redhat.com/downloads/content/290/ver=4.11/rhel---8/4.11.22/x86_64/product-software
[download oc client cli and the opeshift-installer]

$ echo $PATH
[print the bianry files location on your server]

$ tar -xvzf oc-4.11.18-linux.tar.gz -C <binary directory from the $PATH variable>
[extract the binary files to the designated location]

$ tar -xvzf tar/openshift-install-linux.tar.gz -C <install directory>
[extract the openshift installation tool to the install location]

$ oc version
[check oc version]

$ OCP_RELEASE=[client version from the `oc version` stdout]
[create OCP_RELEASE variable with the oc version as value]

$ podman login -u init -p 6Ioty2XCw3H0Tk1549qpfsB7DlGRVj8g
[login to your registry]

cat $XDG_RUNTIME_DIR/containers/auth.json > /root/pull-secret.json
[create pull-scret with with the credentials of your registry]

## CREATE VARIABLES TO PUSH THE RELEVANT IMAGES FOR THE INSTALLATION ##
$ LOCAL_REGISTRY='<local_registry_host_name>:<local_registry_host_port>'
$ LOCAL_REPOSITORY='ocp4/openshift4'
$ PRODUCT_REPO='openshift-release-dev'
$ LOCAL_SECRET_JSON='<path_to_pull_secret>'
$ RELEASE_NAME="ocp-release"
$ ARCHITECTURE=`uname -m`

$ mkdir mirror-images
[create directory for the images]

$ REMOVABLE_MEDIA_PATH='/root/mirror-images/'
[create variable to use it in the push command, [!] the path must be absolute path]

$ oc image mirror -a ${LOCAL_SECRET_JSON} --from-dir=${REMOVABLE_MEDIA_PATH}/mirror "file://openshift/release:${OCP_RELEASE}*" ${LOCAL_REGISTRY}/${LOCAL_REPOSITORY} 
[push the images to your local registry]




## START THE INSTALLATION ##

$ ./openshift-install version
[check the version of the insatll tool,[!] the version must be the same as the oc client tool]

$ dig +noall +answer @<nameserver_ip> api.<cluster_name>.<base_domain> 
$ dig +noall +answer @<nameserver_ip> console-openshift-console.apps.<cluster_name>.<base_domain>
$ dig +noall +answer @<nameserver_ip> -x <openshift machines ip>
[check the DNS resolve for your machines]

$ ssh-keygen
[generate ssh key]

$ cat <path>/<file_name>.pub
[check the public key]

$ eval "$(ssh-agent -s)"
[start the ssh agent]

$ ssh-add <path>/<private key>
[add your praivet key to the ssh agent] 


$ mkdir <installation_directory>
[create installation directory]

$ ./openshift-install create install-config --dir <installation_directory>
[generate install-config file]

vim install-config.yaml
[edit the install-config file to fit your needs]

        {

        apiVersion: v1
        baseDomain: example.com 
        compute: 
        - hyperthreading: Enabled 
          name: worker
          replicas: 0 
        controlPlane: 
          hyperthreading: Enabled 
          name: master
          replicas: 3 
        metadata:
          name: test 
        platform:
          vsphere:
            vcenter: your.vcenter.server 
            username: username 
            password: password 
            datacenter: datacenter 
            defaultDatastore: datastore 
            folder: "/<datacenter_name>/vm/<folder_name>/<subfolder_name>" 
            resourcePool: "/<datacenter_name>/host/<cluster_name>/Resources/<resource_pool_name>" 
            diskType: thin 
        fips: false 
        pullSecret: '{"auths":{"<local_registry>": {"auth": "<credentials>","email": "you@example.com"}}}' 
        sshKey: 'ssh-ed25519 AAAA...' 
        additionalTrustBundle: | 
          -----BEGIN CERTIFICATE-----
          ZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZ
          -----END CERTIFICATE-----
        imageContentSources: 
        - mirrors:
          - <local_registry>/<local_repository_name>/release
          source: quay.io/openshift-release-dev/ocp-release
        - mirrors:
          - <local_registry>/<local_repository_name>/release
          source: quay.io/openshift-release-dev/ocp-v4.0-art-dev

        }

## [!!] VERY IMPORTENT ##
$ cp <path/install-config.yaml> <path/install-config.yaml.bak>
[create copy of the install-config file]

$ ./openshift-install create manifests --dir <installation_directory>
[generate the mnifests files]

$ cd <path to install directory>
[get in the insatll directory]

$ rm -f openshift/99_openshift-cluster-api_master-machines-*.yaml openshift/99_openshift-cluster-api_worker-machineset-*.yaml
[delete the master and worker yaml files]

$ sed 's/true/false/g' manifests/cluster-scheduler-02-config.yml
[this change parameter to prevent the orcestrator to run pods on the master nodes]
[change <mastersSchedulable:> parameter to - false]

$ cd <path to the directory with the install script>
[go back to the directory with the installer tool]

$ ./openshift-install create ignition-configs --dir <installation_directory>
[generate the ignition files] 

$ base64 -w0 <installation_directory>/master.ign > <installation_directory>/master.64
$ base64 -w0 <installation_directory>/worker.ign > <installation_directory>/worker.64
$ base64 -w0 <installation_directory>/bootstrap.ign > <installation_directory>/bootstrap.64
[convert the ignition files to base64 format]

$ jq -r .infraID <installation_directory>/metadata.json 
[generate inventory name for the cluster in the vsphere and create vsphere directory with this name]

https://mirror.openshift.com/pub/openshift-v4/dependencies/rhcos/4.11/
[download the rhcos-vmware.x86_64]

## [!!] VERY IMPORTENT ##
deploy OVF tamplate from your local drive
## [!!] DO NOT START THE COREOS TEMPLATE ##

## CREATE VM'S FROM THE TEMPLATE ##

## MINIMAL REQUIREMENTS ##

        {
                    CPU   MEMORY    STORAGE
        bootstrap   8     16        120
        master0     8     16        120
        master1     8     16        120
        master2     8     16        120
        worker0     4     8         100
        worker1     4     8         100

        }

guestinfo.afterburn.initrd.network-karg <[EXAMPLE: ip=<machine ip>::<default gateway>:<prefix>:::none nameserver=<dns server ip1> nameserver=<dns server ip2> ...]>
guestinfo.ignition.config.data <copy of the ignition file content>
guestinfo.ignition.config.data.encoding <base64>
disk.EnableUUID <TRUE>
stealclock.enable <TRUE>

## ADD THE PARAMETERS ABOVE TO THE ADVANCE CONFIG IN YOUR MACHINE TO LOAD THE MCHINE WITH THE IGNITION FILES ##


## FOR LOSERS - export KUBECONFIG=<installation_directory>/auth/kubeconfig ## 
$ cp install-config/auth/kubeconfig .kube/config
[copy the kubconfig file to the designated location]

$ oc get csr |grep Pending
[search for nodes request]

## RUN THIS CAMMAND MANY TIMES ##
$ oc get csr |grep -i pending |awk '{print $1}' |while read x;do oc adm certificate approve $x;done
[approve all the nodes requsets]

$ ./openshift-install wait-for install-complete --dir install-config/ --log-level=debug
[run this command to wait and pray for the installation tp complete successfully]

## DONE ##

$ oc patch OperatorHub cluster --type json -p '[{"op": "add", "path": "/spec/disableAllDefaultSources", "value": true}]'
[disable the operator hub sources from the internet]

