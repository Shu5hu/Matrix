# variables

```
ORGANIZATION_ID=<organization_name>
LOCATION=<yout_location>
ADMIN_USERNAME=<satellite_admin_user>
ADMIN_PASSWORD=<satellite_admin_password>
SATELLITE_FQDN=<satellite_hostname.your.domain>
MANIFEST_FILE=</path/to/manifest_file.zip>
PROXY_NAME=<name_for_proxy_connection>
PROXY_URL=<http://myproxy.example.com:port>
```

# Prerequisites 

```
ping -c1 $(hostname -f)
```

```
subscription-manager register
```

```
subscription-manager list --all --available --matches 'Red Hat Satellite'
```

```
subscription-manager attach --pool=<pool_id>
```

```
subscription-manager list --consumed
```

```
subscription-manager repos --disable "*"
```

```
subscription-manager repos --enable=rhel-8-for-x86_64-baseos-rpms --enable=rhel-8-for-x86_64-appstream-rpms --enable=satellite-6.11-for-rhel-8-x86_64-rpms --enable=satellite-maintenance-6.11-for-rhel-8-x86_64-rpms
```

```
yum repolist
```

```
dnf module enable satellite:el8
```

```
yum update -y
```

```
yum install satellite -y 
```

```
yum install chrony sos createrepo_c tmux -y
```

```
systemctl enable --now chronyd
```

###### In case you use tmux

```
tmux
```

> *cntrl + b + %*
> 
> *cntrl +b + ->*
> ```
> tail -f /var/log/foreman-installer/satellite.log
> ```
> *cntrl + b + <-*

&nbsp;

# Install Satellite server 

```
satellite-installer --scenario satellite --foreman-initial-organization ${ORGANIZATION_ID} --foreman-initial-location ${LOCATION} --foreman-initial-admin-username ${ADMIN_USERNAME} --foreman-initial-admin-password ${ADMIN_PASSWORD}
```

*Import manifest*

```
hammer subscription upload --file ${MANIFEST_FILE} --organization ${ORGANIZATION_ID}
```

*Register hosts*

```
curl --insecure --output katello-ca-consumer-latest.noarch.rpm https://${SATELLITE_FQDN}/pub/katello-ca-consumer-latest.noarch.rpm
```

```
yum localinstall -y katello-ca-consumer-latest.noarch.rpm
```

*Configuring Satellite Server with an HTTP Proxy*

```
hammer http-proxy create --name=${PROXY_NAME} --url=${PROXY_URL}
```

* *Optional: `--username=<proxy_username> --password=<proxy_password>`*

```
hammer settings set --name=content_default_http_proxy --value=${PROXY_NAME}
```

# Satellite maintain commands

```
satellite-maintain service status
```

```
hammer ping
```

```
satellite-maintain service restart
```

```
foreman-maintain packages install <package name>
```

```
satellite-maintain packages unlock
```


