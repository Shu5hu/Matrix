#

```
yum update
```

* *You must first take your system to the last update before the proccess*

Change the the kernel in the next reboot

```
grubby --set-default /boot/vmlinuz-`rpm -q --qf "%{BUILDTIME}\t%{EVR}.%{ARCH}\n" kernel | sort -nr | head -1 | cut -f2`
```

```
reboot
```

* *For the next step your system must be connected, in case is not, download this files and bring them into your ristricted environment*

```
curl -o /etc/pki/rpm-gpg/RPM-GPG-KEY-redhat-release https://www.redhat.com/security/data/fd431d51.txt
```

*DEBUG: `cat /etc/pki/rpm-gpg/RPM-GPG-KEY-redhat-release`*
