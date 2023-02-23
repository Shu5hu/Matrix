### Self-sign certificate proccess -

---

##### Creating CA -

 create directory for the certificate proccess
 
 `$ mkdir ~/openssl`

 `$ cd ~/openssl`
 
 generate CA certs to sign the route certificate
 
 `$ openssl req -x509 -new -nodes -key myCA.key -sha256 -days 3650 -out myCA.pem`
 
##### Creating the certificate -

create tls key

`$ openssl genrsa -out tls.key 2048`

create request for the CA

  * CN must match the DNS name of the route which is [EXAMPLE=(route name)-(prohect name).apps-crc.testing]

`$ openssl req -new -key tls.key -out tls.csr`



##### Self-signing the certificate -

create the certificate signing by the CA

`$ openssl x509 -req -in tls.csr -CA myCA.pem -CAkey myCA.key -CAcreateserial -out tls.crt -days 1650 -sha256`

check certificate information

`$ openssl x509 -in <cert file> -text -noout`

