# Create server certificate -

*Check Apache used certififcate to see that is a self sign*

```
openssl x509 -in /etc/pki/katello/certs/katello-apache.crt -text |egrep '(Issuer:|Subject:|CA:|DNS:|Digital|Not Before|Not After)'
```

```
mkdir ~/satellite_cert
```

```
openssl genrsa -out ~/satellite_cert/satellite_cert_key.pem 4096
```

```
vi ~/satellite_cert/openssl.cnf
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

```
openssl req -new -key ~/satellite_cert/satellite_cert_key.pem -config ~/satellite_cert/openssl.cnf -out ~/satellite_cert/satellite_cert_csr.pem
```

* *Send the certificate signing request to the Certificate Authority. The same Certificate Authority must sign certificates for Satellite Server and Capsule Server.*


# Create self-sign CA 

```
mkdir ~/satellite_cert/ca
```

```
openssl genrsa -out ~/satellite_cert/ca/ca.key 4096
```

```
vi ~/satellite_cert/ca/ca.cnf
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
openssl req -new -x509 -days 3650 -config ~/satellite_cert/ca/ca.cnf -key ~/satellite_cert/ca/ca.key -out ~/satellite_cert/ca/ca.crt
```


# Sign the satellite certificate


```
openssl x509 -req -days 365 -in ~/satellite_cert/satellite_cert_csr.pem -CA ~/satellite_cert/ca/ca.crt -CAkey ~/satellite_cert/ca/ca.key -CAcreateserial -out ~/satellite_cert/satellite.crt -extensions usr_cert -extfile ~/satellite_cert/openssl.cnf
```

```
openssl req -text -noout -verify -in ~/satellite_cert/satellite_cert_csr.pem
```

# Generate the certificate install command -

```
katello-certs-check -c ~/satellite_cert/satellite.crt -k ~/satellite_cert/satellite_cert_key.pem -b ~/satellite_cert/ca/ca.crt
```

* *This commans will generate the certificate install caommns in case all the conditions met*


