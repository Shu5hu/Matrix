#

*Check Apache used certififcate to see that is a self sign -*

```
openssl x509 -in /etc/pki/katello/certs/katello-apache.crt -text |egrep '(Issuer:|Subject:|CA:|DNS:|Digital|Not Before|Not After)'
```

*Create directory for the satellite server certificates -*

```
mkdir /root/satellite_cert
```

*Create praivte key -*

```
openssl genrsa -out /root/satellite_cert/satellite_cert_key.pem 4096
```

*Create config file -*

```
vi /root/satellite_cert/openssl.cnf
```

> [ req ] </br>
> distinguished_name  = req_distinguished_name </br>
> policy              = policy_anything </br>
> x509_extensions     = usr_cert </br>
> req_extensions      = v3_req </br>
> </br>
> [ req_distinguished_name ] </br>
> commonName                      = Common Name (eg, your name or your server hostname) </br>
> </br>
> [ usr_cert ] </br>
> subjectKeyIdentifier    = hash </br>
> authorityKeyIdentifier  = keyid,issuer </br>
> basicConstraints        = CA:FALSE </br>
> extendedKeyUsage        = serverAuth </br>
> keyUsage                = nonRepudiation, digitalSignature, keyEncipherment, dataEncipherment </br>
> subjectAltName          = @alt_names </br>
> </br>
> [ v3_req ] </br>
> basicConstraints        = CA:FALSE </bt>
> extendedKeyUsage        = serverAuth </br>
> keyUsage                = nonRepudiation, digitalSignature, keyEncipherment, dataEncipherment </br>
> subjectAltName          = @alt_names </br>
> </br>
> [ alt_names ] </br>
> DNS.1 = your.server.com </br>
#
*Generate the Certificate Signing Request -*

```
openssl req -new -key /root/satellite_cert/satellite_cert_key.pem -config /root/satellite_cert/openssl.cnf -out /root/satellite_cert/satellite_cert_csr.pem
```

Send the certificate signing request to the Certificate Authority. The same Certificate Authority must sign certificates for Satellite Server and Capsule Server.

#

### *Create CA to sign on the certificate in case you do not have CA -*

*Create directory for the self sign root CA -*

```
mkdir /root/satellite_cert/ca
```

*Create CA key -*

```
openssl genrsa -out /root/satellite_cert/ca/ca.key 4096
```

*Create CA config file -*

```
vi /root/satellite_cert/ca/ca.cnf
```

> [ req ] </br>
> distinguished_name = req_distinguished_name </br>
> policy             = policy_anything </br>
> x509_extensions     = v3_ca </br>
> </br>
> [ req_distinguished_name ] </br>
> commonName                      = Common Name (eg, your name or your server hostname) ## Print this message </br>
> </br>
> [ v3_ca ] </br>
> subjectKeyIdentifier = hash </br>
> authorityKeyIdentifier = keyid:always,issuer </br>
> basicConstraints = critical,CA:true </br>

*Create CA certificate -*

```
openssl req -new -x509 -days 3650 -config /root/satellite_cert/ca/ca.cnf -key /root/satellite_cert/ca/ca.key -out /root/satellite_cert/ca/ca.crt
```

#

*Sign on the satellite certificate with our new CA -*

```
openssl x509 -req -days 365 -in /root/satellite_cert/satellite_cert_csr.pem -CA /root/satellite_cert/ca/ca.crt -CAkey /root/satellite_cert/ca/ca.key -CAcreateserial -out /root/satellite_cert/satellite.crt -extensions usr_cert -extfile /root/satellite_cert/openssl.cnf
```

*Verify the sign request -*

```
openssl req -text -noout -verify -in /root/satellite_cert/satellite_cert_csr.pem
```

*Generate the certificate install command -*

```
katello-certs-check -c /root/satellite_cert/satellite.crt -k /root/satellite_cert/satellite_cert_key.pem -b /root/satellite_cert/ca/ca.crt
```


