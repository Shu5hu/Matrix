#### Self-sign certificate proccess -

##### Creating CA -

> `$ mkdir ~/openssl`
>
> `$ cd ~/openssl`


create directory for the certificate proccess

openssl genrsa -des3 -out myCA.key 2048
[create CA key]

openssl req -x509 -new -nodes -key myCA.key -sha256 -days 3650 -out myCA.pem
[generate CA certs to sign the route certificate]

Creating the certificate -

openssl genrsa -out tls.key 2048
[create tls key]

openssl req -new -key tls.key -out tls.csr
[create request for the CA]
* CN must match the DNS name of the route which is [EXAMPLE=(route name)-(prohect name).apps-crc.testing]

Self-signing the certificate -

openssl x509 -req -in tls.csr -CA myCA.pem -CAkey myCA.key -CAcreateserial -out tls.crt -days 1650 -sha256
[create the certificate signing by the CA]

openssl x509 -in [cert file] -text -noout
[check certificate information]
