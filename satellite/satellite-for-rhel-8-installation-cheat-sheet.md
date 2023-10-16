# Variables

```
ORGANIZATION_ID=<organization_name>
```

```
LOCATION=<your_location>
```

```
ADMIN_USERNAME=<satellite_admin_user>
```

```
ADMIN_PASSWORD=<satellite_admin_password>
```

```
SATELLITE_FQDN=<satellite_hostname.your.domain>
```

```
SATELLITE_VERSION=<6.XX>
```

```
MANIFEST_FILE=</path/to/manifest_file.zip>
```

```
PROXY_NAME=<name_for_proxy_connection>
```

```
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
subscription-manager repos --enable=rhel-8-for-x86_64-baseos-rpms --enable=rhel-8-for-x86_64-appstream-rpms --enable=satellite-${SATELLITE_VERSION}-for-rhel-8-x86_64-rpms --enable=satellite-maintenance-${SATELLITE_VERSION}-for-rhel-8-x86_64-rpms
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
yum install satellite chrony sos createrepo_c tmux -y 
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

*Configuring Satellite Server with an HTTP Proxy*

```
hammer http-proxy create --name=${PROXY_NAME} --url=${PROXY_URL}
```

* *Optional: `--username=<proxy_username> --password=<proxy_password>`*

```
hammer settings set --name=content_default_http_proxy --value=${PROXY_NAME}
```

&nbsp;

# Export/Import Library Content

*Export all library content*

```
hammer content-export complete library --organization="${ORGANIZATION_ID}"
```

* *After the export complete create tar.gz file from the export directory in the /var/lib/pulp/exports/ directory to move it to the disconnected satellite server*

*Import all library content*

* *Unarchive the content in the /var/lib/pulp/imports/ directory*
  
*Change the owner of the unarcive content to pulp if its not the case*

```
chown -R pulp:pulp /var/lib/pulp/imports/<example:2021-03-02T03-35-24-00-00>
```

*Verify that the ownership is set correctly*

```
ls -lh /var/lib/pulp/imports/<example:2021-03-02T03-35-24-00-00>
```

* *Update the CDN configuration settings to Export Sync*

    Satellite WebUI --> Content --> Subscriptions --> Manage Manifest --> CDN Configuration --> Select Export Sync -->  Update

*Import the content*

```
hammer content-import library --organization="${ORGANIZATION_ID}" --path=/var/lib/pulp/imports/<example:2021-03-02T03-35-24-00-00>
```

&nbsp;

# Satellite maintain commands

*Download kattelo CA*

```
curl --insecure --output katello-ca-consumer-latest.noarch.rpm https://${SATELLITE_FQDN}/pub/katello-ca-consumer-latest.noarch.rpm
```

*Install kettelo CA on the host*

```
yum localinstall -y katello-ca-consumer-latest.noarch.rpm
```

*Check status of satellite services*

```
satellite-maintain service status
```

*Check satellite connectivity*

```
hammer ping
```

*Restart all satellite services*

```
satellite-maintain service restart
```

*Install packeges with foreman*

```
foreman-maintain packages install <package name>
```

*Disable foreman installer, use this command to yum instead foreman*

```
satellite-maintain packages unlock
```

*Cleanup tasks from the satellite task manu*

```
foreman-rake foreman_tasks:cleanup TASK_SEARCH='result == <result>' STATES='<state>' VERBOSE=true
```

