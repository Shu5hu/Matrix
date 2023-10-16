# Prerequisites - 

* *rhel 7.9 in connected environment to download all the leapp dependencies*

</br>

# Connected Server Process

*register to your redhat account*

```
subscription-manager register
```

*attach auto subscription to the machine*

```
subscription-manager attach --auto
```

*enable the rhel-7-server-extras-rpms repository*

```
subscription-manager repos enable=rhel-7-server-extras-rpms
```

*create directory for the leapp rpms*

```
mkdir /leapp
```

*download the leapp-upgrade rpms*

```
yum install leapp-upgrade --downloadonly --downloaddir /leapp
```

* *if you get an error from the last command about the leapp rpms dpwnload them and copy them to their dependencies*

*download the leapp rpms from here*

[access.redhat.com/downloads/content/69/ver=/rhel---7/7.9/x86_64/packages](https://access.redhat.com/downloads/content/69/ver=/rhel---7/7.9/x86_64/packages)

    leapp-upgrade-el7toel8-0.18.0-3.el7_9.noarch.rpm
    leapp-0.15.1-1.el7_9.noarch.rpm       
    leapp-upgrade-el7toel8-deps-0.18.0-3.el7_9.noarch.rpm
    leapp-deps-0.15.1-1.el7_9.noarch.rpm  
    python2-leapp-0.15.1-1.el7_9.noarch.rpm

* *copy those packages to the /leapp directory if they are not allready there*

*archive the leapp directory*

```
tar -cvf leapp.tar /leapp
```

*copy the tar file to the disconnected server to start the leapp proccess*

```
scp /path/to/leapp.tar <username>@<disconnected server hostname>:</path/to/leapp>
```

</br>

# Disconnected Server Proccess -

* *connect the iso from the vcenter edit machine*

*create dircetory to mount the rhel 7.9 iso*

```
mkdir /local-repo
```

*edit the fstab file to mount the iso on /dev/sr0*

```
vi /etc/fstab
```
    
    /dev/sr0	/local-repo		iso9660		loop	0 0

*update the mounts*

```
mount -a
```

*create repo file to get the rhel 7 packages*

```
vi /etc/yum.repos.d/rhel7.repo
```

    [rhel-7-server]
    name=rhel-7-server
    enabled=1
    gpgcheck=1
    gpgkey=file:///local-repo/RPM-GPG-KEY-redhat-release
    baseurl=file:///local-repo/

### <span style="color:red">**[!] TAKE SNAPSHOT**</span>

*update the machine to the latest version*

```
yum update -y
```

* *if the kernel is updated reboot the machine*

*install createrepo package to create leapp repository*

```
yum install createrepo
```

*unarchive the leapp.tar*

```
tar -xvf /path/to/leapp.tar
```

*move the leapp directory to /*

```
mv leapp/ /
```

*make /leapp directory a repository*

```
createrepo /leapp/
```

*create repository file*

```
vi /etc/yum.repos.d/leapp.repo
```

    [leapp-upgrade]
    name=leapp-upgrade
    enabled=1
    gpgcheck=0
    baseurl=file:///leapp/

*install the leapp tool*

```
yum install leapp-upgrade -y
```

*download the rhel-8 dvd bainery iso*

[https://developers.redhat.com/products/rhel/download#rhel-new-product-download-list-61451?source=sso](https://developers.redhat.com/products/rhel/download#rhel-new-product-download-list-61451?source=sso)

* *copy the rhel 8 iso to the disconnected server*

*run a pre upgrade command to check if the machine is ready for the upgrade*

```
leapp preupgrade --iso /path/to/iso --target 8.8 --no-rhsm
```

* *the pre upgrade check will fail probably, check the issues on this file -*

```
less /var/log/leapp/leapp-report.txt
```

* *after fixing the issues run the command again until you get successfull report*
* *[!] dont start the upgrade before you get successfull report*

### <span style="color:red">**[!] TAKE SNAPSHOT**</span>

*run the upgrade*

```
leapp upgrade --iso /path/to/iso --target 8.8 --no-rhsm
```

</br>

# Post Upgrade Proccess -

*create environment variable with the old kernel version*

```
export old_kernel=`ls -d /lib/moduels/*.el7* |awk -F '/' '{print $NF}'`
```

*check the stdout of the variable*

```
echo $old_kernel
```

*remove the rhel7 and the leapp repositories*

```
[ -x /usr/sbin/weak-modules ] && /usr/sbin/weak-modules --remove-kernel $old_kernel
```

```
/bin/kernel-install remove $old_kernel /lib/modules/$old_kernel/vmlinuz
```

```
yum remove leapp-deps-el8 leapp-repository-deps-el8
```

```
rpm -qa | grep -e '\.el[67]' | grep -vE '^(gpg-pubkey|libmodulemd|katello-ca-consumer)' | sort | while read lines ;do rpm -e $lines ;done
```

```
rm -r /lib/modules/*el7*
```
* *this command can fail if the files are allready not there*

```
rm -rf /var/log/leapp /root/tmp_leapp_py3 /var/lib/leapp
```

```
rm /boot/vmlinuz-*rescue* /boot/initramfs-*rescue*
```

*remove the /dev/sr0 line from the /etc/fstab*

```
sed -i '/^\/dev\/sr0/d' /etc/fstab
```

*unmount /local-repo directory*

```
umount /local-repo
```

*update the fstab file*

```
mount -a
```

*mount the rhel 8 iso*

```
mount -o loop /path/to/rhel-8-iso /local-repo
```

*move the rhel7 repo file from the yum.repos.d repository*

```
mv /etc/yum.repos.d/rhel7.repo /tmp/
```

*create repo file for the rhel 8 repositories*

```
vi /etc/yum.repos.d/rhel8.repo
```

    [BaseOS]
    name=BaseOS
    enabled=1
    gpgcheck=1
    gpgkey=file:///local-repo/RPM-GPG-KEY-redhat-release
    baseurl=file:///local-repo/BaseOS/

    [AppStream]
    name=AppStream
    enabled=1
    gpgcheck=1
    gpgkey=file:///local-repo/RPM-GPG-KEY-redhat-release
    baseurl=file:///local-repo/AppStream/

*reinstall kernel core*

```
dnf reinstall -y kernel-core-$(uname -r)
```

*restart the machine*

```
reboot
```