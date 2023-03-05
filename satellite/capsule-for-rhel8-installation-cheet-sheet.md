# Serve configuration

###### Generate register command to satellite server

	in the Satellite web UI, navigate to Hosts > Register Host.
	Click Generate to create the registration command.
	Click on the files icon to copy the command to your clipboard.
	Log on to the host you want register and run the previously generated command.
	Update subscription manager configuration for rhsm.baseurl and server.hostname:

###### Regster to satellite with kattelo agent

```
curl --insecure --output katello-ca-consumer-latest.noarch.rpm https://<SATELLITE_FQDN>/pub/katello-ca-consumer-latest.noarch.rpm
```

```
yum localinstall -y katello-ca-consumer-latest.noarch.rpm
```

```
subscription-manager config --rhsm.baseurl=https://<SATELLITE_FQDN>/pulp/content --server.hostname=<SATELLITE_FQDN>
```

* *[!] Check the /etc/yum.repos.d/redhat.repo file and ensure that the appropriate repositories have been enabled.*

```
subscription-manager repos --disable "*"
```

```
subscription-manager repos --enable=rhel-8-for-x86_64-baseos-rpms --enable=rhel-8-for-x86_64-appstream-rpms --enable=satellite-capsule-6.11-for-rhel-8-x86_64-rpms --enable=satellite-maintenance-6.11-for-rhel-8-x86_64-rpms
```

```
dnf module enable satellite-capsule:el8
```

```
yum update -y
```

```
yum install satellite-capsule chrony -y
```

```
systemctl enable --now chronyd
```

# Steps on satellite server

###### Create capsule server certificate

*Create directory for the certificates*

```
mkdir ~/capsule_cert
```

*Create praivte key*

```
openssl genrsa -out /root/capsule_cert/capsule_cert_key.pem 4096
```

*Create config file*

```
vi ~/capsule_cert/openssl.cnf
```

	```
	[ req ]
	distinguished_name  = req_distinguished_name
	policy              = policy_anything
	x509_extensions     = usr_cert
	req_extensions      = v3_req

	[ req_distinguished_name ]
	commonName                      = Common Name (eg, your name or your server hostname)

	[ usr_cert ]
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
	DNS.1 = your.server.com
	```


*Generate the Certificate Signing Request*

```
openssl req -new -key ~/capsule_cert/capsule_cert_key.pem -config ~/capsule_cert/openssl.cnf -out ~/capsule_cert/capsule_cert_csr.pem
```

*sign on the capsule certificate with the same CA as the satellite server*

```
openssl x509 -req -days 365 -in ~/capsule_cert/capsule_cert_csr.pem -CA ~/satellite_cert/ca/ca.crt -CAkey ~/satellite_cert/ca/ca.key -CAcreateserial -out ~/capsule_cert/capsule.crt -extensions usr_cert -extfile ~/capsule_cert/openssl.cnf
```

*generate capsule certificate command*

```
katello-certs-check -t capsule -c ~/capsule_cert/capsule.crt -k ~/capsule_cert/capsule_cert_key.pem -b ~/satellite_cert/ca/ca.crt
```

*Create environment variable with the capsule server fqdn*

```
export CAPSULE=<CAPSULE_FQDN>
```

* *Example:*

				capsule-certs-generate --foreman-proxy-fqdn "$CAPSULE" \
                                   --certs-tar  "~/$CAPSULE-certs.tar" \
                                   --server-cert "/root/capsule_cert/capsule.crt" \
                                   --server-key "/root/capsule_cert/capsule_cert_key.pem" \
                                   --server-ca-cert "/root/satellite_cert/ca/ca.crt"
			
* *This command will generate capsule server install procedure, [!] follow this procedure to start installation*
								 
* *Example:*

  	To finish the installation, follow these steps:

 	 If you do not have the Capsule registered to the Satellite instance, then please do the following:

 	 1. yum -y localinstall http://satellite01.redhat.local/pub/katello-ca-consumer-latest.noarch.rpm
 	 2. subscription-manager register --org "Matrix"

  	Once this is completed run the steps below to start the Capsule installation:

 	 1. Ensure that the satellite-capsule package is installed on the system.
 	 2. Copy the following file ~/<capsule_fqdn>-certs.tar to the system <capsule_fqdn> at the following location ~/<capsule_fqdn>-certs.tar
 	 scp ~/<capsule_fqdn>-certs.tar root@<capsule_fqdn>:~/<capsule_fqdn>-certs.tar
 	 3. Run the following commands on the Capsule (possibly with the customized
  	 	parameters, see satellite-installer --scenario capsule --help and
    	 	documentation for more info on setting up additional services):

  	 satellite-installer \
                    --scenario capsule \
                    --certs-tar-file                              "/root/capsule01.redhat.local-certs.tar"\
                    --foreman-proxy-register-in-foreman           "true"\
                    --foreman-proxy-foreman-base-url              "https://satellite01.redhat.local"\
                    --foreman-proxy-trusted-hosts                 "satellite01.redhat.local"\
                    --foreman-proxy-trusted-hosts                 "capsule01.redhat.local"\
                    --foreman-proxy-oauth-consumer-key            "eEdQtvXmNKgEVL8vvfDTyMAFH2BFiDtA"\
                    --foreman-proxy-oauth-consumer-secret         "htVdXYthUoKvTRScJ92xdUXdTRvnx7rp"
		    
*Copy the .tar file to your capsule server*

```
scp ~/<capsule_fqdn>-certs.tar root@<capsule_fqdn>:~/<capsule_fqdn>-certs.tar
```

# Steps on capsule server

###### Run the installation command

*After installation complete you need to sync your content to the capsule server, here you can find the sync logs*

```
tail -f /var/log/httpd/forman-ssl_access_ssl.log	
```

