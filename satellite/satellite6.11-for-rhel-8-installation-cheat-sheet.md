---
###### *In case you use firewalld*
```
firewall-cmd --add-port="53/udp" --add-port="53/tcp" --add-port="67/udp" --add-port="69/udp" --add-port="80/tcp" --add-port="443/tcp" --add-port="5647/tcp" --add-
port="8000/tcp" --add-port="9090/tcp" --add-port="8140/tcp"
```
```
firewall-cmd --runtime-to-permanent
```
```
firewall-cmd --list-all
```
---
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
subscription-manager attach --pool=*<pool_id>*
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
---
###### *In case you use tmux*
```
tmux
```
> cntrl + b + %
> cntrl +b + ->
> ```
> tail -f /var/log/foreman-installer/satellite.log
> ```
> cntrl + b + <-
```
satellite-installer --scenario satellite --foreman-initial-organization *<My_Organization>* --foreman-initial-location *<My_Location>* --foreman-initial-admin-username *<admin_user_name>* --foreman-initial-admin-password *<admin_password>*
```
---
###### Import manifest -
```
hammer subscription upload --file ~/*<manifest_file.zip>* --organization *<My_Organization>*
```
###### Register hosts -
```
curl --insecure --output katello-ca-consumer-latest.noarch.rpm https://*<satellite_fqdn>*/pub/katello-ca-consumer-latest.noarch.rpm
```
```
yum localinstall -y katello-ca-consumer-latest.noarch.rpm
```
---
###### Satellite-maintain commands - 
> ```
> satellite-maintain service status
> ```
> ```
> hammer ping
> ```
> ```
> satellite-maintain service restart
> ```
> ```
> foreman-maintain packages install *<package name>*
> ```
> ```
> satellite-maintain packages unlock
> ```
---
##### Configuring Satellite Server with an HTTP Proxy -
hammer http-proxy create --name=myproxy --url http://myproxy.example.com:8080 {{ OPTIONAL: (--username=proxy_username --password=proxy_password) }}
hammer settings set --name=content_default_http_proxy --value=myproxy

